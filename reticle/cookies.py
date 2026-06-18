from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


Cookie = dict[str, Any]


def load_browser_cookies(cookie_file_path: Path) -> list[Cookie]:
    with cookie_file_path.open("r", encoding="utf-8") as cookie_file:
        cookies = json.load(cookie_file)

    if not isinstance(cookies, list):
        raise ValueError(f"Expected a list of cookies in {cookie_file_path}.")

    return cookies


def add_cookies_to_browser(driver: WebDriver, cookies: Iterable[Cookie]) -> None:
    for cookie in cookies:
        driver.add_cookie(_prepare_cookie_for_selenium(cookie))


def _prepare_cookie_for_selenium(cookie: Cookie) -> Cookie:
    selenium_cookie = cookie.copy()
    selenium_cookie.pop("sameSite", None)
    selenium_cookie.pop("expiry", None)
    return selenium_cookie
