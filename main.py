'''
Uses GitHub API to grab patch data for a PR and calculate changed lines
'''

import os
import re
import json
import requests
from pprint import pprint

class MissingToken(Exception):
    '''Raised when the GitHub token is missing'''
    
class MissingPatchData(Exception):
    '''Raised when the patch data is missing'''    

def fetch_patch():
    '''Grabs the patch data from the GitHub API.'''
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
    line_array = []
    sublist = []
    final_dict = {}
    for entry in patch_data:
        if entry['additions'] != 0:
            if 'patch' in entry:
                patch_array = re.split('\n', entry['patch'])
                # clean patch array
                patch_array = [i for i in patch_array if i]

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
        # Remove deleted/renamed files (which appear as empty arrays)
        if line_array:        
            final_dict[file_name] = line_array
    return final_dict

if __name__ == "__main__":
    
    TOKEN = os.getenv('INPUT_TOKEN')
    branch_name = os.getenv('INPUT_BRANCH')
    repo = os.getenv('INPUT_REPO')
    pr = os.getenv('INPUT_PR')
    github_output = os.getenv('GITHUB_OUTPUT')
    delimiter = os.getenv('INPUT_DELIMITER')

    if not TOKEN:
        raise MissingToken('Missing GitHub token')

    data = fetch_patch()
    added_line_data = parse_patch_data(data)
    added_lines = get_lines(added_line_data)
    filename_list = ''
    for filename in added_lines:
        filename_list += filename + delimiter

    with open(github_output, 'a', encoding='utf-8') as f:
        f.write(
            f'changed_lines={json.dumps(added_lines)}\n' +
            f'changed_files={filename_list.strip()}\n'
            )