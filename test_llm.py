from pathlib import Path
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

base_dir = Path(__file__).resolve().parent
character_dir = base_dir / "character"

persona = (character_dir / "persona.md").read_text(encoding="utf-8")
voice = (character_dir / "voice.md").read_text(encoding="utf-8")
behavior = (character_dir / "behavior.md").read_text(encoding="utf-8")

instructions = f"""
{persona}

{voice}

{behavior}
"""

response = client.responses.create(
    model="gpt-5.6-terra",
    instructions=instructions,
    input="Hello Avery. Introduce yourself to me in two or three sentences.",
)

print(response.output_text)