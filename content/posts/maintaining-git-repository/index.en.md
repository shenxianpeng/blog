---
title: How to Slim Down Your Git Repository
summary: How to remove unnecessary files and history from a Git repository to reduce its size, providing two methods: using BFG Repo Cleaner or `git filter-branch`.
tags:
  - Git
date: 2020-03-21
author:
---

Maintaining a Git repository often involves reducing its size. If you've imported a repository from another version control system, you may need to clean up unnecessary files after the import. This article mainly discusses how to remove unwanted files from a Git repository.



> Please exercise extreme caution...
>
> The steps and tools in this article employ advanced techniques involving destructive operations.  Ensure you carefully read and back up your repository before you begin. The easiest way to create a backup is to clone your repository using the `--mirror` flag, and then package and compress the entire cloned directory. With this backup, you can restore from the backup repository if key elements of your repository are accidentally corrupted during maintenance.
>
> Remember, repository maintenance can be disruptive to repository users.  Communicating with your team or repository followers is essential. Ensure everyone has checked out their code and agrees to halt development during repository maintenance.

## Understanding File Removal from Git History

Recall that cloning a repository clones the entire history—including all versions of every source code file. If a user commits a large file, such as a JAR, then every subsequent clone includes that file. Even if the user eventually deletes the file in a later commit, the file remains in the repository's history. To completely remove the file from your repository, you must:

* Delete the file from your project's current file tree;
* Remove the file from the repository's history—rewriting Git history to remove the file from all commits containing it;
* Delete all reflog history pointing to the old commit history;
* Repack the repository using `git gc` to garbage collect now-unused data.

Git's `gc` (garbage collection) will remove all actual unused data or data not referenced in any of your branches or tags in the repository. For it to work, we need to rewrite all Git repository history containing the unwanted files, the repository will no longer reference it, and `git gc` will discard all unused data.

Rewriting repository history is a tricky business because each commit depends on its parent commits, so even a small change alters every subsequent commit's hash.  There are two automated tools that can help you do this:

1. `BFG Repo Cleaner`—Fast, simple, and easy to use; requires Java 6 or later runtime environment.
2. `git filter-branch`—Powerful, more cumbersome to configure, slower for larger repositories, and is part of the core Git suite.

Remember, after rewriting history, whether you use BFG or `filter-branch`, you must delete `reflog` entries pointing to the old history and finally run the garbage collector to remove the old data.


## Rewriting History with BFG

BFG is specifically designed to remove unwanted data like large files or passwords from a Git repository, so it has a simple flag to remove large historical files (not in the current commit): `--strip-blobs-bigger-than`

BFG [Download](https://repo1.maven.org/maven2/com/madgag/bfg)

```bash
java -jar bfg.jar --strip-blobs-bigger-than 100M
```

Any files larger than 100MB (excluding files in your recent commits—as BFG protects your latest commits by default) will be removed from your Git repository's history. You can also specify files by name:

```bash
java -jar bfg.jar --delete-files *.mp4
```

BFG is 10–1000 times faster than `git filter-branch` and generally easier to use—see the full [usage instructions](https://rtyley.github.io/bfg-repo-cleaner/#usage) and [examples](https://rtyley.github.io/bfg-repo-cleaner/#examples) for more details.

## Alternatively, Rewriting History with `git filter-branch`

The `filter-branch` command can rewrite a Git repository's history, like BFG, but the process is slower and more manual. If you don't know where these large files are, your first step will be to find them:

### Manually Finding Large Files in Your Git Repository

[Antony Stubbs](https://stubbisms.wordpress.com/2009/07/10/git-script-to-show-largest-pack-objects-and-trim-your-waist-line/) wrote a BASH script that does this well.  The script inspects the contents of your pack files and lists large files. Before you start deleting files, do the following to obtain and install this script:

1. [Download the script](https://confluence.atlassian.com/bitbucket/files/321848291/321979854/1/1360604134990/git_find_big.sh) to your local system.
2. Place it in an easily accessible location relative to your Git repository.
3. Make the script executable:

    ```bash
    chmod 777 git_find_big.sh
    ```

4. Clone the repository to your local system.
5. Change the current directory to your repository's root.
6. Manually run the Git garbage collector:

    ```bash
    git gc --auto
    ```

7. Find the size of the `.git` folder:

    ```bash
    # Note the file size for later reference
    du -hs .git/objects
    45M .git/objects
    ```

8. Run `git_find_big.sh` to list large files in your repository:

    ```bash
    git_find_big.sh
    All sizes are in kB's. The pack column is the size of the object, compressed, inside the pack file.
    size  pack  SHA                                       location
    592   580   e3117f48bc305dd1f5ae0df3419a0ce2d9617336  media/img/emojis.jar
    550   169   b594a7f59ba7ba9daebb20447a87ea4357874f43  media/js/aui/aui-dependencies.jar
    518   514   22f7f9a84905aaec019dae9ea1279a9450277130  media/images/screenshots/issue-tracker-wiki.jar
    337   92    1fd8ac97c9fecf74ba6246eacef8288e89b4bff5  media/js/lib/bundle.js
    240   239   e0c26d9959bd583e5ef32b6206fc8abe5fea8624  media/img/featuretour/heroshot.png
    ```

The large files are all JAR files. The pack size column is the most relevant. `aui-dependencies.jar` compresses to 169kb, but `emojis.jar` only compresses to 500kb. `emojis.jar` is a candidate for deletion.

### Running `filter-branch`

You pass this command a filter that modifies the Git index. For example, a filter can delete each retrieved commit. This usage is:

```bash
git filter-branch --index-filter 'git rm --cached --ignore-unmatch&nbsp; _pathname_ ' commitHASH
```

The `--index-filter` option modifies the repository's index, and the `--cached` option deletes files from the index, not the disk. This is faster because you don't need to check each revision before running the filter.
The `ignore-unmatch` option in `git rm` prevents the command from failing when trying to remove a non-existent file `pathname`. By specifying a commit HASH, you delete `pathname` from every commit starting at that HASH. To delete from the beginning, omit this parameter or specify `HEAD`.

If your large files are in different branches, you will need to delete each file by name. If the large files are all on a single branch, you can delete the branch itself.

#### Option 1: Deleting Files by Filename

Use the following steps to delete large files:

1. Use the following command to delete the first large file you found:

    ```bash
    git filter-branch --index-filter 'git rm --cached --ignore-unmatch filename' HEAD
    ```

2. Repeat step 1 for each remaining large file.

3. Update references in your repository. `filter-branch` creates backups of your original references under `refs/original/`. Once you are sure you have deleted the correct files, run the following to remove the backups and allow the garbage collector to reclaim large objects:

    ```bash
    git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
    ```

#### Option 2: Deleting a Branch Directly

If all your large files are on a single branch, you can delete the branch directly. Deleting the branch automatically removes all references.

1. Delete the branch:

    ```bash
    git branch -D PROJ567bugfix
    ```

2. Remove all reflog references to the branch:

    ```bash
    git reflog expire --expire=now PROJ567bugfix
    ```

#### Garbage Collecting Unused Data

1. Delete all reflog references from now to the past (unless you explicitly operated only on one branch):

    ```bash
    git reflog expire --expire=now --all
    ```

2. Repack the repository by running the garbage collector and removing old objects:

    ```bash
    git gc --prune=now
    ```

3. Push all your changes back to the repository:

    ```bash
    git push --all --force
    ```

4. Ensure that all your tags are also up-to-date:

    ```bash
    git push --tags --force
    ```

[Original Article](https://confluence.atlassian.com/bitbucket/maintaining-a-git-repository-321848291.html)