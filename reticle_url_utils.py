from typing import List


def filter_uri_list(uri_list: List[str], block_list: List[str]) -> List[str]:
    """
    Filter the list of URIs to remove any that contain the specified substrings.

    Args:
        uri_list (List): List of URIs to filter.

    Returns:
        List[str]: Filtered list of URIs.
    """
    filtered_uri_list = []

    for uri in uri_list:
        if not any(substring in uri for substring in block_list):
            filtered_uri_list.append(uri)

    return filtered_uri_list


def modify_query_param(uri: str, param_name: str, new_value: str) -> str:
    """
    Modify the value of a query parameter in the URI if it exists.

    Args:
        uri (str): The URI to modify.
        param_name (str): The name of the query parameter to modify.
        new_value (str): The new value to set for the query parameter.

    Returns:
        str: The modified URI.
    """
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

    parsed_url = urlparse(uri)
    query_params = parse_qs(parsed_url.query)

    if param_name in query_params:
        query_params[param_name] = [new_value]

    new_query_string = urlencode(query_params, doseq=True)
    return urlunparse(parsed_url._replace(query=new_query_string))
