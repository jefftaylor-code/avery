\# Avery Memory Findings



Date: 2026-09-22



\## Purpose



Probe the current persistent-memory behavior before redesigning memory hygiene.



No production memory logic was changed during these tests.



\## Results



\### 1. User isolation



PASS



\- Jeff memories remain scoped to Jeff.

\- Test User 2 memories remain scoped to Test User 2.

\- No cross-user leakage observed.

\- Automated Gate 0 regression verifies isolation in a fresh Python process.



\### 2. Correction behavior



Input:



"Actually, my favorite test animal is now a raven, not an otter."



Stored state:



\- Old memory remains: Jeff's favorite test animal is an otter.

\- New memory added: Jeff's favorite test animal is a raven, not an otter.



Later recall:



Avery answered that the favorite test animal is a raven.



Finding:



The LLM can currently resolve the newer contradiction correctly, but obsolete state remains in storage.



Desired future behavior:



The new value should supersede or update the old value rather than accumulate beside it.



\### 3. Refinement / preference shift



Input:



"Thailand interests me, but Malaysia is probably a stronger retirement candidate for me right now."



Stored state:



\- Older Thailand/Southeast Asia memories remain.

\- New Malaysia-preference memory was added.



Later recall:



Avery correctly said Malaysia is currently favored over Thailand.



Finding:



Reasoning handles the refinement, but storage accumulates historical and current state without explicit distinction.



Desired future behavior:



Current preference should be represented clearly while useful history may optionally be retained separately.



\### 4. Temporary information



Input:



"I'm drinking coffee right now."



Result:



No durable memory was created.



PASS



\### 5. Explicit durable preference



Input:



"For future reference, I prefer technical explanations that show me what each component does rather than hiding things behind no-code tools."



Result:



A durable preference memory was created.



PASS



\### 6. Confirmatory question



Input:



"Did I tell you that I'm considering Thailand for retirement?"



Result:



No new memory row was created.



PASS



Finding:



Question phrasing alone does not appear to cause duplicate memory creation.



\## Current Strengths



\- Persistent storage works.

\- Persistence survives process restart.

\- User isolation works.

\- Temporary information can be rejected.

\- Explicit durable preferences are captured.

\- Avery can use newer information to resolve conflicting older information.

\- Confirmatory questions can be ignored by the extractor.



\## Current Weakness



Semantic duplicates and superseded facts remain in the database.



Examples include:



\- multiple EchoStar-status memories

\- multiple Council-plan memories

\- multiple retirement-interest memories

\- otter and raven both remaining after correction

\- Thailand and Malaysia preference states both remaining



Exact-string deduplication is insufficient.



\## Memory Hygiene Requirement



The next design should distinguish at least:



\- NEW -> create

\- DUPLICATE -> ignore

\- CORRECTION -> update/supersede

\- REFINEMENT -> merge or update

\- TEMPORARY -> ignore

\- CONFIRMATORY QUESTION -> ignore



The system should preserve user isolation and must not turn model inference into stored user fact.



\## Next Engineering Task



Design and test stable semantic memory identity/update behavior before adding voice, avatar, deployment, RAG, or other features.

