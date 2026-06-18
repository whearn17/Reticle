import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class ReticleOptions:
    base_url: str
    access_log_path: Path
    screenshot_directory: Path
    cookie_file_path: Path
    ignored_uri_substrings: list[str]
    query_param_overrides: dict[str, str]
    replay_delay_seconds: float


def parse_cli_args(argv: Sequence[str] | None = None) -> ReticleOptions:
    parser = argparse.ArgumentParser(
        description="Replay HTTP access log requests in a browser."
    )

    parser.add_argument(
        "-u",
        "--url",
        dest="base_url",
        required=True,
        help="Base URL of the website to replay logs against.",
    )

    parser.add_argument(
        "-l",
        "--log",
        dest="access_log_path",
        type=Path,
        required=True,
        help="Path to the HTTP access log file to replay.",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="screenshot_directory",
        type=Path,
        required=True,
        help="Directory where replay screenshots will be saved.",
    )

    parser.add_argument(
        "--cookies",
        dest="cookie_file_path",
        type=Path,
        default=Path("cookies.json"),
        help="Path to a Selenium-compatible JSON cookie file.",
    )

    parser.add_argument(
        "--ignore",
        dest="ignored_uri_substrings",
        nargs="+",
        default=[],
        help="Drop any request URI containing one of these substrings.",
    )

    parser.add_argument(
        "--modify-params",
        dest="query_param_overrides",
        nargs="+",
        metavar="KEY=VALUE",
        type=_parse_query_param_override,
        default=[],
        help="Replace query parameter values when those parameters already exist.",
    )

    parser.add_argument(
        "--delay",
        dest="replay_delay_seconds",
        type=float,
        default=3.0,
        help="Seconds to wait between replayed requests.",
    )

    parsed_args = parser.parse_args(argv)

    return ReticleOptions(
        base_url=parsed_args.base_url,
        access_log_path=parsed_args.access_log_path,
        screenshot_directory=parsed_args.screenshot_directory,
        cookie_file_path=parsed_args.cookie_file_path,
        ignored_uri_substrings=parsed_args.ignored_uri_substrings,
        query_param_overrides=dict(parsed_args.query_param_overrides),
        replay_delay_seconds=parsed_args.replay_delay_seconds,
    )


def _parse_query_param_override(raw_override: str) -> tuple[str, str]:
    if "=" not in raw_override:
        raise argparse.ArgumentTypeError(
            "Query parameter overrides must use KEY=VALUE format."
        )

    parameter_name, replacement_value = raw_override.split("=", maxsplit=1)

    if not parameter_name:
        raise argparse.ArgumentTypeError("Query parameter names cannot be empty.")

    return parameter_name, replacement_value
