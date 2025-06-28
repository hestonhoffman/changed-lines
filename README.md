# Changed Lines

![GitHub tag (with filter)](https://img.shields.io/github/v/tag/hestonhoffman/changed-lines)

This GitHub action returns the file names and modified lines of each file in a pull request. This action is intended for custom linters, where you want to compare log lines against modified lines in your PR.

The action uses the patch data returned from the [Git API PR endpoint](https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-pull-requests-files) to collect the modified file names and lines. Changes in your PR are compared against the target branch and line numbers in the output are relative to the modified file. If the entire file is new, all lines appear in the output.


> [!NOTE]
> This action only works with pull requests.
> This action only works on Linux runners.

The action outputs a JSON formatted string. For example:
```json
{"test_file_1.py": [13, 30, 39], "test_file_2.md": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33], "test_file_3.txt": [14, 18, 19]}
```

## Using Changed Lines

```yaml
on: [ pull_request ]

jobs:
  find_changed_lines:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Find changed lines
        id: changed_lines
        uses: hestonhoffman/changed-lines@v1
      - name: Print changed lines
        run: echo ${{ steps.changed_lines.outputs.changed_lines }}
```

## Return only a list of changed files

The `outputs.changed_files` output gives you only the changed filenames in a space-delimited list. For example:
```bash
test_file_1.py test_file_2.md test_file_3.txt
```

## File delimiter

To change the delimiter, use the `delimiter` input. The following example outputs filenames separated by commas:
```yaml
[...]
    steps:
      - uses: actions/checkout@v4
      - name: Find changed lines
        id: changed_lines
        uses: hestonhoffman/changed-lines@v1
        with:
          delimiter: ','
      - name: Print changed files
        run: echo ${{ steps.changed_lines.outputs.changed_files }}
```

## Filter by file type

To return the output for only certain file types, use the `file_filter` input and specify a comma-separated list of file extensions. The following example only returns markdown and text files:
```yaml
[...]
    steps:
      - uses: actions/checkout@v4
      - name: Find changed lines
        id: changed_lines
        uses: hestonhoffman/changed-lines@v1
        with:
          file_filter: '.md, .txt'
      - name: Print changed files
        run: echo ${{ steps.changed_lines.outputs.changed_files }}
```

## Use an alternate GitHub API URL

Use the `api_url` input if you need to use a custom GitHub API URL. This is useful if you're a GitHub Enterprise user.

```yaml
[...]
    steps:
      - uses: actions/checkout@v4
      - name: Find changed lines
        id: changed_lines
        uses: hestonhoffman/changed-lines@v1
        with:
          api_url: https://example.com
      - name: Print changed files
        run: echo ${{ steps.changed_lines.outputs.changed_files }}
```

Thanks to Jacob Tomlinson [for a helpful tutorial](https://jacobtomlinson.dev/posts/2019/creating-github-actions-in-python/).

## Local development

You can use the instructions below to load some environment variables so you can run the script locally. You'll need a GitHub personal access token with repo privileges.

If you want to run the script locally:
1. (Optional) Set up a virtual environment using your preferred method.
1. Install the python modules:
   ```shell
   pip install -r requirements.txt
   ```
1. Make a copy of `example.env` and change the environment variables to point to a PR you want to test against:
   
   **Note**: This file (`.env`) is ignored by git, but make sure you don't accidentally commit it somehow, as it stores your git token.
   
   ```shell
   cp example.env .env
   ```
1. Run the script:
   ```shell
   python main.py
   ```
1. Check the generated text file for the results. The environment `GITHUB_OUTPUT` variable sets this to `temp.txt` by default.

## Deleted files and lines

Deleted files and lines don't show up in the output. This is intentional because the main use case for the action is to pass changed lines to a linter for GitHub command annotations. The GitHub API doesn't allow annotations on deleted lines.