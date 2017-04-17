import webbrowser, os


class WebsiteGenerator:


  landing_page = None
  landing_sidebar = None
  landing_main = None
  landing_page_url = None
  landing_sidebar_url = 'website/wpear_landing_sidebar.html'
  landing_main_url = 'website/wpear_landing_main.html'


  def __init__(self, file_name='website/index.html'):
    # create website directory
    cwd = os.getcwd()
    website_dir = cwd+'/website'
    if not os.path.exists(website_dir):
      os.makedirs(website_dir)

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
                <NOFRAMES>
              """
    self.landing_page.write(sidebar)


  def showHomePage(self, item_list):
    # Can make different types of viz with different colors
    file_head = """<html><head>
    <title>WPEAR</title>
    <body style="background-color: #EAEDED; height: 100%"><center><h1><br>WPEAR</h1>"""
    self.landing_main.write(file_head)

    for item in item_list:
      if 'SECTION:' in item:
        if item != item_list[0]:
            self.landing_main.write("""</div>""")
        self.landing_main.write("""<br><div id = """ + item.split(':')[1] +""""><h2><p>""" +  item.split(':')[1] + """</p></h2>""")
      elif len(item) > 1:
        self.landing_main.write("""<img src='""" + item[0] + """' alt='""" + item[1] + """'><br>""")
        self.landing_main.write("""<br>""")

    file_end = """</center></body></html>"""
    self.landing_main.write(file_end)
    self.landing_main.close()

    webbrowser.open_new(self.landing_page_url)


# showWebsite(['SECTION:Forecast', ['img.jpg', 'file_1'], ['img.jpg', 'file_2'], 'SECTION:Observed'])
# w = WebsiteGenerator()
# forcst_img = "/home/maoxia/Desktop/WPEAR/wpear/sample_data/hrrr_fcast.20170415_t00z.2MT_DPT.IND90k.wrfsfcf01.heatmap.png"
# obs_img = "/home/maoxia/Desktop/WPEAR/wpear/sample_data/rtma_obs.20170415_t00z.2MT_DPT.IND90k.2dvaranl_ndfd.heatmap.png"
# diff_img = "/home/maoxia/Desktop/WPEAR/wpear/sample_data/hrrr_fcast.20170415_t00z.2MT_DPT.IND90k.wrfsfc.heatmap_anim.gif"
# w.showHomePage(['SECTION:Forecast', [forcst_img, 'file_1',], 'SECTION:Observed', [obs_img, 'file_2'], 'SECTION:Forecast vs Observed', [diff_img, 'file_3']])