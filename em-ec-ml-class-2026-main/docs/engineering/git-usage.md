# Git Usage

Git is the version control system used to track the source code of a project, collaborate with other contributors, and keep a clean history of every change. This note covers the four operations used daily: creating a branch, committing, stashing work in progress, and rebasing.

## Principles

- Never work directly on `main`: it should always hold a stable, working version of the project. All work happens on dedicated branches, merged back through a pull request.
- A branch has a single purpose (one feature, one fix), and lives for a short time. Long-lived branches drift away from `main` and become painful to merge.
- A commit is a small, coherent unit of change, with a message explaining *what* it does. A reader should understand the history of the project from `git log` alone.
- Keep your branch up to date with its source branch frequently, to resolve conflicts early while they are still small.

In VSCode, all git operations are available from the **Source Control** view (`Ctrl+Shift+G`), and the **branch name** shown in the bottom-left corner of the status bar.

## 1. Create a branch and switch to it

### Naming conventions

Branch names are lowercase, use `/` to separate a type prefix from a short description, and `-` between words:

| Prefix       | Purpose                                         | Example                            |
| ------------ | ----------------------------------------------- | ---------------------------------- |
| `feature/`   | New functionality                               | `feature/add-data-preprocessing`   |
| `fix/`       | Bug fix                                         | `fix/missing-values-imputation`    |
| `hotfix/`    | Urgent fix to apply on a released version       | `hotfix/1.2.1-crash-on-empty-file` |
| `release/`   | Preparation of a release (version bump, notes)  | `release/1.3.0`                    |
| `chore/`     | Maintenance: dependencies, config, tooling      | `chore/upgrade-pandas`             |
| `docs/`      | Documentation only                              | `docs/git-usage-notes`             |
| `refactor/`  | Code restructuring without behavior change      | `refactor/split-training-pipeline` |

When a ticketing system is used, the ticket id can be added: `feature/ML-42-add-data-preprocessing`.

Feature branches are created from `main` and merged back into it. Release branches are created from `main` when a version is ready to be stabilized; only fixes are added to them, and they are tagged (`v1.3.0`) once released.

### CLI

```bash
# Start from an up-to-date main
git switch main
git pull

# Create the branch and switch to it
git switch -c feature/add-data-preprocessing
# (older equivalent: git checkout -b feature/add-data-preprocessing)

# List branches, the current one is marked with *
git branch

# Publish the branch on the remote and set upstream tracking
git push -u origin feature/add-data-preprocessing
```

### VSCode

1. Click the branch name in the bottom-left corner of the status bar, select `main`.
2. In the Source Control view, click `...` > **Pull** (or the sync icon in the status bar) to update it.
3. Click the branch name again and choose **+ Create new branch...**.
4. Type the branch name, e.g. `feature/add-data-preprocessing`, and press `Enter`. VSCode switches to the new branch automatically.
5. Click **Publish Branch** in the Source Control view to push it to the remote.

## 2. Add commits to a branch

### Naming conventions

Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org) format:

```
<type>(<optional scope>): <short description in imperative mood>

<optional body explaining why the change is made>
```

| Type       | Usage                                              | Example                                          |
| ---------- | -------------------------------------------------- | ------------------------------------------------ |
| `feat`     | New feature                                        | `feat: add standard scaling to preprocessing`    |
| `fix`      | Bug fix                                            | `fix: handle empty dataframe in train split`     |
| `chore`    | Maintenance, dependencies, tooling                 | `chore: bump scikit-learn to 1.6`                |
| `docs`     | Documentation only                                 | `docs: add git usage notes`                      |
| `refactor` | Code change that neither fixes a bug nor adds a feature | `refactor: extract feature engineering module` |
| `test`     | Add or update tests                                | `test: add unit tests for imputer`               |
| `style`    | Formatting, no code logic change                   | `style: apply ruff formatting`                   |
| `perf`     | Performance improvement                            | `perf: vectorize distance computation`           |
| `ci`       | CI/CD configuration                                | `ci: run tests on pull requests`                 |

Good practices:

- Use the imperative mood ("add", not "added" or "adds"), no final period, keep the first line under ~70 characters.
- One commit = one logical change. Don't mix a feature, a refactor and a formatting pass in the same commit.
- Never commit secrets, data files, or large model artifacts: list them in `.gitignore`.

### CLI

```bash
# See which files are modified, staged or untracked
git status

# Inspect the changes before staging
git diff

# Stage specific files (preferred over "git add ." to avoid committing unwanted files)
git add src/preprocessing.py tests/test_preprocessing.py

# Commit the staged changes
git commit -m "feat: add standard scaling to preprocessing"

# Commit with a body (opens the editor)
git commit

# Review the history of the branch
git log --oneline

# Push the new commits to the remote branch
git push
```

### VSCode

1. Open the Source Control view (`Ctrl+Shift+G`). Modified files are listed under **Changes**; click a file to see its diff.
2. Hover a file and click **+** to stage it (or **+** on the **Changes** header to stage all). Staged files move to **Staged Changes**.
3. Type the commit message in the text box at the top, e.g. `feat: add standard scaling to preprocessing`.
4. Click **Commit** (or `Ctrl+Enter`).
5. Click **Sync Changes** (or `...` > **Push**) to push the commits to the remote.
6. The history can be browsed in the **Source Control Graph** section at the bottom of the Source Control view.

