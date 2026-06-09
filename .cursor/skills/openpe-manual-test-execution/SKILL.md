---
name: openpe-manual-test-execution
description: Run finalized manual/Polarion OpenPERouter test cases against an OpenShift cluster using KUBECONFIG and report results in a table. Use in QE Phase 3 after detailed plan and Polarion testcase IDs exist.
---

# OpenPERouter manual test execution (Phase 3)

## When to use

**Phase 3** of the OpenPERouter QE lifecycle: first execution of finalized procedures, typically keyed by **Polarion testcase work item IDs**.

**Prerequisite:** User has **explicitly approved** proceeding past Phase 2.

## Required inputs

- **Polarion testcase IDs** (execution order if relevant)
- **`KUBECONFIG`** path or env from the user
- **Procedure source:** Polarion steps and/or approved detailed Google Doc

**Resolution:** IDs and Doc URL from the user message. Export `KUBECONFIG` exactly as supplied. Optionally run `scripts/check_cluster_context.sh`.

## Workflow

1. **Confirm gate** — Phase 2 approval; prefer a **different** cluster from Phase 2 when the lifecycle calls for it.
2. **Configure CLI** — `export KUBECONFIG=...`; verify with `oc whoami` / `scripts/check_cluster_context.sh`.
3. **Per testcase** — Execute Setup → Steps → Expected (`Run:` + `Sample output:`) → Teardown. Capture evidence on failures.
4. **Report** — Markdown table:

   | Polarion ID | Test title (short) | Result (Pass/Fail/Blocked/Skipped) | Notes |
   | ----------- | ------------------ | ------------------------------------ | ----- |

5. **Bugs** — Product bug → Jira `project = OCPBUGS`, **component = `Networking / OpenPERouter`** (confirm with user if Jira component differs).

## Constraints

- Do not store kubeconfig or tokens in the workspace or Google Docs.
- Align with `references/openpe-qe-lifecycle-reference.mdc`.
