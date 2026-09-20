# Week 3 — Object-Oriented Programming

Build objects that store coordinates and paths, reject invalid combinations,
and keep each planning run's results separate. Complete TODO 1–8, write at least
four independent tests, run the demo, and submit your code through GitHub and LMS.
You do not implement a planner, collision checker, controller or simulator.

Read [Week 3 Reading, Section 7](docs/week_03_object_oriented_programming_reading_v11.pdf)
for the Assignment and [PROTECTED_FILES.md](PROTECTED_FILES.md) for the edit
boundary. This README provides the commands in working order. Chapter practice
uses a separate folder. Do not paste chapter examples over the Assignment files.

<details>
<summary>Already started? Keep your repository and completed TODOs</summary>

The 21 September simplification keeps the public API, TODO 1–8 and all 76
published tests. Your code still applies. Do not clone again or replace your
three editable files. No new invitation is needed for the same repository.

Download the existing-student update ZIP from the
[Week 3 V10 release](https://github.com/SSUMechE/applied-programming-2026-week03-starter/releases/tag/week03-v10-simplified-assignment)
and extract it outside your repository. From Anaconda Prompt in your existing
repository, run the extracted updater. Replace the example path:

```bat
python "C:\Downloads\week03-update\apply_week03_update.py" --repo .
```

The updater checks the supplied files before updating them and preserves your
three editable files and existing personal work. Read its result. If a protected
file differs, stop and ask for help instead of forcing an overwrite. Use the new
Reading and checker after a successful update. Review `git diff`, then run the
updater's printed `git add -- ...` command to stage the official updates before
the normal code/test commit. The updater does not stage, commit or push for you.

</details>

## 1. Open the repository and prepare the environment

Create a private repository from
[the Week 3 template](https://github.com/SSUMechE/applied-programming-2026-week03-starter)
only if you do not already have one:

1. Select **Use this template → Create a new repository** under your account.
2. Name it `applied-programming-w03-<student-id>` and select **Private**.
3. Use **Settings → Collaborators → Add people** to invite **SSUMechE**.

Invitation pending and accepted/active are different states. A correct invitation
sent on time and awaiting only instructor acceptance is not a student omission.

On Windows use **Anaconda Prompt**, not the Python `>>>` prompt. Replace the
folder, GitHub ID and student ID below. If already cloned, enter that folder
instead of cloning again.

```bat
cd /d "C:\your-course-folder"
git clone https://github.com/YOUR-GITHUB-ID/applied-programming-w03-YOUR-STUDENT-ID.git
cd applied-programming-w03-YOUR-STUDENT-ID
git remote -v
```

Both `origin` addresses must point to your private Week 3 repository. On first
HTTPS clone, Git Credential Manager may open browser sign-in. Use the repository
owner's account and complete your own two-factor authentication. A GitHub account
password is not a Git HTTPS password. Follow the course Credential Manager or
personal access token guidance. Never put a token in a URL, file or LMS entry.
For `Repository not found`, check the URL and signed-in account first.

Run subsequent commands from the **repository root**. Reuse your working Week 1
environment. If it does not exist, first run `conda env create -f environment.yml`.

```bat
conda activate applied-programming-2026
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

The first install adds dependencies. The second links this package to saved
source edits. Expect `[PASS] Week 3 object-programming environment is ready.`
This checks setup, not the unfinished TODOs. Stop at the first installation error.

<details>
<summary>Installation fails: corrected Conda route and Python 3.12 alternative</summary>

For `DLL load failed`, `_socket`, `_multiarray_umath` or an application-control
error, do not disable Windows security, delete your environment or replace TODO
files. This corrected route passed on the instructor's PC, but individual
managed-PC restrictions can still require administrator help.

In Anaconda Prompt at the repository root, create a separate environment:

```bat
set PYTHONUTF8=1
conda create -n applied-programming-w03 --override-channels -c conda-forge python=3.12.13 pip=26.2.1
```

Confirm with `y`. If the name already exists, skip creation. `PYTHONUTF8` addresses
a possible `cp949` decoding error, not a security block.

```bat
conda activate applied-programming-w03
python -c "import socket, ssl; print('IMPORTS_OK')"
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

Expect `IMPORTS_OK` and the verifier PASS. Do not install NumPy separately with
`conda install` here. In later windows, activate `applied-programming-w03`.

If Anaconda is unavailable or still fails, use an official Python 3.12
installation with the Windows Python launcher. Check `py -3.12 --version`.
If missing, use the official
[Python Windows downloads](https://www.python.org/downloads/windows/) or ask the
administrator. Do not download individual DLLs from third-party sites.

From the existing repository, create `.venv` only if it does not exist:

```bat
py -3.12 -m venv .venv
```

Then activate it and check:

```bat
.venv\Scripts\activate
python --version
python -c "import sys; print(sys.executable)"
python -c "import socket, ssl; print('IMPORTS_OK')"
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
python scripts/verify_environment.py
```

Expect Python 3.12.x, this repository's `.venv\Scripts\python.exe`, `IMPORTS_OK`
and the verifier PASS. Stop at the first error and report it without credentials.
Do not delete an existing failing `.venv`. In later windows, return here and run
`.venv\Scripts\activate`. Do not upload the environment folder.

</details>

## 2. Complete TODO 1–8

An untouched starter gives `68 failed, 8 passed` with
`python scripts/run_baseline.py`. These are expected unfinished-TODO failures.
If you already edited TODOs, keep your work and run the relevant check below.

Open the two source files, find each TODO, replace its `raise NotImplementedError`
body, and save. Keep provided fields, names, signatures, decorators and TODO
numbers. Reading Section 7 gives the required behavior. Do not reimplement
`geometry.py` or the provided `PlanningRun._results` field.

| File | TODOs and bodies to complete |
|---|---|
| `src/ap_week03_planning/domain.py` | 1: `_normalized_values`, `Configuration.__post_init__`. 2: `Configuration.dimension`, `.as_array`. |
| Same file | 3: `ConfigurationBounds.__post_init__`, `.dimension`. 4: `.contains`. |
| Same file | 5: `Path.__post_init__`, `.dimension`, `.start`, `.goal`, `.as_array`, `.length`. |
| Same file | 6: `PlanningProblem.__post_init__`. 7: `PlanResult.__post_init__`, `.succeeded`. |
| `src/ap_week03_planning/history.py` | 8: `PlanningRun.__post_init__`, `.record_result`, `.results`, `.latest`. |

Run each command **after completing the named group**:

```bat
python -m pytest -q tests/test_published_contract.py -k test_configuration_ -x
```

After TODO 1–2: `21 passed, 55 deselected`.

```bat
python -m pytest -q tests/test_published_contract.py -k test_bounds_ -x
```

After TODO 3–4: `11 passed, 65 deselected`.

```bat
python -m pytest -q tests/test_published_contract.py -k "test_path_ or test_problem_" -x
```

After TODO 5–6: `17 passed, 59 deselected`. Some path tests also need the problem.

```bat
python -m pytest -q tests/test_published_contract.py -k "result or run" -x
```

After TODO 7–8: `16 passed, 60 deselected`.

`-k` selects names, `-x` stops at the first failure, and `-q` reduces detail.
`deselected` tests did not run. After all TODOs, run the full published suite:

```bat
python -m pytest -q tests/test_published_contract.py
```

Expected: **76 passed**. This full suite includes cases outside the grouped checks.

## 3. Write tests and check the completed program

Replace the placeholder in `tests/test_student_evidence.py` with **at least four
distinct top-level `test_...` functions**. Cover these four behaviors with your
own inputs and assertions:

- Normal construction or use gives the expected result.
- Invalid construction or an invalid update raises `PlanningModelError`.
- Changing a caller-owned input or returned array does not change stored values.
- Two `PlanningRun` instances keep separate result histories.

Parametrized variants of one function still count as one function. Do not copy
published test bodies, leave placeholder-only tests or count skipped tests.

```bat
python -m pytest -q
python -m ap_week03_planning.demo
python scripts/check_submission.py
```

Expect **at least 80 passed**, then the demo's six lines:

```text
problem_id: demo-tool-path
configuration dimension: 2
waypoints: 4
path length: 4.356407
result count: 1
succeeded: True
```

The demo uses supplied coordinates, not keyboard input. The local checker must
finish with `[PASS] Week 3 code and test checkpoint: ...`. It runs the tests and
checks their basic structure. The instructor reviews category coverage,
meaningful assertions and independence. A pass is not GitHub or LMS submission.

## 4. Review and push your code

```bat
git status --short
git diff
git add src/ap_week03_planning/domain.py
git add src/ap_week03_planning/history.py
git add tests/test_student_evidence.py
git diff --staged
git commit -m "Complete Week 3 planning domain objects"
git push origin main
git rev-parse HEAD
git ls-remote origin refs/heads/main
git status --short
```

Review changes before committing. Press `q` to leave a Git pager. `add` selects
files, `commit` saves a local revision, and `push` uploads it. The two full commit
IDs must match. Confirm the submitted code and tests are visible at that revision.

## 5. Submit through LMS

Submit within **one week of the Week 3 lab**. The exact date/time is in LMS.
Use the same three fields as Weeks 1 and 2. Fictional example:

```text
Repository URL:
https://github.com/student-example/applied-programming-w03-20261234

Full commit ID:
0123456789abcdef0123456789abcdef01234567

Confirmation:
The repository is private. SSUMechE has active collaborator access.
The commit above is the revision to be graded.
```

- Replace every example value. Report a correct on-time invitation as pending
  if only instructor acceptance remains. That pending state is not an omission.
- Follow the designated repository name, file structure and LMS format. Missing
  mandatory submission requirements by the deadline results in zero, with the
  pending-invitation exception above. This is not automatic zero for every test
  failure.
- GitHub upload alone is not submission. No LMS file attachment is required.
- Do not submit the public template URL, local path, branch name, `latest`,
  short hash, unpushed commit or credentials. Later pushes do not replace the
  submitted revision. Retain private visibility and instructor access for grading.
