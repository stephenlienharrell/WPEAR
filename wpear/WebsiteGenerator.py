#from selenium import webdriver
import webbrowser

def showWebsite(forecast_image, observed_image, compared_image, time):
    html_file = open('main.html', 'w+')
    file_head = """<html><head>
    <title>WPEAR Website</title>
    <body><p><center>WPEAR Website</center></p>
    <p>Displaying the visualizations for """ + time + """</p>
    <h2>Forecast Visualization</h2>
    <img src='""" + forecast_image + """' alt="Forecast file" style="width:304px;height:228px;">
    <h2>Observed Visualization</h2>
    <img src='""" + observed_image + """' alt="Observed file" style="width:304px;height:228px;">
    <h2>Compared Visualization</h2>
    <img src='""" + compared_image + """' alt="Compared file" style="width:304px;height:228px;">
    </body></html>"""

    html_file.write(file_head)
    html_file.close()

    webbrowser.open_new('main.html')
    pass