import netCDF4 as nc
import math
import numpy as np
import csv
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import windrose
fpaths = ["hotcase", "coldcase"]
latlon = [16,40]
flag_csv = 0

for fi in fpaths:

    for i in range(0,2):
        inve = "_inv" if(i==1) else "" 
        print(fi + inve)
        
        conv = 3600*24*412.5*1000/36
        if(i==1):
            coords=[63-latlon[0],127-latlon[1]]
        else:
            coords=latlon

        in_files = []
        for i in range(0,10):
            in_files.append("bin/"+fi+"_run_t42/snapshots/MOST_SNAP."+format(i, "05d")+".nc")
        print(in_files)

        wdir=[]
        wspd=[]

        

        for file in in_files:
            wdtemp=[]
            wstemp=[]
            dat = nc.Dataset(file)
            ua=(dat['ua'][:,9,coords[0], coords[1]])
            va=(dat['va'][:,9,coords[0], coords[1]])
            for i in range(len(ua)):
                wdtemp.append(math.atan2(-ua[i], -va[i])/math.pi/2*360 + 180)
                wstemp.append(math.sqrt(ua[i]**2+va[i]**2))
            wdir.append(wdtemp)
            wspd.append(wstemp)
        wdir = np.asarray(wdir)
        wspd = np.asarray(wspd)

        print(len(ua))
        print(len(wspd))
        print(len(wspd[0]))

        outdata=wdir
    

        #plot
        plt.close()
        fig = plt.figure()
        bins = np.arange(1, 18, 3)
        seasons = ["Spring (MAM)", "Summer (JJA)", "Autumn (SON)", "Winter (DJF)"]
        pos = [[0, 0.3, 0.5, 0.5],[0.5, 0.3, 0.5, 0.5],[0, -0.4, 0.5, 0.5],[0.5, -0.4, 0.5, 0.5]]

        fig.suptitle('Windrose for [{0},{1}]\n{2}'.format(latlon[0],latlon[1],fi+inve))
        for j in range(0,4):
            wdp = []
            wsp = []
            wpw = []
            #windRange = range(1, 18, 3)
            dr = [(180 + (j*90))%360, (269 + (j*90))%360 + 1]
            print(dr)
            for d in range(dr[0],dr[1]):
                wdp.extend(wdir[:,d])
                wsp.extend(wspd[:,d])

            ax = fig.add_subplot(2,2, j+1, projection="windrose",position=pos[j])
            
            ax.bar(np.asarray(wdp), np.asarray(wsp), bins=bins, normed=True, calm_limit=1)
            #ax.set_ylim(0, 25)
            fmt = '%.0f%%' 
            yticks = mtick.FormatStrFormatter(fmt)
            ax.yaxis.set_major_formatter(yticks)
            ax.set_title(label=seasons[j])
            
            #ax.contour(wdir[dr[0]:dr[1]], wspd[dr[0]:dr[1]], bins=bins, colors="black")     
        plt.legend(bbox_to_anchor=(1.1, 1),loc='lower left', borderaxespad=0.)    
        plt.savefig('outputs/{0}_[{1:0d},{2:0d}]_wind'.format(fi+inve,latlon[0], latlon[1]), bbox_inches="tight")

        if(flag_csv==1):
            with open('outputs/{0}_[{1:0d},{2:0d}]_data.csv'.format(fi+inve,latlon[0], latlon[1]), 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for tada in outdata:
                    spamwriter.writerow(tada)
                    #print(tada)
