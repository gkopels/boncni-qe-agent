---
name: openpe-e2e-automation
description: Add OpenPERouter automated tests on the user's GitHub fork branch and validate via GitHub Actions; no PR unless user requests. Use in QE Phase 4.
---

# OpenPERouter e2e test automation (Phase 4)

## When to use

**Phase 4** of the OpenPERouter QE lifecycle: implement **automated** tests in the **product** repository (or the suite the user designates), validated on **GitHub CI** on the **user’s** fork.

**Prerequisite:** User **explicitly approved** completion of Phase 3 for this feature set.

## Non-negotiables

- **Clone the user’s fork** (or repo the user specifies) with the **user’s** Git credentials.
- Create a **test branch**; add or extend tests following **upstream** patterns in that repo.
- **Push** so **GitHub Actions** on the user’s repo runs.
- **Do not open a pull request** by default. Open a PR only if the user explicitly asks.

## Repository facts

Primary upstream: [openperouter/openperouter](https://github.com/openperouter/openperouter)

- Inspect the repo for existing test layout (`e2e/`, `test/`, `hack/`, Makefile/CI workflows, KIND or cluster scripts).
- Prefer extending the **same** framework CI already runs.
- Docs: [openperouter.github.io](https://openperouter.github.io/) (install, EVPN, SRv6, examples including MetalLB integration).

If the user points automation at a different fork or internal mirror, follow that path instead.

## Workflow

1. **Confirm gate** — User approves automation; confirm **fork URL**, **branch name**, and target repo.
2. **Clone and branch** — `git clone` user fork; `git checkout -b <test-branch>`.
3. **Implement tests** — Match existing suite style and CI assumptions.
4. **Local sanity (optional)** — Run a narrow subset if the user’s machine and docs support it.
5. **Push and CI** — Monitor Actions on the **user’s** GitHub repo; report conclusion and run link.
6. **Response** — Branch name, commits, CI status, follow-ups.

## Analysis clone vs automation clone

- **Read-only analysis** for plans: `.cursor/workspaces/openpe-repo-analysis/`
- **Automation work:** user-provided clone/fork path — do not conflate unless the user wants one workspace.

## Constraints

- No credentials in commits.
- Respect `references/openpe-qe-lifecycle-reference.mdc` phase ordering.
