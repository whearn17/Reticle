import re
from collections.abc import Iterable
from pathlib import Path


APACHE_COMBINED_LOG_PATTERN = re.compile(
    r"^(?P<ip>\d+\.\d+\.\d+\.\d+)\s+"
    r"(?P<ident>-|[^ ]+)\s+"
    r"(?P<user>-|[^ ]+)\s+"
    r"\[(?P<date>[^\]]+|-)\]\s+"
    r"(?P<request>\"(?:(?P<method>\S+)\s+"
    r"(?P<uri>/[^\"\s]+)\s+"
    r"HTTP/(?P<http_version>[\d.]+)|-)\")\s+"
    r"(?P<status>\d{3}|-)\s+"
    r"(?P<size>\d+|-)\s+"
    r"(?P<referer>\"(?:[^\"]*|-)\")\s+"
    r"(?P<agent>\"(?:[^\"]*|-)\")$"
)

LOG_FORMAT_PATTERNS = {
    "apache_combined": (APACHE_COMBINED_LOG_PATTERN,),
}


class UnsupportedAccessLogFormatError(ValueError):
    pass


def read_request_uris(access_log_path: Path) -> list[str]:
    log_format = detect_access_log_format(access_log_path)
    log_lines = read_non_empty_lines(access_log_path)

    if log_format == "apache_combined":
        return extract_apache_request_uris(log_lines)

    raise UnsupportedAccessLogFormatError(f"Unsupported log format: {log_format}")


def detect_access_log_format(access_log_path: Path) -> str:
    first_log_line = read_first_non_empty_line(access_log_path)

    for log_format, patterns in LOG_FORMAT_PATTERNS.items():
        if any(pattern.match(first_log_line) for pattern in patterns):
            return log_format

    raise UnsupportedAccessLogFormatError(
        f"Could not detect the access log format for {access_log_path}."
    )


def read_first_non_empty_line(access_log_path: Path) -> str:
    with access_log_path.open("r", encoding="utf-8") as access_log:
        for raw_line in access_log:
            log_line = raw_line.strip()

            if log_line:
                return log_line

    raise ValueError(f"{access_log_path} does not contain any log entries.")


def read_non_empty_lines(access_log_path: Path) -> list[str]:
    with access_log_path.open("r", encoding="utf-8") as access_log:
        return [line.strip() for line in access_log if line.strip()]


def extract_apache_request_uris(log_lines: Iterable[str]) -> list[str]:
    request_uris: list[str] = []

    for log_line in log_lines:
        match = APACHE_COMBINED_LOG_PATTERN.match(log_line)

        if match:
            request_uris.append(match.group("uri"))

    return request_uris
