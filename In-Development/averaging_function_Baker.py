### NOTES ###
__NOTES__ = """
This file was copied off of averaging_function_Johannes.py by Abraham Baker 
Date Created: Jan 25 2025
Last Updated: Jan 25 2025
Purpose: Increase clarity and efficiency of the original without altering fundamental functionality

NOTES FOR SOMEONE WHO KNOWS PANDAS BETTER THAN I DO:

- Check these two lines:
    df = pd.DataFrame(pd.read_csv(full_path, sep=' ', header=None))  
    df.columns = ["x", "y", "z"] 
If I am correct, this could be replaced by the following line:
    df = pd.DataFrame(pd.read_csv(full_path, sep=' ', header= ["x", "y", "z"] )) 
But for goodness sakes nobody swap it until an experienced user has confirmed that I am correct!


- In function get_avg, there is a parameter cols = ["x", "y", "z"]. Why is this not obtained from the dataframe object?

UPDATE LOG: WRITE BELOW HERE IF YOU ALTER THIS FILE

1. Abraham Baker, Jan 25 2025
    Created the file and added all the comments currently in it. 
    Also added the __NOTES__ file 
    modified get_avg to be more readable. For original see averaging_function_Johannes.py

2. [Your name], [date]
    [Brief summary of edits]
"""
### CODE ###

import pandas as pd
import numpy as np

full_path = "/home/lidar/ingenium_cartographer/labtest5_pointcloud/labtest5.txt"         # file path of the pointcloud.txt file
df = pd.DataFrame(pd.read_csv(full_path, sep=' ', header=None))  # Read the file path above like a .csv and convert it to a Pandas dataframe object. Do not add a header to the df
df.columns = ["x", "y", "z"] # Define columns. These, best I can tell, are now the header objects for the df. See __NOTES__ string above
print("DataFrame acquired.")

def get_avg(df, step, axes=None):  # average the df file in the axis omitted from the axes parameter. Axes should be a list containing some out of ["x", "y", "z"]. Step seems to be a float in meters, over which interval the axis omitted is averaged.
    cols = ["x", "y", "z"] # List of all the columns in the df file.
    if (axes != None):
        axes = [cols.index(n) for n in axes] # Replace axes with a list containing the indices from the cols list of the string parameters currently in the axes list.
    else:
        axes = [0,1,2]
    rounded_cols = [f"rounded_{n}" for n in cols]
    df[rounded_cols] = df[cols].div(step).round().mul(step)
    return df.groupby([rounded_cols[n] for n in axes]).mean()[cols]

# Average across all dimensions

# Flatten the z axis
averaged_df = get_avg(df, 0.03, ["x", "y"])
print("Function Called.")
np.savetxt('labtest5_AVG.txt', averaged_df, delimiter=' ')
