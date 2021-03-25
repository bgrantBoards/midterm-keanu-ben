# Import necessary packages
from bs4 import BeautifulSoup
import pandas as pd
import re
# import string

def get_soup(file_path):
    """Generates a BeautifulSoup object from a locally stored html page located
    at file_path

    Args:
        file_path (string): location of the html file on your machine

    Returns:
        BeautifulSoup object: created from local html file
    """ 
    with open(file_path, encoding = "ISO-8859-1") as f:
        contents = f.read()

    # raw html data
    return BeautifulSoup(contents, 'lxml')

def clean_td(td):
    """Return the cleaned up text from an HTML table element.

    Args:
        td (bs4.element.Tag): an HTML td element.
    
    Returns:
        (string) cleaned text from the td element.
    """
    # row_item.text removes the tags from the entries
    dirty_text = td.text

    # the following regex is to remove \xa0 and \n and comma from row_item.text
    # xa0 encodes the flag, \n is the newline and comma separates thousands in
    # numbers
    clean_text = re.sub("(\xa0)|(\n)|,","", dirty_text)

    return clean_text

def accident_table_to_dictionary(table):
    """
    Scrapes an HTML table of accident data and returns the data in dictionary
    form.

    Args:
        table (bs4.element.Tag): accident data in the form of an HTML table
        element.
    
    Returns:
        (dictionary): the data in dict form.
    """
    body = table.find_all("tr")

    # get the body part of the table, as opposed to the header part
    body_rows = body[1:]

    accident_data = {}

    for row_num in range(len(body_rows)): # A row at a time
        # get td elements from row:
        row_items = body_rows[row_num].find_all("td")

        heading = clean_td(row_items[0]) # describes type of datapoint
        value = clean_td(row_items[1])   # the datapoint
        accident_data[heading] = [value]

    return accident_data

def dataframe_from_accident_page(file_path):
    """
    Scrapes a locally stored accident details page from planecrashinfo.com and
    returns the data in a Panda DataFrame.

    Args:
        file_path (string): location of the accident page to scrape.
    """
    soup = get_soup(file_path)

    # generate HTML content for the first table on the page
    table = soup.find("table")

    # scrape the data and put it into a dictionary
    accident_data = accident_table_to_dictionary(table)

    # convert the dictionary to Pandas DataFrame
    return pd.DataFrame(data=accident_data)

page_path = "wget_planecrashinfo/1924/1924-4.htm"

# print(dataframe_from_accident_page(page_path))
print(dataframe_from_accident_page(page_path))