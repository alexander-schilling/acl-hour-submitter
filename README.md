# Hour Submitter

## Requirements

1. [Python 3](https://www.python.org/downloads/)
2. [Google Chrome](https://www.google.com/chrome/) and [Chromedriver](https://chromedriver.chromium.org/downloads) (must be compatible versions, if Chrome is updated, Chromedriver must be updated as well replacing `chromedriver.exe` in `drivers` folder)

## How to use

1. Run `pip install -r requirements.txt`
2. Edit `files/activity_data.json` with your activity data
   - `username` is your login username
   - `password` is your login password
   - `start_date` `DD/MM/YYYY` is the first date you want to submit hours for
   - `end_date` `DD/MM/YYYY` is the last date you want to submit hours for
   - `role` is labeled as `Rol en esta tarea`, must be exactly the same as the role in the dropdown
   - `project` is labeled as `Nº Proy / Cco`, must be a valid project number
   - `quotation` is labeled as `Nº Cotización`, must be a valid quotation number
   - `task` is labeled as `Nº Tarea Carta Gantt`, must be a valid task
   - `hours` is the number of hours per activity
   - `minutes` is the number of minutes per activity
   - `activity` is labeled as `Tipo Actividad`, must be exactly the same as the activity in the dropdown
   - `description` is labeled as `Descripción Tarea`
3. Run `python3 main.py`
   Optional arguments:
   - `--headless` to run in headless mode
   - `--height` to set the height of the browser window
   - `--width` to set the width of the browser window
4. Profit

## Development utilities

- [Selenium Docs](https://selenium-python.readthedocs.io/)
- [Installation](https://selenium-python.readthedocs.io/installation.html)
- [Drivers](https://selenium-python.readthedocs.io/installation.html#drivers) (Chromedriver for Win32 is included in the drivers folder)
