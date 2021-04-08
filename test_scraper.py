# Import necessary packages
import pytest
import pandas as pd
from bs4 import BeautifulSoup

# Import scraper code
import page_scraper

# import site_scraper
# # #     href_to_path

# TEST_TD = BeautifulSoup("<td>Jackson\xa0\n</td>", "lxml").find("td")

CLEAN_TD_CASES = [
    ("\xa0", "<td>Jackson\xa0\n</td>"),
    ("\n", "<td>Jackson\xa0\n</td>"),
    ("\xa0", "<td>\xa0\n</td>"),
    ("\n", "<td>\xa0\n</td>"),
    ("\xa0", "<td>\xa0Jack\n</td>"),
    ("\n", "<td>J\xa0Jack\n</td>"),
]

@pytest.mark.parametrize("dirt, td_element_string", CLEAN_TD_CASES)
def test_clean_td(dirt, td_element_string):
    td_element = BeautifulSoup(td_element_string, "lxml").find("td")
    assert dirt not in td_element

TEST_SOUP = page_scraper.get_soup("test_page.html")
TEST_TABLES = TEST_SOUP.find_all("table")
TABLE_TO_DICT_CASES = [
    (TEST_TABLES[0], {"Eve":["Jackson"], "Jill":["Smith"]}),
    (TEST_TABLES[1],\
        {
        "Data1":["Value1"],
        "Data2":["Value2"],
        "Data3":["Value3"],
        "Data4":["Value4"]
        })
]

@pytest.mark.parametrize("table, dict", TABLE_TO_DICT_CASES)
def test_table_to_dictionary(table, dict):
    assert page_scraper.accident_table_to_dictionary(table) == dict

GET_HEADERS_CASES = [
    ({'col1': [1, 2], 'col2': [3, 4]}, "col1,col2"),
    ({'col1': [1, 2, 5, 6, 7], 'col2': [3, 4, 5, 6, 7]}, "col1,col2"),
    ({'col1': [1], 'col2': [1], 'col3': [1], 'col4': [1], 'col5': [1], 'col6': [1]},\
        "col1,col2,col3,col4,col5,col6")
]

@pytest.mark.parametrize("df_dict, csv_header_string", GET_HEADERS_CASES)
def test_get_headers(df_dict, csv_header_string):
    df = pd.DataFrame(data=df_dict)

    assert page_scraper.get_headers(df) == csv_header_string

GET_FIRST_ROW_CASES = [
    ({'col1': ["1", "2"], 'col2': ["3", "4"]}, "1,3"),
    ({'col1': ["4", "2", "5", "6", "7"],\
        'col2': ["6", "4", "5", "6", "7"]},\
        "4,6"),
    ({'col1': ["1"], 'col2': ["1"], 'col3': ["1"],\
        'col4': ["1"], 'col5': ["1"], 'col6': ["1"]},\
        "1,1,1,1,1,1"),
    ({'col1': ["This"], 'col2': ["is"], 'col3': ["the"], 'col4': ["first"],\
        'col5': ["row"], 'col6': ["!"]},\
        "This,is,the,first,row,!")
]

@pytest.mark.parametrize("df_dict, csv_row_string", GET_FIRST_ROW_CASES)
def test_get_first_row(df_dict, csv_row_string):
    df = pd.DataFrame(data=df_dict)

    assert page_scraper.get_first_row(df) == csv_row_string

HREF_TO_PATH_CASES = [
    ("squid/ward.txt", "sponge.bob", "squid/sponge.bob"),
    ("../wget_planecrashinfo/database.htm", "1922/1922.htm",\
    "../wget_planecrashinfo/1922/1922.htm"),
    ("../wget_planecrashinfo/database.htm", "1988/1988.htm",\
    "../wget_planecrashinfo/1988/1988.htm"),
    ("../wget_planecrashinfo/1922/1922.htm", "1922-7.htm",\
    "../wget_planecrashinfo/1922/1922-7.htm"),
    ("../wget_planecrashinfo/1963/1963.htm", "1963-15.htm",\
    "../wget_planecrashinfo/1963/1963-15.htm"),
]

@pytest.mark.parametrize("current_path, href_path, resultant_path",\
    HREF_TO_PATH_CASES)

def test_href_to_path(current_path, href_path, resultant_path):
    assert page_scraper.href_to_path(current_path, href_path) == resultant_path