# Import necessary packages
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
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

def get_headers(df):
    """Returns csv formatted string of headers from Pandas dataframe df.

    Args:
        df (Pandas DataFrame): dataframe
    
    Returns:
        (string): csv formatted string of headers.
    """
    header_list = df.columns.values
    return ",".join(header_list)

def get_first_row(df):
    """Returns csv formatted string of the first row from a Pandas dataframe df.

    Args:
        df (Pandas DataFrame): dataframe
    
    Returns:
        (string): csv formatted string of first row's data.
    """
    row_list = df.iloc[0].values
    return ",".join(row_list)

def write_to_file(df, file_path):
    """
    Writes the information from a Pandas DataFrame to a csv data file.
    All dataframes written to a single file must have the same number of columns
    and column names.

    If the file specified by file_path does not exist, it will be created and
    initialized with the header row and first data row from df. All subsequent
    writes will only write new data rows (each data row is the first row from
    df).

    Args:
        df (Pandas DataFrame): crash dataframe
        file_path (string): path of data file
    """
    with open(file_path, "a") as data_file:
        # if file is empty, write header
        data_file.seek(0)
        if os.path.getsize(file_path) == 0:
            data_file.write(get_headers(df))
            data_file.write("\n")

        # write the first row of data from df
        data_file.write(get_first_row(df))
        data_file.write("\n")

def scrape_and_write_data(crash_page_path, data_file_path):
    """
    Scrapes a locally stored crash data webpage and writes the scraped table
    data to a data file.

    Args:
        webpage_path (string): path to webpage htm file
        data_file_path (string): path to csv data file
    """
    # get Pandas DataFrame for crash data
    df = dataframe_from_accident_page(crash_page_path)

    # write crash data to the data file
    write_to_file(df, data_file_path)

# page_path1 = "../wget_planecrashinfo/1986/1986-1.htm"
# page_path2 = "../wget_planecrashinfo/1986/1986-2.htm"

# scrape_and_write_data(page_path1, "patrick.csv")
# scrape_and_write_data(page_path2, "patrick.csv")
