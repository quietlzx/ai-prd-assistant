#!/usr/bin/env python3
"""Structure-only harness for the AI PRD Assistant workflow."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


PIPELINE_STATUSES = {
    "RUNNING",
    "READY",
    "DRAFT_WITH_GAPS",
    "BLOCKED",
    "HARNESS_FAILED",
}
VALIDATION_STATUSES = {"READY", "DRAFT_WITH_GAPS", "BLOCKED", "HARNESS_FAILED"}
REVIEW_STATES = {"pending", "approved", "rejected", "revision"}

DISCLAIMER = (
    "本回答由AI基于你有权访问的内部文档生成，仅供内部资料检索参考，"
    "不可替代公司正式制度、业务审批、法务、人力或财务结论。"
    "请以正式文件和授权人员意见为准。"
)

REQUIRED_RUN_FIELDS = {
    "run_id",
    "framework_version",
    "pipeline_status",
    "review_state",
    "timestamp",
    "input_summary",
}

REQUIRED_BRIEF_FIELDS = {
    "product_goal",
    "target_users",
    "scenarios",
    "business_constraints",
    "success_metrics",
    "scope_boundaries",
    "unknowns",
}

REPORT_FILES = ("05_report.md", "05_report.html")


class HarnessFailure(Exception):
    """Raised when a structural contract fails."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HarnessFailure(f"missing file: {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise HarnessFailure(f"invalid JSON in {path.name}: {exc}") from exc

    if not isinstance(value, dict):
        raise HarnessFailure(f"{path.name} must contain a JSON object")
    return value


def require_fields(value: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(field for field in fields if field not in value)
    if missing:
        raise HarnessFailure(f"{label} missing fields: {', '.join(missing)}")

    null_fields = sorted(
        field for field in fields if value.get(field) is None
    )
    if null_fields:
        raise HarnessFailure(
            f"{label} contains null fields: {', '.join(null_fields)}"
        )


def require_known(value: Any, allowed: set[str], label: str) -> None:
    if value not in allowed:
        choices = ", ".join(sorted(allowed))
        raise HarnessFailure(f"{label} must be one of: {choices}")


def require_nonempty_list(value: Any, label: str) -> None:
    if not isinstance(value, list) or not value:
        raise HarnessFailure(f"{label} must be a non-empty list")


def check_pending_markers(markdown: str) -> None:
    if re.search(r"\[待确认\](?!:)", markdown):
        raise HarnessFailure(
            "unnumbered [待确认] marker found; use [待确认:Gxx] and "
            "centralize the item in Appendix A"
        )


def check_single_file_html(html: str) -> None:
    external_patterns = (
        r"<script[^>]+src\s*=",
        r"<link[^>]+href\s*=",
        r"url\(\s*['\"]?https?://",
        r"\bhttps?://",
    )
    for pattern in external_patterns:
        if re.search(pattern, html, flags=re.IGNORECASE):
            raise HarnessFailure(
                "single-file HTML contains an external script, stylesheet, "
                "font, or network URL"
            )


def check_report_text(markdown: str) -> None:
    if DISCLAIMER not in markdown:
        raise HarnessFailure("Markdown report is missing the required disclaimer")
    check_pending_markers(markdown)

    if "附录 A：待确认事项清单" not in markdown:
        raise HarnessFailure("Markdown report is missing Appendix A")


def validate_run(run_dir: Path) -> dict[str, Any]:
    if not run_dir.is_dir():
        raise HarnessFailure(f"run directory does not exist: {run_dir}")

    run = load_json(run_dir / "run.json")
    require_fields(run, REQUIRED_RUN_FIELDS, "run.json")
    require_known(
        run["pipeline_status"], PIPELINE_STATUSES, "pipeline_status"
    )
    require_known(run["review_state"], REVIEW_STATES, "review_state")

    brief = load_json(run_dir / "01_brief.json")
    require_fields(brief, REQUIRED_BRIEF_FIELDS, "01_brief.json")

    validation = load_json(run_dir / "02_validation.json")
    require_fields(
        validation,
        {"status", "reason", "gaps", "clarification_questions"},
        "02_validation.json",
    )
    require_known(
        validation["status"], VALIDATION_STATUSES, "validation status"
    )

    if validation["status"] == "BLOCKED":
        require_nonempty_list(
            validation["clarification_questions"],
            "clarification_questions",
        )
        for downstream in (
            "03_prd.md",
            "04_ai_risks.md",
            "04_review_packet.json",
            "04_human_review.json",
            *REPORT_FILES,
        ):
            if (run_dir / downstream).exists():
                raise HarnessFailure(
                    f"BLOCKED run must not create downstream artifact: "
                    f"{downstream}"
                )
        return {"status": "BLOCKED", "run_id": run["run_id"]}

    missing = [
        name
        for name in ("03_prd.md", "04_ai_risks.md", "04_review_packet.json")
        if not (run_dir / name).is_file()
    ]
    if missing:
        raise HarnessFailure(
            f"required Stage 3-4 artifacts missing: {', '.join(missing)}"
        )

    prd = (run_dir / "03_prd.md").read_text(encoding="utf-8")
    risks = (run_dir / "04_ai_risks.md").read_text(encoding="utf-8")
    if "验收标准" not in prd:
        raise HarnessFailure("PRD is missing acceptance criteria")
    if "风险编号" not in risks or "验证方法" not in risks:
        raise HarnessFailure("AI risk artifact is missing fixed risk fields")

    review = load_json(run_dir / "04_human_review.json")
    require_fields(
        review,
        {"review_state", "reviewer", "reviewed_at", "change_requests"},
        "04_human_review.json",
    )
    require_known(review["review_state"], REVIEW_STATES, "review state")
    if review["review_state"] != run["review_state"]:
        raise HarnessFailure(
            "run.json review_state and 04_human_review.json disagree"
        )

    if run["review_state"] == "approved":
        missing_reports = [
            name for name in REPORT_FILES if not (run_dir / name).is_file()
        ]
        if missing_reports:
            raise HarnessFailure(
                f"approved run missing report artifacts: "
                f"{', '.join(missing_reports)}"
            )
        markdown = (run_dir / "05_report.md").read_text(encoding="utf-8")
        html = (run_dir / "05_report.html").read_text(encoding="utf-8")
        check_report_text(markdown)
        check_single_file_html(html)
        if DISCLAIMER not in html:
            raise HarnessFailure("HTML report is missing the required disclaimer")
    else:
        premature = [
            name for name in REPORT_FILES if (run_dir / name).exists()
        ]
        if premature:
            raise HarnessFailure(
                "reports must not exist before review approval: "
                f"{', '.join(premature)}"
            )

    return {
        "status": "PASS",
        "run_id": run["run_id"],
        "pipeline_status": run["pipeline_status"],
        "review_state": run["review_state"],
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-prd-harness-") as temp:
        run_dir = Path(temp)
        write_json(
            run_dir / "run.json",
            {
                "run_id": "self-test",
                "framework_version": "v1.0-framework",
                "pipeline_status": "DRAFT_WITH_GAPS",
                "review_state": "pending",
                "timestamp": "2026-09-27",
                "input_summary": "self test",
            },
        )
        write_json(
            run_dir / "01_brief.json",
            {
                "product_goal": {},
                "target_users": [],
                "scenarios": [],
                "business_constraints": [],
                "success_metrics": [],
                "scope_boundaries": {},
                "unknowns": [],
            },
        )
        write_json(
            run_dir / "02_validation.json",
            {
                "status": "DRAFT_WITH_GAPS",
                "reason": "pending decisions",
                "gaps": [],
                "clarification_questions": [],
            },
        )
        (run_dir / "03_prd.md").write_text(
            "验收标准\n\n附录 A：待确认事项清单\n\n[待确认:G01]\n",
            encoding="utf-8",
        )
        (run_dir / "04_ai_risks.md").write_text(
            "风险编号 验证方法\n",
            encoding="utf-8",
        )
        write_json(run_dir / "04_review_packet.json", {"status": "pending"})
        write_json(
            run_dir / "04_human_review.json",
            {
                "review_state": "pending",
                "reviewer": "",
                "reviewed_at": "",
                "change_requests": [],
            },
        )
        validate_run(run_dir)

        run = load_json(run_dir / "run.json")
        run["review_state"] = "approved"
        write_json(run_dir / "run.json", run)
        write_json(
            run_dir / "04_human_review.json",
            {
                "review_state": "approved",
                "reviewer": "self-test",
                "reviewed_at": "2026-09-27",
                "change_requests": [],
            },
        )
        (run_dir / "05_report.md").write_text(
            "验收标准\n\n附录 A：待确认事项清单\n\n"
            "[待确认:G01]\n\n"
            f"{DISCLAIMER}\n",
            encoding="utf-8",
        )
        (run_dir / "05_report.html").write_text(
            f"<html><body><p>{DISCLAIMER}</p></body></html>",
            encoding="utf-8",
        )
        validate_run(run_dir)

    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("run_directory", type=Path)

    subparsers.add_parser("self-test")
    args = parser.parse_args()

    try:
        if args.command == "self-test":
            self_test()
            return 0

        result = validate_run(args.run_directory.resolve())
    except HarnessFailure as exc:
        print(f"HARNESS_FAILED: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
