# ChicagoCollisionDataSummaryGeneration

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Overview](#overview)
  - [Data Description](#data-description)
  - [Clean Raw Data](#clean-raw-data)
  - [Create Joined Summary](#create-joined-summary)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->

## About The Project

Summary for Chicago Bird Collision data

### Built With

This project mainly utilize below mentioned python libraries.

- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This project requires knowledge of python3, pandas, and, numpy libraries.

### Installation

1. Clone this repo

```sh
git clone https://github.com/harshal2802/ChicagoCollisionDataSummaryGeneration.git
```

2. Change directory to above cloned repo

```sh
cd ChicagoCollisionDataSummaryGeneration
```

3. pip install -r requirements.txt

<!-- Overview -->

# Overview

Problem Statement is to generate the combined summary of Chicago collision data :

<!-- Data Description -->

### Data Description

Given dataset contains mainly 3 files described below

1.  df_chicago_collision_data.json: This dataset has information on the dates and the locality where the light measurements
    were taken. <br>
    Columns - Genus, Species, Date, Locality
2.  df_flight_call.json: This dataset provides the information of whether or not a particular bird family uses flight
    call to communicate with each other. Per the paper, this is an important indicator that
    affects bird-building collisions. <br>
    Columns - Species, Family, Collisions, Flight, Call, Habitat, Stratum
3.  df_light_levels.json: This dataset provides the light levels (integer value) as measured on various dates. <br>
    Columns - Date, Light Score

<!-- Clean Raw Data -->

## Clean Raw Data

To generate the summary from the provided dataset we first need to clean the provided raw data.
I have defined a function named :: 'CleanRawData' to apply following operations on an input dataframe:<br>
<br>

1. Clean String Columns: <br>
   - strip: Data of string type may contain arbitrary leading and trailing spaces which may add unnecessary error into subsequent analysis <br><br>
   - lower:This will convert all the string values to lower case to avoid discriminations in string values. <br>
   <br>
2. drop_duplicates: We will remove all the duplicate records to avoid double counting in all the data tables. <br>
   <br>
3. dropna: To exclude the unpopulated data from tables we will remove all the records which contains None values <br>
   <br>
4. strip the column names: We will also remove the leading and trailing spaces from column names. <br>
   <br>
5. Rename columns in flight_call.json file: As observed, the columns names in flight_call table are incorrect. We need to rename the columns as follows:: <br>
    - Species -> Genus 
    - Family -> Species 
    - Collisions -> Family 
    - Call -> Flight Call 
<!-- Create Joined Summary -->

## Create Joined Summary

Once We have cleaned all the Dataframes and renamed the columns in the flight_call table, we are now ready to join all the Dataframes to generate summary.

### Join 1:: between df_chicago_collision_data and df_light_levels ( inner join on *Date* column )

As we observe that the *chicago_collision_data* can directly get connected to *light_levels* data to get *Light Score* information in the joined Dataframe. 
<br>
Here are a few observations about these two tables:

- We have observed that there are some missing data points in the light_levels table. We will remove all the records which have missing values as these records with missing values are not useful in the final results 
- There is a total of 3063 days of data available in the light_levels dataset. These 3063 days spread between '2000-03-06' and '2018-05-26'.
- There is a total of 5318 days of data available in chicago_collision_data. These 5318 days spread between '1978-09-15' and '2016-11-30'.
- We observed that the values in the Date column were taken randomly. Hence we can not extrapolate the missing data points. Therefore it does not make sense to keep the records that have the missing data points. 
- We will be applying the inner join between these two tables to avoid having rows with null values.



### Join 2:: between First Join result and df_flight_call ( inner join on *Genus* and *Species* column )

The result of the above Join 1 can also be extended by the *flight_call* table by using *Genus* and *Species* columns. <br>
Here are few observations about these tables:
- There are missing values for Genus value "ammodramus" and Species values in ['nelsoni', 'henslowii', 'leconteii'] in flight_call table. <br>
  We will ignore these values inorder to generate the summary table.
- We will be applying the inner join between these two tables to avoid having rows with null values.

### Here is the graphical view of above join ::

```
_____________________________________________________________________________
|                                                                            |
|df_chicago_collision_data:                                                  |
|    - Genus            :: join key 2 -----|                                 |
|    - Species          :: join key 2 -----|                                 |
|    - Date             :: join key 1 -----|---------|                       |
|    - Locality                            |---------|-------- inner join 2  |
|df_flight_call:                           |         |                       |    
|    - Genus            :: join key 2 -----|         |                       |
|    - Species          :: join key 2 -----|         |                       |
|    - Family                                        | -------- inner join 1 |
|    - Flight                                        |                       |
|    - Flight Call                                   |                       |    
|    - Habitat                                       |                       |    
|    - Stratum                                       |                       |  
|df_light_levels:                                    |                       |
|    - Date             :: join key 1 ---------------|                       |
|    - Light Score                                                           |
|____________________________________________________________________________|
```

<!-- USAGE EXAMPLES -->

## Usage

To generate summary data file for given Chicago bird collision dataset please use below command

```sh
python generate_summary.py --input_path data --output_file_path data/summary.json
```

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Harshal Chourasiya - [Linkedin](https://www.linkedin.com/in/harshal-chourasiya-39bb0426/), [Github](https://github.com/harshal2802)

[Project Link](https://github.com/harshal2802/ChicagoCollisionDataSummaryGeneration)

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

- [Zonotrichia wikipedia](https://en.wikipedia.org/wiki/Zonotrichia)
- [Nocturnal flight-calling behaviour predicts vulnerability to artificial light in migratory birds](https://royalsocietypublishing.org/doi/10.1098/rspb.2019.0364)
- [Original version of data](https://github.com/rfordatascience/tidytuesday/tree/47567cb80846739c8543d158c1f3ff226c7e5a5f/data/2019/2019-04-30/raw)