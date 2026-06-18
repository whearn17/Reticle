from __future__ import annotations

import time
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

from reticle.urls import build_replay_url


def replay_request_uris(
    driver: WebDriver,
    base_url: str,
    request_uris: Iterable[str],
    screenshot_directory: Path,
    delay_seconds: float,
) -> None:
    for request_index, request_uri in enumerate(request_uris):
        replay_url = build_replay_url(base_url, request_uri)
        screenshot_path = screenshot_directory / f"screenshot_{request_index:04}.png"

        capture_replay_screenshot(driver, replay_url, screenshot_path)

        if delay_seconds > 0:
            time.sleep(delay_seconds)


def capture_replay_screenshot(
    driver: WebDriver,
    replay_url: str,
    screenshot_path: Path,
) -> None:
    driver.get(replay_url)
    driver.save_screenshot(str(screenshot_path))
