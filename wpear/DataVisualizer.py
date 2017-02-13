#! /usr/bin/python

import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

class DataVisualizer():
    """A DataVisualizer generates visualizations of data from converted grib file.
    DataVisualizers have the following properties:

    Attributes:
        mode: A string representing mode of the visualization
        shapeFile: A string representing the name of shape file
    """

    def __init__(self, mode):
        """Return a DataVisualizer generating the data visualization
        in *mode* mode
        """
        if mode is not None:
            self.mode = mode

        self.mode = 'static'
        # default shapeFile
        self.shapeFile = './shapefile/tl_2013_18_cousub/tl_2013_18_cousub'


    def K2F(self, temperatures):
        """Convert temperatures in Kelvin to Fahrenheit
        temperatures: N-dimensional array containing temperatures data in Kelvin
        """
        return temperatures * 1.8 - 459.67


    def Heatmap(self, grib_object, file_name):
        """Visualize Data from grib object
        grib_object: an object containing raw data to be visualized
        file_name:   a string representing the name of generated picture
        """
        data = grib_object.values
        lat,lon = grib_object.latlons()
        unit = grib_object['units']
        data_type = grib_object['name']

        fig = plt.figure(figsize=(7,12))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

        m = Basemap(
                width=9000000,
                height=12000000,
                resolution='c', # c, l, i, h, f or None
                projection='lcc',
                lat_0=40.2, lon_0=-86.1,
                llcrnrlon=-88.1, llcrnrlat= 37.77,
                urcrnrlon=-84.78, urcrnrlat=41.76)

        x, y = m(lon,lat)
        cs = m.pcolormesh(x,y,data,
                        shading='flat',
                        cmap=plt.cm.jet)

        cbar = m.colorbar(cs,location='bottom', pad=0.05,
                          spacing='proportional')
        cbar_ax = cbar.ax
        cbar_ax.text(0.0, -1.0, unit, horizontalalignment='left')
        m.readshapefile(self.shapeFile,'areas')
        plt.title(data_type)
        plt.savefig(file_name)


# Make a static DataVisualizer(default)
v = DataVisualizer(None)

# Manually get grib data object
gribFile = './sample_data/hrrr.t00z.wrfnatf00.grib2'
grbs = pygrib.open(gribFile)
grb = grbs.select(name='Vertical velocity')[0]

# Generate visualization
file_name = "out/pic.jpg"
v.Heatmap(grb, file_name)
