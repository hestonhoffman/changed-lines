'''
Uses GitHub API to grab patch data for a PR and calculate changed lines
'''

import os
import re
import json
import requests

class MissingToken(Exception):
    '''Raised when the GitHub token is missing'''
    
class MissingPatchData(Exception):
    '''Raised when the patch data is missing'''

class MissingApiUrl(Exception):
    '''Raised when the GitHub api url is missing'''

def fetch_patch():
    '''Grabs the patch data from the GitHub API.'''
    git_session = requests.Session()
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization':f'Bearer {TOKEN}'
        }
    git_request = git_session.get(
        f'{api_url}/repos/{repo}/pulls/{pr}/files',
        headers=headers
        )
    return git_request.json()

def parse_patch_data(patch_data):
    '''Takes the patch data and returns a dictionary of files and the lines'''
    final_dict = {}
    for entry in patch_data:
        line_array = []
        sublist = []
        # We don't need removed files
        if entry['status'] != 'removed':
            # We can only operate on files with additions and a patch key
            # Some really long files don't have a patch key because github 
            # doesn't want to return the whole file and instead retuens a 
            # message in the PR that the file is too large to display
            if entry['additions'] != 0 and 'patch' in entry:
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

    api_url = os.getenv('INPUT_API_URL')
    TOKEN = os.getenv('INPUT_TOKEN')
    branch_name = os.getenv('INPUT_BRANCH')
    repo = os.getenv('INPUT_REPO')
    pr = os.getenv('INPUT_PR')
    github_output = os.getenv('GITHUB_OUTPUT')
    delimiter = os.getenv('INPUT_DELIMITER')
    file_filter = os.getenv('INPUT_FILE_FILTER')

    if not TOKEN:
        raise MissingToken('Missing GitHub token')

    if not api_url:
        raise MissingApiUrl('Missing Github api url')

    data = fetch_patch()
    added_line_data = parse_patch_data(data)
    added_lines = get_lines(added_line_data)
    
    filename_list = ''
    filter_added_lines = {}
        
    if file_filter:
        file_filter = set(file_filter.replace(' ','').split(','))
        for filename in added_lines:
            if os.path.splitext(filename)[1] in file_filter:
                filter_added_lines[filename] = added_lines[filename]
    else:
        filter_added_lines = added_lines
    
    for filename in filter_added_lines:
        filename_list += filename + delimiter

    with open(github_output, 'a', encoding='utf-8') as f:
        f.write(
            f'changed_lines={json.dumps(filter_added_lines)}\n' +
            f'changed_files={filename_list.strip()}\n'
            )
