import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from utf8_io import configure_utf8_stdio, utf8_subprocess_env


configure_utf8_stdio()


def plot_scripts():
    examples_dir = ROOT / "scripts" / "examples"
    return sorted(examples_dir.glob("*.py"))


def run_examples(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    failures = []
    for script in plot_scripts():
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=output_dir,
            text=True,
            capture_output=True,
            encoding="utf-8",
            env=utf8_subprocess_env(),
        )
        if result.returncode != 0:
            failures.append(
                {
                    "script": script.name,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )
    return failures


def run_review(output_dir, review_dir):
    metadata_files = sorted(output_dir.glob("*.metadata.json"))
    if not metadata_files:
        raise RuntimeError("No .metadata.json files found. Generate figures before review.")
    review_dir.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        [
            "acadp-review",
            "--metadata-dir",
            str(output_dir),
            "--output-dir",
            str(review_dir),
        ],
        text=True,
        capture_output=True,
        encoding="utf-8",
        env=utf8_subprocess_env(),
        check=True,
    )


def run_auto_revise(output_dir, revise_dir, max_rounds):
    metadata_files = sorted(output_dir.glob("*.metadata.json"))
    if not metadata_files:
        raise RuntimeError("No .metadata.json files found. Generate figures before auto revise.")
    revise_dir.mkdir(parents=True, exist_ok=True)
    # Use acadp._reviser via a helper script since it has no CLI entry point.
    script = f"""\
import json, sys
from pathlib import Path
from dataclasses import dataclass, field
from acadp._reviser import revise_metadata

@dataclass
class ReviewResult:
    major_issues: list = field(default_factory=list)
    minor_issues: list = field(default_factory=list)
    suggested_caption: str = ""

meta_dir = Path(r"{output_dir}")
rev_dir = Path(r"{revise_dir}")
rev_dir.mkdir(parents=True, exist_ok=True)
for mf in sorted(meta_dir.glob("*.metadata.json")):
    meta = json.loads(mf.read_text(encoding="utf-8"))
    review = ReviewResult()  # no prior review, pass empty
    revised, changes, blocked = revise_metadata(meta, review)
    if changes:
        out = rev_dir / mf.name
        out.write_text(json.dumps(revised, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"REVISED={{mf.name}}: {{', '.join(changes)}}")
    else:
        print(f"SKIPPED={{mf.name}}: no changes needed")
"""
    return subprocess.run(
        [sys.executable, "-c", script],
        text=True,
        capture_output=True,
        encoding="utf-8",
        env=utf8_subprocess_env(),
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Generate all plot examples.")
    parser.add_argument(
        "--output-dir",
        default="example_outputs",
        help="Directory for generated PNG and metadata JSON files.",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Generate review_report.json and review_report.md after plotting.",
    )
    parser.add_argument(
        "--review-dir",
        default=None,
        help="Directory for review outputs; defaults to <output-dir>/review.",
    )
    parser.add_argument(
        "--auto-revise",
        action="store_true",
        help="Apply safe metadata repairs after review and run a final review.",
    )
    parser.add_argument(
        "--max-revision-rounds",
        type=int,
        default=2,
        help="Maximum safe auto-revision rounds.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    failures = run_examples(output_dir)
    png_count = len(list(output_dir.glob("*.png")))
    metadata_count = len(list(output_dir.glob("*.metadata.json")))
    print(f"PNG_COUNT={png_count}")
    print(f"METADATA_COUNT={metadata_count}")

    if failures:
        for failure in failures[:5]:
            print(f"FAILED={failure['script']}", file=sys.stderr)
            print(failure["stderr"], file=sys.stderr)
        raise SystemExit(1)

    if args.review or args.auto_revise:
        review_dir = Path(args.review_dir).resolve() if args.review_dir else output_dir / "review"
        result = run_review(output_dir, review_dir)
        if result.stdout.strip():
            print(result.stdout.strip())
        print(f"REVIEW_REPORT={review_dir / 'review_report.json'}")
        if args.auto_revise:
            revise_dir = review_dir / "auto_revise"
            result = run_auto_revise(output_dir, revise_dir, args.max_revision_rounds)
            if result.stdout.strip():
                print(result.stdout.strip())
            print(f"REVISION_PLAN={revise_dir / 'revision_plan.json'}")
            print(f"FINAL_REVIEW_REPORT={revise_dir / 'final_review' / 'review_report.json'}")


if __name__ == "__main__":
    main()
