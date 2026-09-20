"""Check Week 3 code and tests. GitHub and LMS still need a separate check."""

from __future__ import annotations

import ast
import hashlib
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_SHA256_LF = "9ad3b6bd19512f6b7e8760cc7e64b1e88e58236135edea4c232f1ccd3990593f"
PUBLIC_OBJECTS = {
    "Configuration", "ConfigurationBounds", "Path", "PlanningProblem",
    "PlanResult", "PlanningRun",
}
PUBLIC_METHODS = {"as_array", "contains", "length", "record_result"}


def functions(tree: ast.Module) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    return {
        node.name: node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def body_key(function: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Ignore the function name/docstring when finding verbatim copied bodies."""
    body = list(function.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        if isinstance(body[0].value.value, str):
            body.pop(0)
    return ast.dump(ast.Module(body=body, type_ignores=[]), include_attributes=False)


def reached_nodes(function: ast.AST, definitions: dict[str, ast.AST]) -> list[ast.AST]:
    """Include local helpers, so helper-based independent cases are accepted."""
    pending = [function]
    visited: set[int] = set()
    nodes: list[ast.AST] = []
    while pending:
        current = pending.pop()
        if id(current) in visited:
            continue
        visited.add(id(current))
        nodes.extend(ast.walk(current))
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for argument in current.args.args:
                fixture = definitions.get(argument.arg)
                if fixture is not None:
                    pending.append(fixture)
        for node in ast.walk(current):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                helper = definitions.get(node.func.id)
                if helper is not None:
                    pending.append(helper)
    return nodes


def check_student_structure() -> tuple[set[str], list[str]]:
    student = ast.parse((ROOT / "tests/test_student_evidence.py").read_text(encoding="utf-8"))
    published = ast.parse((ROOT / "tests/test_published_contract.py").read_text(encoding="utf-8"))
    definitions = functions(student)
    tests = {name: node for name, node in definitions.items() if name.startswith("test_")}
    failures: list[str] = []
    if "test_student_placeholder" in tests:
        failures.append("replace test_student_placeholder with your own tests")
        del tests["test_student_placeholder"]
    if len(tests) < 4:
        failures.append(f"need at least 4 distinct top-level student test functions, found {len(tests)}")

    # Accept imports with aliases, not just one prescribed import spelling.
    constructors = set(PUBLIC_OBJECTS)
    assertion_names: set[str] = set()
    for node in ast.walk(student):
        if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("ap_week03_planning"):
            constructors.update(alias.asname or alias.name for alias in node.names if alias.name in PUBLIC_OBJECTS)
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if ((node.module or "").startswith("numpy.testing") and alias.name.startswith("assert_")) or (node.module == "pytest" and alias.name == "raises"):
                    assertion_names.add(alias.asname or alias.name)
    copied_bodies = {body_key(node) for node in functions(published).values()}
    seen_bodies: set[str] = set()
    for name, function in tests.items():
        key = body_key(function)
        if key in copied_bodies:
            failures.append(f"{name}: body copies a published test/helper")
        if key in seen_bodies:
            failures.append(f"{name}: duplicates another student test body")
        seen_bodies.add(key)
        nodes = reached_nodes(function, definitions)
        calls = [node.func for node in nodes if isinstance(node, ast.Call)]
        api_call = any(
            (isinstance(call, ast.Name) and call.id in constructors)
            or (isinstance(call, ast.Attribute) and call.attr in PUBLIC_OBJECTS | PUBLIC_METHODS)
            for call in calls
        )
        assertion = any(
            isinstance(node, ast.Assert)
            and any(isinstance(part, (ast.Name, ast.Attribute, ast.Call, ast.Subscript)) for part in ast.walk(node.test))
            for node in nodes
        ) or any(
            (isinstance(call, ast.Attribute) and (call.attr == "raises" or call.attr.startswith("assert_")))
            or (isinstance(call, ast.Name) and call.id in assertion_names)
            for call in calls
        )
        if not api_call:
            failures.append(f"{name}: call a Week 3 public object or method")
        if not assertion:
            failures.append(f"{name}: assert an observed result or expected exception, not only a constant")
    return set(tests), failures


def check_tests(test_names: set[str]) -> list[str]:
    failures: list[str] = []
    published = ROOT / "tests/test_published_contract.py"
    digest = hashlib.sha256(published.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    if digest != PUBLISHED_SHA256_LF:
        return ["protected tests/test_published_contract.py differs from the supplied file"]
    environment = os.environ.copy()
    environment["PYTEST_ADDOPTS"] = ""
    environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    with tempfile.TemporaryDirectory(prefix="ap_week03_pytest_") as temporary:
        report = Path(temporary) / "results.xml"
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
             f"--junitxml={report}", "tests/test_published_contract.py", "tests/test_student_evidence.py"],
            cwd=ROOT, check=False, capture_output=True, text=True, timeout=180,
            env=environment,
        )
        print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="")
        if completed.returncode:
            failures.append("the published and student test suite does not pass")
        if not report.is_file():
            return failures + ["pytest did not produce execution results"]
        cases = list(ET.parse(report).getroot().iter("testcase"))
    passed = [case for case in cases if not any(case.find(kind) is not None for kind in ("failure", "error", "skipped"))]
    published_passed = [case for case in passed if case.get("classname", "").endswith("test_published_contract")]
    student_passed_cases = [case for case in passed if case.get("classname", "").endswith("test_student_evidence")]
    student_passed = {case.get("name", "").split("[", 1)[0] for case in student_passed_cases}.intersection(test_names)
    visible_count = len(published_passed) + len(student_passed_cases)
    if len(published_passed) != 76:
        failures.append(f"need all 76 published cases passed, found {len(published_passed)}")
    if visible_count < 80:
        failures.append(f"need at least 80 passing published plus student cases, found {visible_count}")
    if len(student_passed) < 4:
        failures.append(f"need at least 4 distinct student test functions with passing execution, found {len(student_passed)}")
    print(f"[INFO] passed cases={visible_count}, passing distinct student functions={len(student_passed)}")
    return failures


def main() -> int:
    failures: list[str] = []
    try:
        names, structure_failures = check_student_structure()
        failures.extend(structure_failures)
    except (OSError, SyntaxError, UnicodeError) as exc:
        names = set()
        failures.append(f"cannot read student tests: {exc}")
    try:
        failures.extend(check_tests(names))
    except Exception as exc:
        failures.append(f"test check could not finish: {type(exc).__name__}: {exc}")
    print("[REVIEW] The instructor checks coverage of normal use, invalid input, ownership and separate histories, meaningful assertions, independence and protected-source changes.")
    print("[INFO] This local checker does not verify GitHub access, push or LMS submission.")
    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1
    print("[PASS] Week 3 code and test checkpoint: 76 published cases and at least 4 student test functions passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
