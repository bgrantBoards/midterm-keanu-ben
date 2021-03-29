import dateparser as dp

date1 = "March 29 2021"

parsed = dp.parse(date1)

p_year = parsed.year

print(type(p_year))