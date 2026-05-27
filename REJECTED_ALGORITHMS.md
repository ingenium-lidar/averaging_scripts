# Rejected Algorithms

This file contains records of averaging algorithms which the LiDAR team has tested and then rejected. 


## averaging_function_Baker_A: Isotropic 3D Voxel Centroid Filtering

This algorithm divided the pointcloud into cubes of a certain size (tested with 30 cm sides) and averaged the locations of the points within that cube. It was rejected because:

1. It did not filter enough points out compared to Johannes' algorithm, leaving the output cloud a tangled white mess

2. It failed utterly to filter outlier points--any given voxel that had a single point in it at the start had a point in it by the end, making it utterly useless for removing things like leaves (at which Johannes's algorithm is not perfect, but it's pretty good when there's enough ground coverage)

3. It failed to produce a surface-like object for the "ground" portion of the dig

To examine this algorithm for yourself, run Johannes' algorithm, but with `["x", "y", "z"]` specified as the function parameter instead of `["x", "y"]`


## averaging_function_Baker_B: Isotropic 2.5D Voxel Grid Downsampling With Columnar Centroid Projection and *n*-Sigma Outlier Removal

This algorithm was based on Johannes' algorithm, except that after implementing Johannes' algorithm, it then removed points that were *n* standard deviations from the mean of the column. Additionally, it used parametrically-controlled "super-voxels" (composed of an *m*x*m* grid of standard-size voxels) to determine the mean that was applied to each of the standard voxels.

This algorithm was analyzed with *m* and *n* ranging from 1-4 in integer steps. 

The greatest problem that emerged was that, at the values of *m* and *n* which succesfully began removing floating debris, small deviations in the surface were also being removed. 

### *m*-Analysis

At very small values of *m* (eg 1), the algorithm became insensitive. Flying debris, due to the nature of Johannes' algorithm, would be isolated into its own column, and so the mean of that column would be the mean of the flying debris. This had the effect of removing *all* outlier points in *all* columns and failing to remove dataset-outliers when the outliers resided in their own column, when the purpose of the *m* voxel parameter was to bias the column mean in favor of the wider "true surface". 

Medium *m* values worked the best. However, medium and large *m* values (2-4) both shared the same issue: they worked quite well at identifying high floating points and removing them, but their "footprint" was so wide that if a relatively homogenous, flat area was scanned, and there were a single rock in that area, sittting on the surface, the wider voxel footprint would weight the mean so heavily towards the wider flat surface that the rock would be deemed an outlier and removed.

### *n*-Analysis

To attempt to fix this issue with larger *m* values, *n* varying was attempted. The way the algorithm worked was this: any points more than *n* standard devations from the supervoxel mean were removed, where the supervoxel was an *m*x*m* square of standard voxels. If bigger *m*s weighted the mean too heavily toward the true surface and wiped out variations, then surely *n* increases could solve that problem!

Unfortunately, *n*s of 3 and above simply had no effect on the data set at all, and *n*=2 caused signficant surface alteration without removing the problematic floating elements. 

### Conclusion

*m* and *n* were pushed to their limits in both directions until they began to unacceptably alter the dataset. Under no combination of parameters was the result detectably superior to Johannes' algorithm, and therefore, this algorithm was rejected. 


## averaging_function_Baker_C: Multi-Stage Isotropic 2.5D Voxel Grid Downsampling With Columnar Centroid Projection

This algorithm also implemented Johannes' algorithm first, but then implemented it a second time with voxels *n* times larger. The idea was to outweigh the floating debris with points from the surface. Unfortunately, after Johannes' algorithm, the surface and floating clouds have the same density. The end result was an unacceptable thinning of the data (resulting in much lower surface resolution) without any removal of floating debris. *n* was tested at 2 and 3. 