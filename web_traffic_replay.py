from selenium import webdriver

if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")


def replay_url(url: str, driver: webdriver.Chrome, screenshot_save_path: str) -> None:
    """
    Replay a single URL using the provided WebDriver instance.

    Args:
        url (str): The URL to replay.
        driver (webdriver.Chrome): The WebDriver instance to use for replaying the URL.
    """

    driver.get(url)

    driver.save_screenshot(screenshot_save_path)
