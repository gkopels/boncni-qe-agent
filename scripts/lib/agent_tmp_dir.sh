#!/usr/bin/env bash
# Resolve the gitignored directory for agent-generated transient files.
# Override with BOND_CNI_AGENT_TMP_DIR if needed.

bond_cni_agent_tmp_dir() {
  local root_dir="${1:?root_dir required}"
  local dir="${BOND_CNI_AGENT_TMP_DIR:-${root_dir}/.cursor/workspaces/agent-tmp}"
  mkdir -p "${dir}"
  printf '%s\n' "${dir}"
}
