
# Johannes' Algorithm, but it does Johannes standard once, and then repeats the algorithm again with squares 3x larger to try and remove high floating clouds

import pandas as pd
import numpy as np
import sys
sys.path.append('/home/lidar/Documents/GitHub/averaging_scripts/avglib')
from acquire_df import load_df

df = load_df(config_path="avglib/averaging_config.json")
print("DataFrame acquired.")


def get_avg(df, step, axes=None, supervoxel_size = 3):
    print("Doing Johannes Things")
    cols = ["x", "y", "z"]
    axes = [cols.index(n) for n in axes] if axes else range(3)
    rounded_cols = [f"rounded_{n}" for n in cols]
    df[rounded_cols] = df[cols].div(step).round().mul(step)
    df = df.groupby([rounded_cols[n] for n in axes]).mean()

    print("Doing Baker Things")

    bigger_rounded_cols = [f"bigger_rounded_{n}" for n in cols]
    df[bigger_rounded_cols] = df[cols].div(step*supervoxel_size).round().mul(step*supervoxel_size)
    df = df.groupby([bigger_rounded_cols[n] for n in axes]).mean()

    return df[cols]

# Average across all dimensions

# Flatten the z axis
averaged_df = get_avg(df, 0.03, ["x", "y"], supervoxel_size=3)
print("Function Called.")
np.savetxt('/home/lidar/Documents/Data/Testing Data/24-2024-07-03/2023-02-14-21-49-41_pointcloud - CUT-AVGABB.asc', averaged_df, delimiter=' ')
print("Program has finished running.")


'''
Ok. What am I trying to do?

I want to remove outlier columns

I want to find outliers by putting a 3x3 grid in the xy plane, 
and then averaging the zs in each grid cell. If a point's z is 
more than 3 standard deviations away from the mean z in its grid cell, 
it's an outlier and should be removed.

How do I implement this in an algorithm?
1. First, I need to create a new dataframe with the same columns as the original, but with additional columns for the rounded x and y values. These rounded values will be used to group the points into grid cells.
2. Next, I need to group the points by their rounded x and y values, and calculate the mean and standard deviation of the z values in each group.
3. Then, I need to iterate through each point in the original dataframe, and check if its z value is more than 3 standard deviations away from the mean z value of its corresponding group. If it is, I will mark it as an outlier.
4. Finally, I will create a new dataframe that only includes the points that are not marked as outliers, and return this new dataframe.

'''