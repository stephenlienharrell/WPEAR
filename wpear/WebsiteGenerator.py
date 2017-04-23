#from selenium import webdriver
import webbrowser
import os.path

def showWebsite(file_dir, item_list):
    obs_file = next(item for item in item_list if (len(item)==2) & (item[1]=='obs'))[0]
    dir = parseDirectory(file_dir, obs_file)
    dir = os.path.normpath(dir + 'day.html')
    file_fullpath = os.path.realpath(dir)
    html_file = open(file_fullpath, 'w+')

    file_head = """<html><head>
    <font size="3"><title>WPEAR</title>
    <body style="background-color: #EAEDED;"><center><p><h1><br>WPEAR</h1></center>"""
    html_file.write(file_head)
    image_size = """'padding-left:60px; padding-right:60px;padding-top:20px;padding-bottom:20px;width:100%;height:80%;'"""

    for item in item_list:
        if 'SECTION:' in item:
            if item != item_list[0]:
                html_file.write("""<p style="clear: both;"><hr>""")
            html_file.write("""<br><center><h2><p>""" +  item.split(':')[1] + """</p></h2></center>""")
            continue
        elif len(item) > 1:
            title = generateTitle(obs_file, item[0])
            html_file.write("""<p style="float:left;font-size:18pt;text-align:center;min-width:550px;margin-right:3%;">&nbsp;&nbsp;&nbsp;&nbsp;""")
            html_file.write(title + """<img src='""" + item[0] + """' alt='""" + item[1] +
                """' style="""+ image_size + """'></p>""")

    file_end = """</body></html>"""
    html_file.write(file_end)
    html_file.close()

    webbrowser.open_new(file_fullpath)

def parseDirectory(webdir, file_name):
    directory = webdir
    if directory.endswith('/') == False:
        directory += '/'

    seg = file_name.partition('.')
    date_part = seg[len(seg)-1]

    year = date_part[:4]
    month = date_part[4:6]
    day = date_part[6:8]

    directory+= year + '/' + month + '/' + day + '/'
    return directory

def generateTitle(obs_name, file_name):
    name = ""

    # Observed file processing
    obs_seg = obs_name.partition('.')
    datehour_obs = obs_seg[len(obs_seg) - 1]
    date_obs = datehour_obs.partition('_')[0]
    hour_obs = datehour_obs.partition('_')[2]
    obs_hour = hour_obs[1:3]

    #Second file processing
    file_seg = file_name.partition('.')
    datehour_file = file_seg[len(obs_seg) - 1]
    hour_file = datehour_file.partition('_')[2]
    file_hour = hour_file[1:3]

    diff = (int(obs_hour) - int(file_hour)) % 24

    if "fcast" in file_name:
        name+="Forecast from " + str(diff)
        if diff == 1:
            name += " hour ago"
        else:
            name += " hours ago"
    elif "obs" in file_name:
        name+="Observed weather at " + obs_hour + ":00"

    return name
#showWebsite('web/',['SECTION:Forecast', ['rtma_obs.20170419_t01z.2MT_DPT.IND90k.2dvaranl_ndfd.heatmap.png', 'obs'], ['hrrr_fcast.20170419_t00z.2MT_DPT.IND90k.wrfsfc.heatmap_anim.gif', 'fcast'], ['hrrr_fcast.20170418_t23z.2MT_DPT.IND90k.wrfsfc.heatmap_anim.gif', 'fcast'], 'SECTION:Observed'])
