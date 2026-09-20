# Week 3 — Object-Oriented Programming

Complete objects that store coordinates and paths, reject invalid combinations,
and keep each planning run's results separate. The path is supplied. You do not
implement a planner, collision checker, controller or simulator.

**Assignment guidance updated — 21 September 2026.** The implementation,
TODO numbers, tests and submission requirements have not changed. If you have
already started, keep your existing private repository and completed work.
Use the revised Reading with the same TODOs. Do not clone again, overwrite your
source files or send another invitation just to use the new instructions.

## Read first

1. [Week 3 Reading](docs/week_03_object_oriented_programming_reading_v10.pdf),
   including Section 7, **Assignment 3, Part A**.
2. This README for the execution order and commands.
3. [PROTECTED_FILES.md](PROTECTED_FILES.md) for the edit boundary.

The Reading is the complete specification. Its chapter practice uses a separate
folder outside this repository. Do not paste those practice files over the
Assignment starter. Week 4 continuation does not postpone the Week 3 submission.

## 1. Open your private Week 3 repository

If you do not have one yet, use
[the Week 3 template](https://github.com/SSUMechE/applied-programming-2026-week03-starter):

1. Select **Use this template → Create a new repository** under your own account.
2. Name it `applied-programming-w03-<student-id>` and select **Private**.
3. In **Settings → Collaborators → Add people**, invite `SSUMechE`.

Invitation sent/pending and accepted/active are different states. You can work
while acceptance is pending. A correct invitation sent on time and awaiting
only instructor acceptance is not a student omission.

Use **Anaconda Prompt** on Windows, not the Python `>>>` prompt. Replace the
example folder, GitHub ID and student ID below with your own values. If already
cloned, enter the existing folder instead of running `git clone` again.

```bat
cd /d "C:\your-course-folder"
git clone https://github.com/YOUR-GITHUB-ID/applied-programming-w03-YOUR-STUDENT-ID.git
cd applied-programming-w03-YOUR-STUDENT-ID
git status
git remote -v
```

Both `origin` addresses must point to your private Week 3 repository. For a first
HTTPS clone, Git Credential Manager may open browser sign-in. Use the repository
owner's account and complete your own two-factor authentication. If Git asks
for a password, a GitHub account password is not valid for Git HTTPS. Follow the
course's Credential Manager or personal access token instructions. Never put a
token in a URL, file, note, screenshot or LMS entry. For `Repository not found`,
check the URL and signed-in account before changing Python code.

## 2. Install and check the environment

Run all remaining commands from the **repository root**. Reuse your working
Week 1 environment. If activation says it does not exist, first run
`conda env create -f environment.yml`, then run the block below.

```bat
conda activate applied-programming-2026
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

The first installation command installs the listed dependencies. The second
links this Week 3 package to your source, so a new run uses saved TODO edits.
The verifier should finish with:

```text
[PASS] Week 3 object-programming environment is ready.
```

This checks the environment, not your unfinished implementation. Stop on an
installation error. The corrected YAML uses Conda for Python/pip and pip for
course packages, as in Week 1. Do not change a working environment.

<details>
<summary>Installation fails: corrected Conda repair and Python 3.12 alternative</summary>

For `DLL load failed`, `_socket`, `_multiarray_umath` or an application-control
error, do not disable Windows security, delete the course environment or replace
your TODO files. The corrected setup passed on the instructor's PC. It is not a
guarantee that every managed PC permits these binaries.

### Conda environment repair

In Anaconda Prompt, inside your existing Week 3 repository, create a separate
environment. Students with an older template do not need to edit the protected
YAML or re-import the template.

```bat
set PYTHONUTF8=1
conda create -n applied-programming-w03 --override-channels -c conda-forge python=3.12.13 pip=26.2.1
```

Confirm installation with `y`. If that name exists, skip creation and activate
it. `PYTHONUTF8` addresses a possible `cp949` decoding error, not a security block.

```bat
conda activate applied-programming-w03
python -c "import socket, ssl; print('IMPORTS_OK')"
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

Stop at the first error. Expect `IMPORTS_OK` and the verifier's PASS line.
Do not install NumPy separately with `conda install` in this environment.
In later windows, return to this repository and activate
`applied-programming-w03` before the normal commands.

### Python 3.12 alternative

If Anaconda is unavailable or the repaired environment still fails, open a new
Anaconda Prompt or Windows Command Prompt and enter the existing repository.

```bat
set PYTHONUTF8=1
cd /d "C:\your-course-folder\applied-programming-w03-YOUR-STUDENT-ID"
py -3.12 --version
```

Continue only with Python 3.12.x. If missing, install an official
[Python 3.12 Windows distribution](https://www.python.org/downloads/windows/)
with the Python launcher, or ask the managed-PC administrator. Do not download
individual DLLs from third-party sites.

Create `.venv` only if it does not already exist:

```bat
py -3.12 -m venv .venv
```

Activate and check it:

```bat
.venv\Scripts\activate
python --version
python -c "import sys; print(sys.executable)"
python -c "import socket, ssl; print('IMPORTS_OK')"
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python -c "import numpy; print(numpy.__version__)"
python scripts/verify_environment.py
```

Expect Python 3.12.x, this repository's `.venv\Scripts\python.exe`,
`IMPORTS_OK`, NumPy `2.5.1` and the verifier's PASS line. Stop at the first
error. Do not delete or replace an existing `.venv` that fails these checks.
Report the command and complete error without credentials. Remaining Windows
policy blocks need administrator review, not disabled security.

In later windows, return to this repository and run `.venv\Scripts\activate`.
The existing `.gitignore` excludes `.venv`. Do not upload environment files.

After either recovery, use `python scripts/run_baseline.py` only for an untouched
starter. If TODOs are already edited, use `python -m pytest -q` instead. Do not
undo completed work to recreate the original baseline.

</details>

## 3. Record the baseline, then implement TODO 1–8

Before editing an untouched starter:

```bat
python scripts/run_baseline.py
```

Expect `68 failed, 8 passed`, followed by the wrapper's baseline PASS line.
Record the summary and first FAILED node ID in section 0 of the existing
`artifacts/engineering_note.md`, then save. If you have already begun, keep your
work and original record. Do not restore the starter just to repeat this step.

Open the two source files in your editor. Search for the TODO number, replace
the corresponding `raise NotImplementedError(...)` with your implementation,
and save. Keep class names, fields, signatures, decorators and TODO numbers.
Do not remove every stub at once. The Reading Section 7.4 gives the exact
behavior and expected values for each TODO before its grouped check.

| TODO | File and exact bodies to complete |
|---|---|
| 1 | `domain.py`: `_normalized_values`, `Configuration.__post_init__` |
| 2 | `domain.py`: `Configuration.dimension`, `Configuration.as_array` |
| 3 | `domain.py`: `ConfigurationBounds.__post_init__`, `.dimension` |
| 4 | `domain.py`: `ConfigurationBounds.contains` |
| 5 | `domain.py`: `Path.__post_init__`, `.dimension`, `.start`, `.goal`, `.as_array`, `.length` |
| 6 | `domain.py`: `PlanningProblem.__post_init__` |
| 7 | `domain.py`: `PlanResult.__post_init__`, `.succeeded` |
| 8 | `history.py`: `PlanningRun.__post_init__`, `.record_result`, `.results`, `.latest` |

Both files are under `src/ap_week03_planning/`. The numerical function in
`geometry.py` and the `PlanningRun._results` field are already provided.
Do not reimplement them. Invalid public construction/update raises
`PlanningModelError`, not a silently repaired object.

After each completed group, run its check:

```bat
python -m pytest -q tests/test_published_contract.py -k test_configuration_ -x
python -m pytest -q tests/test_published_contract.py -k test_bounds_ -x
python -m pytest -q tests/test_published_contract.py -k "test_path_ or test_problem_" -x
python -m pytest -q tests/test_published_contract.py -k "result or run" -x
```

| Run after | Expected result |
|---|---|
| TODO 1–2: configuration check | `21 passed, 55 deselected` |
| TODO 3–4: bounds check | `11 passed, 65 deselected` |
| TODO 5–6: path/problem check | `17 passed, 59 deselected` |
| TODO 7–8: result/run check | `16 passed, 60 deselected` |

`-k` selects test names, `-x` stops at the first failure and `-q` reduces detail.
`deselected` tests did not run. Some path tests construct a `PlanningProblem`,
so run the full path/problem group after TODO 6. These separate counts are not
the full-suite total. When all TODOs are complete, run:

```bat
python -m pytest -q tests/test_published_contract.py
```

Expected: `76 passed`.

## 4. Add your tests and generate the results

Replace the placeholder in `tests/test_student_evidence.py` with at least eight
distinct top-level `test_...` functions using independent inputs. Follow the
eight categories in Reading Section 7.5. Run:

```bat
python -m pytest -q
```

Expect at least `84 passed`. Skipped tests do not count. Counts alone do not
establish that your cases and assertions cover the required categories.

Then run the supplied demo and output generator without editing them:

```bat
python -m ap_week03_planning.demo
python scripts/generate_outputs.py
```

They use the fixed four-waypoint example from the Reading, not keyboard input
or a JSON input file. The demo prints dimension `2`, waypoint count `4`, length
`4.356407`, result count `1` and `succeeded: True` for `demo-tool-path`.
The generator prints two `[PASS] wrote ...` lines and saves:

- `artifacts/planning_objects_report.json`: open in an editor and check the
  values against the demo. The saved length is approximately `4.35640661761539`.
- `artifacts/planning_objects_preview.svg`: open in a browser and check the four
  labels `start`, `q1`, `q2`, `goal` in order.

The SVG displays the stored path, not a planner, collision check or physical
execution. Regeneration replaces these two files using current source.
Do not hand-edit them or type the expected output yourself. If a TODO raises
`NotImplementedError`, complete that body instead of changing the demo.

## 5. Finish the note and build the package

Open `artifacts/engineering_note.md` in your editor. Write answers in all seven
sections, 0–6, using your actual results. Save, then verify the saved contents:

```bat
type artifacts\engineering_note.md
```

Fill the wheel filename in section 5 after the next build, then leave no
`REPLACE_ME` or empty answer. Do not overwrite completed answers with a fresh
template. The Reading explains each section's required content.

A wheel is the installable `.whl` package built from your completed source.
The editable installation is for development. The wheel checks the packaged
form without relying on that source link. You do not write a packaging script.
Inspect `dist` before rebuilding and remove only an obsolete Week 3 wheel if
necessary so the final folder contains exactly one wheel.

```bat
python -m build --wheel --no-isolation
dir /b dist\*.whl
```

With unchanged metadata, the filename is
`ap_week03_planning-0.1.0-py3-none-any.whl`. Record it in note section 5,
save the note, then run:

```bat
python scripts/check_submission.py
```

`--no-isolation` uses the installed build tools. The checker compares generated outputs and imports this wheel in
a separate isolated Python interpreter using existing dependencies. It does
not create a new virtual environment or install the wheel with pip.

The checker does not establish explanation quality, GitHub access or LMS
submission. Your only manually edited files are the two TODO files, the student
test file and the note. Commit the generated JSON, SVG and wheel too.

## 6. Review, commit and push

```bat
git status --short
git diff
git add src/ap_week03_planning/domain.py
git add src/ap_week03_planning/history.py
git add tests/test_student_evidence.py artifacts dist
git diff --staged
git commit -m "Complete Week 3 planning domain objects"
git push origin main
git rev-parse HEAD
git ls-remote origin refs/heads/main
git status --short
```

Review the unstaged and staged changes before committing. If a pager opens,
press `q`. `add` selects changes, `commit` records them locally and `push`
uploads them. Compare the two full commit IDs and confirm the working tree is
clean. On GitHub, check the note and generated files at that revision.
Record the full ID for LMS, not inside a note that would require another commit.

## 7. Submit through LMS

Submit within **one week of the Week 3 lab**. Follow the exact LMS date/time.
Use the same three fields as Weeks 1 and 2:

1. Your private `applied-programming-w03-<student-id>` repository URL.
2. Its full 40-character commit ID, matching the pushed revision.
3. Confirmation of private visibility, actual `SSUMechE` access state and the
   revision to be graded.

Fictional example — replace every example value with your own:

```text
Repository URL:
https://github.com/student-example/applied-programming-w03-20261234

Full commit ID:
0123456789abcdef0123456789abcdef01234567

Confirmation:
The repository is private. SSUMechE has active collaborator access.
The commit above is the revision to be graded.
```

- If a correct on-time invitation awaits only instructor acceptance, report
  that it is pending instead. This is not a student omission. Follow the LMS
  contact guidance if it remains pending after the announced checking time.
- Follow the designated name, file structure and LMS format. Missing mandatory
  submission requirements by the deadline results in zero for the assignment,
  with the pending-invitation exception above.
- GitHub upload without LMS submission is not a submission. No extra LMS file
  attachment is required. Keep code, tests, note, JSON/SVG and wheel in GitHub.
- Do not submit the public template URL, a local path, branch name, `latest`,
  short hash, unpushed commit or any credential. Later pushes do not replace
  the submitted revision. Retain private visibility and access through grading.

The submission-format rule does not make every failed numerical test an
automatic zero for the entire assignment.
