\# Avery Memory Hygiene Acceptance Tests



Date: 2026-09-22



\## Purpose



Define the required behavior for Avery's next memory-system revision.



Implementation must preserve:

\- persistent memory

\- process-restart persistence

\- per-user isolation

\- current browser behavior

\- memory inspector visibility



\## Test 1 — New durable fact



Starting state:

No memory exists for `favorite\_color`.



Input:

"My favorite color is blue."



Expected:

\- One durable memory is created.

\- Later recall returns blue.

\- Restart does not lose the memory.



PASS if:

Exactly one current fact represents favorite color = blue.



\---



\## Test 2 — Exact duplicate



Starting state:

favorite color = blue



Input:

"My favorite color is blue."



Expected:

\- No additional semantic duplicate is created.

\- Existing fact remains unchanged.



PASS if:

Only one current favorite-color fact exists.



\---



\## Test 3 — Paraphrased duplicate



Starting state:

favorite color = blue



Input:

"I really like blue best."



Expected:

\- System recognizes this as the same underlying fact.

\- No redundant second memory is created.



PASS if:

One current favorite-color fact remains.



\---



\## Test 4 — Correction



Starting state:

favorite animal = otter



Input:

"Actually, my favorite animal is now a raven."



Expected:

\- Current favorite-animal fact becomes raven.

\- Otter is no longer treated as the current value.

\- Later recall returns raven.



PASS if:

Avery does not have competing current otter/raven facts.



\---



\## Test 5 — Refinement



Starting state:

retirement interest = Thailand / Southeast Asia



Input:

"Malaysia is currently a stronger retirement candidate for me than Thailand."



Expected:

\- Current retirement preference reflects Malaysia > Thailand.

\- Useful prior context may be preserved without confusing it with current state.



PASS if:

Later recall accurately describes the current preference.



\---



\## Test 6 — Temporary fact



Input:

"I'm drinking coffee right now."



Expected:

\- No durable memory created.



PASS if:

Inspector shows no new durable coffee memory.



\---



\## Test 7 — Explicit durable preference



Input:

"For future reference, I prefer technical explanations that show how each component works."



Expected:

\- Durable preference is stored.

\- Later advice can use it.



PASS if:

Preference survives restart and appears once.



\---



\## Test 8 — Confirmatory question



Starting state:

retirement interest includes Thailand



Input:

"Did I tell you I'm considering Thailand for retirement?"



Expected:

\- No new memory created.



PASS if:

Memory count/state is unchanged.



\---



\## Test 9 — User isolation



Jeff:

favorite animal = raven



Test User 2:

favorite animal = red panda



Expected:

\- Jeff recalls raven only.

\- Test User 2 recalls red panda only.

\- No leakage after restart.



PASS if:

Automated isolation regression still passes.



\---



\## Test 10 — Model inference is not user fact



Input:

"I use Immich and I'm moving away from Dropbox."



Avery may infer:

"Jeff values independence and control."



Expected:

\- Source facts may be stored.

\- Avery's inferred personality interpretation must NOT automatically become a user fact.



PASS if:

Inspector contains only grounded user-supplied information.



\---



\# Gate for Memory Hygiene



Memory hygiene is complete only when Tests 1–10 pass without breaking Gate 0 regression.

