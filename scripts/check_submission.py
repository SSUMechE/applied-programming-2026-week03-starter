"""Check the existing visible Week 3 checkpoint without claiming manual review."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_SHA256_LF = "9ad3b6bd19512f6b7e8760cc7e64b1e88e58236135edea4c232f1ccd3990593f"
NOTE_HEADINGS = (
    "0. Intentional baseline", "1. Object responsibilities", "2. Invariant evidence",
    "3. Inheritance and composition", "4. Aliasing and ownership",
    "5. Generated evidence", "6. Week 4 bridge",
)
NOTE_PROMPTS = {
    "1. Object responsibilities": (
        "In two or three sentences, explain which objects are frozen value objects and "
        "why \x60PlanningRun\x60 alone owns mutable result history."
    ),
    "2. Invariant evidence": (
        "Name one constructor invariant and one state-update invariant. For each one, "
        "identify the independent test that demonstrates it."
    ),
    "3. Inheritance and composition": (
        "Explain the inheritance relationship used by \x60PlanningModelError\x60 and one "
        "composition relationship among the planning-domain objects. Do not state that "
        "one technique is always better than the other."
    ),
    "4. Aliasing and ownership": (
        "Explain how your \x60Configuration\x60, \x60Path\x60, and \x60PlanningRun.results\x60 code "
        "prevents a caller-owned mutable container from changing internal state."
    ),
    "6. Week 4 bridge": (
        "State what Week 4 must add at the JSON boundary without weakening these object invariants."
    ),
}
NOTE_FIELDS = (
    "Student name", "Student ID", "GitHub repository URL", "Baseline summary",
    "First FAILED pytest node ID", "Published test result", "Published + student test result",
    "\x60planning_objects_report.json\x60 interpretation", "\x60planning_objects_preview.svg\x60 interpretation",
    "Wheel filename",
)


def student_test_names() -> set[str]:
    tree = ast.parse((ROOT / "tests/test_student_evidence.py").read_text(encoding="utf-8"))
    return {
        node.name for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_") and node.name != "test_student_placeholder"
    }


def student_test_count() -> int:
    return len(student_test_names())


def check_note(test_names: set[str]) -> list[str]:
    path = ROOT / "artifacts/engineering_note.md"
    if not path.is_file():
        return ["missing artifact: artifacts/engineering_note.md"]
    text = path.read_text(encoding="utf-8")
    failures = []
    if "REPLACE_ME" in text:
        failures.append("engineering_note.md still contains REPLACE_ME placeholders")
    sections = {}
    for part in re.split(r"(?m)^## ", text)[1:]:
        heading, _, body = part.partition("\n")
        sections[heading.strip()] = body
    for heading in NOTE_HEADINGS:
        if heading not in sections:
            failures.append(f"engineering note is missing its existing section: {heading}")
            continue
        body = " ".join(sections[heading].split()).replace("REPLACE_ME", "").strip()
        prompt = NOTE_PROMPTS.get(heading, "")
        if prompt:
            body = body.replace(prompt, "").strip()
        if not body:
            failures.append(f"engineering note has no written answer in: {heading}")
    for label in NOTE_FIELDS:
        matches = re.findall(r"(?m)^[ \t]*(?:-[ \t]*)?" + re.escape(label) + r":[ \t]*([^\r\n]*)", text)
        if not matches or not matches[0].strip() or matches[0].strip() == "REPLACE_ME":
            failures.append(f"engineering note has no answer for: {label}")
    invariant_text = unicodedata.normalize("NFKC", sections.get("2. Invariant evidence", ""))
    references = {name for name in test_names if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", invariant_text)}
    if not references:
        failures.append("name your actual independent invariant test functions in note section 2")
    return failures


def check_generated_outputs() -> list[str]:
    failures = []
    saved_report = ROOT / "artifacts/planning_objects_report.json"
    saved_preview = ROOT / "artifacts/planning_objects_preview.svg"
    for path in (saved_report, saved_preview):
        if not path.is_file():
            failures.append(f"missing generated artifact: {path.relative_to(ROOT)}")
    if failures:
        return failures
    try:
        report = json.loads(saved_report.read_text(encoding="utf-8"))
        if not isinstance(report, dict):
            return ["generated report must contain a JSON object"]
        import ap_week03_planning
        expected_init = ROOT / "src/ap_week03_planning/__init__.py"
        if Path(ap_week03_planning.__file__).resolve() != expected_init.resolve():
            return ["regeneration must import this repository's editable source"]
        spec = importlib.util.spec_from_file_location("_week03_output_check", ROOT / "scripts/generate_outputs.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory(prefix="ap_week03_outputs_") as temporary:
            module.ROOT = Path(temporary)
            module.ARTIFACTS = module.ROOT / "artifacts"
            module.main()
            expected_report = (module.ARTIFACTS / saved_report.name).read_text(encoding="utf-8")
            expected_preview = (module.ARTIFACTS / saved_preview.name).read_text(encoding="utf-8")
        if saved_report.read_text(encoding="utf-8") != expected_report:
            failures.append("planning_objects_report.json differs from fresh protected generation")
        if saved_preview.read_text(encoding="utf-8") != expected_preview:
            failures.append("planning_objects_preview.svg differs from fresh protected generation")
    except Exception as exc:
        failures.append(f"cannot verify generated outputs: {type(exc).__name__}: {exc}")
    return failures


WHEEL_SMOKE_CODE = r"""
import sys
from pathlib import Path
wheel = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(wheel))
from ap_week03_planning import Configuration, ConfigurationBounds, PlanningProblem
lower = Configuration((0.0, 0.0))
upper = Configuration((2.0, 2.0))
problem = PlanningProblem(
    "wheel-check", Configuration((0.25, 0.5)), Configuration((1.5, 1.75)),
    ConfigurationBounds(lower, upper),
)
assert problem.problem_id == "wheel-check"
prefix = str(wheel).replace("\\", "/") + "/"
for name, module in tuple(sys.modules.items()):
    if name == "ap_week03_planning" or name.startswith("ap_week03_planning."):
        origin = str(getattr(module, "__file__", "")).replace("\\", "/")
        if not origin.startswith(prefix):
            raise RuntimeError(f"{name} imported from outside this exact wheel: {origin}")
