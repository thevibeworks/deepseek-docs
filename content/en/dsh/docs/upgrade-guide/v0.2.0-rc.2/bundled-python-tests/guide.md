---
title: "NumPy and pandas upstream tests require a separate environment"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.0-rc.2/bundled-python-tests/guide.md
fetched: 2026-10-10
---
# NumPy and pandas upstream tests require a separate environment

English | [中文](guide.zh.md)

## Change

Desktop and Python SDK runtime distributions previously included NumPy and pandas test directories. Bundled distributions now omit those directories, so scripts importing their test modules or running their complete upstream suites need a separate installation. Data processing, Office authoring, `numpy.testing`, `pandas.testing`, and `pandas._testing` remain available.

## Migration

1. If your scripts import `numpy.*.tests` or `pandas.tests`, install the original NumPy and pandas distributions and their upstream testing dependencies in a separate Python environment. Keep that environment outside the managed Harness runtime directory, which upgrades replace.
2. Run the affected scripts or upstream suites with that environment's interpreter. Scripts that use only library functionality or retained testing helpers require no changes.
3. Confirm that the previously failing test-module imports and affected scripts succeed with the separate interpreter. The bundled versions are recorded in the [runtime lock](../../../../scripts/primary-runtime/lock.json).
