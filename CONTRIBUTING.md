# Contributing to ITEA

Thank you for your interest. ITEA is maintained by a single author, so the
paths below are kept simple.

## Reporting a problem or asking for help

Open an issue at https://github.com/Aval22/ITEA/issues. For a bug, include
the command you ran, the `itea` version (`python -c "import itea; print(itea.__version__)"`),
and the full error. For a question about the methodology, cite the indicator
and the document section you are reading. Issues are usually answered within
two weeks.

## Proposing a change

1. Fork the repository and create a branch from `main`.
2. Install in editable mode with the test extras: `pip install -e ".[test]"`.
3. Fetch the public inputs once (`itea fetch`) so that the end-to-end
   reproduction test runs, then run `pytest`.
4. Open a pull request describing what changes and why. Changes that alter
   published index values need a CHANGELOG entry explaining the reason.

Data corrections (for instance a misgraded AXI task) are welcome as issues
with the task's `SOC_CODE`, `Task_ID` and the proposed grade with its
rationale.

## Code of conduct

Be respectful and constructive. Harassment or personal attacks are not
tolerated; the maintainer may close or lock threads that break this rule.
