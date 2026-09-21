import os
import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from openai import OpenAI
from pydantic import BaseModel
from db import init_db, add_user, add_memory_if_new, get_memories

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
init_db()
add_user("jeff", "Jeff")

BASE_DIR = Path(__file__).resolve().parent
CHARACTER_DIR = BASE_DIR / "character"
STATIC_DIR = BASE_DIR / "static"


def load_character():
    persona = (CHARACTER_DIR / "persona.md").read_text(encoding="utf-8")
    voice = (CHARACTER_DIR / "voice.md").read_text(encoding="utf-8")
    behavior = (CHARACTER_DIR / "behavior.md").read_text(encoding="utf-8")

    return {
        "persona": persona,
        "voice": voice,
        "behavior": behavior,
    }


character = load_character()


def build_instructions(user_id):
    memories = get_memories(user_id)

    if memories:
        memory_text = "\n".join(
            f"- {memory}" for memory in memories
        )
    else:
        memory_text = "No persistent memories are stored for this user."

    return f"""
{character["persona"]}

{character["voice"]}

{character["behavior"]}

# Persistent Memories for Current User

The following memories belong only to the current user.
Use them naturally when relevant.
Do not claim memories that are not listed here.

{memory_text}
"""


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    user_id: str
    display_name: str
    message: str
    history: list[HistoryMessage] = []


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Avery — Persistent Character Lab</title>
        </head>
        <body>
            <h1>Avery</h1>
            <p>Persistent Character Lab — Gate 0</p>
            <p>Character definition loaded successfully.</p>
        </body>
    </html>
    """

def extract_memories(user_id, message):

    existing_memories = get_memories(user_id)

    existing_text = "\n".join(
        f"- {memory}" for memory in existing_memories
    )

    prompt = f"""
You are the memory extraction component for a persistent AI character.

Analyze ONLY the user's message below.

Store information only if it is likely to be useful in a future conversation.

Good memories include:
- preferences
- interests
- personal projects
- goals
- recurring activities
- stable facts about the user
- important people, places, or commitments

Do not store:
- casual greetings
- temporary conversational remarks
- questions
- assistant-generated information
- guesses or implications
- sensitive information unless the user clearly intends it to be relevant later

Existing memories:
{existing_text}

User message:
{message}

Return ONLY a JSON array of short standalone memory strings.

Example:
["Jeff prefers black coffee.", "Jeff is studying for an AWS certification."]

If there is nothing useful to remember, return:
[]
"""

    response = client.responses.create(
        model="gpt-5.6-terra",
        input=prompt,
    )

    try:
        memories = json.loads(response.output_text)
    except json.JSONDecodeError:
        return []

    if not isinstance(memories, list):
        return []

    for memory in memories:
        if isinstance(memory, str) and memory.strip():
            add_memory_if_new(
                user_id,
                memory.strip()
            )


@app.post("/chat")
def chat(request: ChatRequest):

    user_id = request.user_id

    add_user(
        request.user_id,
        request.display_name
    )

    conversation = []

    for item in request.history:
        conversation.append({
            "role": item.role,
            "content": item.content
        })

    conversation.append({
        "role": "user",
        "content": request.message
    })

    response = client.responses.create(
        model="gpt-5.6-terra",
        instructions=build_instructions(user_id),
        input=conversation,
    )
	
    extract_memories(user_id, request.message)

    return {
        "reply": response.output_text
    }