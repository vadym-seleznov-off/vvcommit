# COMMANDS

This document describes the available commands in `vvcommit`.

---

## HELP

Displays all available commands and requests.

```bash
vvcommit help
```


---

## SETTINGS

Configure your GitHub login and preferred authentication method. Once set, `vvcommit` remembers these values so you do not need to enter your username for every command.

```bash
vvcommit settings <github-login> <s|h>

```

* `s` stands for SSH
* `h` stands for HTTPS

---

## SWITCH

Switches your Git authentication method between HTTPS and SSH. This command automatically updates the `AUTH_METHOD` in your `settings.vvcommit` file.

```bash
vvcommit switch

```

---

## INITIALIZATION & PUSH

### Initialize a New Repository

1. Create a new repository on GitHub (set the name, description, and visibility).
2. Run the initialization command in your local directory:

If settings are configured:

```bash
vvcommit init <repo-name>

```

Without configured settings:

```bash
vvcommit init <github-login> <repo-name>

```

### Push to an Existing Repository

If settings are configured:

```bash
vvcommit push-ex <repo-name>

```

Without configured settings:

```bash
vvcommit push-ex <github-login> <repo-name>

```

---

## COMMIT

### 1. Commit without pushing

```bash
vvcommit com "commit message"

```

### 2. Commit and push to the current branch

```bash
vvcommit curr "commit message"

```

### 3. Commit and push to a specific branch

*(Note: `cbranch` stands for Commit Branch)*

```bash
vvcommit cbranch <branch-name> "commit message"

```

---

## PULL

### 1. Pull the current branch

```bash
vvcommit pull

```

### 2. Pull a specific branch

```bash
vvcommit pull <branch-name>

```

---

## BRANCH MANAGEMENT

> **Note:** Working with branches is currently not recommended as this feature is under active development.

### 1. Create and Switch to a Branch

```bash
vvcommit branch-create <type> <name>

```

**Example:**
`vvcommit branch-create f login` creates and switches to `feature/login`.

| Key | Prefix | Example Output |
| --- | --- | --- |
| **f** | `feature/` | `feature/login` |
| **b** | `bugfix/` | `bugfix/header` |
| **h** | `hotfix/` | `hotfix/patch-1` |
| **e** | *No prefix* | `custom-name` |
| **c** | *Custom prefix* | Prefix determined by user settings |

### 2. Merge and End a Branch

When ending a branch, only the branch name suffix is required:

```bash
vvcommit branch-end <branch-suffix>

```

#### Optional Flags

Delete local branch after merging:

```bash
vvcommit branch-end delete <branch-suffix>

```

Delete both local and remote branches after merging:

```bash
vvcommit branch-end delete remote <branch-suffix>

```

---

## IGNORE

Manage files in `.gitignore` using a single command.

### Add Files or Directories to .gitignore

Adds specified paths to `.gitignore`, then automatically commits and pushes the changes.

```bash
vvcommit ignore "firstfile.py secondfile.c dir/"

```

### Restore Files from .gitignore

Removes specified paths from `.gitignore` and restores them back to the repository.

```bash
vvcommit ignore "firstfile.py secondfile.c dir/" --restore

```

---

## UPDATE

Update `vvcommit` to the latest version directly from GitHub.

Default update (creates a safety backup):

```bash
vvcommit update

```

Update without creating a backup file:

```bash
vvcommit update --no-backup
```
