# EOCC Data Analysis
We obtain the data from the below website.
https://www.eeoc.gov/statistics/employment/jobpatterns/eeo1/2009

1. **by_state_epi.ipynb**: This notebook webscrapes each state's (or an indicated state's) information and calculates the EPI (executive parity index) for various racial groups for each state (or an inputted state). It then conducts welch's t-test and counts number of groups that the Asian EPI is significantly less than (as opposed to equal to) with a significance level of 0.05. The files and results are saved to the **By State EPI** directory.
2. **national_aggregate_epi**: This notebook webscrapes information from the EOCC website on national aggregate employment data. It then calculates the EPI of different racial groups on the national aggregate level. The created files and results are saved to the **National Aggregate EPI** directory.
3. **states_and_industries_epi**: This notebook calculates different racial groups' EPI for the inputted state and industry (NAICS-2). The created files and results are saved to the **States and Industries EPI** directory.
