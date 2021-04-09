# Description:
**SoftDes Midterm Project centered around collecting and interpreting data.**

We researched a plane crash database that documents the entire history of crashes in aviation from 1908 to 2021.

The database contains information on a myriad of different facts about each crash but for the purposes of our project, we focused on 3 fields in particular: Summary, Date, and Fatalities.

# To Replicate Our Results:

To replicate the results of our computational essay you will need to obtain additional python libraries instrumental in running the code.

### Computational Essay Dependencies:

- `pip install dateparser`
- `pip install pandas`
- `pip install numpy`
- `pip install matplotlib`
- `pip install collections`

### Web Scraper Dependencies:

- `pip install bs4`
- `pip install pandas`

## Downloading the Database

[`wget`](https://programminghistorian.org/en/lessons/automated-downloading-with-wget) was used to ease the volume of requests from the database website as it can recursively traverse a website and download all the pages that need to be scraped for data. This eliminated the need to use APIs to make multiple requests to the website every time we needed data. Accessing local files was way faster than making web requests from the database. We found this to be rather convenient because we would be working with 102 links that represented the years 1920-2021, and inside those 102 links there were additional links that brought you to specific crash dates that occurred within that specific year. To summarize, `wget` allowed us to download 5001 pages from the database and have them on our machines for local access.

Unfortunately, in order to recreate our CSV data file on your own machine (for instance, if you are reading this in the future and want to access the updated database) you will need to download the [database website](http://www.planecrashinfo.com/database.htm) to your machine with the following `wget` command:

``` bash
wget --recursive --level=2 --no-parent --convert-links http://www.planecrashinfo.com/database.htm
```

*Note that you will need to run this command in the repository’s parent directory so the folder that `wget` creates is on the same level as the repo. This is crucial for the scraper code to find the correct pages to scrape.*

Because the scraper code accesses local files through manually constructed file paths, the code can only run on Mac and Linux systems, not Windows, as files need to be accessible through `dir/dir/file.ext` styled paths.

We used the `matplotlib` library to create all of our plots. The specifics are found in the notebook `remember_remember.ipynb`
