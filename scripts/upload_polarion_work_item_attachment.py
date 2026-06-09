#!/usr/bin/env python3
"""Upload a file attachment to a Polarion work item."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from adapters.polarion_adapter import PolarionAdapter, read_qe_env  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Upload a file attachment to a Polarion work item."
    )
    parser.add_argument("--work-item", required=True, help="Work item id (e.g. OCP-89648)")
    parser.add_argument("--file", required=False, type=Path, help="Local file to upload")
    parser.add_argument("--title", default=None, help="Attachment title (default: file name)")
    parser.add_argument(
        "--mime-type",
        default=None,
        help="MIME type (default: application/octet-stream)",
    )
    parser.add_argument(
        "--project-id",
        default=None,
        help="Polarion project id (default: POLARION_PROJECT_ID from .env)",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="List existing attachments and exit (no upload)",
    )
    args = parser.parse_args(argv)

    env = read_qe_env(ROOT / ".env")
    base = env.get("POLARION_BASE_URL")
    proj = args.project_id or env.get("POLARION_PROJECT_ID")
    token = env.get("POLARION_TOKEN")
    if not all([base, proj, token]):
        print("Missing POLARION_BASE_URL, POLARION_PROJECT_ID, or POLARION_TOKEN", file=sys.stderr)
        return 2

    adapter = PolarionAdapter(base_url=base, project_id=proj, token=token)
    wid = args.work_item.strip()

    if args.list_only:
        items = adapter.list_work_item_attachments(wid)
        if not items:
            print(f"No attachments on {wid}.")
            return 0
        for item in items:
            attrs = item.get("attributes") or {}
            print(f"{item.get('id')}\t{attrs.get('title') or ''}\t{attrs.get('fileName') or ''}")
        return 0

    if not args.file:
        print("--file is required unless --list-only is set.", file=sys.stderr)
        return 2

    created = adapter.upload_work_item_attachment(
        wid,
        args.file,
        title=args.title,
        mime_type=args.mime_type,
    )
    links = created.get("links") or {}
    print(f"Uploaded to {wid}: {created.get('id')}")
    if links.get("self"):
        print(f"  REST: {links['self']}")
    portal = f"{base.rstrip('/')}/polarion/#/project/{proj}/workitem?id={wid}"
    print(f"  Portal: {portal}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
