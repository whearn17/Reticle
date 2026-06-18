from collections.abc import Sequence

from reticle.cli import ReticleOptions, parse_cli_args
from reticle.cookies import add_cookies_to_browser, load_browser_cookies
from reticle.log_reader import read_request_uris
from reticle.replay import replay_request_uris
from reticle.urls import apply_query_param_overrides, remove_ignored_request_uris


def main(argv: Sequence[str] | None = None) -> int:
    options = parse_cli_args(argv)
    replay_access_log(options)
    return 0


def replay_access_log(options: ReticleOptions) -> None:
    from selenium import webdriver

    access_log_path = options.access_log_path.resolve()
    screenshot_directory = options.screenshot_directory.resolve()
    cookie_file_path = options.cookie_file_path.resolve()

    screenshot_directory.mkdir(parents=True, exist_ok=True)

    request_uris = read_request_uris(access_log_path)
    request_uris = prepare_request_uris(
        request_uris,
        ignored_uri_substrings=options.ignored_uri_substrings,
        query_param_overrides=options.query_param_overrides,
    )

    print(f"Replaying {len(request_uris)} request(s) from {access_log_path}")

    driver = webdriver.Chrome()

    try:
        driver.get(options.base_url)
        browser_cookies = load_browser_cookies(cookie_file_path)
        add_cookies_to_browser(driver, browser_cookies)
        driver.refresh()

        replay_request_uris(
            driver=driver,
            base_url=options.base_url,
            request_uris=request_uris,
            screenshot_directory=screenshot_directory,
            delay_seconds=options.replay_delay_seconds,
        )
    finally:
        driver.quit()


def prepare_request_uris(
    request_uris: list[str],
    ignored_uri_substrings: list[str],
    query_param_overrides: dict[str, str],
) -> list[str]:
    prepared_request_uris = remove_ignored_request_uris(
        request_uris,
        ignored_uri_substrings,
    )

    return [
        apply_query_param_overrides(request_uri, query_param_overrides)
        for request_uri in prepared_request_uris
    ]
