import dateparser as dp
import pandas as pd
import matplotlib.pyplot as plt

# date1 = "October 01 1916"

# parsed = dp.parse(date1)

# print(parsed)

# print(parsed.year, "\n", parsed.month, "\n", parsed.day, "\n")

dates = pd.read_csv("all_data.csv")["Date:"]

crashes_by_year = {}

for date in dates:
    # if crashes_by_year

    # use date parser on date:
    year = dp.parse(date).year

    if year in crashes_by_year:
        crashes_by_year[year] += 1
    else:
        crashes_by_year[year] = 1

plt.plot(crashes_by_year.keys(), crashes_by_year.values())
plt.show()
