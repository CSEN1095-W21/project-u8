
# 120 Years of Olympic History data analysis

# Introduction:
This project uses the dataset called 120 years of Olympic history from
Kaggle. Methods like Data Cleaning and Data Preparation were used to get the data ready for analyzing.

# Dataset:
The Dataset used here is called 120 years of Olympic history .It contains historical dataset on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016.
- Source: Kaggle
- Location: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results
- Content
The file athlete_events.csv contains 271116 rows and 15 columns; Each row corresponds to an individual athlete competing in an individual Olympic event (athlete-events). 
The columns are the following:<br>
	1. `ID` - Unique number for each athlete;
	2. `Name` - Athlete's name;
	3. `Sex` - M or F;
	4. `Age` - Integer;
	5. `Height` - In centimeters;
	6. `Weight` - In kilograms;
	7. `Team` - Team name;
	8. `NOC` - National Olympic Committee 3-letter code;
	9. `Games` - Year and season;
	10. `Year` - Integer;
	11. `Season`- Summer or Winter;
	12. `City` - Host city;
	13. `Sport` - Sport;
	14. `Event` - Event;
	15. `Medal` - Gold, Silver, Bronze, or NA.


# Data Exploration: 
- In this step, we used data visualization and statistical techniques to describe dataset characterizations, such as size, quantity, and accuracy, in order to better understand the nature of the data.


# Data Preparation and Cleaning:
## Handing Missing values:
 1. By initial analysis, we found that `Age, Height, Weight and Medals` had lot of missing values. 
 2. The column `Medal` had 231333 missing values. This is fine because not all the participants can win a medal. So replaced these values with `non`.
 3. To get the region of the Team in the athlete events.csv, there was merge done for athlete events and region dataset based on their NOC values.
 4. Problems – Some NOC present in the athlete events dataset does not associate to a country from the regions dataset. But we can easily add them manually based on their city Name. This was performed to reduce the number of missing values in the dataset.
## Handing Outliers:
 5. the columns `Age, Height and Weight` contain outliers values 
 6. we have found a strong relationship between the height and the weight so we have decided to handle them via Local Outlier Factor (LOF) 
 7. however for the age,  values range from  `[10 to 97]`  as shown in the boxplot figure of the outlier in the visualtization before cleaning section. So, because all of these values are real, we can't get rid of any of them, so we've decided to keep all age outliers.
# Visualizations Types
 8. we have used Barcharts, Boxplots, Distribution, Piecharts, and Scatterplots/Regplots to demonstrate the relationship between columns. 
# Added Datasets
Here we will mention the datasets we merged to our dataset
 1. **noc_regions**
 -Location:  [https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results?select=noc_regions.csv];
 1. ` NOC` (National Olympic Committee 3 letter code);
 2. `Country name` (matches with regions in  map_data("world"));
  3. `Notes`;
 2. **Country Wise GDP Data**
 -  Source: Kaggle;
-   Location:  [https://www.kaggle.com/chadalee/country-wise-gdp-data];
1. `Country Name`;
2. `Country Code`;
3. `Years` a column for each year represents the GDP value of the country in this year;
3.  **Country Wise Population Data** 
-   Source: Kaggle;
-   Location:  [https://www.kaggle.com/chadalee/country-wise-population-data];
1. `Country Name`;
2. `Country Code`;
3. `Years`a column for each year represents the population of the country in this year;


# Added Features

 1. `Host_Country` represent the hosting country for this row
 2. `GDP/Capita` is a GDP per capita that generally indicates how rich each person in this country is
 3. `Medal_Won` true if a medal is won in this event
 4. `Team_Event` true if this event is a team event 
 5. `Single_Event`true if this event is a single player event

# Research Questions:
The motivation of this anylsis is to find out the answers to the following questions: 

1. Who are the greatest olympics playing nations of all time ?
2.  What sports are the top countries best at?
3.  Does the size of the contingent relate with the number of medals ?
4.  Do hosting the olympics is an advatage to the hosting team ?
5.  Do richer countries perform better at olympics ?
6.  Can we predict the medal tally of a country ?


# Airflow Pipelines: 

### Description: 
In this section a simplified ETL pipline was implemented to can and perform preprocessing steps.

This pipeline includes the following tasks: 
1. Load datasets from CSV files
2. Cleaning the Data 
3. Data Integration 
4. Feature Engineering  

A csv file for the dataframe is saved at the end of each pipeline.

### Pipeline Dependencies: 
The following graph shows the dependencies in the pipeline: 
![Pipeline Dependencies](https://i.postimg.cc/26mmjKSr/Annotation-2021-12-31-143608.png)

# Bonus Airflow Task: 

### Description: 
In this section, we selected China as one of the top performing countries in the Tokyo 2021 Olympics. and India as one of the poor performing countries.

We implemented a pipeline to run daily for a month to perform the following steps: 
 1. Get 20 tweets for each country 
 2. Perform sentiment analysis on the tweets using for example Python’s Textblob library.
 3. Average the sentiments of the tweets you retrieved so far for both countries
 4. Compare the results with the performance of the country in the Olympics.
 5. Results are saved in a csv file.
 
Except for the last task, the return value of each task is passed to the next task via XCOM.

### Pipeline Dependencies: 

![Pipeline Dependencies](https://i.postimg.cc/NMspb60Q/Annotation-2021-12-31-150315.png)
 
