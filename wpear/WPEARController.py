import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def StartRun():
    print "Do Stuff"
    sample1='sample_data/multi_1.ak_10m.dp.201612.grb2'
    Visualize(sample1)


def Visualize(grib):
    """Visualize data
    Data from local sample Grib2 file
    """
    plt.figure()
    grbs=pygrib.open(grib)
    grb = grbs.select(name='Primary wave direction')[0]
    data=grb.values
    lat,lon = grb.latlons()
    m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
            urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
            resolution='c')
    x, y = m(lon,lat)
    cs = m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)
    m.drawcoastlines()
    m.fillcontinents()
    m.drawmapboundary()
    m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])
    plt.colorbar(cs,orientation='vertical')
    plt.title('NWW3 Primary wave direction from GRiB')
    plt.show()
