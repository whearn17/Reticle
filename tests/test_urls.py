import unittest

from reticle.urls import (
    apply_query_param_overrides,
    build_replay_url,
    remove_ignored_request_uris,
    replace_query_param,
)


class UrlTests(unittest.TestCase):
    def test_removes_request_uris_with_ignored_substrings(self) -> None:
        request_uris = ["/admin", "/static/app.js", "/login"]

        filtered_request_uris = remove_ignored_request_uris(request_uris, ["static"])

        self.assertEqual(filtered_request_uris, ["/admin", "/login"])

    def test_replaces_existing_query_parameter(self) -> None:
        updated_request_uri = replace_query_param(
            "/admin?page=1&token=old",
            "token",
            "new",
        )

        self.assertEqual(updated_request_uri, "/admin?page=1&token=new")

    def test_leaves_missing_query_parameter_unchanged(self) -> None:
        updated_request_uri = replace_query_param(
            "/admin?page=1",
            "token",
            "new",
        )

        self.assertEqual(updated_request_uri, "/admin?page=1")

    def test_applies_multiple_query_parameter_overrides(self) -> None:
        updated_request_uri = apply_query_param_overrides(
            "/admin?page=1&token=old",
            {"page": "2", "token": "new"},
        )

        self.assertEqual(updated_request_uri, "/admin?page=2&token=new")

    def test_builds_replay_url_from_base_url_and_request_uri(self) -> None:
        replay_url = build_replay_url("https://example.test", "/admin")

        self.assertEqual(replay_url, "https://example.test/admin")


if __name__ == "__main__":
    unittest.main()
