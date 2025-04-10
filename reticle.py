from selenium import webdriver
import web_traffic_replay
import reticle_arguments
import http_log_reader
import pathlib
import json


if __name__ == "__main__":

    print("Program starting")

    args = reticle_arguments.parse_arguments()

    site = args.site

    screenshot_save_path = args.output_path
    screenshot_save_path = pathlib.Path(screenshot_save_path).resolve()

    url_list = http_log_reader.process_log_file("./samples/apache2.log")

    driver = webdriver.Chrome()

    driver.get(site)

    cookies = None

    with open("cookies.json", "r") as f:
        cookies = json.load(f)

    for cookie in cookies:
        cookie.pop("sameSite", None)
        cookie.pop("expiry", None)
        driver.add_cookie(cookie)

    driver.refresh()

    for count, url in enumerate(url_list):

        web_traffic_replay.replay_url(f"{site}{url}", driver, screenshot_save_path=f"{screenshot_save_path}/screenshot_{count}.png")
