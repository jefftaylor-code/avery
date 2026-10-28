\# Avery Memory V1 Automated Test Plan



Date: 2026-09-22



\## Objective



Verify Memory Schema V1 against deterministic scenarios before integrating it into Avery.



All tests must use a temporary database.



The production Avery database must not be modified.



\---



\## Test Sequence



\### Test 1 — CREATE



Existing state:

none



Input:

"My favorite color is blue."



Expected operation:

CREATE



Expected state:

favorite\_color = blue



Expected memory count for key:

1



\---



\### Test 2 — Exact duplicate



Existing:

favorite\_color = blue



Input:

"My favorite color is blue."



Expected operation:

IGNORE



Expected state:

favorite\_color = blue



Expected memory count for key:

1



\---



\### Test 3 — Semantic duplicate



Existing:

favorite\_color = blue



Input:

"I really like blue best."



Expected operation:

IGNORE



Expected state:

favorite\_color = blue



Expected memory count for key:

1



\---



\### Test 4 — Correction



Existing:

favorite\_test\_animal = otter



Input:

"Actually, my favorite test animal is now a raven."



Expected operation:

UPDATE



Expected state:

favorite\_test\_animal = raven



Expected competing current memories:

0



\---



\### Test 5 — Refinement



Existing:

retirement\_location\_interest = Thailand / Southeast Asia



Input:

"Malaysia is currently a stronger retirement candidate for me than Thailand."



Expected operation:

UPDATE



Expected state:

Must clearly represent Malaysia as the current stronger candidate while preserving useful Southeast Asia context.



\---



\### Test 6 — Temporary fact



Input:

"I'm drinking coffee right now."



Expected operation:

IGNORE



Expected durable memory change:

none



\---



\### Test 7 — Explicit durable preference



Input:

"For future reference, I prefer technical explanations that show how each component works."



Expected operation:

CREATE or UPDATE appropriate preference key



Expected state:

one durable explanation-style preference



\---



\### Test 8 — Confirmatory question



Existing:

retirement\_location\_interest includes Thailand



Input:

"Did I tell you I'm considering Thailand for retirement?"



Expected operation:

IGNORE



Expected state change:

none



\---



\### Test 9 — User isolation



Jeff:

favorite\_test\_animal = raven



Test User 2:

favorite\_test\_animal = red panda



Expected:

Each user receives only their own value.



Restart process.



Expected:

Isolation and persistence remain intact.



\---



\### Test 10 — No inferred personality storage



Input:

"I use Immich and I'm moving away from Dropbox."



Possible Avery inference:

"Jeff values independence and control."



Expected:

Grounded user facts may be stored.



The inferred personality conclusion must NOT be stored automatically.



\---



\# Required Outputs Per Test



Each automated test should print:



\- TEST NAME

\- INPUT

\- OPERATION

\- KEY

\- OLD VALUE

\- NEW VALUE

\- PASS / FAIL



Example:



TEST: Correction

OPERATION: UPDATE

KEY: favorite\_test\_animal

OLD: otter

NEW: raven

RESULT: PASS



\---



\# Final Regression Requirement



After Memory V1 tests pass:



python gate0\_regression.py



must still return:



GATE 0 REGRESSION: PASS

