from unittest import TestCase
from algo.search import search, format_filters


class TestFormatFilters(TestCase):
    def test_format_filters_location(self):
        filters = ["location:GLO"]
        assert format_filters(filters) == "location:GLO"

    def test_format_filters_multiple_locations(self):
        filters = ["location:GLO|ROW"]
        assert format_filters(filters) == "(location:GLO OR location:ROW)"

    def test_format_filters_two_filter_fields(self):
        filters = ["location:GLO", "name:cheese"]
        assert format_filters(filters) == "location:GLO AND name:cheese"

    def test_format_filters_multiple_fields_multiple_values(self):
        filters = ["location:GLO|ROW", "name:cheese|sheep"]
        assert (
            format_filters(filters)
            == "(location:GLO OR location:ROW) AND (name:cheese OR name:sheep)"
        )


class TestSearch(TestCase):
    def test_search_base(self):
        res = search("cat")
        assert "cat" in res["hits"][0]["name"]

    def test_default_page_num(self):
        res = search("cat")
        assert res["page"] == 0

    def test_custom_page_num(self):
        res = search("cat", page_num=2)
        assert res["page"] == 2

    def test_default_page_len(self):
        res = search("cat")
        assert len(res["hits"]) == 100

    def test_custom_page_len(self):
        res = search("cat", page_len=10)
        assert len(res["hits"]) == 10

    def test_default_fields(self):
        search_term = "nuclear"
        page_len = 1000
        res = search(search_term, page_len=page_len)
        assert res["nbHits"] < page_len  # this way we know we have all hits
        # check that matches are returned in fields other than just name
        assert not all(search_term in hit["name"] for hit in res["hits"])

    def test_custom_search_fields(self):
        search_term = "nuclear"
        page_len = 1000
        res = search(search_term, fields=["name"], page_num=page_len)
        assert res["nbHits"] < page_len  # this way we know we have all hits
        # check that matches all contain serach term in name field
        assert all(search_term in hit["name"] for hit in res["hits"])

    def test_location_filter(self):
        res_no_filter = search("cheese")
        res_with_filter = search("cheese", filters=["location:glo"])
        locations_without_filter = {hit["location"] for hit in res_no_filter["hits"]}
        locations_with_filter = {hit["location"] for hit in res_with_filter["hits"]}
        assert len(locations_without_filter) > len(locations_with_filter)
        assert locations_with_filter == {"GLO"}

    def test_multi_location_filter(self):
        res_no_filter = search("cheese")
        res_with_filter = search("cheese", filters=["location:GLO|ROW"])
        filter_locations = {"GLO", "RoW"}
        assert len({hit["location"] for hit in res_no_filter["hits"]}) > len(
            filter_locations
        )
        assert {hit["location"] for hit in res_with_filter["hits"]} == filter_locations
