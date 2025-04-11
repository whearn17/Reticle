from abc import abstractmethod
from typing import List
import re

if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")


LOG_TYPE_MAP = {
    "APACHE2": [
        r"^(?P<ip>\d+\.\d+\.\d+\.\d+)\s+(?P<ident>-|[^ ]+)\s+(?P<user>-|[^ ]+)\s+\[(?P<date>[^\]]+|-)\]\s+(?P<request>\"(?:(?P<method>\S+)\s+(?P<uri>/[^\"\s]+)\s+HTTP/(?P<http_version>[\d.]+)|-)\")\s+(?P<status>\d{3}|-)\s+(?P<size>\d+|-)\s+(?P<referer>\"(?:[^\"]*|-)\")\s+(?P<agent>\"(?:[^\"]*|-)\")$"
    ]
}


class _HTTPAccessLogProcessor:
    """
    Abstract base class for HTTP access log processors.
    """

    @abstractmethod
    def get_url_list(self, logs: List) -> List:
        """
        Extracts URLs from log entries.

        :param logs: List of log entries.
        :return: List of URLs.
        """
        pass


class _Apache2LogProcessor(_HTTPAccessLogProcessor):
    """
    Processor for Apache2 HTTP access logs.
    """

    def get_uri_list(self, logs: List) -> List:
        """
        Extracts URLs from Apache2 log entries.

        :param logs: List of log entries.
        :return: List of URLs.
        """

        urls = []

        for log in logs:

            match = re.match(
                r"^(?P<ip>\d+\.\d+\.\d+\.\d+)\s+(?P<ident>-|[^ ]+)\s+(?P<user>-|[^ ]+)\s+\[(?P<date>[^\]]+|-)\]\s+(?P<request>\"(?:(?P<method>\S+)\s+(?P<uri>/[^\"\s]+)\s+HTTP/(?P<http_version>[\d.]+)|-)\")\s+(?P<status>\d{3}|-)\s+(?P<size>\d+|-)\s+(?P<referer>\"(?:[^\"]*|-)\")\s+(?P<agent>\"(?:[^\"]*|-)\")$", log)

            if match:
                urls.append(match.group('uri'))

        return urls


def _get_log_processor(log_type: str) -> _HTTPAccessLogProcessor:
    """
    Factory method to return the correct log processor based on log type.

    :param log_type: Type of HTTP access log.
    :return: Log processor instance.
    """

    if log_type == "APACHE2":
        return _Apache2LogProcessor()
    else:
        raise ValueError(f"Unsupported log type: {log_type}")


def _get_http_access_log_type(file_path: str) -> str:
    """
    Determines the type of HTTP access log based on regex of common formats.

    :param file_path: Path to the log file.
    :return: Type of HTTP access log.
    """

    first_line = None

    with open(file_path, 'r') as log_file:

        first_line = log_file.readline().strip()

        for log_type, regex_list in LOG_TYPE_MAP.items():
            for regex in regex_list:
                if re.match(regex, first_line):
                    return log_type


def process_log_file(file_path: str) -> List:
    """
    Reads a log file and returns a list of log entries.

    :param file_path: Path to the log file.
    :return: List of log entries.
    """

    logs = []

    log_type = _get_http_access_log_type(file_path)

    log_processor: _HTTPAccessLogProcessor = _get_log_processor(log_type)

    with open(file_path, 'r') as log_file:

        for line in log_file:

            line = line.strip()

            if line:

                logs.append(line)

    uri_list = log_processor.get_uri_list(logs)

    return uri_list
