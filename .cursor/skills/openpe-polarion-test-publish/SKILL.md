---
name: openpe-polarion-test-publish
description: Publish OpenPERouter (or CNF) manual test cases to Polarion with testcase work items and a LiveDoc home page that embeds full descriptions and Step/Expected Result tables—not only work-item macros.
---

# OpenPERouter / Polarion testcase + LiveDoc publish

## When to use

The user wants **Polarion test cases** and/or a **LiveDoc module** for OpenPERouter manual tests (often from a detailed test plan tied to a Jira Epic).

**QE lifecycle:** In the standard four-phase flow (`references/openpe-qe-lifecycle-reference.mdc`), Polarion publish happens in **Phase 2** **after** the user **approves** the **detailed** Google Doc.

## Non-negotiable behavior

After attaching testcase work items to a LiveDoc module, **always PATCH `homePageContent`** so the document itself shows:

- Document title and Contents (traceability **once per testcase** under that test — not at document top)
- Per testcase: title, link to WI, **Description**, **Setup**, **Test steps** as a **two-column table** (Step | Expected Result), **Teardown**
- Per testcase: **one `module-workitem` macro** plus readable inline HTML and a portal link. **No** trailing "Linked Polarion test cases" footer. **`validate_livedoc_home_html_policy`** requires exactly one macro per `work_item_id`, forbids **`<h1>`–`<h6>`**, and forbids the linked-section footer.

Use **bold `<p>` labels only** (`html_section_label`) — never `<h1>`–`<h6>`.

**Test steps — Expected Result:** For every epic `steps` tuple `(step_text, expected_text)`, set `expected_text` with **`expected_sample_output(verify_command, sample_text)`**. When building from an approved detailed Doc, copy **Run + Sample output** from each step’s **Expected** block (`openpe-detailed-test-plan`).

## Testcase work-item metadata (mandatory on create)

Use Polarion `case*` REST attributes (not UI label names). Defaults: `CNF_METALLB_TESTCASE_METADATA_DEFAULTS` in `adapters/polarion_test_publish.py` (same CNF/telco defaults as MetalLB unless the user specifies otherwise).

| UI label | Polarion attribute | Value |
|----------|-------------------|-------|
| Level | `caselevel` | `component` |
| Component | `casecomponent` | `telco` |
| Subcomponent | `subcomponent` | `cnfnetwork` |
| Sub Team | `subteam` | `kni` |
| Products | `products` | `ocp` |
| Test type | `testtype` | `functional` |
| Automation | `caseautomation` | `notautomated` |
| Upstream | `upstream` | `no` |

**Per testcase:** `posneg` (`Positive`/`Negative`) and `importance` (`Critical`/`High`/`Medium`/`Low`) → mapped by `resolve_testcase_metadata()`.

## Code to reuse

Same shared adapters/scripts as MetalLB Polarion publish:

| Piece | Role |
|-------|------|
| `adapters.polarion_adapter.html_section_label` | Bold `<p>` section titles |
| `adapters/polarion_livedoc.build_livedoc_home_html` | Standard HTML + policy validation |
| `PolarionAdapter.publish_livedoc_home_page` | Build + PATCH |
| `adapters.polarion_test_publish.expected_sample_output` | Expected Result Run + Sample output |
| `scripts/publish_polarion_livedoc_tests.py` | `--epic-module <import.path>` |
| `examples/polarion_livedoc_epic_module/sample_epic.py` | Template for epic modules |

See `references/openpe-polarion-livedoc-workflow.mdc` and `references/openpe-polarion-deletion-guardrails.mdc`.

## Space / location

Prefer LiveDoc space **`CNF`**. Override with `POLARION_SPACE_ID` or `--space-id`.

## Traceability env

- **Preferred:** `POLARION_TRACE_*` in `.env` or shell `export`.
- **Convenience:** `OPENPE_JIRA_EPIC_KEY`, `OPENPE_HIGH_LEVEL_PLAN_URL`, `OPENPE_DETAILED_PLAN_URL` when the corresponding `POLARION_TRACE_*` is unset (`merge_traceability_from_env` also accepts MetalLB/Bond CNI keys).

## Delete

**Two separate** user confirmations in chat; plan-only scripts by default. Follow `references/openpe-polarion-deletion-guardrails.mdc`.
