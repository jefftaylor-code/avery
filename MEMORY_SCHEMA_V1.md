\# Avery Memory Schema V1



Date: 2026-09-22



\## Objective



Fix semantic duplication and stale-current-state problems without building a complex memory platform.



The next revision should support:



\- new durable facts

\- semantic duplicate rejection

\- correction/update

\- refinement/update

\- temporary-information rejection

\- confirmatory-question rejection

\- strict per-user isolation



Do not add embeddings, vector search, RAG, multi-agent memory, or memory scoring yet.



\---



\# Core Principle



A memory is not just a sentence.



A durable memory has:



1\. a user

2\. a stable semantic key

3\. a current value

4\. timestamps



Example:



user\_id:

jeff



key:

favorite\_test\_animal



value:

raven



Rather than storing:



\- Jeff's favorite test animal is an otter.

\- Jeff's favorite test animal is a raven, not an otter.



the system stores one current fact:



favorite\_test\_animal = raven



\---



\# Proposed Current-Memory Table



memories



\- id

\- user\_id

\- memory\_key

\- memory\_value

\- created\_at

\- updated\_at



Constraint:



UNIQUE(user\_id, memory\_key)



This guarantees that one user cannot have multiple current memories for the same semantic key.



\---



\# Examples



\## Favorite animal



memory\_key:

favorite\_test\_animal



memory\_value:

raven



\---



\## Retirement location



memory\_key:

retirement\_location\_interest



memory\_value:

Malaysia is currently a stronger retirement candidate than Thailand; Southeast Asia remains of interest.



\---



\## Communication preference



memory\_key:

explanation\_style\_preference



memory\_value:

Prefers technical explanations that clarify what each component does rather than hiding implementation behind no-code tools.



\---



\## Parking Lot projects



memory\_key:

parking\_lot\_projects



memory\_value:

Immich; Dropbox migration/pCloud evaluation; Council of experts.



\---



\## Council use cases



memory\_key:

council\_use\_cases



memory\_value:

Investment analysis; Venture Lab idea analysis; retirement strategies.



\---



\## EchoStar status



memory\_key:

echostar\_job\_status



memory\_value:

Interviewed with EchoStar in Littleton and is awaiting a response or possible offer.



\---



\# Memory Extraction Contract



For every user message, the memory extractor should return zero or more operations.



Allowed actions:



IGNORE

CREATE

UPDATE



Example new fact:



{

&#x20; "action": "CREATE",

&#x20; "key": "favorite\_color",

&#x20; "value": "blue"

}



Example correction:



{

&#x20; "action": "UPDATE",

&#x20; "key": "favorite\_test\_animal",

&#x20; "value": "raven"

}



Example temporary statement:



{

&#x20; "action": "IGNORE"

}



Example confirmatory question:



{

&#x20; "action": "IGNORE"

}



\---



\# Decision Rules



\## CREATE



Use when:



\- information is useful beyond the current conversation

\- no equivalent semantic memory exists

\- information is grounded in what the user actually stated



\---



\## UPDATE



Use when:



\- the same semantic subject already exists

\- the user corrects it

\- the user changes preference

\- the user adds material refinement

\- newer information supersedes current state



UPDATE replaces the current value for that key.



\---



\## IGNORE



Use when:



\- information is temporary

\- message is only a question

\- message merely confirms known information

\- information is already represented accurately

\- information is model inference rather than user-supplied fact

\- information would provide no useful future continuity



\---



\# Duplicate Rule



Exact-string comparison is not sufficient.



Before CREATE, the extractor receives the current memories for that user and determines whether the new information refers to an existing semantic key.



Examples:



"My favorite color is blue."



and:



"I really like blue best."



should both resolve to:



favorite\_color



The second message should therefore produce IGNORE, not CREATE.



\---



\# Correction Rule



Example existing state:



favorite\_test\_animal = otter



Input:



"Actually, my favorite test animal is now a raven."



Expected operation:



UPDATE

favorite\_test\_animal = raven



There must not be two competing current values.



\---



\# Refinement Rule



Existing:



retirement\_location\_interest =

Thailand / Southeast Asia



Input:



"Malaysia is currently a stronger retirement candidate for me than Thailand."



Expected:



UPDATE



New value should preserve useful context while clearly identifying current state.



\---



\# User Isolation



Every lookup, create, and update operation must include user\_id.



The uniqueness boundary is:



(user\_id, memory\_key)



Never:



memory\_key globally



Therefore:



Jeff:

favorite\_test\_animal = raven



Test User 2:

favorite\_test\_animal = red panda



can coexist safely.



\---



\# Historical Memory



Not required for V1.



V1 stores current useful state.



If later evidence shows historical changes are valuable, add a separate history/audit mechanism.



Do not complicate the current-memory table now.



\---



\# Retrieval



For current V1 scale:



Retrieve all current memories for the selected user.



No embeddings or semantic retrieval required yet.



Later, if memory volume becomes large, retrieval strategy can be revisited.



\---



\# Migration Strategy



Do not attempt automated migration of the existing dirty database initially.



Safer approach:



1\. Preserve current DB as evidence.

2\. Build/test V1 against a temporary database.

3\. Pass MEMORY\_ACCEPTANCE.md tests.

4\. Pass existing Gate 0 regression.

5\. Only then decide whether to:

&#x20;  - manually normalize Jeff's existing memories, or

&#x20;  - create a fresh V1 memory database.



\---



\# Non-Goals



V1 does NOT add:



\- embeddings

\- vector databases

\- RAG

\- memory importance scores

\- decay

\- forgetting algorithms

\- long-term history

\- autonomous memory reflection

\- multi-agent memory

\- voice

\- avatar



\---



\# Success Condition



Memory Schema V1 is successful when:



\- MEMORY\_ACCEPTANCE.md Tests 1–10 pass

\- gate0\_regression.py still passes

\- browser memory inspector shows clean current state

\- corrected facts no longer accumulate contradictory current memories

