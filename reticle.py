from selenium import webdriver
import web_traffic_replay
import reticle_arguments
import reticle_url_utils
import http_log_reader
import pathlib
import json
import time


if __name__ == "__main__":

    print("Program starting")

    args = reticle_arguments.parse_arguments()

    site = args.url

    screenshot_save_path = args.output
    screenshot_save_path = pathlib.Path(screenshot_save_path).resolve()

    log_file_path = args.log
    log_file_path = pathlib.Path(log_file_path).resolve()

    uri_list = http_log_reader.process_log_file(log_file_path)

    ignore_list = args.ignore

    if ignore_list:
        uri_list = reticle_url_utils.filter_uri_list(uri_list, ignore_list)

    modify_params = args.modify_params

    if modify_params:
        for param in modify_params:
            key, value = param.split("=")
            uri_list = [reticle_url_utils.modify_query_param(uri, key, value) for uri in uri_list]

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

    for count, uri in enumerate(uri_list):

        full_url = f"{site}{uri}"

        web_traffic_replay.replay_url(full_url, driver, screenshot_save_path=f"{screenshot_save_path}/screenshot_{count}.png")

        time.sleep(3)
