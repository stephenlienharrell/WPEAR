import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def StartRun():
    shapeFile = "shapefile/tl_2013_18_cousub/tl_2013_18_cousub"
    gribFile='sample_data/multi_2.at_15m.t18z.grib2'
    Visualize(gribFile, shapeFile)


def Visualize(gribFile, shapeFile):
    """Visualize data
    Data from local sample Grib2 file
    """
    plt.figure(figsize=(12,16))
    grbs=pygrib.open(gribFile)
    grb = grbs.select(name='Wind speed')[0]
    data=grb.values
    lat,lon = grb.latlons()

    m = Basemap(resolution='l', # c, l, i, h, f or None
            projection='merc',
            lat_0=40.2, lon_0=-86.1,
            llcrnrlon=-88.1, llcrnrlat= 37.77,
            urcrnrlon=-84.78, urcrnrlat=41.76)

    x, y = m(lon,lat)
    cs = m.pcolormesh(x,y,data,
                    shading='flat',
                    cmap=plt.cm.jet)

    m.drawcoastlines()
    m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    m.drawmapboundary(fill_color='#46bcec')
    plt.colorbar(cs,orientation='vertical')
    m.readshapefile(shapeFile,'areas')
    plt.show()
