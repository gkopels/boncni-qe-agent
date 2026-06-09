# cnf-qe-agent

Cursor-oriented workflows for **MetalLB**, **Bond CNI**, and **OpenPERouter** OpenShift networking QE: high-level test plans drafted in chat (Google Docs publish on request), detailed test plans (Google Docs), Polarion LiveDoc publishing, and a four-phase lifecycle with explicit approval gates.

Pick the skill set that matches your Epic:

| Area | Skills (invoke in chat as `/skill-name`) | QE lifecycle reference |
| ---- | ---------------------------------------- | ---------------------- |
| **MetalLB** | `metallb-high-level-test-plan`, `metallb-detailed-test-plan`, `metallb-polarion-test-publish`, `metallb-manual-test-execution`, `metallb-e2e-automation` | [metallb-qe-lifecycle.mdc](.cursor/skills/metallb-detailed-test-plan/references/metallb-qe-lifecycle.mdc) |
| **Bond CNI** | `bond-cni-high-level-test-plan`, `bond-cni-detailed-test-plan`, `bond-cni-polarion-test-publish`, `bond-cni-manual-test-execution`, `bond-cni-e2e-automation` | [bond-cni-qe-lifecycle.mdc](.cursor/skills/bond-cni-detailed-test-plan/references/bond-cni-qe-lifecycle.mdc) |
| **OpenPERouter** | `openpe-high-level-test-plan`, `openpe-detailed-test-plan`, `openpe-polarion-test-publish`, `openpe-manual-test-execution`, `openpe-e2e-automation` | [openpe-qe-lifecycle.mdc](.cursor/skills/openpe-detailed-test-plan/references/openpe-qe-lifecycle.mdc) |

OpenPERouter product docs: [openperouter.github.io](https://openperouter.github.io/). Source: [openperouter/openperouter](https://github.com/openperouter/openperouter).

See [AGENTS.md](AGENTS.md) for agent guardrails. Skill layout and conventions are in [`.cursor/skills/README.md`](.cursor/skills/README.md).

Local-only directories (repo analysis clones, tooling venvs, **agent temp output** at `.cursor/workspaces/agent-tmp/`) live under `.cursor/workspaces/` and are not committed. Agents must put transient markdown and similar artifacts only in that gitignored tree—not in `/tmp` or tracked paths. Copy `.env.example` to `.env` and fill in real values (`.env` stays gitignored).

**Jira:** Agents read Epic context through `adapters/jira_adapter.py` using `JIRA_*` in `.env` (see [AGENTS.md](AGENTS.md)); Atlassian MCP is not used for Jira unless you explicitly request it.
