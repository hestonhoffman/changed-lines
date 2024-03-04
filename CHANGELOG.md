## Changelog

### 1.5

- ([feature][5]) Filter output by file type.

[5]: https://github.com/hestonhoffman/changed-lines/pull/10

### 1.4

- ([bug][4]) Fix a bug that was causing a `'patch_array' referenced before assignment` error.

[4]: https://github.com/hestonhoffman/changed-lines/pull/9

### 1.3

- ([bug][3]) Ignore deleted files in a PR.

[3]: https://github.com/hestonhoffman/changed-lines/pull/6

### 1.2

- ([bug][2]) Account for entries with no patch data: When a diff is too large to display in the PR, GitHub doesn't provide the patch, so there's no way to grab the modified lines. Entries that don't contain patch data are now skipped.

[2]: https://github.com/hestonhoffman/changed-lines/pull/5

### 1.1

- ([bug][1]) Account for entries with no additions: Entries that didn't include additions would cause the action to fail. Entries with no additions are now skipped.

[1]: https://github.com/hestonhoffman/changed-lines/commit/73fec4dd4b78a0a29de46a8660f492f3f2eef70f

### 1

- (feature) Adds output for filenames only (changed_filenames).
- (feature) Adds a delimiter input for the changed_filenames output.



