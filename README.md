# Agentic Software Engineering Entry Test

## Task 1: Check pinned dependencies

The script checks package and version existence using the PyPI JSON API and
reports the oldest valid pinned release, using the first listed file's
`upload_time` as required by the assignment.

### Run step by step

1. Install Python 3 if it is not already available.
2. Open a terminal in this folder.
3. Run on Windows:

   ```powershell
   py check_requirements.py
   ```

   On macOS or Linux:

   ```bash
   python3 check_requirements.py
   ```

4. To check the paper's sample input, run:

   ```powershell
   py check_requirements.py sample_requirements.txt
   ```

Only the Python standard library is used. Internet access is required.
`requirements.txt` is input data: do not install its contents.

### How it works

1. Count all input lines. Each line must have the form `package==version`.
2. Request `https://pypi.org/pypi/<name>/json`.
3. If that returns 404, count a missing package and move to the next line.
4. Otherwise request `https://pypi.org/pypi/<name>/<version>/json`.
5. If that returns 404, count a missing version and move to the next line.
6. For a valid release, read `urls[0]["upload_time"]` and compare dates.
7. Print the four requested results.

Network failures and other HTTP errors stop the script; they are not counted
as missing packages. A release without files also produces an explicit error.
Blank lines and comments are not accepted because this exercise expects one
pinned dependency per line.

The paper's expected sample output is:

```text
Dependencies checked: 5
Packages not on PyPI: 1
Versions not on PyPI: 1
Oldest pinned release: numpy==1.16.0 (2019)
```

PyPI availability can change, so current results may differ from the paper.
API documentation: https://docs.pypi.org/api/json/

### Submission procedure from the paper

1. Create a public GitHub or GitLab repository.
2. Upload the files in this folder.
3. Submit the repository link on PANDA.

No repository has been created or published by this project.

## Task 2: Trace the given program

The `flask` entry is skipped because it has no equals sign. The other four
entries contribute major-version digits 2, 1, 0, and 2. Therefore `p` is 4,
`ms` is 5, and `ms / p` is 1.25. The last processed name is `pandas=`, whose
first four characters become `PAND` after conversion to uppercase.

Exact output:

```text
Pinned: 4
Average major version: 1.25
Acronym: PAND
```
