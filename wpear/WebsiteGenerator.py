#from selenium import webdriver
import webbrowser

def showWebsite(forecast_image, forecast_name, observed_image, observed_name, compared_image):
    html_file = open('main.html', 'w+')
    file_head = """<html><head>
    <title>WPEAR Website</title>
    <body><center><p>WPEAR</p>
    <h2>""" + forecast_name  + """ Visualization</h2>
    <img src='""" + forecast_image + """' alt="Forecast file" >
    <h2>""" + observed_name + """ Visualization</h2>
    <img src='""" + observed_image + """' alt="Observed file" >
    <h2>Compared Visualization</h2>
    <img src='""" + compared_image + """' alt="Compared file" >
    </center></body></html>"""

    html_file.write(file_head)
    html_file.close()

    webbrowser.open_new('main.html')
    pass
