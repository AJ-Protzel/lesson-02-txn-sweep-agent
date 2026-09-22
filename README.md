# lesson-02-txn-sweep-agent

Second in a series of small agent projects. Lesson 01 was
[lesson-01-csv-qa-agent](https://github.com/AJ-Protzel/lesson-01-csv-qa-agent).

Planned: an agent over a real transaction export, graded by an eval written
before the agent exists.

## Ground rules for this one

Lesson 01 was built for me while I watched, which produced a working repo and
not much else. These rules exist to stop that happening twice.

- Discovery first. The spec comes out of a customer conversation, not a chatbot
  handing me a finished one.
- The eval is written before any agent code, against real and messy data.
- Expected answers are computed independently, never taken from the model being
  tested.
- The system prompt is written by hand.
- Two cases are expected to fail. Every failure gets a decision recorded in
  `decisions.md`: fix the prompt, fix the grader, or accept the limit.
- Ship when the pass rate stops moving, not at 100%.
