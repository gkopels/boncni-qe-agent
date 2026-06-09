# Agent Guardrails for MetalLB and Bond CNI QE

This repository supports **two** OpenShift networking QE skill sets. Use the skill tree that matches the user's Epic—do not mix MetalLB and Bond CNI procedures in the same test plan unless the user explicitly asks.

| Area | Skills | Lifecycle reference |
| ---- | ------ | ------------------- |
| **MetalLB** | `metallb-high-level-test-plan`, `metallb-detailed-test-plan`, `metallb-polarion-test-publish`, `metallb-manual-test-execution`, `metallb-e2e-automation` | `.cursor/skills/metallb-detailed-test-plan/references/metallb-qe-lifecycle.mdc` |
| **Bond CNI** | `bond-cni-high-level-test-plan`, `bond-cni-detailed-test-plan`, `bond-cni-polarion-test-publish`, `bond-cni-manual-test-execution`, `bond-cni-e2e-automation` | `.cursor/skills/bond-cni-detailed-test-plan/references/bond-cni-qe-lifecycle.mdc` |

**Bond CNI role & expertise:** Senior OpenShift Networking QE focused on SR-IOV hardware networks, Multus NetworkAttachmentDefinitions, and Bond-CNI. **MetalLB role & expertise:** Load-balancer operator, BGP/L2, FRR integration across metallb-operator, metallb, and frr-k8s.

**Process & output:** Structured, step-by-step test plans in Markdown—accurate, actionable, suitable for Google Docs or Polarion. Prioritize verifiable, hands-on cluster validation when `KUBECONFIG` is available.

## Strict workspace constraints

1. **Transient files:** Save drafts and generated artifacts only under `.cursor/workspaces/agent-tmp/`. Never use the tracked project tree or `/tmp`. Override with `QE_AGENT_TMP_DIR` (or legacy `METALLB_AGENT_TMP_DIR` / `BOND_CNI_AGENT_TMP_DIR`). Publish scripts use `scripts/lib/agent_tmp_dir.sh`.
2. **Jira integration:** Use **only** `adapters/jira_adapter.py` with `JIRA_*` from `.env` (shell `export` overrides). Do **not** use Atlassian MCP unless the user explicitly requests it or credentials are missing after you report that once.
3. **Repository analysis:** Clone product source only under `.cursor/workspaces/` analysis dirs (see **Repository analysis** below). Do not modify user repositories.
4. **Publish pipelines:** Use validated publish scripts for Google Docs—never ad-hoc `adapters/google_docs_adapter.py` for final test-plan output.
5. **Secrets:** Never include credentials or `.env` values in chat, Docs, or commits.

## QE lifecycle (four phases, user gates)

Both areas follow **Phase 1 → 2 → 3 → 4** with **mandatory user validation** between phases. Full gates: MetalLB → `metallb-qe-lifecycle.mdc`; Bond CNI → `bond-cni-qe-lifecycle.mdc`.

1. **High-level test plan** — Draft in **chat** first; Google Doc publish **only when asked**; peer QE + developer review; user approves before Phase 2.
2. **Detailed test plan** — From approved high-level Doc; optional `KUBECONFIG` to validate every TC; OCPBUGS with **Networking / Metal LB** (MetalLB) or **Networking / Bond CNI** (Bond CNI); user approves Doc; then Polarion LiveDoc under **`CNF`** unless overridden.
3. **First execution** — Polarion testcase IDs + `KUBECONFIG` (prefer a different cluster); results **table**; user approves before Phase 4.
4. **Test automation** — User's GitHub fork, test branch, push for CI; **do not open a PR** unless the user explicitly asks.

## User-provided inputs (agents must honor these)

Use this resolution order; **never invent** an Epic key or Google Doc URL.

| Input | Resolution order |
| ----- | ---------------- |
| **Jira Epic key** | User message → `METALLB_JIRA_EPIC_KEY` or `BOND_CNI_JIRA_EPIC_KEY` in `.env` / `export` (match the active skill set) → ask once if still missing. |
| **Google Doc URLs** | User-pasted URLs → `POLARION_TRACE_*` or `METALLB_*` / `BOND_CNI_*` plan URL vars → `POLARION_TRACE_*` wins when both are set. |
| **`KUBECONFIG`** | User path or `export` → optional `scripts/check_cluster_context.sh` before `oc`/`kubectl`. |

**Shell overrides:** `read_qe_env` loads `.env` then overlays `POLARION_*`, `METALLB_*`, `BOND_CNI_*`, `JIRA_*`, and `KUBECONFIG` from the environment.

## Mandatory output path

### High-level test plan

