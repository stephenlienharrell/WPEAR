import webbrowser, os
from os import walk


class WebsiteGenerator:

  
  def __init__(self, webdir, landing_file='index.html', sidebar_file='sidebar.html'):
    
    self.landing_file = webdir + '/' + landing_file
    self.sidebar_file = webdir + '/' + sidebar_file
    self.landing_page = open(self.landing_file, 'w+')
    self.sidebar_page = open(self.sidebar_file, 'w+')
    self.webdir = webdir
    

  def showWebsite(self):
    webbrowser.open_new(self.landing_file)


  def addSidebarToLandingPage(self):
    sidebar = """
                <HTML>
                <HEAD>
                  <TITLE>Weather Prediction Evaluation and Reporting (WPEAR)</TITLE>
                </HEAD>
                <FRAMESET cols=20%,*>
                <FRAME src="{}" noresize frameborder="0" frameborder="0" scrolling="auto" />
                <FRAME src="" name="page" noresize frameborder="0" scrolling="auto" />
                </frameset>
                <NOFRAMES>
              """.format(self.sidebar_file.split('/')[-1])
    self.landing_page.write(sidebar)
    self.sidebarHandler()



  def sidebarHandler(self):
    self._writeSidebarHead()
    self._writeSidebarBodyHeader()

    years = []
    for (dirpath, dirnames, filenames) in walk(self.webdir):
      years.extend(dirnames)
      break
    years.sort()
    for year in years:
      yeardir = self.webdir + '/' + year
      months = []
      self._writeYearStart(year)
      
      for (ydirpath, ydirnames, yfilenames) in walk(yeardir):
        months.extend(ydirnames)
        break
      months.sort()
      for month in months:
        monthdir = yeardir + '/' + month
        days = []
        self._writeMonthStart(month)

        for (mdirpath, mdirnames, mfilenames) in walk(monthdir):
          days.extend(mdirnames)
          break
        days.sort()
        for day in days:
          self._writeDay(day, monthdir + '/' + day + '/day.html')  

        self._writeMonthEnd()
      self._writeYearEnd()

    # self._writeYearStart('2017')
    # self._writeMonthStart('Jan')
    # self._writeDay('12', 'index.html')
    # self._writeDay('13', 'http://www.crh.noaa.gov/product.php?site=ind&product=AFD&issuedby=IND&glossary=0')
    # self._writeMonthEnd()
    # self._writeMonthStart('Dec')
    # self._writeDay('12', 'index.html')
    # self._writeDay('13', 'index2.html')
    # self._writeMonthEnd()
    # self._writeYearEnd()

    # self._writeYearStart('2016')
    # self._writeMonthStart('Jan')
    # self._writeDay('12', 'index.html')
    # self._writeDay('13', 'index2.html')
    # self._writeMonthEnd()
    # self._writeMonthStart('Dec')
    # self._writeDay('12', 'index.html')
    # self._writeDay('13', 'index2.html')
    # self._writeMonthEnd()
    # self._writeYearEnd()

    self._writeSidebarBodyFooter()




  def _writeSidebarHead(self):
    head = """
          <!DOCTYPE html>
          <html>
          <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css">
            <script src="https://code.jquery.com/jquery-1.11.3.min.js"></script>
            <script src="https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
            <style>
              .custom-btn {
                  width: 9px !important;
            }
            </style>
          </head> """
    self.sidebar_page.write(head)      

   
  def _writeSidebarBodyHeader(self, title='WPEAR'):
    entry = """
              <body>
              <div data-role="page" id="pageone">
                <div data-role="header">
                  <h1>%s</h1>
                </div>
                <div data-role="main" class="ui-content">
                  <h2>Calendar</h2>""" % (title)
    self.sidebar_page.write(entry)    


  def _writeSidebarBodyFooter(self):
    exit = """
              </div>
              <div data-role="footer">
                <h1>Created by: Stephen Harrell,  <br/> Lala Vaishno De,  <br/> Mengxue Luo,  <br/> Dhairya Doshi</h1>
              </div>

            </div> 

          </body>
          </html>"""
    self.sidebar_page.write(exit)


  def _writeYearStart(self, year):
    text = """
              <div data-role="collapsible"  >
              <h4>%s</h4>
              <ul data-role="listview">""" % (year)
    self.sidebar_page.write(text)


  def _writeYearEnd(self):
    text = """
              </ul>
            </div>"""
    self.sidebar_page.write(text)


  def _writeMonthStart(self, month):
    text = """
              <div data-role="collapsible">
                <h4>%s</h4>    
                  <ul data-role="listview">
                    <div data-role="controlgroup" data-type="horizontal"  >""" % (month)
    self.sidebar_page.write(text)


  def _writeMonthEnd(self):
    text = """
                </div>
              </ul>
            </div>"""
    self.sidebar_page.write(text)


  def _writeDay(self, day, url):
    text = """
              <a target="page" href="%s" data-role="button" class="custom-btn">%s</a></li>""" % (url, day)
    self.sidebar_page.write(text)

  
  def getLocalDirs(self, path):
    dirs = []
    for(dirpath, dirnames, filenames) in walk(path):
      dirs.extend(dirnames)
      break
    return dirs

  def getLocalFiles(self, path):  
    files = []
    for(dirpath, dirnames, filenames) in walk(path):
      files.extend(filenames)
      break
    return files


  def generateDailyPage(self, file_dir, item_list):
    dir = parseDirectory(file_dir, next(item for item in item_list if len(item)==2)[0])
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


  def parseDirectory(self, webdir, file_name):
      #file_name = "hrrr_fcast.20170413_t00z.2MT_DPT.IND90k.wrfsfcf01.grb2"
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


  def parseDayDirectory(self, file_name):
    # file_name = "web/2017/04/23/hrrr_fcast/hrrr_fcast.20170423_t00z.2MT_DPT.IND90k.wrfsfcf01.heatmap.png"
    seg = file_name.split('/')
    directory = ''
    for i in range(4):
      directory += seg[i] + '/'
    return directory


  def generateHomePage(self, item_list):
    image_titles = ['Observation Visualization', 
                    'Forcast Visualization', 
                    'Standard Deviation Visualization', 
                    'Observation vs Forcast Visualization']

    cur_dir = os.getcwd() + '/'
    dir = self.parseDayDirectory(item_list['forecast_viz'])
    dir = os.path.normpath(dir + 'demo.html')
    file_fullpath = os.path.realpath(dir)
    html_file = open(file_fullpath, 'w+')
    # html_file = self.landing_page

    self._writeHomePageHeader(html_file)
    page_prefix = """
              <body>
              <center>
              <h1>
                  <br>
                  WPEAR
              </h1>
              <ul class='rig columns-2'>"""

    html_file.write(page_prefix)
    
    html_file.write("<li><img src='" + cur_dir + item_list['observation_viz'] + "' alt='observation' /><h3>"
        + image_titles[0] + "</h3> <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p> </li>")
    html_file.write("<li><img src='" + cur_dir + item_list['forecast_viz'] + "' alt='forecast' /><h3>"
        + image_titles[1] + "</h3></li></ul>")
    html_file.write("<ul class='rig columns-2'>")
    html_file.write("<li><img src='" + cur_dir + item_list['stdv_viz'] + "' alt='standard deviation'/><h3>"
        + image_titles[2] + "</h3></li>")
    html_file.write("<li><img src='" + cur_dir + item_list['animated_diff_viz'] + "' alt='animated difference' /><h3>"
        + image_titles[3] + "</h3></li></ul>")

    file_end = """</center></body></html>"""
    html_file.write(file_end)
    html_file.close()


  def _writeHomePageHeader(self, html_file):
    file_head = """
        <html>
          <head>
              <style type="text/css">
                  body {
                      #background-color: #EAEDED
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
          </head>"""
    html_file.write(file_head)

    
################################### Test run  script ####################################
# wg = WebsiteGenerator(webdir='web')
# wg.addSidebarToLandingPage()
# wg.showWebsite()