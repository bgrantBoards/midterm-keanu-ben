import string
from bs4 import BeautifulSoup, SoupStrainer
from page_scraper import get_soup, scrape_and_write_data

def href_to_path(current_path, href):
    """
    Returns the full relative path to the destination of an href link on a
    parent page.

    Args:
        current_path (string): path of the directory containing the parent page
        href (string): contents of the link href attribute
    """
    path_chain = current_path.split("/")
    path_chain.pop()
    path_chain.append(href)

    return "/".join(path_chain)

def scrape_and_write_year_page(year_page_path, data_file_path):
    """
    Scrapes a locally stored year data webpage, finds each linked crash page,
    scrapes those pages, and writes the scraped table data to a data file.

    Args:
        webpage_year_page_pathpath (string): path to webpage htm file
        data_file_path (string): path to csv data file
    """
    soup = get_soup(year_page_path)

    for link in soup.find_all('a', href=True):
        crash_page_path = href_to_path(year_page_path, link['href'])

        # do not run for the last link which redirects to site index:
        if "index" not in link['href']:
            scrape_and_write_data(crash_page_path, data_file_path)

def scrape_and_write_database(data_file_path):
    """
    Goes through and scrapes and writes data for all years on the database page.

    Args:
        data_file_path (path): path to csv data file being written to
    """
    database_path = "../wget_planecrashinfo/database.htm"
    soup = get_soup(database_path)

    for link in soup.find_all('a', href=True):
        year_page_path = href_to_path(database_path, link['href'])

        # do not run for the last link which redirects to site index:
        if "index" not in link['href']:
            scrape_and_write_year_page(year_page_path, data_file_path)


data_path = "squidward.csv"
year_page = "../wget_planecrashinfo/2020/2020.htm"

# scrape_and_write_year_page(year_page, data_path)

scrape_and_write_database("all_data.csv")
