import netCDF4 as nc
import math
import numpy as np
import csv

fpaths = ["hotcase", "coldcase"]
latlon = [17,72]
for fi in fpaths:
    for i in range(0,2):
        inve = "_inv" if(i==1) else "" 
        print(fi + inve)
        dat_av = nc.Dataset("sources/"+fi+inve+"_av.nc")
        dat_max = nc.Dataset("sources/"+fi+inve+"_month_max.nc")
        dat_min = nc.Dataset("sources/"+fi+inve+"_month_min.nc")
        
        conv = 3600*24*412.5*1000/36
        if(i==1):
            coords=[64-latlon[0],128-latlon[1]]
        else:
            coords=latlon

        time = dat_av['time'][:]
        zdec = dat_av['zdec'][:]
        tas = dat_av['tas'][:,coords[0], coords[1]] - 273.15
        maxt = dat_max['tas'][:,coords[0], coords[1]] - 273.15
        mint = dat_min['tas'][:,coords[0], coords[1]] - 273.15
        hur = dat_av['hur'][:,9,coords[0], coords[1]]
        pr = dat_av['pr'][:,coords[0], coords[1]] * conv
        prsn = dat_av['prsn'][:,coords[0], coords[1]] * conv
        rss = dat_av['rss'][:,coords[0], coords[1]] 
        ssru = dat_av['ssru'][:,coords[0], coords[1]] 
        ua = dat_av['ua'][:,9,coords[0], coords[1]]
        va = dat_av['va'][:,9,coords[0], coords[1]]

        tdew = []
        wdir = []
        wspd = []

        print(hur)

        for f in range(0, 36):
            tdew.append(243.04*(math.log(hur[f]/100)+17.625*tas[f]/(243.04+tas[f]))/(17.625-(math.log(hur[f]/100)+17.625*tas[f]/(243.04+tas[f]))))
            wdir.append(math.atan2(-ua[f], -va[f])/math.pi/2*360 + 180)
            wspd.append(math.sqrt(ua[f]**2+va[f]**2))

        rin = rss - ssru

        outdata = [time, zdec, tas, maxt, mint, tdew, pr, prsn, rin, ua, va, wspd, wdir]

        with open('{0}_[{1:0d},{2:0d}]_data.csv'.format(fi+inve,latlon[0], latlon[1]), 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for tada in outdata:
                spamwriter.writerow(tada)
                #print(tada)
