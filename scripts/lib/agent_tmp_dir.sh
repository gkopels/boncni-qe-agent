#!/usr/bin/env bash
# Resolve the gitignored directory for agent-generated transient files.
# Override with QE_AGENT_TMP_DIR, or legacy METALLB_AGENT_TMP_DIR / BOND_CNI_AGENT_TMP_DIR.

qe_agent_tmp_dir() {
  local root_dir="${1:?root_dir required}"
  local dir="${QE_AGENT_TMP_DIR:-${METALLB_AGENT_TMP_DIR:-${BOND_CNI_AGENT_TMP_DIR:-${root_dir}/.cursor/workspaces/agent-tmp}}}"
  mkdir -p "${dir}"
  printf '%s\n' "${dir}"
}
