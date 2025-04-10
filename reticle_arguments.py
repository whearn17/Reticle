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
        "-h",
        "--hostname",
        type=str,
        required=True,
        help="The base website to replay logs for.",
    )

    parser.add_argument(
        "-s",
        "--screenshot",
        type=str,
        required=True,
        help="Path to save the screenshot.",
    )

    return parser.parse_args()
