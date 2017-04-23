#from selenium import webdriver
import webbrowser
import os.path

def showWebsite(item_list):
    dir = parseDirectory('web/', '')
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
            html_file.write("""<p style="float:left;font-size:18pt;text-align:center;min-width:550px;margin-right:3%;">&nbsp;&nbsp;&nbsp;&nbsp;""")
            html_file.write(item[1] + """<img src='""" + item[0] + """' alt='""" + item[1] +
                """' style="""+ image_size + """'></p>""")
        #if len(item) > 2:
        #    html_file.write(item[2])

    file_end = """</body></html>"""
    html_file.write(file_end)
    html_file.close()

    webbrowser.open_new(file_fullpath)

def parseDirectory(webdir, file_name):
    file_name = "hrrr_fcast.20170413_t00z.2MT_DPT.IND90k.wrfsfcf01.grb2"
    directory = webdir
    if directory.endswith('/') == False:
        directory += '/'

    seg = file_name.partition('.')
    date_part = seg[len(seg)-1]
    file_part = seg[0]

    year = date_part[:4]
    month = date_part[4:6]
    day = date_part[6:8]

    directory+= year + '/' + month + '/' + day + '/'
    return directory

#showWebsite(['SECTION:Forecast', ['giphy.gif', 'file_1'], ['giphy.gif', 'file_2'], ['giphy.gif', 'file_3'], ['giphy.gif', 'file_4'],['giphy.gif', 'file_1'], ['giphy.gif', 'file_2'], ['giphy.gif', 'file_3'], ['giphy.gif', 'file_4'],'SECTION:Observed'])
