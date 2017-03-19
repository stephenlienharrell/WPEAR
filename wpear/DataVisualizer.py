#!/usr/bin/env python

import os
import sys
import pygrib
import random
import imageio
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D

class DataVisualizer():
    """A DataVisualizer generates visualizations of data from converted grib file.
    DataVisualizers have the following properties:

    Attributes:
        shapeFile: A string representing the name of shape file
    """

    def __init__(self):
        """Return a DataVisualizer generating the data visualization
        """
        # default shapeFile
        self.shapeFile = './shapefile/tl_2013_18_cousub/tl_2013_18_cousub'


    def K2F(self, temperatures):
        """Convert temperatures in Kelvin to Fahrenheit
        temperatures: N-dimensional array containing temperatures data in Kelvin
        """
        return temperatures * 1.8 - 459.67


    def setPlotLabels(self, ax, grib_object):
        """Set labels for the plot
        ax: axis object
        grib_object: an object containing raw data to be visualized
        """
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitudes')
        ax.set_zlabel(grib_object['name'] + '(' + grib_object['units'] + ')')


    def setTitle(self, ax, grib_object):
        """Set title for plot
        grib_object: an object containing raw data to be visualized
        """
        plt.title(grib_object['name'])
        tlt = ax.title
        tlt.set_position([0.6, 1])


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
        plt.close(fig)

    
    def Frame(self, grib_object, file_name, vmin, vmax):
        """Generate a Heatmap as one frame for final GIF product
        grib_object:    an object containing raw data to be visualized
        file_name:   a string representing the name of generated picture
        vmin:        lower limit
        vmax:        upper limit 
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
        bounds = np.linspace(vmin, vmax, 10)
        norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
        # norm = mpl.colors.Normalize(vmin=vmin,vmax=vmax)

        cs = m.pcolormesh(x,y,data,
                        shading='gouraud',
                        norm=norm,
                        cmap=plt.cm.jet)


        cbar = plt.colorbar(cs,location='bottom', fraction=0.046, pad=0.06)
        
        # Adjust the position of Unit
        cbar_ax = cbar.ax
        cbar_ax.text(0.0, -1.3, unit, horizontalalignment='left')
        m.readshapefile(self.shapeFile,'areas')
        plt.title(data_type)
        plt.savefig(file_name)
        plt.close(fig)    


    def Animated(self, grib_objects, file_name):
        """Generate Animated Heatmap with Data from grib_objects
        grib_objects:   a list of grib objects
        file_name:      a string representing the name of generated picture
        """
        filenames = []
        images = []
        count = 0
        vmin = sys.maxint
        vmax = -vmin - 1

        while (count < len(grib_objects)):
            filenames.append('tmp/' + 'pic_' + str(count) + '.jpg')
            # Get min and max among all data
            if grib_objects[count]['maximum'] > vmax:
                vmax = grib_objects[count]['maximum']

            if grib_objects[count]['minimum'] < vmin:
                vmin = grib_objects[count]['minimum']
            count += 1

        while (count > 0):
            index = len(grib_objects) - count
            self.Frame(grib_objects[index], filenames[index], vmin, vmax)
            print 'File ' + filenames[index] + " generated"
            count -= 1

        for filename in filenames:
            images.append(imageio.imread(filename))

        kargs = { 'duration' : 0.5 }
        imageio.mimsave(file_name, images, 'GIF', **kargs)

        # remove tmp files in tmp dir
        # for f in filenames:
            # os.remove(f)


    def SimplePlot(self, grib_object, file_name):
        """Generate Basic 3D Stat Plot with Data from grib object
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

        ax.plot(xs, ys, zs, color = 'black')

        self.setPlotLabels(ax, grib_object)
        self.setTitle(ax, grib_object)

        plt.savefig(file_name)


    def WireframePlot(self, grib_object, file_name):
        """Generate 3D Wireframe Plot with Data from grib object
        grib_object: an object containing raw data to be visualized
        file_name:   a string representing the name of generated picture
        """
        data = grib_object.values
        lat,lon = grib_object.latlons()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x = lon
        y = lat
        z = data

        ax.plot_wireframe(x, y, z, rstride=1210, cstride=1210)

        self.setPlotLabels(ax, grib_object)
        self.setTitle(ax, grib_object)

        plt.savefig(file_name)


    def SurfacePlot(self, grib_object, file_name):
        """Generate a 3D surface colored plot
        grib_object: an object containing raw data to be visualized
        file_name:   a string representing the name of generated picture
        """
        data = grib_object.values
        lat,lon = grib_object.latlons()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x = lon
        y = lat
        z = data

        surf = ax.plot_surface(x, y, z, cmap=plt.cm.coolwarm,
                               rstride=15, cstride=15,
                               linewidth=0, antialiased=False)
        # Set Lables
        self.setPlotLabels(ax, grib_object)
        self.setTitle(ax, grib_object)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.savefig(file_name)


    def ScatterPlot(self, grib_object, file_name):
        """Generate 3D Scatter Plot
        grib_object: an object containing raw data to be visualized
        file_name:   a string representing the name of generated picture
        """
        data = grib_object.values
        lat,lon = grib_object.latlons()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        N = len(lon) * len(lon[0])
        xs = lon.reshape(N, )
        ys = lat.reshape(N, )
        zs = data.reshape(N, )

        idx = random.sample(range(N), 1000)

        ax.scatter(xs[idx], ys[idx], zs[idx], alpha=0.5,cmap=plt.cm.flag)
        # Set Lables
        self.setPlotLabels(ax, grib_object)
        self.setTitle(ax, grib_object)
        plt.savefig(file_name)



# Make a static DataVisualizer(default)
v = DataVisualizer()

# Manually get grib data object
# gribFile = './sample_data/hrrr.t00z.wrfsfcf00.grib2'
# grbs = pygrib.open(gribFile)
# grb = grbs.select(name='Temperature')[0]

# Generate static visualization
# file_name = "out/pic.jpg"
# v.Heatmap(grb, file_name)
# grbs.close()

# Manually get list of grib data object
msgs = []
indir = 'sample_data'
for root, dirs, filenames in os.walk(indir):
    for filename in filenames:
        grbs = pygrib.open(os.path.join(root,filename))
        grb = grbs.select(name='Temperature')[0]
        msgs.append(grb)
        grbs.close

# Generate animated visualization
file_name = "out/pic.gif"
v.Animated(msgs, file_name)


# v.SimplePlot(grb, file_name)
# v.WireframePlot(grb, file_name)
# v.SurfacePlot(grb, file_name)
#v.ScatterPlot(grb, file_name)
