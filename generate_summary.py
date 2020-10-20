
import os
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(
    description='Generate summary for Chicago Bird Collision data')

parser.add_argument('--input_path', type=str, required=True,
                    help="""Path of directory having Chicago Bird collision data in JSON format. (This path must include all of chicago_collision_data.json, flight_call.json, light_levels.json files)""")

parser.add_argument('--output_file_path', type=str, required=True,
                    help="""Path of output file""")
args = parser.parse_args()

################## Read Data from input Path into pandas dataframe ######################


def ReadInputData(input_file_path):
    """Read json file from input_file_path and return a dataframe
    """
    if os.path.exists(input_file_path):
        return pd.read_json(input_file_path)
    exit("File not found :: "+input_file_path)

################################ Clean raw data #########################################


def CleanRawData(df_in, dropna_columns=[]):
    """Returns a clean dataframe by applying standard set of operations
        Operations Applied:
        1. Column Type: str
            - strip :: Since raw data may contain leading and trailing spaces so, it makes more sense to be proactive in removing leading and trailing spaces
            - lower :: Based on the dataset it makes more sense to transform every string column value to lower case
        2. Drop Duplicate records from entire dataframe
        3. Drop records containing null values
        4. Clean the column name by removing leading and trailing spaces from column names
    """
    for column in df_in.select_dtypes([np.object]):
        df_in[column] = df_in[column].apply(
            lambda x: x.strip().lower())
    if len(dropna_columns) > 0:
        # Removing the records which contains null values.
        # For categorical values in the given data we can not extrapolate missing values.
        # For rest of the numerical values like "Flight" and "Light Score" we can not replace by mean of some default value as the sample days are not uniform
        df_in.dropna(inplace=True, subset=dropna_columns)
    df_in.columns = [c.strip() for c in df_in.columns]
    return df_in.drop_duplicates()


def RenameColumnsInFlightCallDataframe(df_flight_call):
    """Rename columns in flight_call table to the correct values
    """
    column_mapping = {"Species": "Genus", "Family": "Species",
                      "Collisions": "Family", "Call": "Flight Call"}
    flight_call_columns = [column_mapping.get(
        c, c) for c in df_flight_call.columns]
    df_flight_call.columns = flight_call_columns
    return df_flight_call

################################ Create Joined Summary ##################################


def CreateJoinedSummary(df_chicago_collision_data, df_flight_call, df_light_levels):
    """Returns Summary dataframe by combining all three dataframes
    Data Description:
        df_chicago_collision_data:
            - Genus            :: join key 2 -----|
            - Species          :: join key 2 -----|
            - Date             :: join key 1 -----|---------|
            - Locality                            |---------|-------- inner join 2
        df_flight_call:                           |         |
            - Genus            :: join key 2 -----|         |
            - Species          :: join key 2 -----|         |
            - Family                                        | -------- inner join 1
            - Flight                                        |
            - Flight Call                                   |
            - Habitat                                       |
            - Stratum                                       |
        df_light_levels:                                    |
            - Date             :: join key 1 ---------------|
            - Light Score
    Processing Description:
        Joining light_levels on top of chicago_collision_data
            - We will now combine light_levels data using "Date" column to complete the dataset
            - Join type: we will connect light_levels data using inner join
            - Important points:
                1. We have observed that there are some missing data points in light_levels table. We will simply remove all the records which have missing values.
                2. There is total 3063 days of data available in light_levels dataset. These 3063 days are spreaded between '2000-03-06' and '2018-05-26'.
                3. There is total 5318 days of data available in chicago_collision_data. These 5318 days are spreaded between '1978-09-15' and '2016-11-30'.
                4. We observed that values in Date column are taken randomly so we can not extrapolate the missing data points so it does not makes sense to keep the records which have missing data points
        Join between above generated data table and flight_call:
            - From the above data description we can clearly say that the information in above joined data table can be extended by 
            flight_call table based on "Genus" and "Species" columns. 
            - Join type: We can apply "inner" as we can not analyze the records which are only present in chicago_collision_data or flight_call
            - Important points:
                1. There are missing values for Genus value "ammodramus" and Species values in ['nelsoni', 'henslowii', 'leconteii'] in flight_call table. We will ignore these values inorder to generate the summary table
    """
    # Join between chicago_collision_data and light_level
    df_summary = pd.merge(df_chicago_collision_data, df_light_levels,
                          how='inner', left_on=['Date'], right_on=['Date'])
    # Join between df_new and flight_call using 'Genus','Species' tables
    df_summary = pd.merge(df_summary, df_flight_call,  how='inner', left_on=[
        'Genus', 'Species'], right_on=['Genus', 'Species'])
    return df_summary


################################ main ###################################################
if __name__ == "__main__":
    # Step 1: Get input arguments
    input_path = args.input_path
    output_file_path = args.output_file_path

    # Step 2: Read raw JSON data from input path
    # Define file names to read from input_path
    files_to_read = ["chicago_collision_data.json",
                     "flight_call.json", "light_levels.json"]
    # Create path for files
    files_to_read = list(
        map(lambda x: os.path.join(input_path, x), files_to_read))

    # Read chicago_collision_data.json into a dataframe
    df_chicago_collision_data = ReadInputData(files_to_read[0])

    # Read flight_call.json into a dataframe
    df_flight_call = ReadInputData(files_to_read[1])

    # Read light_levels.json into a dataframe
    df_light_levels = ReadInputData(files_to_read[2])

    # Step 3: Apply transformations on raw data frames
    # Clean raw dataframe
    df_chicago_collision_data = CleanRawData(
        df_chicago_collision_data, dropna_columns=df_chicago_collision_data.columns)
    df_flight_call = CleanRawData(
        df_flight_call, dropna_columns=df_flight_call.columns)
    df_light_levels = CleanRawData(
        df_light_levels, dropna_columns=df_light_levels.columns)

    # Renaming the columns in flight call dataframe as mentioned in the original article
    df_flight_call = RenameColumnsInFlightCallDataframe(df_flight_call)

    # Step 4: Create Summary table by joining above three dataframes
    df_summary = CreateJoinedSummary(
        df_chicago_collision_data, df_flight_call, df_light_levels)

    # Step 5: Save  summary to output_file_path
    os.makedirs("/".join(output_file_path.split("/")[:-1]), exist_ok=True)
    df_summary.to_json(output_file_path)
