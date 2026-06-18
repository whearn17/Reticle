import tempfile
import unittest
from pathlib import Path

from reticle.log_reader import (
    detect_access_log_format,
    extract_apache_request_uris,
    read_request_uris,
)


APACHE_ACCESS_LOG_LINE = (
    '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] '
    '"GET /admin?page=1 HTTP/1.1" 200 2326 "-" "Mozilla/5.0"'
)


class LogReaderTests(unittest.TestCase):
    def test_extracts_request_uris_from_apache_access_logs(self) -> None:
        request_uris = extract_apache_request_uris([APACHE_ACCESS_LOG_LINE])

        self.assertEqual(request_uris, ["/admin?page=1"])

    def test_reads_request_uris_after_detecting_log_format(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            access_log_path = Path(temporary_directory) / "access.log"
            access_log_path.write_text(APACHE_ACCESS_LOG_LINE, encoding="utf-8")

            self.assertEqual(detect_access_log_format(access_log_path), "apache_combined")
            self.assertEqual(read_request_uris(access_log_path), ["/admin?page=1"])


if __name__ == "__main__":
    unittest.main()
