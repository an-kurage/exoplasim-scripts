import netCDF4 as nc
import math
import numpy as np

latlon=[0, 0]
latlon[0]=input ("Lat index: ")
latlon[1]=input ("Lon index: ")
dat_av = nc.Dataset("sources/hotcase_av.nc")
lsm = dat_av['lsm'][0,latlon[0], latlon[1]]
print("Land") if lsm==1 else print("Sea")