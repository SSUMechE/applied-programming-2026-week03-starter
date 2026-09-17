# Week 3 — Object-Oriented Programming

## Windows installation correction — 17 September 2026

If installation stops with `DLL load failed`, `_socket`,
`_multiarray_umath`, or "An Application Control policy has blocked this file",
stop the failed installation and follow [Conda environment repair](#conda-environment-repair).
Do not disable Windows security, delete your course environment, recreate your
GitHub repository, or replace your completed TODO files. A working environment
does not need to be changed. The assignment and submission requirements are unchanged.

The corrected `environment.yml` now follows Week 1: Conda installs Python and
pip, then pip installs the pinned course packages. The previous Week 3 YAML
instead selected conda-forge builds of NumPy and the test tools. Matching version
numbers do not imply matching binary files. The old fresh Conda setup failed
loading NumPy on the instructor's PC. The corrected fresh setup passed the
environment check, starter baseline and completed assignment checks on that PC.

This repository turns Week 2 numerical path data into tested planning-domain
objects. It is **Assignment 3, Part A**, submitted for Week 3 through the same
GitHub and LMS workflow used in Weeks 1 and 2. Week 4 continues with collections
and the JSON boundary. That continuation does not postpone this week's
submission. Week 3 does not implement a planner, collision checker, robot
controller, or simulator.

## Required reading order

Before changing code, read these documents in order.

1. `docs/week_03_object_oriented_programming_reading_v9_1.pdf`, including its
   final Assignment 3, Part A section.
2. This `README.md`.
3. `PROTECTED_FILES.md`.

The integrated Reading is the canonical specification. This README mirrors
the operational checklist. If the documents appear inconsistent, ask before
changing a protected file. Chapter practice is separate from the unfinished
Assignment TODOs. Follow the Reading's named practice file and execution
instructions in a separate folder outside this repository. Do not copy
explanatory snippets into `domain.py`.

## Create the private Week 3 repository

After the instructor announces its release, open the Week 3 public template.

<https://github.com/SSUMechE/applied-programming-2026-week03-starter>

1. Sign in with your own existing GitHub account.
2. Select **Use this template**, then **Create a new repository**.
3. Set your own account as Owner and name the repository
   `applied-programming-w03-<student-id>`.
4. Select **Private** visibility and create the repository.
5. Under **Settings → Collaborators → Add people**, invite the exact account
   `SSUMechE`.
6. Check whether that invitation is pending or the collaborator access is
   active. Report the actual state.

You may clone and work locally while instructor acceptance is pending. Your
own clone authentication is separate from the instructor's access. A correct
invitation sent on time and awaiting only instructor acceptance is not a
student omission. Follow the LMS contact procedure if it is still pending
after the announced checking time.

Open **Anaconda Prompt** on Windows. Use its Command Prompt syntax for every
command below, not a Python `>>>` prompt. Change to the parent folder where
you keep course repositories. Replace the example path, GitHub username and
student ID with your own values.

```bat
cd /d "C:\your-course-folder"
git clone https://github.com/YOUR-GITHUB-ID/applied-programming-w03-YOUR-STUDENT-ID.git
cd applied-programming-w03-YOUR-STUDENT-ID
git status
git remote -v
```

`git clone` downloads the repository into a new local folder. `git status`
reports its branch and working-file state, and `git remote -v` shows the saved
remote names and addresses. Both `origin` URLs must identify your private
Week 3 repository. Reopen your
existing local copy if you already cloned it. Do not recreate the repository
or overwrite completed work.

On the first authenticated HTTPS clone, Git Credential Manager may open a
browser sign-in window. Sign in as the owner of this private repository and
complete your own two-factor authentication if prompted. If Git instead asks
for a username and password, GitHub account passwords do not authenticate Git
HTTPS operations. Use the course's Git Credential Manager or personal access
token authentication guidance and check that it permits this repository.
Never place a token inside a clone URL, source file, engineering note, LMS
entry or screenshot. Do not send passwords, tokens or authentication codes to
the instructor. A `Repository not found` message can indicate a URL or account
access problem. Check those first rather than changing Python code.

## Install and verify

Run these commands from the cloned repository root in Anaconda Prompt. Reuse
the Week 1 course environment when it already exists.

```bat
conda activate applied-programming-2026
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

Activation selects the environment's Python. In `python -m pip`, `-m` runs
the named module using that Python. The `-r requirements.txt` option installs
the external package versions listed in this file. It does not install this
repository's own Week 3 package.

In `-e .`, the dot means the current repository directory and `-e` requests an
editable installation. Imports then use this source, so running Python again
sees your saved TODO changes without rebuilding a wheel for every edit.
`--no-build-isolation` uses the build tools already installed in the active
environment instead of creating a separate build environment. This is why the
requirements command comes first. It does not implement the TODOs. Resolve an
installation error before continuing to the verifier or baseline.

Only if activation reports that the environment does not exist, create it
from this repository's `environment.yml`, then run the same installation.

```bat
conda env create -f environment.yml
conda activate applied-programming-2026
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

Do not remove or replace an existing course environment merely to repeat this
setup. If `conda` is not recognized, first open Anaconda Prompt rather than an
ordinary shell. For the supported Python 3.12 alternative when Anaconda is
unavailable, use the repository-local environment commands below in Windows
Command Prompt.

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

The verifier checks the Python family, required distributions and this
repository's editable package import. It does not execute unfinished TODO
bodies or establish Assignment completion. A successful check ends with:

```text
[PASS] Week 3 object-programming environment is ready.
```

## Conda environment repair

If your existing Week 1/2 environment passes `python scripts/verify_environment.py`,
keep using it. You do not need a new Python installation or a new environment.

For a failing environment, use the following steps in **Anaconda Prompt** inside
your existing Week 3 repository. They leave the old environment and all TODO
files intact. Students with an older private template do not need to edit the
protected `environment.yml`, import the template again or send another invitation.

1. Enable UTF-8 for this command window and create a separate course environment.

   ```bat
   set PYTHONUTF8=1
   conda create -n applied-programming-w03 --override-channels -c conda-forge python=3.12.13 pip=26.2.1
   ```

   Confirm Conda's installation prompt with `y`. If that name already exists,
   do not overwrite it. Activate it and attempt the checks below instead.
   UTF-8 mode fixes a possible `cp949` decoding error, not a security-policy block.

2. Activate it, check Python's networking libraries, then install the course packages.

   ```bat
   conda activate applied-programming-w03
   python -c "import socket, ssl; print('IMPORTS_OK')"
   python -m pip install -r requirements.txt
   python -m pip install -e . --no-build-isolation
   python scripts/verify_environment.py
   ```

   Stop at the first error. The import check must print `IMPORTS_OK` and the
   verifier must finish with `[PASS] Week 3 object-programming environment is ready.`
   Do not install NumPy separately with `conda install` in this repaired environment.
   The pinned requirements install it using the same pip route as Week 1.

3. For an untouched starter, run `python scripts/run_baseline.py` and expect
   `68 failed, 8 passed`. If you already changed TODOs, use
   `python -m pytest -q` instead. Do not undo your work to reproduce the baseline.

4. In later Anaconda Prompt windows, return to this repository and use
   `conda activate applied-programming-w03` before the normal Week 3 commands.
   Tests, outputs, wheel building and LMS submission are otherwise unchanged.

If Windows still explicitly blocks Python or a DLL, do not disable security.
Report the complete error and use the verified alternative below if your PC
permits it. A managed-PC administrator must review remaining policy blocks.

## Windows recovery

Use this section only when the normal installation fails. The same repository
and source files are used. Anaconda Prompt is the command window. For this
recovery, Python runs from a separate `.venv` instead of the failing Conda
environment. `PYTHONUTF8` addresses a separate `cp949` decoding error. It does
not fix an application-control block.

1. Close the failed command window. Open a new **Anaconda Prompt** and change
   to your existing Week 3 repository folder. Do not clone again.

   ```bat
   set PYTHONUTF8=1
   cd /d "C:\your-course-folder\applied-programming-w03-YOUR-STUDENT-ID"
   py -3.12 --version
   ```

   Replace the path with your actual folder. Continue only if the last command
   reports Python 3.12.x. If `py` is missing or cannot find Python 3.12, install
   an official Python 3.12 Windows distribution from
   <https://www.python.org/downloads/windows/> with the Python launcher, then
   reopen Anaconda Prompt and repeat this check. Do not install an unrelated
   Python version or download DLLs from third-party sites. On a managed PC,
   ask its administrator to install an approved Python 3.12 distribution.

2. Create `.venv` only if this repository does not already have one.

   ```bat
   py -3.12 -m venv .venv
   ```

   If `.venv` already exists, skip creation. Activate it and check its Python
   version below. If that version is not 3.12.x or activation fails, stop and
   send the error to the instructor instead of deleting or replacing files.

3. Activate the environment and check its interpreter and standard libraries.

   ```bat
   .venv\Scripts\activate
   python --version
   python -c "import sys; print(sys.executable)"
   python -c "import socket, ssl; print('IMPORTS_OK')"
   ```

   The executable path must end in this repository's
   `.venv\Scripts\python.exe`. The import check must print `IMPORTS_OK`.
   If Windows also blocks this interpreter or a DLL, stop. Send the command
   and complete error text to the instructor or the managed-PC administrator.
   Do not turn off Smart App Control, antivirus, or application-control policy.

4. Install the unchanged requirements and Week 3 package.

   ```bat
   python -m pip install -r requirements.txt
   python -m pip install -e . --no-build-isolation
   python -c "import numpy; print(numpy.__version__)"
   python scripts/verify_environment.py
   ```

   NumPy must report `2.5.1`. The verifier must finish with
   `[PASS] Week 3 object-programming environment is ready.`
   Stop at the first error rather than running the later commands.

5. For an untouched starter, run `python scripts/run_baseline.py`. Its expected
   summary is `68 failed, 8 passed`. If you have already changed TODOs, run
   `python -m pytest -q` instead. Do not undo your work to reproduce the baseline.

6. When you reopen Anaconda Prompt, return to this repository and run
   `.venv\Scripts\activate` before the normal Week 3 commands. Use this same
   environment for editing, testing, output generation and wheel building.
   The existing `.gitignore` excludes `.venv`. Do not upload environment files.

This recovery does not repair Windows policy or guarantee that every managed PC
will allow the packages. Report any remaining block for administrator review.
Keep passwords, tokens and authentication codes out of diagnostic screenshots.
Students who already created a private repository can follow these commands
directly. No template re-import, source replacement or new invitation is needed.

## Record the starter baseline and begin the note

```bat
python scripts/run_baseline.py
notepad artifacts\engineering_note.md
```

The untouched starter must report `68 failed, 8 passed`, followed by a PASS
line that verifies this intentional baseline. In the existing engineering
note, record the summary and first FAILED node ID before editing code. Save
the note with **Ctrl+S**. Do not copy a new template over your saved answers.

## Complete TODO 1–8 in dependency order

Edit only the TODO implementations in `src/ap_week03_planning/domain.py` and
`src/ap_week03_planning/history.py`. Keep the public contract and TODO numbers.
Complete TODO 1–4 first, then run these focused checks. The test-name prefixes
avoid selecting the path, problem and run tests for later TODOs.
`python -m pytest` runs pytest through the selected Python. `-q` reduces the
output detail, but does not change which tests run or turn failures into
passes. `-k` selects matching test names and `-x` stops after the first failure.

```bat
python -m pytest -q tests/test_published_contract.py -k test_configuration_ -x
python -m pytest -q tests/test_published_contract.py -k test_bounds_ -x
```

The first command reports `21 passed, 55 deselected`. The second reports
`11 passed, 65 deselected`. They are separate runs, not a full-suite total.
Complete TODO 5–6 next.

```bat
python -m pytest -q tests/test_published_contract.py -k test_path_ -x
python -m pytest -q tests/test_published_contract.py -k test_problem_ -x
```

The path command reports `8 passed, 68 deselected`. The problem command reports
`9 passed, 67 deselected`. Complete TODO 7–8, then run the result/run group.

```bat
python -m pytest -q tests/test_published_contract.py -k "result or run" -x
```

This command reports `16 passed, 60 deselected`. Now remove the name filter
and run the entire published file.

```bat
python -m pytest -q tests/test_published_contract.py
```

The completed published suite must report `76 passed`. A deselected test has not run.
A focused-test pass does not replace the full-suite run.

## Add independent tests

Replace the placeholder in `tests/test_student_evidence.py` with at least
eight distinct top-level `test_...` functions. Use inputs different from the
published examples and cover the categories in the integrated Assignment.
These include valid and invalid construction, frozen ownership, path/problem
composition, separate run histories and an invalid update that leaves the
history unchanged.

```bat
python -m pytest -q
```

The published plus student suite must contain at least `84 passed`. Skipped
tests are not passed tests. The checker can verify counts and execution.
Whether the tests cover the required categories and make independent claims
still requires review.

## Generate outputs, finish the note and build the wheel

Run the next two commands from the repository root after the TODOs and tests
are complete. Neither command asks you to type coordinates or reads a JSON
input file. Both call the protected `build_demo_run()` in
`src/ap_week03_planning/demo.py`. It supplies the same fixed example each time:

| Supplied input | Value and meaning |
|---|---|
| Problem ID | `demo-tool-path`, the name attached to this one request |
| Start and goal | `(0.0, 0.0)` and `(3.2, 2.0)` metres |
| Lower and upper bounds | `(0.0, 0.0)` and `(4.0, 3.0)` metres |
| Ordered waypoints | `(0.0, 0.0)`, `(1.0, 1.4)`, `(2.4, 1.1)`, `(3.2, 2.0)` metres |

Your completed classes validate and store these values. The supplied path
already contains all four waypoints. No search algorithm chooses a path.
The caller records one successful result in a `PlanningRun`.

```bat
python -m ap_week03_planning.demo
```

This command prints six lines in the current terminal. It does not create the
JSON report or SVG preview.

```text
problem_id: demo-tool-path
configuration dimension: 2
waypoints: 4
path length: 4.356407
result count: 1
succeeded: True
```

The dimension is the number of coordinates per waypoint. The path length is
the sum of the three straight-segment lengths, printed to six decimal places
in metres. `succeeded: True` means this recorded result contains a valid path
under the Week 3 object contract. It does not mean a planner or robot ran.
If execution raises `NotImplementedError`, return to the named TODO. Do not
edit the protected caller or type the expected output yourself.

```bat
python scripts/generate_outputs.py
```

This command uses the same fixed inputs and writes two files. Successful
execution exits with code zero and prints a `[PASS] wrote ...` line for each
file, followed by `path_length=4.356407` and `result_count=1`.

| Generated file | How to open it and what to check |
|---|---|
| `artifacts/planning_objects_report.json` | Open in your text editor. Check the named fields for this problem, including four waypoints, one result and `path_length` equal to approximately `4.35640661761539`. This is the numerical summary, not an input file. |
| `artifacts/planning_objects_preview.svg` | Open the file in a web browser. SVG is an image format the browser can draw. Check that `start`, `q1`, `q2` and `goal` label the four supplied points in order. The connecting line displays the stored path, not a planned or simulated trajectory. |

Keep both files in `artifacts`. Rerunning the generator replaces these two
generated files with results from your currently installed source. It does
not fill the engineering note. Do not edit the JSON or SVG by hand.

```bat
notepad artifacts\engineering_note.md
```

Complete every existing note section using your actual results. Explain the
object responsibilities, constructor and update invariants with their test
names, inheritance and composition, aliasing prevention, generated outputs
and the Week 4 bridge. Save with **Ctrl+S**, close the editor and read back
what was saved.

```bat
type artifacts\engineering_note.md
```

The editable installation used during development points to the current
source. A wheel is a separate `.whl` package file that can be installed without
that editable link. The build command creates this distributable from the
current project. It does not run the course tests or install the resulting
wheel. Before rebuilding, inspect `dist` and remove only an obsolete Week 3
`.whl` file if necessary so the final folder contains exactly one wheel.

```bat
python -m build --wheel --no-isolation
dir /b dist\*.whl
```

Here `-m build` runs the build module through the selected Python. `--wheel`
selects wheel output, and `--no-isolation` uses the active environment's
installed build tools. This is a build setting, not a test setting.
`dir /b` lists matching filenames without extra directory details. With the
unchanged package metadata, it should print:

```text
ap_week03_planning-0.1.0-py3-none-any.whl
```

This file is inside `dist`. Finding it confirms a build output, not Assignment
completion. Run the separate submission checker next.

```bat
python scripts/check_submission.py
```

Confirm that no `REPLACE_ME` or empty answer remains. The JSON report and SVG
come from the protected generator. Do not edit them by hand. The SVG displays
the supplied path stored in your objects. It is not evidence of planning,
collision checking, robot execution or physics. The checker compares saved
outputs with a fresh temporary generation. For the wheel check, it runs a
separate isolated Python interpreter and verifies that the course package is
imported from that exact wheel, not the editable source. It uses existing
dependencies. It does not create a new virtual environment or install the
wheel with pip. The build command's `--no-isolation` option does not change
this later interpreter check. The checker's PASS does not establish
explanatory correctness, remote access or LMS submission.

The full commit ID is recorded after the commit. Do not place it inside a
note that would then require a different commit.

## Commit and push the Week 3 revision

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

`status --short` lists changed or untracked paths. `git diff` displays the
unstaged changes, while `git diff --staged` displays changes selected by
`git add`. If a pager opens, press `q` to return to the prompt. `git add` does
not upload files. `git commit` records the selected changes locally, and
`git push origin main` uploads the branch to its saved remote.
`git rev-parse HEAD` prints the local commit ID. `git ls-remote` reads the
remote branch ID without creating a commit.

Compare the two full commit IDs and check that the working tree is clean.
Open your private Week 3 repository on GitHub and check the note and generated
files at that pushed revision. Record its full 40-character commit ID for the
LMS submission. A later push does not silently replace the revision you submit.

## Submit the exact Week 3 revision through LMS

The deadline is one week after the corresponding Week 3 lab class. Follow the
exact date and time announced in LMS. Submit these same three fields used in
Weeks 1 and 2.

1. The URL of your private `applied-programming-w03-<student-id>` repository.
2. The full 40-character commit ID printed by `git rev-parse HEAD`, matching
   the pushed remote revision.
3. Confirmation that the repository is private, the actual `SSUMechE` access
   state, and that the stated commit is the revision to be graded.

The following entry is fictional. Replace every example value with your own
repository information.

```text
Repository URL:
https://github.com/student-example/applied-programming-w03-20261234

Full commit ID:
0123456789abcdef0123456789abcdef01234567

Confirmation:
The repository is private. SSUMechE has active collaborator access.
The commit above is the revision to be graded.
```

If the correct invitation was sent on time and only instructor acceptance is
pending, report that state instead of claiming active access. This is not a
student submission omission. Follow the LMS contact guidance if it remains
pending after the announced checking time.

- Follow the designated repository name, file structure and LMS format.
- Missing mandatory submission requirements by the deadline results in zero
  for the assignment. The timely pending-invitation exception above applies.
- GitHub upload without LMS submission is not recognized as submission.
- No additional LMS file attachment is required. Keep the source, tests, note,
  generated files and wheel in the submitted repository revision.

The submission-format rule does not mean that every failed numerical test
automatically makes the entire assignment zero. Do not submit the public
template URL, a local path, a branch name, `latest`, a short hash or an unpushed
commit. Never submit passwords, tokens, authentication codes or recovery codes.
Keep the repository private and retain instructor access until grading is
complete. Week 4 builds on these domain objects without replacing this Week 3
LMS submission.
