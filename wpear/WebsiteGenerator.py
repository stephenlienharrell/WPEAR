#from selenium import webdriver
import webbrowser

def showWebsite(item_list):
    html_file = open('main.html', 'w+')
    file_head = """<html><head>
    <title>WPEAR</title>
    <body style="background-color: #EAEDED;"><center><p><h1><br>WPEAR</h1></center>"""
    html_file.write(file_head)
    image_size = """'padding:20px;width:375px;height:500px;'"""

    for item in item_list:
        if 'SECTION:' in item:
            if item != item_list[0]:
                html_file.write("""<p style="clear: both;"><hr>""")
            html_file.write("""<br><center><h2><p>""" +  item.split(':')[1] + """</p></h2></center>""")
        elif len(item) > 1:
            html_file.write("""<p style="float:left;font-size:16pt;text-align:center;width:23%;margin-right:2%;">&emsp;""")
            html_file.write(item[1] + """<img src='""" + item[0] + """' alt='""" + item[1] +
                """' style="""+ image_size + """'></p>""")

    file_end = """</body></html>"""
    html_file.write(file_end)
    html_file.close()

    webbrowser.open_new('main.html')

def parseDirectory(file_name):
    directory = "web/"


showWebsite(['SECTION:Forecast', ['giphy.gif', 'file_1'], ['giphy.gif', 'file_2'], ['giphy.gif', 'file_3'], ['giphy.gif', 'file_4'],
['giphy.gif', 'file_1'], ['giphy.gif', 'file_2'], ['giphy.gif', 'file_3'], ['giphy.gif', 'file_4'],
             'SECTION:Observed'])
