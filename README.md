
# 120 Years of Olympic History data analysis

## Introduction:
This project uses the dataset called 120 years of Olympic history from
Kaggle. Methods like Data Cleaning and Data Preparation were used to get the
data ready for analyzing.

## Dataset:
The Dataset used here is called 120 years of Olympic history .It contains historical dataset on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016.
- Source: Kaggle
- Location: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results
- Content:
     - The file athlete_events.csv contains 271116 rows and 15 columns. Each row corresponds to an
individual athlete competing in an individual Olympic event (athlete-events). The columns are `ID,
Name, Sex, Age , Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event and
Medal`.
     - The file noc_regions.csv contains 230 rows and 3 columns. The columns are `NOC` (National
Olympic Committee 3 letter code),Country name and Notes.

## Data Preparation and Cleaning:

- By initial analysis, we found that `Age, Height, Weight and Medals` had lot of missing values. 
- The column `Medal` had 231333 missing values. This is fine because not all the participants can win a medal. So replaced these values with `non`.
- To get the region of the Team in the athlete events.csv, there was merge done for athlete events and region dataset based on their NOC values.
- Problems – Some NOC present in the athlete events dataset does not associate to a country from the regions dataset. But we can easily add them manually based on their city Name. This was performed to reduce the number of missing values in the dataset.

## Research Questions:

  

1. Does hosting the Olympics improve performance?
2. Has Egypt's number of medals in the summer event increased over time?
3. Has Egypt's number of medals in the winter event increased over time?
4. Whats' the distribution of age for male/females over the years?
5. Number of women relative to men across countries
