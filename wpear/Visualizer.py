#! /usr/bin/python

import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

class Visualizer():
    """A Visualizer generates visualizations of data of converted grib file.
    Visualizers have the following properties:

    Attributes:
        mode: A string representing mode of the visualization
        gribFile: A string representing the name of grib file
        shapeFile: A string representing the name of shape file
                   (by default is shapefile of IN state)
    """

    def __init__(self, mode, gribFile):
        """Return a Visualizer to visualize data from *data* and
        generate the data visualization in *mode* mode
        """
        if mode is not None:
            self.mode = mode

        if gribFile is not None:
            self.gribFile = gribFile

        self.mode = 'static'
        self.gribFile = './sample_data/hrrr.t00z.wrfnatf00.grib2'
        # default shapeFile
        self.shapeFile = './shapefile/tl_2013_18_cousub/tl_2013_18_cousub'

    def visualize(self):
        """Visualize Data from gribFile
        """
        plt.figure(figsize=(7,12))
        grbs=pygrib.open(self.gribFile)
        grb = grbs.select(name='Temperature')[0]
        data=grb.values
        lat,lon = grb.latlons()

        # m = Basemap(resolution='l', # c, l, i, h, f or None
        #         projection='merc',
        #         lat_0=40.2, lon_0=-86.1,
        #         llcrnrlon=-88.1, llcrnrlat= 37.77,
        #         urcrnrlon=-84.78, urcrnrlat=41.76)

        m=Basemap(resolution='c',
                projection='merc',
                llcrnrlon=lon.min(), urcrnrlon=lon.max(),
                llcrnrlat=lat.min(),urcrnrlat=lat.max())

        x, y = m(lon,lat)
        cs = m.pcolormesh(x,y,data,
                        shading='flat',
                        cmap=plt.cm.jet)

        m.drawcoastlines()
        m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
        m.drawmapboundary(fill_color='#46bcec')
        plt.colorbar(cs,orientation='vertical')
        m.readshapefile(self.shapeFile,'areas')
        plt.show()


v = Visualizer(None, None)
v.visualize()
