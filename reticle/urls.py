from collections.abc import Iterable
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse


def remove_ignored_request_uris(
    request_uris: Iterable[str],
    ignored_uri_substrings: Iterable[str],
) -> list[str]:
    ignored_substrings = tuple(ignored_uri_substrings)

    if not ignored_substrings:
        return list(request_uris)

    return [
        request_uri
        for request_uri in request_uris
        if not contains_ignored_substring(request_uri, ignored_substrings)
    ]


def contains_ignored_substring(
    request_uri: str,
    ignored_substrings: Iterable[str],
) -> bool:
    return any(substring in request_uri for substring in ignored_substrings)


def apply_query_param_overrides(
    request_uri: str,
    query_param_overrides: dict[str, str],
) -> str:
    modified_request_uri = request_uri

    for parameter_name, replacement_value in query_param_overrides.items():
        modified_request_uri = replace_query_param(
            modified_request_uri,
            parameter_name,
            replacement_value,
        )

    return modified_request_uri


def replace_query_param(
    request_uri: str,
    parameter_name: str,
    replacement_value: str,
) -> str:
    parsed_uri = urlparse(request_uri)
    query_params = parse_qs(parsed_uri.query)

    if parameter_name not in query_params:
        return request_uri

    query_params[parameter_name] = [replacement_value]
    updated_query_string = urlencode(query_params, doseq=True)

    return urlunparse(parsed_uri._replace(query=updated_query_string))


def build_replay_url(base_url: str, request_uri: str) -> str:
    return urljoin(base_url.rstrip("/") + "/", request_uri.lstrip("/"))