print("[PASS] built wheel imports its own package and constructs a PlanningProblem.")
"""


def check_wheel() -> list[str]:
    wheels = list((ROOT / "dist").glob("ap_week03_planning-*.whl"))
    if len(wheels) != 1:
        return [f"expected exactly one Week 3 wheel in dist, found {len(wheels)}"]
    wheel = wheels[0].resolve()
    try:
        with zipfile.ZipFile(wheel) as archive:
            if "ap_week03_planning/__init__.py" not in archive.namelist():
                return ["built wheel does not contain ap_week03_planning/__init__.py"]
            if archive.testzip() is not None:
                return ["built wheel archive has a CRC error"]
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"built wheel is not a readable wheel archive: {exc}"]
    with tempfile.TemporaryDirectory(prefix="ap_week03_wheel_") as temporary:
        completed = subprocess.run(
            [sys.executable, "-I", "-c", WHEEL_SMOKE_CODE, str(wheel)],
            cwd=temporary, check=False, capture_output=True, text=True, timeout=60,
        )
    print(completed.stdout, end="")
    if completed.returncode:
        return ["built wheel failed its own-package import smoke test: " + completed.stderr.strip()]
    return []


def check_tests(test_names: set[str]) -> list[str]:
    failures = []
    published = ROOT / "tests/test_published_contract.py"
    digest = hashlib.sha256(published.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    if digest != PUBLISHED_SHA256_LF:
        failures.append("protected tests/test_published_contract.py differs from the supplied file")
    with tempfile.TemporaryDirectory(prefix="ap_week03_pytest_") as temporary:
        report = Path(temporary) / "results.xml"
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={report}"],
            cwd=ROOT, check=False, capture_output=True, text=True, timeout=180,
        )
        print(completed.stdout, end="")
        if completed.returncode:
            failures.append("the published and student test suite does not pass")
        if not report.is_file():
            return failures + ["pytest did not produce execution evidence"]
        cases = list(ET.parse(report).getroot().iter("testcase"))
    passed = [case for case in cases if not any(case.find(kind) is not None for kind in ("failure", "error", "skipped"))]
    published_passed = [case for case in passed if case.get("classname", "").endswith("test_published_contract")]
    student_passed = {
        case.get("name", "").split("[", 1)[0] for case in passed
        if case.get("classname", "").endswith("test_student_evidence")
    }.intersection(test_names)
    if len(published_passed) != 76:
        failures.append(f"need all 76 published cases passed, found {len(published_passed)}")
    if len(passed) < 84:
        failures.append(f"need at least 84 passing published plus student cases, found {len(passed)}")
    if len(student_passed) < 8:
        failures.append(f"need at least 8 distinct student test functions with passing execution, found {len(student_passed)}")
    print(f"[INFO] passed cases={len(passed)}, passing distinct student functions={len(student_passed)}")
    return failures


def main() -> int:
    failures = []
    try:
        names = student_test_names()
    except (OSError, SyntaxError, UnicodeError) as exc:
        names = set()
        failures.append(f"cannot read student test functions: {exc}")
    if len(names) < 8:
        failures.append(f"need at least 8 distinct top-level student test functions, found {len(names)}")
    for check in (lambda: check_note(names), check_generated_outputs, check_wheel, lambda: check_tests(names)):
        try:
            failures.extend(check())
        except Exception as exc:
            failures.append(f"checkpoint check could not finish: {type(exc).__name__}: {exc}")
    print("[REVIEW] Test-category coverage, independent claims, explanatory correctness and all protected-file changes require instructor review.")
    print("[INFO] This local checker does not verify GitHub access, push or LMS submission.")
    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1
    print(f"[PASS] local checkpoint: {len(names)} student functions, filled note fields, regenerated outputs, own-wheel import and passing visible cases verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
