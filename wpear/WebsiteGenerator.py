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
    file_head = """
        <html>
          <head>
              <style type="text/css">
                  body {
                      background-color: #EAEDED
                  }
                  ul.rig {
                      list-style: none;
                      font-size: 0px;
                      margin-left: -2.5%; /* should match li left margin */
                  }
                  ul.rig li {
                      display: inline-block;
                      padding: 10px;
                      font-size: 16px;
                      font-size: 1rem;
                      vertical-align: top;
                      box-sizing: border-box;
                      -moz-box-sizing: border-box;
                      -webkit-box-sizing: border-box;
                  }
                  ul.rig li img {
                      max-width: 100%;
                      height: auto;
                      margin: 0 0 10px;
                  }
                  ul.rig li h3 {
                      margin: 0 0 5px;
                  }
                  ul.rig li p {
                      font-size: .9em;
                      line-height: 1.5em;
                      color: #999;
                  }

                  /* class for 2 columns */
                  ul.rig.columns-2 li {
                      width: 47.5%; /* this value + 2.5 should = 50% */
                  }
                  /* class for 3 columns */
                  ul.rig.columns-3 li {
                      width: 30.83%; /* this value + 2.5 should = 33% */
                  }
                  /* class for 4 columns */
                  ul.rig.columns-4 li {
                      width: 22.5%; /* this value + 2.5 should = 25% */
                  }
                   
                  @media (max-width: 480px) {
                      ul.grid-nav li {
                          display: block;
                          margin: 0 0 5px;
                      }
                      ul.grid-nav li a {
                          display: block;
                      }
                      ul.rig {
                          margin-left: 0;
                      }
                      ul.rig li {
                          width: 100% !important; /* over-ride all li styles */
                          margin: 0 0 20px;
                      }
                  }
                  
              </style>
          </head>
          <body>
              <center>
              <h1>
                  <br>
                  WPEAR
              </h1>
              <ul class='rig columns-2'>"""

    self.landing_main.write(file_head)
    image_titles = ['Observation Visualization', 
                    'Forcast Visualization', 
                    'Standard Deviation Visualization', 
                    'Observation vs Forcast Visualization']

    self.landing_main.write("<li><img src='" + item_list[0] + "' /><h3>"
        + image_titles[0] + "</h3></li>")
    self.landing_main.write("<li><img src='" + item_list[1] + "' /><h3>"
        + image_titles[1] + "</h3></li></ul>")
    self.landing_main.write("<ul class='rig columns-2'>")
    self.landing_main.write("<li><img src='" + item_list[2] + "' /><h3>"
        + image_titles[2] + "</h3></li>")
    self.landing_main.write("<li><img src='" + item_list[3] + "' /><h3>"
        + image_titles[3] + "</h3></li></ul>")

    file_end = """</center></body></html>"""
    self.landing_main.write(file_end)
    self.landing_main.close()

    webbrowser.open_new(self.landing_page_url)


# showWebsite(['SECTION:Forecast', ['img.jpg', 'file_1'], ['img.jpg', 'file_2'], 'SECTION:Observed'])
w = WebsiteGenerator()
img = "/home/maoxia/Desktop/pic.png"
w.showHomePage([img, img, img, img])