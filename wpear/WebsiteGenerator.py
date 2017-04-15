import webbrowser


class WebsiteGenerator:


  landing_page = None
  landing_sidebar = None
  landing_main = None
  landing_page_url = None
  landing_sidebar_url = 'wpear_landing_sidebar.html'
  landing_main_url = 'wpear_landing_main.html'


  def __init__(self, file_name='index.html'):
    self.landing_page_url = file_name
    self.landing_page = open(file_name, 'w+')
    self.landing_sidebar = open(self.landing_sidebar_url, 'w+')
    self.landing_main = open(self.landing_main_url, 'w+')
    self.addSidebar()

  def showWebsite(self, item_list):
    file_head = """<html><head>
    <title>WPEAR</title>
    <body style="background-color: #EAEDED;"><center><p><h1><br>WPEAR</h1></p>"""
    self.landing_main.write(file_head)

    for item in item_list:
      if 'SECTION:' in item:
        if item != item_list[0]:
            self.landing_main.write("""</div>""")
        self.landing_main.write("""<br><div id = """ + item.split(':')[1] +""""><h2><p>""" +  item.split(':')[1] + """</p></h2>""")
      elif len(item) > 1:
        self.landing_main.write("""<h3>""" + item[1] + """</h3><img src='""" + item[0] + """' alt='""" + item[1] + """'><br>""")
        self.landing_main.write("""<br>""")
    # <h2>""" + observed_name + """ Visualization</h2>
    # <img src='""" + observed_image + """' alt="Observed file" >
    # <h2>Compared Visualization</h2>
    # <img src='""" + compared_image + """' alt="Compared file" >

    file_end = """</center></body></html>"""
    self.landing_main.write(file_end)
    self.landing_main.close()

    webbrowser.open_new(self.landing_page_url)


  def addSidebar(self):
    sidebar = """
    <HTML>
    <HEAD>
      <TITLE>Weather Prediction Evaluation and Reporting (WPEAR)</TITLE>
    </HEAD>
    <FRAMESET cols=20%,*>
    <FRAME src="wpear_landing_sidebar.html" noresize frameborder="0" frameborder="0" scrolling="auto" />
    <FRAME src="wpear_landing_main.html" name="page" noresize frameborder="0" scrolling="auto" />
    </frameset>
    <NOFRAMES>"""
    self.landing_page.write(sidebar)





# showWebsite(['SECTION:Forecast', ['img.jpg', 'file_1'], ['img.jpg', 'file_2'], 'SECTION:Observed'])