from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from argparse import ArgumentParser
from os import path

file_path = path.dirname(path.abspath(__file__))

def get_chrome_options(args):
	"""
		Sets chrome options for Selenium.
		Chrome options for headless browser is enabled.
	"""

	chrome_options = Options()
	if args.headless:
		chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument(f"--window-size={args.width}x{args.height}")
	chrome_prefs = {}
	chrome_options.experimental_options["prefs"] = chrome_prefs
	chrome_prefs["profile.default_content_settings"] = {"images": 2}

	return chrome_options

def get_chrome_driver():
	"""
		Returns a Chrome driver.
	"""

	parser = ArgumentParser()
	parser.add_argument("--headless", action="store_true", help="Run headless")
	parser.add_argument("--width", type=int, default=1024, help="Browser width")
	parser.add_argument("--height", type=int, default=768, help="Browser height")
	args = parser.parse_args()

	chrome_options = get_chrome_options(args)
	chromedriver_path = f"{file_path}/chromedriver"
	driver = Chrome(executable_path=chromedriver_path, options=chrome_options)
	driver.set_window_size(args.width, args.height)

	return driver
