#!/usr/bin/env python
# coding: utf-8

# ### LiDAR Averaging Code 
# 27 April 2023
# Daniel Humphrey
# 
# Reduces the noise in the LiDAR point cloud data by adaptively averaging particles based on the relative particle density of each cell and its neighbors. Vary grid spacing n and minimum particles per cell m to find optimal settings. 
# 
# Basic theory goes as follows: we want the code to squash the noisy data down into surfaces. A surface consists of a plane oriented in a certain direction; we want the code to average perpendicular to that plane. If we fill the points into a three dimensional grid and find the point density in each cell, we can then average most strongly in the direction with the greatest change in particle density. 

# In[1]:


import numpy as np
import pandas as pd

full_path = r"""/home/lidar/ingenium_cartographer/AshkelonArch_pointcloud/AshkelonArchExitArchFloor.asc"""
df = pd.DataFrame(pd.read_csv(full_path, sep=' ', header=None))
# df = pd.DataFrame(pd.read_csv("94-202200706cutAVGgeo.txt", sep=' ', header=None)) # I used this for script development
df = df[list(range(3))]
df.columns = ["x", "y", "z"]
print("DataFrame acquired.")

def get_avg(df, step):
    
    df = df.div(step).round().mul(step) # rounding
    n = 1 # grid spacing
    m = 5 # mininum number of particles per grid space
    
    grid_origin = [min(df['x']), min(df['y']), min(df['z'])]
    cell_indices = np.floor((df-grid_origin) / n).astype(int) # making an index of each point in the grid, normalized to the origin
    
    cellX, cellY, cellZ = cell_indices.max() + 2 # defining the number of cells on each axis, with some (necessary) breathing room
    
    point_counts = np.zeros((cellX*cellY*cellZ, 1), dtype=int)
    point_sum = np.zeros((cellX*cellY*cellZ, 3), dtype=float)
    
    print('Arrays Initialized')
    
    for i in np.arange(df.shape[0]): # looping over every point
        a, b, c = cell_indices.iloc[i] # getting the cell index for every point
        point_counts[a * cellY * cellZ + b * cellZ + c] += 1 # linear indexing
        point_sum[a * cellY * cellZ + b * cellZ + c, :3] += df.loc[i].values
        
    print('Particles Filled Into Cells, Sums Counted')
    
    # removing unnecessary zero values/rows (most efficient for doing unweighted average)
    # point_counts = np.repeat(np.reshape(point_counts[point_counts != 0], (-1,1)), 3, axis=1)
    # point_sum = point_sum[~np.all(point_sum == 0, axis=1)]
    # cell_averages = point_sum / point_counts + grid_origin # Unweighted, particle reducing average
    
    averages = np.zeros((df.shape[0], 3))
    
    for i in np.arange(df.shape[0]): # looping over every point
        a, b, c = cell_indices.iloc[i] # getting the cell index
        cell_dens = point_counts[a * cellY * cellZ + b * cellZ + c] # finding the number of points in the cell
        
        if cell_dens < m: 
            averages[i, :3] = None # clearing out cells without enough points within it
            
        px, py, pz = df.iloc[i] # position of the point
        sx, sy, sz = point_sum[a * cellY * cellZ + b * cellZ + c, :3] / cell_dens # average position of all the points within the cell
        
        # densities of the surrounding cells
        cell_dens_plus_x = point_counts[(a + 1) * cellY * cellZ + b * cellZ + c] 
        cell_dens_minus_x = point_counts[(a - 1) * cellY * cellZ + b * cellZ + c]
        cell_dens_plus_y = point_counts[a * cellY * cellZ + (b + 1) * cellZ + c]
        cell_dens_minus_y = point_counts[a * cellY * cellZ + (b - 1) * cellZ + c]
        cell_dens_plus_z = point_counts[a * cellY * cellZ + b * cellZ + c + 1]
        cell_dens_minus_z = point_counts[a * cellY * cellZ + b * cellZ + c - 1]
        
        # density difference between surrounding cells and the cell where the point is located
        weight_plus_x = abs(cell_dens - cell_dens_plus_x)
        weight_minus_x = abs(cell_dens - cell_dens_minus_x)
        weight_plus_y = abs(cell_dens - cell_dens_plus_y)
        weight_minus_y = abs(cell_dens - cell_dens_minus_y)
        weight_plus_z = abs(cell_dens - cell_dens_plus_z)
        weight_minus_z = abs(cell_dens - cell_dens_minus_z)
        
        # greater weight is given to axes in which there is greater variation in density
        x_weight = (weight_plus_x + weight_minus_x) / ((weight_plus_x + weight_minus_y) + (weight_plus_y + weight_minus_y) + (weight_plus_z + weight_minus_z))
        y_weight = (weight_plus_y + weight_minus_y) / ((weight_plus_x + weight_minus_y) + (weight_plus_y + weight_minus_y) + (weight_plus_z + weight_minus_z))
        z_weight = (weight_plus_z + weight_minus_z) / ((weight_plus_x + weight_minus_y) + (weight_plus_y + weight_minus_y) + (weight_plus_z + weight_minus_z))
        
        # small weight => position stays the same. large weight => position becomes averaged.
        x = x_weight * (sx - px) + px
        y = y_weight * (sy - py) + py
        z = z_weight * (sz - pz) + pz
        
        averages[i, 0] = x
        averages[i, 1] = y
        averages[i, 2] = z
        
    mask = ~np.any(averages == None, axis=1) # taking out the null values
    averages = averages[mask]
    averaged_df = pd.DataFrame(averages) # changing back to dataframe object
    print('Particles Adaptively Averaged')
    
    return averaged_df


averaged_df = get_avg(df, 0.03)
np.savetxt('AshkelonArchExitArchFloorAVG.txt', averaged_df, delimiter=' ')


# In[ ]:




