import re
import json
import requests
from bs4 import BeautifulSoup

json_file_str = 'rules.json'
eslit_doc_url = 'https://eslint.org/docs/rules'

def code_wrapper(code, flag):
    return f'examples of {flag} code for this rule:\n\n```javascript\n{code}```'

def gethtml(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

blocks = []
with open(json_file_str, 'r') as json_file:
    rules = json.load(json_file)['rules']
    for key in rules.keys():
        url = f'{eslit_doc_url}/{key}'
        soup = gethtml(url)
        title = f'### {key}'
        codes = [title]
        matches_per_rule_counter = 0
        print(title)
        for element in soup.find_all('pre'):
            lines = [line for line in element.strings]
            if any(re.search(key, line) for line in lines) and matches_per_rule_counter < 2:
                flag = "incorrect" if matches_per_rule_counter == 0 else "correct"
                code = code_wrapper(''.join(lines), flag)
                codes.append(code)
                matches_per_rule_counter += 1
                print(code)
        blocks.append('\n\n'.join(codes))
        print('======================================')

with open('README.md', 'w') as readme_file:
    text = '\n\n'.join(blocks)
    readme_file.write(text)
    print('\n\n FILE CREATED!!')
