#from selenium import webdriver
import webbrowser

def showWebsite(item_list):
    html_file = open('main.html', 'w+')
    file_head = """<html><head>
    <title>WPEAR</title>
    <body style="background-color: #EAEDED;"><center><p><h1><br>WPEAR</h1></p>"""
    html_file.write(file_head)

    for item in item_list:
        if 'SECTION:' in item:
            if item != item_list[0]:
                html_file.write("""</div>""")
            html_file.write("""<br><div id = """ + item.split(':')[1] +""""><h2><p>""" +  item.split(':')[1] + """</p></h2>""")
        elif len(item) > 1:
            html_file.write("""<h3>""" + item[1] + """</h3><img src='""" + item[0] + """' alt='""" + item[1] + """'><br>""")
            html_file.write("""<br>""")
    # <h2>""" + observed_name + """ Visualization</h2>
    # <img src='""" + observed_image + """' alt="Observed file" >
    # <h2>Compared Visualization</h2>
    # <img src='""" + compared_image + """' alt="Compared file" >

    file_end = """</center></body></html>"""
    html_file.write(file_end)
    html_file.close()

    webbrowser.open_new('main.html')



# showWebsite(['SECTION:Forecast', ['img.jpg', 'file_1'], ['img.jpg', 'file_2'], 'SECTION:Observed'])