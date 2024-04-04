from typing import List, Dict
from algo.setup_algolia import get_algolia_index


def format_filters(filters):
    formatted_filters = []
    for filter in filters:
        field, values = filter.split(":")
        if "|" in values:
            values = values.split("|")
            formatted_values = " OR ".join([f"{field}:{value}" for value in values])
            formatted_filters.append(f"({formatted_values})")
        else:
            formatted_filters.append(f"{field}:{values}")
    return " AND ".join(formatted_filters)


def search(
    search_string: str | None = None,
    filters: List[str] | None = None,
    fields: List[str] | None = None,
    page_num=0,
    page_len=100,
    # sort_by_column: str | None = None,
    # sort_reverse: bool = False,
    # fuzz_value=0,
):
    """Search for activities."""
    index = get_algolia_index()
    request_options: Dict[str, int | List[str] | str] = {
        "hitsPerPage": page_len,
        "page": page_num,
    }
    if fields:
        request_options["restrictSearchableAttributes"] = fields
    if filters:
        request_options["filters"] = f"{format_filters(filters)}"
    return index.search(search_string, request_options)
