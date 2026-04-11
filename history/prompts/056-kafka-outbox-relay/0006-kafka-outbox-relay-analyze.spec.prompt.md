---
id: 0006
title: kafka-outbox-relay-analyze
stage: spec
date: 2026-04-02
surface: terminal
model: gemini-cli
feature: 056-kafka-outbox-relay
branch: 056-kafka-outbox-relay
user: zohai
command: /sp.analyze
labels: [analyze, consistency, quality]
links:
  spec: specs/056-kafka-outbox-relay/spec.md
  plan: specs/056-kafka-outbox-relay/plan.md
  tasks: specs/056-kafka-outbox-relay/tasks.md
files:
  - specs/056-kafka-outbox-relay/spec.md
  - specs/056-kafka-outbox-relay/plan.md
  - specs/056-kafka-outbox-relay/tasks.md
---

## Prompt

Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md.

## Response snapshot

Identified 4 minor issues across the artifacts:
1. **Shutdown Measurement**: SC-004 (< 2s) lacks a timed verification task. (MEDIUM)
2. **Ambiguity**: "Robust" producer class needs clearer failure scenarios. (LOW)
3. **Underspecification**: Exponential backoff parameters are not defined. (MEDIUM)
4. **Inconsistency**: Plan mentions `DESC` (latest first) but Spec/Tasks specify FIFO (earliest first). (LOW)

Produced a full analysis report with a coverage summary table and constitution alignment check.

## Outcome

- ✅ Impact: Identified minor inconsistencies that could lead to implementation bugs (e.g., LIFO instead of FIFO).
- 🧪 Tests: Ensured all functional requirements have corresponding implementation tasks.
- 📁 Files: N/A (Read-only analysis)
- 🔁 Next prompts: /sp.implement
- 🧠 Reflection: Cross-referencing task-level verification against success criteria revealed missing timing measurements.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
