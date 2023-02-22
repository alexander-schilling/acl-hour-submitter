import json
from pathlib import Path
import os.path
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

files_path = Path(__file__).parent.parent / 'files'

def json_from_file(file_name, file_extension='.json') -> dict:
    file_path = f"{files_path}/{file_name}{file_extension}"

    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    file.close()

    return data

def json_to_file(file_name, data, file_extension='.json'):
    file_path = f"{files_path}/{file_name}{file_extension}"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    file.close()

def print_json(data):
    print(json.dumps(data, indent=2))

def element_to_text(element) -> str:
    return element.get_attribute('textContent')

def parse_text(text, parse_type) -> int|float:
    text = text.replace(',', '')

    if parse_type == 'int':
        return int(text)
    elif parse_type == 'float':
        return float(text)

def alternate_click(driver, element):
    # actions = ActionChains(driver)
    # actions.move_to_element(element).click().perform()

    element.send_keys(Keys.ENTER)

