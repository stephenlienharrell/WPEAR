#! /usr/bin/python

import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D

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
        """Generate Heatmap with Data from grib object
        grib_object: an object containing raw data to be visualized
        file_name:   a string representing the name of generated picture
        """
        data = grib_object.values
        lat,lon = grib_object.latlons()
        unit = grib_object['units']
        data_type = grib_object['name']

        fig = plt.figure(figsize=(8,8))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

        m = Basemap(
                resolution='c', # c, l, i, h, f or None
                projection='cyl',
                lat_0=39.72, lon_0=-86.29,
                llcrnrlon=-87.79, llcrnrlat= 38.22,
                urcrnrlon=-84.79, urcrnrlat=41.22)

        parallels = np.arange(38.22, 41.22, 0.5)
        m.drawparallels(parallels,labels=[False,True,True,False])
        meridians = np.arange(-87.79, -84.79, 0.5)
        m.drawmeridians(meridians,labels=[True,False,False,True])

        x,y = m(lon, lat)
        cs = m.pcolormesh(x,y,data,
                        shading='flat',
                        cmap=plt.cm.jet)

        cbar = plt.colorbar(cs,location='bottom', fraction=0.046, pad=0.06)
        # Adjust the position of Unit
        cbar_ax = cbar.ax
        cbar_ax.text(0.0, -1.3, unit, horizontalalignment='left')
        m.readshapefile(self.shapeFile,'areas')
        plt.title(data_type)
        plt.savefig(file_name)
        # plt.show()


    def Scatter_Plot(self, grib_object, file_name):
        """Generate Scatter Plot with Data from grib object
        grib_object: an object containing raw data to be visualized
        file_name:   a string representing the name of generated picture
        """
        data = grib_object.values
        lat,lon = grib_object.latlons()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        size = len(lat) * len(lat[0])
        xs = lon.reshape(size, )
        ys = lat.reshape(size, )
        zs = data.reshape(size, )

        ax.plot(xs, ys, zs)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitudes') 
        ax.set_zlabel(grib_object['name'])
        # plt.savefig(file_name)
        plt.show()


# Make a static DataVisualizer(default)
v = DataVisualizer(None)

# Manually get grib data object
gribFile = './sample_data/hrrr.t00z.wrfnatf00.grib2'
grbs = pygrib.open(gribFile)
grb = grbs.select(name='Temperature')[0]

# Generate visualization
file_name = "out/pic.jpg"
# v.Heatmap(grb, file_name)
v.Scatter_Plot(grb, file_name)
