\# Gate 0 — Primitive



Date: 2026-09-20



\## Objective



Prove that one AI character can maintain a stable identity and persistent, isolated memory for separate users through a browser interface.



\## Result



PASS



\## Demonstrated



\- Browser-based text interaction with Avery.

\- Avery's identity is defined externally through:

&#x20; - persona.md

&#x20; - voice.md

&#x20; - behavior.md

\- Avery clearly identifies as an AI character.

\- Current-session conversational context works.

\- Useful user information is automatically extracted from conversation.

\- Memories persist in SQLite after browser refresh.

\- Memories are retrieved and used in later conversations.

\- User memories remain isolated.



\## Evidence



Jeff:

\- Favorite test animal: otter.

\- Project: small solar-powered backyard weather station.



Test User 2:

\- Favorite test animal: red panda.



Isolation test:

\- Test User 2 did not initially know Jeff's otter memory.

\- Test User 2 learned red panda.

\- After browser refresh, Test User 2 recalled red panda.

\- Switching back to Jeff returned otter, not red panda.



\## Architecture Proven



Browser

→ FastAPI

→ character definition

→ OpenAI LLM

→ memory extraction

→ SQLite per-user memory

→ later retrieval



\## Gate 0 Conclusion



Persistent identity + durable isolated user memory works.



Proceed to Gate 1 — Experience.

