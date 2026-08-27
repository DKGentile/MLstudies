# Project Spec — Fill Before Training

## Operational question

What must the system detect and track, for whom, and what decision will its output
support?

## Constraints

| Constraint | Target | Why |
|---|---|---|
| Classes | | |
| Camera/input | | |
| Minimum useful object size | | |
| Accuracy metric and threshold | | |
| Desktop latency budget | | |
| Nano latency budget | | |
| Memory budget | | |
| Acceptable missed-track duration | | |

## Non-goals

List at least three things this iteration will not solve.

## Risks

Describe one dataset risk, one model risk, one deployment risk, and one schedule
risk. Give each a cheap early test.

## Definition of done

- [ ] Dataset, model-weight, and framework licenses plus split policy recorded
- [ ] Baseline accuracy reproduced from a command
- [ ] At least one export parity check passed
- [ ] Tracker synthetic tests passed
- [ ] Latency table includes methodology and hardware
- [ ] Failure cases are shown, not hidden
- [ ] Jetson result or time-boxed deferral is documented
