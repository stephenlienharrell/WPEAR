import pygrib
import numpy



class DataComparator:
  

  def difference(self, forecast_file, observed_file): 
    print 'using difference'
    grbs_f = pygrib.open(forecast_file)
    grbs_o = pygrib.open(observed_file)
    
    temp15_arr_f = grbs_f.select(name='2 metre temperature')[0]
    temp15_arr_o = grbs_o.select(name='2 metre temperature')[0]

    arr = temp15_arr_f.values - temp15_arr_o.values
    ret_file = pygrib.open(forecast_file)
    gobj = ret_file.select(name='2 metre temperature')[0]
    gobj.values=numpy.array(arr)
    return gobj

#DataComparator('hrrr.t15z.wrfsubhf01.grib2', 'hrrr.t15z.wrfsubhf01.grib2')
