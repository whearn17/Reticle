import argparse

if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Replay web traffic from HTTP access logs.")

    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="Base URL of the website to replay logs for.",
    )

    parser.add_argument(
        "-l",
        "--log",
        type=str,
        required=True,
        help="Path to the HTTP access log file to replay.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output file path to save the screenshot (e.g., ./output/screenshot.png).",
    )

    parser.add_argument(
        "--ignore",
        nargs="+",
        default=[],
        help="List of substrings to block if found in the request URI.",
    )

    parser.add_argument(
        "--modify-params",
        nargs="+",
        metavar="KEY=VALUE",
        help="Modify one or more query parameter values in the URL if they exist. Example: --modify-param session_id=12345 token=xyz123",
    )

    return parser.parse_args()
