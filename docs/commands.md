# COMMANDS

THIS FILE DESCRIBES AVAILABLE COMMANDS IN VVCOMMIT

## HELP
USE:
```bash
vvcommit help
```
to look at the all requests that are available now

## SWITCH 
```bash
vvcommit switch 
```

this command switches git auth method from HTTPS->SSH and reverse
(AND ALSO CHANGES AUTH_METHOD IN UR SETTINGS FILE AUTOMATICALLY)

## INITIALIZATION
UPDATED IN A LATEST VERSION!!!

1. With this tool you can init your github repo with one line. Just go into github page and click at "new repo". Then give it a name, description and visibility flag.
   Now you can just do:

```bash
vvcommit init github-login repo-name
```
and here github login is OPTIONAL if u have settings in ur setting.vvcommit file
so u can use just

```bash
vvcommit init <github-login> <repo-name>
```
and it will automatically choose a auth-method and paste ur github-login in
Of course you can also push stuff into existing repo:

```bash
vvcommit push-ex <github-login> <repo-name>
```

or

```bash
vvcommit push-ex <repo-name>
```

## COMMIT

1. Commit without pushing:

```bash
vvcommit com "commit message"
```

2. Commit and push into current branch:

```bash
vvcommit curr "commit message"
```

3. Commit and push to a specific branch:

### cbranch == commit branch, not copy branch!

```bash
vvcommit cbranch branch-name "commit message"
```

## PULL

1. Pull current branch (kinda useless but):

```bash
vvcommit pull
```

2. Pull a specific branch:

```bash
vvcommit pull branch-name
```

## BRANCH CREATION

1. Create and switch to a new branch:

```bash
vvcommit branch-create <type> <name>
```

Example:

```bash
vvcommit branch-create f login
```

that will create branch feature/login

| Key | Prefix        |
| --- | ------------- |
| f   | feature/      |
| b   | bugfix/       |
| h   | hotfix/       |
| e   | no prefix     |
| c   | custom prefix |

2. Branch Merge
   When ending a branch, only the suffix is required:

```bash
vvcommit branch-end footer-bug
```

We got also 2 flags here delete, and remote if we wanna delete this branch after merging and if we want to also delete from remote
Example:

```bash
vvcommit branch-end delete remote footer-bug
```

OR

```bash
vvcommit branch-end delete footer-bug
```

## UPDATE

Also we an always get latest version of tool from github using command:

```bash
vvcommit update
```

or if we don't want to save backup file (for safety)

```bash
vvcommit update --no-backup
```

## IGNORE

UPDATED IN LATEST VERSION!

Now with this request you can simply ignore things with one line

example:

```bash
vvcommit ignore "firstfile.py secondfile.c dir/"
```

this command will add this files/dirs into .gitignore, then commit + push them (later I will add feature that you can add to .gitignore without pushing and commiting)

and you can restore them back into project with only 1 flag:

```bash
vvcommit ignore "firstfile.py secondfile.c dir/" --restore
```

this command will remove this files from .gitignore and bring them back into github repo

# FOR NOW WORKING WITH BRANCHES IS NOT RECOMMENDED
