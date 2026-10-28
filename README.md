# Avery: a persistent AI character

Avery is a chat character that remembers the people it talks to. Each user's memories are kept separate and come back in later sessions, even after a restart.

Most chat assistants either forget you between sessions or mix up whose facts are whose. Avery is a small prototype that tackles both problems, built in stages with a pass/fail gate before each new feature.

## How it works

```
Browser -> FastAPI -> character files -> OpenAI model
                          |
              memory extraction after each message
                          |
              SQLite, one memory list per user -> used in later sessions
```

- **Character.** Avery's identity lives in three Markdown files: `character/persona.md`, `voice.md` and `behavior.md`. You change the character by editing text, not code. Avery always says it is an AI and must not invent memories.
- **Memory.** After each user message, a second model call pulls out facts worth keeping (preferences, projects, goals) and stores them in SQLite under that user. Exact duplicates are skipped.
- **Recall.** Each reply is built from the character files plus that user's stored memories, and nobody else's.
- **Inspector.** `GET /memories/{user_id}` shows what is stored for a user.

## What's proven

**Gate 0: PASS** (see `GATE0_RESULTS.md`)
- Memories persist after a browser refresh.
- Two test users kept separate memories: Jeff's favourite test animal was an otter, Test User 2's was a red panda, and neither leaked into the other.
- `gate0_regression.py` repeats this automatically and checks persistence in a fresh Python process.

```
PASS: persistence survived process restart
PASS: no cross-user memory leakage
GATE 0 REGRESSION: PASS
```

**Gate 1, experience: provisional pass.** Persistent memory clearly improved the conversations.

## Known gaps

These are written up rather than hidden (see `MEMORY_FINDINGS.md`):
- **Semantic duplicates.** The extractor stores near-identical variants of the same fact.
- **Corrections pile up.** "My favourite animal is now a raven" adds a new memory but leaves the old otter one in place. The model picks the newer one, but stale facts stay in storage.

The next step is in `MEMORY_SCHEMA_V1.md`, `MEMORY_ACCEPTANCE.md` and `MEMORY_V1_TEST_PLAN.md`: stable keys with update semantics, so each user has one current fact per key, and model guesses are never stored as user facts. New features (voice, avatar) wait until memory hygiene passes its tests.

## Run it

```bash
pip install -r requirements.txt
echo OPENAI_API_KEY=your-key > .env
mkdir data
uvicorn app:app --reload
```

Open http://127.0.0.1:8000. The database is created at `data/character.db`. Both `.env` and the database are git-ignored.

Regression test (no API key needed):

```bash
python gate0_regression.py
```
