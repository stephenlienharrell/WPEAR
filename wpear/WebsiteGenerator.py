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




################################### Test run  script ####################################
# wg = WebsiteGenerator(webdir='web')
# wg.addSidebarToLandingPage()
# wg.showWebsite()
