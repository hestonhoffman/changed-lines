'''
Uses GitHub API to grab patch data for a PR and calculate changed lines
'''

import os
import re
import json
import requests

class MissingToken(Exception):
    '''Raised when the GitHub token is missing'''

def fetch_patch():
    '''Grabs the patch data from the GitHub API and returns it as a JSON object.'''
    git_session = requests.Session()
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization':f'Bearer {TOKEN}'
        }
    git_request = git_session.get(
        f'https://api.github.com/repos/{repo}/pulls/{pr}/files',
        headers=headers
        )
    return git_request.json()

def parse_patch_data(patch_data):
    '''Takes the patch data and returns a dictionary of files and the lines'''
    final_dict = {}
    for entry in patch_data:
        # patch_dict[entry['filename']] = entry['patch']
        patch_array = re.split('\n', entry['patch'])
        # clean patch array
        patch_array = [i for i in patch_array if i]
        line_array = []
        sublist = []

        for item in patch_array:
            # Grabs hunk annotation and strips out added lines
            if item.startswith('@@ -'):
                if sublist:
                    line_array.append(sublist)
                sublist = [re.sub(r'\s@@(.*)','',item.split('+')[1])]
            # We don't need removed lines ('-')
            elif not item.startswith('-') and not item == '\\ No newline at end of file':
                sublist.append(item)
        if sublist:
            line_array.append(sublist)
            final_dict[entry['filename']] = line_array
    return final_dict

def get_lines(line_dict):
    '''Takes the dictionary of files and lines and returns a dictionary of files and line numbers'''
    final_dict = {}
    for file_name, sublist in line_dict.items():
        line_array = []
        for array in sublist:
            line_number = 0
            if ',' not in array[0]:
                line_number = int(array[0]) - 1
            else:
                line_number = int(array[0].split(',')[0]) - 1
            for line in array:
                if line.startswith('+'):
                    line_array.append(line_number)
                line_number += 1
        final_dict[file_name] = line_array
    return final_dict

if __name__ == "__main__":
    TOKEN = os.getenv('INPUT_TOKEN')
    branch_name = os.getenv('INPUT_BRANCH')
    repo = os.getenv('INPUT_REPO')
    pr = os.getenv('INPUT_PR_NUMBER')
    github_env = os.getenv('GITHUB_ENV')
    
    print(repo)
    print(branch_name)
    print(pr)
    print(github_env)

    if not TOKEN:
        raise MissingToken('Missing GitHub token')

    data = fetch_patch()
    added_lines = parse_patch_data(data)

    with open(github_env, 'a', encoding='utf-8') as f:
        f.write(json.dumps(get_lines(added_lines)))