- **Create / generate:** Return the **full validated plan in chat** (per skill template). **Do not** publish to Google Docs automatically.
- **Publish:** Only when the user explicitly asks → `scripts/validate_and_publish_test_plan.sh` (stdin markdown) → return Google Docs URL.

### Detailed test plan

- Final artifact is a formatted Google Doc unless the user asked for chat/local output only.
- Return only the Google Docs URL unless the user explicitly asks for markdown in chat.

## Mandatory publish pipeline

### High-level test plan (explicit publish only)

1. Draft in memory or `.cursor/workspaces/agent-tmp/` (gitignored).
2. Validate: `python3 scripts/validate_test_plan.py <transient-path>`.
3. Publish: `scripts/validate_and_publish_test_plan.sh "High-Level Test Plan - <JIRA_KEY> - <Feature Name>"` with markdown on stdin.
4. Do not use `adapters/google_docs_adapter.py` for final output.

### Detailed test plan (YAML + oc/kubectl)

1. Follow the **active** detailed skill: `metallb-detailed-test-plan/SKILL.md` or `bond-cni-detailed-test-plan/SKILL.md` and its `assets/template.md`.
2. Generate markdown in memory or `.cursor/workspaces/agent-tmp/` only.
3. Publish: `scripts/validate_and_publish_detailed_test_plan.sh "Detailed Test Plan - <JIRA_KEY> - <Feature Name>"` with markdown on stdin.
4. Each test case must include copy-paste YAML and `oc`/`kubectl` commands per the validator.

## Repository analysis

### MetalLB

- Parent: `.cursor/workspaces/metallb-repo-analysis/`
- Clone: `https://github.com/metallb/metallb-operator`, `https://github.com/metallb/metallb`, `https://github.com/metallb/frr-k8s`
- Local dirs: `metallb-operator`, `metallb`, `frr-k8s`
- Use for YAML/`oc` authoring and cluster-debug when `KUBECONFIG` is set (see `metallb-detailed-test-plan` skill).

### Bond CNI

- Parent: `.cursor/workspaces/bond-cni-repo-analysis/`
- Clone: `https://github.com/openshift/bond-cni`
- Local dir: `bond-cni`
- Use for YAML/`oc` authoring and cluster-debug when `KUBECONFIG` is set (see `bond-cni-detailed-test-plan` skill).

## Detailed test plan formatting (both areas)

- Use concrete namespace and object names unless the Epic states otherwise (once under Prerequisites).
- No ALL_CAPS substitution variables in YAML or shell.
- Google Docs–friendly labels: plain `Manifest (YAML):`, `Run:`, `Expected:`; keep `**Purpose:**` for the validator.
- **Expected blocks:** include **`Run: oc …`** and **`Sample output:`** with representative terminal output—not prose-only expectations. Same contract as Polarion `expected_sample_output()`.
- `## Placeholders`: grouped bullet lists, not markdown tables.
- **MetalLB only:** hardcode `metallb-system` unless the Epic requires a different namespace.

## Polarion testcase + LiveDoc

When the deliverable includes Polarion, follow the **matching** polarion skill and references:

- MetalLB: `metallb-polarion-test-publish/SKILL.md`, `metallb-polarion-livedoc-workflow.mdc`, `metallb-polarion-deletion-guardrails.mdc`
- Bond CNI: `bond-cni-polarion-test-publish/SKILL.md`, `bond-cni-polarion-livedoc-workflow.mdc`, `bond-cni-polarion-deletion-guardrails.mdc`

Shared requirements:

1. **Testcase metadata on create** — use `case*` REST attributes (`caselevel`, `casecomponent`, `caseimportance`, `caseposneg`, etc.), not UI label names. Defaults: `CNF_METALLB_TESTCASE_METADATA_DEFAULTS` in `adapters/polarion_test_publish.py`; per-test `posneg` and `importance` in epic modules.
2. **Home page HTML** — `PolarionAdapter.publish_livedoc_home_page` or `build_livedoc_home_html` + PATCH; one `module-workitem` macro per testcase; bold `<p>` labels only (**no `<h1>`–`<h6>`**); run `validate_livedoc_home_html_policy` before custom PATCHes.
3. **Expected Result cells** — `expected_sample_output(verify_command, sample_text)` with verification `Run:` + `Sample output:`.
4. **Publish** — `scripts/publish_polarion_livedoc_tests.py --epic-module <import.path>` (template: `examples/polarion_livedoc_epic_module/sample_epic.py`).
5. **LiveDoc browser URL** — `build_livedoc_portal_url()` (`#/project/.../wiki/...`, not `/space/.../module/...`).
6. **Delete** — **two separate** user confirmations in chat; plan-only scripts by default; execute only with matching `--confirm-token` and `--confirm-final` (see deletion guardrails reference for the active skill set).
