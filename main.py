import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from drivers.chrome import get_chrome_driver
from tools.utils import json_from_file, element_to_text
from pandas import date_range, to_datetime

# URL
main_url = "https://control.aclspa.com/ContProy/servlet/hrgdm00a"

activity_table_id = 1
activity_table_map = {
    "project": 2,
    "quotation": 3,
    "task": 4,
    "hours": 6,
    "minutes": 7,
    "description": 8,
    "activity": 9,
    "role": 12
}
activity_form_map = {
    "role": "//select[@name='W0006_ROLCOD04L']",
    "project": "//input[@name='W0006_PROYNUM04L']",
    "quotation": "//input[@name='W0006_COTINUM04L']",
    "task": "//input[@name='W0006_CGANNUM04L']",
    "hours": "//input[@name='W0006_CANHOR04L']",
    "minutes": "//input[@name='W0006_CANMIN04L']",
    "activity": "//select[@name='W0006_TIPACT04L']",
    "description": "//textarea[@name='W0006_OBSACT04L']",
}

def get_activity_data():
    activity_data = json_from_file("activity_data")

    return activity_data

def login(driver, activity_data):
    username_input = driver.find_element(By.ID, "W0006_COD_FUN")
    username_input.clear()
    username_input.send_keys(activity_data.get("username"))

    password_input = driver.find_element(By.ID, "W0006_CLAFUN_11")
    password_input.clear()
    password_input.send_keys(activity_data.get("password"))

    login_button = driver.find_element(By.ID, "W0006IMAGE1").find_element(By.XPATH, "./..")
    login_button.click()

    time.sleep(3)

    try:
        session_info = element_to_text(driver.find_element(By.ID, "W0004TXTDIAS"))
        print('Logged in:', session_info)
    except:
        raise Exception("Login failed")

def go_to_register_activity(driver):
    operations_button = driver.find_element(By.ID, "W0006MNUGESOPE").find_element(By.XPATH, "./..")
    operations_button.click()

    time.sleep(1)

    register_activity_button = driver.find_element(By.ID, "W0006IMGOPCREGISTROACTIVIDADES").find_element(By.XPATH, "./..")
    register_activity_button.click()

    time.sleep(3)

    current_path = element_to_text(driver.find_element(By.ID, "span_W0006_TITULO"))

    print("Currently on", current_path)

def get_dates_array(activity_data):
    start_date = to_datetime(activity_data.get("start_date"), format="%d/%m/%Y", errors="coerce")
    end_date = to_datetime(activity_data.get("end_date"), format="%d/%m/%Y", errors="coerce")
    dates = date_range(start=start_date, end=end_date)

    return dates.strftime("%d/%m/%Y").tolist()

def go_to_date(driver, date):
    date_input = driver.find_element(By.ID, "W0006_FECREG04")
    # Didn't work with clear() and send_keys()
    driver.execute_script(f"arguments[0].value = '{date}';", date_input)

    search_button = driver.find_element(By.ID, "W0006IMAGE4").find_element(By.XPATH, "./..")
    search_button.click()

    time.sleep(3)

    date_input = driver.find_element(By.ID, "W0006_FECREG04")
    current_date = element_to_text(driver.find_element(By.ID, "span_W0006_NOMDIA"))
    print('Now in', current_date, date_input.get_attribute("value"))

def does_activity_exists(activities_body, activity_data):
    for activity_row in activities_body:
        is_activity_the_same = True

        for key, value in activity_table_map.items():
            if key == "description":
                continue

            activity_data_value = activity_data[key]
            current_value = element_to_text(activity_row.find_element(By.XPATH, f"./td[{value}]")).strip()

            if activity_data_value != current_value:
                is_activity_the_same = False
                break

        if is_activity_the_same:
            activity_id = activity_row.find_element(By.XPATH, f"./td[{activity_table_id}]")
            return True, element_to_text(activity_id).strip()

    return False, None

def go_to_form(driver):
    new_activity_button = driver.find_element(By.ID, "W0006IMAGE2").find_element(By.XPATH, "./..")
    new_activity_button.click()

    time.sleep(3)

    activity_day = driver.find_element(By.XPATH, "//input[@name='W0006_NOMDIA04L']").get_attribute("value")
    activity_date = driver.find_element(By.XPATH, "//input[@name='W0006_FECREG04L']").get_attribute("value")

    print(f"Now in form for {activity_day} {activity_date}")

def print_activity_form(driver):
    for key, value in activity_form_map.items():
        input_element = driver.find_element(By.XPATH, value)
        print(f"{key}: {input_element.get_attribute('value')}")

def fill_activity_form(driver, activity_data):
    for key, value in activity_form_map.items():
        if "select" in value:
            select = Select(driver.find_element(By.XPATH, value))
            select.select_by_visible_text(activity_data.get(key))
        else:
            input_element = driver.find_element(By.XPATH, value)
            input_element.clear()
            input_element.send_keys(activity_data.get(key))

def submit_activity_form(driver):
    submit_button = driver.find_element(By.ID, "W0006BTNGUARDAR").find_element(By.XPATH, "./..")
    submit_button.click()

    time.sleep(1)

    confirm_button = driver.find_element(By.ID, "W0006BTNCONFGUAR").find_element(By.XPATH, "./..")
    confirm_button.click()

    time.sleep(3)

def verify_activity(driver, activity_data):
    activities_table = driver.find_element(By.ID, "W0006GRID1")

    activities_rows = activities_table.find_elements(By.XPATH, "./tbody/tr")
    activities_body = activities_rows[1:]

    activity_exists, activity_id = does_activity_exists(activities_body, activity_data)

    if not activity_exists:
        raise Exception(f"Couldn't create activity")

    print(f"Activity created successfully with id {activity_id}")

def submit_activity(driver, activity_data):
    activities_table = driver.find_element(By.ID, "W0006GRID1")

    activities_rows = activities_table.find_elements(By.XPATH, "./tbody/tr")
    activities_body = activities_rows[1:]

    print(f"Found {len(activities_body)} activities")

    activity_exists, activity_id = does_activity_exists(activities_body, activity_data)

    if not activity_exists:
        print("Creating new activity")
        go_to_form(driver)
        fill_activity_form(driver, activity_data)
        submit_activity_form(driver)
        verify_activity(driver, activity_data)
    else:
        print(f"Activity already exists with id {activity_id}")

def submit_activities(driver, dates, activity_data):
    for date in dates:
        try:
            go_to_date(driver, date)
            submit_activity(driver, activity_data)
        except Exception as exception:
            print(f"Skipping date {date} because of error:", get_errors(driver, exception))

def get_errors(driver, exception):
    try:
        error = driver.find_element(By.CLASS_NAME, "ErrorViewer")
        return f"ERROR: {element_to_text(error)}"
    except:
        return f"ERROR DESCONOCIDO: {exception}"

def main():
    driver = get_chrome_driver()
    try:
        activity_data = get_activity_data()
        dates = get_dates_array(activity_data)
        print('Submitting for dates:', dates)

        driver.get(main_url)

        login(driver, activity_data)
        go_to_register_activity(driver)
        submit_activities(driver, dates, activity_data)
    except Exception as exception:
        print(get_errors(driver, exception))

    driver.close()

main()
