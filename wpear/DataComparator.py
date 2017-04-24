import pygrib
import numpy as np


class DataComparator:
  

  def difference(self, forecast_file, observed_file): 
    grbs_f = pygrib.open(forecast_file)
    grbs_o = pygrib.open(observed_file)
    
    temp15_arr_f = grbs_f.select(name='2 metre temperature')[0]
    temp15_arr_o = grbs_o.select(name='2 metre temperature')[0]

    arr = temp15_arr_f.values - temp15_arr_o.values
    ret_file = pygrib.open(forecast_file)
    gobj = ret_file.select(name='2 metre temperature')[0]
    gobj.values=np.array(arr)
    return gobj


  def stddev(self, forecast_file_list, observed_file, var):
    'forecast_file_list must be in descending order of times e.g. 11, 10, 9 with obs = 12'
    arr = [[0 for i in range(len(forecast_file_list))] for j in range(3)]
    
    gfile_o = pygrib.open(observed_file)
    gobj_o = gfile_o.select(name='{}'.format(var))[0]
    arr[0][0] = np.mean(gobj_o.values) 
    arr[0][1] = np.std(gobj_o.values)
    
    i = 0
    for file in forecast_file_list:
      gfile_f = pygrib.open(file)
      gobj_f = gfile_f.select(name='{}'.format(var))[0]
      arr[1][i] = np.mean(gobj_f.values)
      arr[2][i] = np.std(gobj_f.values)
      i += 1

    # print arr
    return arr