## 3. Stash and unstash work in progress

Stashing puts your uncommitted changes aside, leaving a clean working directory. It is useful when you need to switch branch quickly (to review a colleague's branch, or fix an urgent bug) without committing half-finished work.

### CLI

```bash
# Stash the current changes, with a description
git stash push -m "wip: tuning of the imputer"

# Include untracked (new) files in the stash
git stash push -u -m "wip: tuning of the imputer"

# List the stashes
git stash list
# stash@{0}: On feature/add-data-preprocessing: wip: tuning of the imputer

# Show the content of a stash
git stash show -p stash@{0}

# Re-apply the latest stash and remove it from the list
git stash pop

# Re-apply a specific stash but keep it in the list
git stash apply stash@{1}

# Delete a stash
git stash drop stash@{1}
```

### VSCode

1. In the Source Control view, click `...` > **Stash** > **Stash**. Choose **Stash (Include Untracked)** to also stash new files.
2. Enter a description for the stash, e.g. `wip: tuning of the imputer`, and press `Enter`. The working directory is now clean.
3. To restore it, click `...` > **Stash** > **Pop Latest Stash**, or **Pop Stash...** to pick a specific one (`Apply` variants keep the stash in the list).
4. Stashes are also listed in the **Stashes** section of the Source Control view, where they can be inspected, applied or dropped.

## 4. Rebase from an updated source branch

While you work on your branch, `main` keeps receiving new commits from other contributors. Rebasing replays your commits on top of the latest `main`, as if you had started your branch from it. It keeps a linear history and lets you resolve conflicts on your side before opening the pull request.

```
Before:            A---B---C  main
                        \
                         D---E  feature/x

After rebase:      A---B---C  main
                            \
                             D'---E'  feature/x
```

Golden rule: only rebase branches you own. Rebasing rewrites the commits of the branch, so a branch shared with other contributors must instead be updated with `git merge main`.

### CLI

```bash
# Commit or stash any work in progress first
git status

# Fetch the latest state of the remote
git fetch origin

# Replay the current branch on top of the updated main
git rebase origin/main

# In case of conflict: edit the conflicting files, then
git add <resolved-file>
git rebase --continue

# Skip a commit that is no longer needed, or abort and go back to the initial state
git rebase --skip
git rebase --abort

# The branch history was rewritten: the push must be forced.
# --force-with-lease refuses to overwrite remote commits you haven't fetched
git push --force-with-lease
```

### VSCode

1. Make sure the working directory is clean (commit or stash, see sections 2 and 3).
2. In the Source Control view, click `...` > **Fetch** to retrieve the latest remote state.
3. Click `...` > **Branch** > **Rebase Branch...**, and select `origin/main`.
4. If conflicts occur, the files are listed under **Merge Changes**. Open each one, resolve the conflict using the inline actions (**Accept Current Change**, **Accept Incoming Change**, **Accept Both Changes**) or the **Resolve in Merge Editor** button, then stage the file with **+**.
5. Click **Continue** in the Source Control view. To cancel, run `git rebase --abort` in the terminal.
6. Push the rewritten branch: VSCode's Sync will refuse it, so use `...` > **Pull, Push** > **Force Push**. This entry only appears once the `git.allowForcePush` setting is enabled; the CLI `git push --force-with-lease` is the safer option.

### Alternative: pull from the source branch

Pulling from `main` into your branch is the other way to bring in its new commits. `git pull` is a `git fetch` followed by a `git merge`: instead of replaying your commits, it creates a **merge commit** that joins the two histories.

```
Before:            A---B---C  main
                        \
                         D---E  feature/x

After pull:        A---B---C  main
                        \   \
                         D---E---M  feature/x
```

| | Pull from `main` (merge) | Rebase on `main` |
| --- | --- | --- |
| Your commits | Kept as they are | Rewritten (`D'`, `E'` get new ids) |
| History | Non-linear, with an extra merge commit `M` each time | Linear, as if the branch started from the latest `main` |
| Conflicts | Resolved once, in the merge commit | Resolved commit by commit, as each one is replayed |
| Push afterwards | Normal `git push` | Force push needed (`--force-with-lease`) |
| Shared branches | Safe | Avoid: it breaks collaborators' copies of the branch |

In practice: rebase your own branches to keep a clean history, and pull (merge) when the branch is shared with other contributors. Also note that on your branch, a plain `git pull` (without naming a branch) only pulls the remote copy of that same branch (`origin/feature/x`), not `main`.

#### CLI

```bash
# Merge the latest remote main into the current branch
git pull origin main

# In case of conflict: edit the conflicting files, then
git add <resolved-file>
git commit
# or abort and go back to the initial state
git merge --abort

# No rewrite happened: a normal push is enough
git push

# Note: git pull can also rebase instead of merging
git pull --rebase origin main   # equivalent to: git fetch + git rebase origin/main
```

#### VSCode

1. Make sure the working directory is clean (commit or stash, see sections 2 and 3).
2. In the Source Control view, click `...` > **Pull, Push** > **Pull from...**.
3. Select the remote `origin`, then the branch `origin/main`.
4. If conflicts occur, resolve them as described in step 4 of the rebase above, stage the files with **+**, then click **Commit** to create the merge commit.
5. Click **Sync Changes** to push the branch, no force push needed.
