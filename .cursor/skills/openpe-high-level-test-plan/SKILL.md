---
name: openpe-high-level-test-plan
description: Generate a high-level test plan for OpenPERouter features using a Jira Epic key, linked design docs/PRs, and deep code analysis of openperouter. Use when the user asks for a high-level test plan, QA scope, or test cases for OpenPE / OpenPERouter / PE router networking.
---

# OpenPERouter High-Level Test Plan

## Purpose

Create a consistent, evidence-based high-level test plan by combining:

- Jira Epic context (feature intent, links, acceptance notes)
- Design documents and PR references
- Source analysis of [openperouter/openperouter](https://github.com/openperouter/openperouter)
- Product docs at [openperouter.github.io](https://openperouter.github.io/)

## Required Inputs

- Jira Epic key (for example `NET-1234` or `CNF-45678`)
- Optional explicit design doc links
- Optional constraints (EVPN vs SRv6, underlay topology, MetalLB/Multus integration, release target)

**Resolution:** Prefer the Epic key and doc URLs **stated in the user message**. If the key is missing, check optional `OPENPE_JIRA_EPIC_KEY` in `.env` (or shell `export`). If still missing, ask once before proceeding—do not guess keys.

**Google Doc title:** When the user asks to **publish**, use `scripts/validate_and_publish_test_plan.sh "High-Level Test Plan - <JIRA_KEY> - <Feature Name>"` with the **same** `<JIRA_KEY>` the user provided (normalize to uppercase if they gave a mixed-case key).

## QE Phase 1 and user gate

This skill covers **Phase 1** only. Phase 1 has **two agent steps** separated by user intent:

1. **Draft (default)** — User asks to *create* / *generate* a high-level test plan → return the full plan **in the chat response** (see **Output Contract**). **Do not** publish to Google Docs.
2. **Publish (explicit only)** — User asks to *publish* the high-level plan (to Google Docs) → run validation + `validate_and_publish_test_plan.sh` and return the Google Docs URL.

After publish, the user may edit the Doc and run **peer QE + Epic assignee (developer) review** until satisfied.

**Do not** start the **detailed** test plan (`openpe-detailed-test-plan`), Phase 3 execution, Polarion publish for procedures, or e2e automation **for the same Epic** until the user **explicitly states** the high-level plan is **approved**.

## Workflow

1. **Collect Jira and doc context**
   - **Mandatory:** `adapters/jira_adapter.py` with `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_TOKEN` from `.env` (see `AGENTS.md` — Jira access). Use `JiraAdapter.from_env().get_issue(<key>)` and `get_remote_issue_links(<key>)`.
   - **Do not** use the Atlassian Cursor MCP for Jira unless the user explicitly requests MCP or `.env` Jira credentials are unavailable (report once, then ask how to proceed).
   - Design docs: Epic description, remote links, user-pasted URLs, and [OpenPERouter docs](https://openperouter.github.io/).

2. **Create temporary analysis workspace**
   - Clone into `.cursor/workspaces/openpe-repo-analysis/`
   - Local directory after clone: `openperouter`
   - Repository: `https://github.com/openperouter/openperouter`
   - Prefer shallow clone; refresh with `git fetch` / `git pull` if present.
   - Analysis-only — do not modify user product forks here.

3. **Analyze OpenPERouter source**
   - CRDs / API (`api/`, `config/crd/`)
   - Controller and router DaemonSets / Deployments
   - Underlay, EVPN/VXLAN, SRv6 L3VPN, passthrough, resiliency paths
   - Host veth / VRF / FRR integration
   - Examples that integrate MetalLB, Multus, Calico (docs + `examples/` if present)
   - Install paths: all-in-one manifests, kustomize, Helm

4. **Define scope**
   - In Scope: directly impacted underlay/overlay behavior and host BGP integrations
   - Out of Scope / Limitations: unsupported overlay modes, fabric dependencies, early-project caveats (docs mark the project early-stage)
   - Explicitly call out whether MetalLB / Multus / FRR-K8s are **integration dependencies** for this Epic vs out of scope

5. **Write high-level test cases**
   - Include happy path, negative/validation, and reconciliation/state propagation.
   - Prefer observable outcomes: CR status/conditions, BGP neighbor state (fabric + host), VRF/veth presence, EVPN/SRv6 route exchange, dataplane connectivity, controller/router pod health.

6. **Render output with exact template**
   - Use `assets/template.md`.
   - Keep drafts in memory or under `.cursor/workspaces/agent-tmp/` only (gitignored).

7. **Validate draft**
   - `python3 scripts/validate_test_plan.py <transient-markdown-path>`

8. **Deliver draft in chat (default — do not publish)**

9. **Publish to Google Docs (only when user explicitly asks)**
   - `scripts/validate_and_publish_test_plan.sh "High-Level Test Plan - <JIRA_KEY> - <Feature Name>"` with markdown on stdin.
   - Do not use `adapters/google_docs_adapter.py` for final output.
   - Return **only** the Google Docs URL unless the user also asked for markdown.

## OpenPERouter deployment context

Default install namespace in docs: **`openperouter-system`**.

Typical components after install:

- `openperouter-controller-*` (controller)
- `openperouter-router-*` (router / FRR in persistent netns)
- `openperouter-nodemarker-*` (node index labeler)

Configuration is CRD-driven (Underlay + overlay/VPN CRs). Tests should cover underlay BGP to ToR, overlay creation (EVPN L2/L3 and/or SRv6 as in Epic scope), and host-side BGP to components such as MetalLB when the Epic requires it.

## Quality Constraints

- Keep feature summary concise and concrete.
- Every test case must include purpose, procedure, expected result, and pass/fail criteria.
- Tie scope statements to evidence (Jira/doc/code paths).
- Never include credentials or secret values from `.env`.
- On **draft**: return the full plan in chat; do **not** publish to Google Docs.
- On **publish**: return the Google Docs URL (unless the user also asked for markdown).

## Output Contract

**Draft response (create / generate):** Include the complete plan markdown using:

- `# High-Level Test Plan: <Feature Name> (<JIRA_KEY>)`
- `## JIRA Reference`
- `## Feature Summary`
- `## Scope` with `### In Scope` and `### Out of Scope / Limitations`
- `## Test Cases` with at least 3 test cases (`TC-01` onward)
- `## References`

## Follow-on: detailed manual plan

After Phase 1 approval, use **`openpe-detailed-test-plan`** and publish via `scripts/validate_and_publish_detailed_test_plan.sh` per `references/openpe-test-plan-workflow.mdc` and `.cursor/skills/openpe-detailed-test-plan/references/openpe-qe-lifecycle.mdc`.
