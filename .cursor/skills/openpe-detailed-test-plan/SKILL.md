---
name: openpe-detailed-test-plan
description: Expand OpenPERouter high-level test cases into a detailed manual test plan with copy-paste YAML manifests and oc/kubectl commands, grounded in Jira, design docs, and openperouter source. Use when the user asks for a detailed test plan or executable YAML/commands for OpenPE / OpenPERouter.
---

# OpenPERouter Detailed Test Plan

## Purpose

Turn each high-level test case into **operator-ready manual steps**: concrete Kubernetes/OpenShift YAML and `oc` / `kubectl` commands, with expected observations and cleanup.

## Required Inputs

- **Jira Epic key**, and/or
- **Approved** high-level test plan Google Doc URL
- Optional: **`KUBECONFIG`** for a dedicated test OpenShift cluster
- Optional: underlay iface names, ToR BGP neighbors, VNI/VPN IDs, MetalLB integration constraints

**Resolution:** Epic key and Doc URL(s) from the **user message first**; optional fallback `OPENPE_JIRA_EPIC_KEY`. For cluster work, export `KUBECONFIG` then `oc whoami` or `scripts/check_cluster_context.sh`. If Phase 1 is not approved, ask before proceeding (see `references/openpe-qe-lifecycle.mdc`).

**Publish title:** `scripts/validate_and_publish_detailed_test_plan.sh "Detailed Test Plan - <JIRA_KEY> - <Feature Name>"`.

## QE Phase 2: cluster validation, bugs, Polarion timing

- **Gate:** Only after **high-level plan approval**.
- **Product repo (mandatory):** Clone/update `https://github.com/openperouter/openperouter` under `.cursor/workspaces/openpe-repo-analysis/openperouter`. Use for YAML/`oc` authoring and cluster-debug.
- **With `KUBECONFIG`:** Exercise **every** proposed TC; align each step **Expected** with **`Run:` + `Sample output:`**.
- **Triage:** Product bug → Jira `project = OCPBUGS`, **component = `Networking / OpenPERouter`** (confirm component with the user if Jira rejects it). Procedure error → fix plan and re-validate.
- **Polarion:** After detailed Doc **approval**, publish under Polarion space **`CNF`** via `openpe-polarion-test-publish` unless the user overrides space.
- **Next phase:** Do not start Phase 3/4 until the user approves.

## Workflow

1. **Align with high-level coverage** — same `TC-0N` IDs and intents.
2. **Collect Jira and doc context** — `adapters/jira_adapter.py` + `.env` `JIRA_*` only (no Atlassian MCP unless asked).
3. **Refresh analysis repo**
   - Parent: `.cursor/workspaces/openpe-repo-analysis/`
   - Clone: `https://github.com/openperouter/openperouter` → local dir `openperouter`
   - Inspect CRDs, controllers, install manifests (`config/all-in-one/`, Helm charts), and examples.
4. **Author executable steps**
   - Ordered `#### Step N` with `Manifest (YAML):`, `Run:`, `Expected:` (plain labels).
   - **Expected** must include verification `Run: oc …` and `Sample output:` (not prose-only).
   - Cover install/upgrade when in scope; Underlay CR; overlay CRs (EVPN/SRv6/passthrough as applicable); host BGP peers; dataplane checks.
5. **Namespace and literals**
   - Hardcode **`openperouter-system`** unless the Epic states another namespace (state once under Prerequisites).
   - No ALL_CAPS substitution variables in YAML/shell.
6. **`## Placeholders`** — grouped bullet lists (not tables).
7. **Render** with `assets/template.md`; keep content under `.cursor/workspaces/agent-tmp/` only.
8. **Validate and publish** via `scripts/validate_and_publish_detailed_test_plan.sh`.
9. **Response** — Google Docs URL only unless the user asked for markdown. Do not Polarion-publish until detailed Doc approval.

## Quality Constraints

- YAML must match real OpenPERouter CRD `apiVersion`/`kind` from analyzed source/docs.
- Keep Google Docs readable: no prose inside fenced YAML; keep `**Purpose:**` for the validator.
- Never embed credentials or switch passwords in the plan.

## Output Contract

Follow `assets/template.md`. Return Docs URL after publish unless the user requested chat/local markdown.
