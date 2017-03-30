import pygrib
import numpy
#import matplotlib.pyplot as plt

def DataSetAverage(data_set):
	total = 0
	for val in data_set:
		total+=val	
	
	return total/len(data_set) 	

def PointAverage(p_lat, p_lon, f_list, output_name):
	lat_max = p_lat+0.03623189
	lat_min = p_lat-0.03623189
	lon_max = p_lon+0.04753755
	lon_min = p_lon-0.04753755
	
	avg_temp_list = []

	for item in f_list:
		data, lats, lons= item.data(lat1=lat_min, lat2=lat_max, lon1=lon_min, lon2=lon_max)
		avg_temp = DataSetAverage(data)
		#print avg_temp
		avg_temp_list.append(avg_temp)
		#print avg_temp_list
	plt.plot(avg_temp_list)
	plt.show()
	plt.savefig(output_name)
	return avg_temp_list
PointAverage(40.427289, -86.914522, [pygrib.open('hrrr.t15z.wrfsubhf01.grib2').select(name='2 metre temperature')[0], pygrib.open('hrrr.t00z.wrfsfcf01.grib2').select(name='2 metre temperature')[0], pygrib.open('hrrr.t15z.wrfsubhf01.grib2').select(name='2 metre temperature')[0]])
			
