import webbrowser, os, datetime
from os import walk
import glob

class WebsiteGenerator:

  
  def __init__(self, hrrr_fcast, rtma_obs, webdir, landing_file='index.html', sidebar_file='sidebar.html'):
    
    self.landing_file = webdir + '/' + landing_file
    self.sidebar_file = webdir + '/' + sidebar_file
    self.landing_page = open(self.landing_file, 'w+')
    self.sidebar_page = open(self.sidebar_file, 'w+')
    self.webdir = webdir
    self.now = datetime.datetime.utcnow()
    self.rtma_obs = rtma_obs
    self.hrrr_fcast = hrrr_fcast


  def runWebManager(self, hrrr_fcast, rtma_obs):

    homepage_url = self.getHomePage(rtma_obs, hrrr_fcast)
    if homepage_url is None:
        return
    self.addSidebarToLandingPage(homepage_url)

    now = datetime.datetime.utcnow()
    first_dir = self.getFirstDay()
    first_day = first_dir[len(first_dir) - 2:]
    # #print first_day
    #day = int(first_day)
    day = self.hrrr_fcast.date.day

    dir = first_dir[:len(first_dir) - 2]

#    while day <= now.day:
#      ##print day
#      diff_list = self.generatePNGList('ADIF', dir, '/*.gif')
#      fcast_list = self.generatePNGList('hrrr_fcast', dir, '/*.gif')
#      rtma_list = self.generatePNGList('rtma_obs', dir, '/*.png')
#      std_dev_list = self.generatePNGList('stddev', dir, '/*.png')
#      # #print diff_list
#      if day != now.day:
#        end_hour = 24
#      else:
#        end_hour = now.hour
#
#      adif_list = []
#      adif_list.append("SECTION:Animated Difference GIFs")
#      for item in diff_list:
#        if item not in adif_list:
#            adif_list.append([item, "diff"])
#
#

    if day != now.day:
      end_hour = 24
    else:
      end_hour = now.hour

#    while list_hour < end_hour:
#      file_list.append(self.generateSectionTitle(day, list_hour))


    fcast_list = []
    for file in self.hrrr_fcast.forecast_animation_files:
        if not os.path.exists(file):
            continue
        fcast_list.append(file)


    rtma_list = []
    for file in self.rtma_obs.visualization_heatmap_files:
        if not os.path.exists(file):
            continue
        rtma_list.append(file)

    std_dev_list = []
    for file in self.rtma_obs.visualization_stddev_files:
        if not os.path.exists(file):
            continue
        std_dev_list.append(file)

    adif_list = []
    adif_list.append('SECTION:Animated Difference')
    for file in self.rtma_obs.visualization_animated_difference_files:
        if not os.path.exists(file):
            continue
        adif_list.append((file, 'adiff'))



    curr_file_list = self.generateFileList(day, end_hour, fcast_list, rtma_list, std_dev_list)
    # #print curr_file_list, adif_list


    self.generateDailyPage(adif_list, curr_file_list, hrrr_fcast)


  def showWebsite(self):
    #webbrowser.open_new(self.landing_file)
    pass


  def generateFileList(self, day, end_hour, hrrr_fcast, rtma_obs, std_dev):
    file_list = []
    list_hour = 0

    while list_hour < end_hour:
      file_list.append(self.generateSectionTitle(day, list_hour))
      for item in rtma_obs:
        # #print inrange(item, day, end_hour)
        if self.inrange(item, day, list_hour) == 0:
          file_list.append([item, "obs"])

      for item in hrrr_fcast:
        # #print inrange(item, day)
        if self.inrange(item, day, list_hour) == 0:
          file_list.append([item, "fcast"])

      for item in std_dev:
        if self.inrange(item, day, list_hour) == 0:
          file_list.append([item, "stddev"])

      list_hour += 1

    ##print 'new file list'
    ##print '{}'.format(file_list)
    return file_list

  def generatePNGList(self, check, pr_dir, type):
    pnglist = []
    list_of_files = []

    str = pr_dir
    for root, dir, files in os.walk(str):
      if len(dir) != 0:
        for sub_dir in dir:
          tmp_dir = os.path.normpath(root + '/' + sub_dir + type)
          list_of_files += glob.glob(tmp_dir)
          list_of_files.sort()

    ##print 'list of files: {}'.format(list_of_files)
    for item in list_of_files:
      if item in pnglist:
        continue
      if check in item:
        if ((check == "hrrr_fcast") | (check == "rtma_obs")):
          if (("rtma_obs.hrrr_fcast" not in item) & ("stddev" not in item)):
              if os.path.exists(item):
                pnglist.append(item)
        elif os.path.exists(item):
          pnglist.append(item)

    return pnglist

  def getFirstDay(self):
    lowest_dir = self.webdir
    str = self.webdir
    for root, dir, files in os.walk(str):
      if len(dir) != 0:
        if unicode(dir[0]).isnumeric():
          lowest_dir += '/' + dir[0]

    lowest_dir = os.path.normpath(lowest_dir)

    ##print lowest_dir
    return lowest_dir

  def generateSectionTitle(self, list_date, list_hour):
    date = str(datetime.datetime.utcnow().date())
    date = date[:len(date) - 2] + str(list_date)
    section_title = "SECTION:" + str(date) + " "
    if list_hour < 10:
      section_title += "0"

    section_title += str(list_hour) + ":00 UTC"
    return section_title

  def inrange(self, file, day, end_hour):
    file = file[file.rfind('/') + 1:]
    file_seg = file.partition('.')
    datehour_file = file_seg[len(file_seg) - 1]
    date_file = datehour_file.partition('_')[0]
    hour_file = datehour_file.partition('_')[2]
    file_day = date_file[6:8]
    file_hour = int(hour_file[1:3])

    diff = (int(day) - int(file_day)) * 24 + (int(end_hour) - int(file_hour))
    return diff

  def addSidebarToLandingPage(self, homepage_url):
    sidebar = """
                <HTML>
                <HEAD>
                  <TITLE>Weather Prediction Evaluation and Reporting (WPEAR)</TITLE>
                </HEAD>
                <FRAMESET cols=20%,*>
                <FRAME src="{}" noresize frameborder="0" frameborder="0" scrolling="auto" />
                <FRAME src="{}" name="page" noresize frameborder="0" scrolling="auto" />
                </frameset>
                <NOFRAMES>
              """.format(self.sidebar_file.split('/')[-1], homepage_url)
    self.landing_page.write(sidebar)
    self.sidebarHandler()



  def sidebarHandler(self):
    self._writeSidebarHead()
    self._writeSidebarBodyHeader()

    self.webdir = os.path.relpath(self.webdir)
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
          daylink =  monthdir + '/' + day + '/day.html'

          reldaylink = daylink.split('/')[-4] + '/' + daylink.split('/')[-3] + '/' + daylink.split('/')[-2] + '/' + daylink.split('/')[-1]
          self._writeDay(day, reldaylink)  

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


  def generateDailyPage(self, adiff_list, item_list, hrrr_fcast):
    ##print 'item_list = {}'.format(item_list)
    list_hour = -1

    dir_file = None
    for item in item_list:
      if (len(item) == 2):
        dir_file = item[0]
        break

    if dir_file == None:
      return

    dir = self.parseDirectory(self.webdir, dir_file)
    ##print 'dir =' + dir
    ##print 'dir file =' + dir_file
    img_src_dir = os.path.normpath(dir)

    day_dir = hrrr_fcast.local_directory[:hrrr_fcast.local_directory.rfind('/')]
    dir = day_dir + '/day.html'
    file_fullpath = os.path.realpath(dir)
    html_file = open(file_fullpath, 'w+')
    ##print file_fullpath

    file_head = """<html><head>
            <font size="3"><title>WPEAR</title>
            <body style="background-color: #EAEDED;"><center><p><h1><br>WPEAR</h1></center>"""
    html_file.write(file_head)
    image_size = """'padding-top:20px;padding-bottom:20px;width:100%;height:80%;"""

    adiff_list.sort()
    for item in adiff_list:
      if 'SECTION:' in item:
        html_file.write("""<br><center><h2><p>""" + item.split("SECTION:")[1] + """</p></h2></center>""")
        continue
      elif len(item) > 1:
        thing = item[0].split('/')[-2] + '/' + item[0].split('/')[-1]
        ##print item[0]
        title = self.generateTitle(-1, thing, "adif")
        html_file.write(
          """<p style="float:left;font-size:18pt;text-align:center;""" +
          """min-width:500px;max-width:550px;min-height:700px;max-height:800px;width:40%;margin-left:2%;margin-right:2%;">""")
        html_file.write(
          title + """<img src='""" + thing + """' alt='""" + item[1] +
          """' style=""" + image_size + """'></p>""")
    html_file.write("""<p style="clear: both;"><hr>""")

    for item in item_list:
      if 'SECTION:' in item:
        if item != item_list[0]:
          html_file.write("""<p style="clear: both;"><hr>""")
        html_file.write("""<br><center><h2><p>""" + item.split("SECTION:")[1] + """</p></h2></center>""")
        list_hour += 1
        continue
      elif len(item) > 1:
        item[0] = item[0].split('/')[-2] + '/' + item[0].split('/')[-1]
        #print item[0]
        title = self.generateTitle(list_hour, item[0], item[1])
        html_file.write(
          """<p style="float:left;font-size:18pt;text-align:center;""")

        if item[1] == "stddev":
          html_file.write(
            """min-width:600px;max-width:650px;min-height:700px;max-height:800px;width:41%;margin-right:2%;margin-left:2%">""")
        else:
          html_file.write(
            """min-width:500px;max-width:550px;min-height:700px;max-height:800px;width:43%;margin-right:2%;margin-left:2%">""")
        html_file.write(
          title + """<img src='""" + item[0] + """' alt='""" + item[1] +
          """' style=""" + image_size + """'></p>""")

    file_end = """</body></html>"""
    html_file.write(file_end)
    html_file.close()

  def parseDirectory(self, webdir, file_name):
    directory = webdir
    if directory.endswith('/') == False:
      directory += '/'

    seg = file_name.partition('.')
    date_part = seg[len(seg) - 1]

    year = date_part[:4]
    month = date_part[4:6]
    day = date_part[6:8]

    directory += year + '/' + month + '/' + day + '/'
    return directory

  def generateTitle(self, obs_hour, file_name, type):
    name = ""
    if type == "adif":
      name += "Animated Difference for "
      tmp_str = file_name[:file_name.rfind('.')]
      date_str = tmp_str[tmp_str.rfind('f') + 1:]
      name += date_str + ":00"

      return name
    elif type == "stddev":
      name += "Std deviation for "
      file_seg = file_name.partition("2MT")[0]
      file_hour = file_seg[len(file_seg) - 4:len(file_seg) - 2]
      name += file_hour + ":00"

      return name
    else:
      if "fcast" in file_name:
        file_seg = file_name.partition("2MT")[0]
        file_hour = file_seg[len(file_seg) - 4:len(file_seg) - 2]

        name += "Animated Forecast for " + file_hour + ":00"
      elif "obs" in file_name:
        name += "Observed weather at "

        if obs_hour < 9:
          name += "0"
        name += str(obs_hour) + ":00"

      return name


  def getHomePage(self, obs, frcast):
    ## Get source files
    graphs = obs.GetDemoGraphs(frcast)
    if len(graphs) == 0:
        #print "No Graphs"
        return None
    ## Generate home page
    self.generateHomePage(graphs, frcast)
    ## Get the demo.html's relative path
    relative_day_dir = '/'.join(frcast.date.strftime(frcast.local_directory_date_format).split('/')[:-1])
    demowebpath = relative_day_dir[1:] + '/demo.html'
    # #print demowebpath
    return demowebpath


  def generateHomePage(self, item_list, frcast):
    image_titles = ['Observation Visualization', 
                    'Forcast Visualization', 
                    'Standard Deviation Visualization', 
                    'Observation vs Forcast Visualization']

    image_descriptions = {}
    image_descriptions['observation_viz'] = "Observation at %s"%(self.getDataHour(item_list['observation_viz']))
    image_descriptions['forecast_viz'] = "Forecast at %s"%(self.getDataHour(item_list['forecast_viz']))
    image_descriptions['stdv_viz'] = "Observations vs %d-Hour Forecasts Over Time"%(frcast.gap_hour)
    image_descriptions['animated_diff_viz'] = "Observations vs %d-Hour Forecasts Over Time"%(frcast.gap_hour)

    day_dir = self.parseDayDirectory(item_list['forecast_viz'])
    file_fullpath = self.webdir + '/' +  day_dir + 'demo.html'
    html_file = open(file_fullpath, 'w+')

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
    
    ## Get relative paths for passed items
    item_list = self.convertToRelativePathsUnderDayDir(item_list) 
    ##print item_list['observation_viz']
    ##print item_list['forecast_viz']
    ##print item_list['stdv_viz']
    ##print item_list['animated_diff_viz']
    


    html_file.write("<li><img src='" +  item_list['observation_viz'] + "' alt='observation' /><h3>"
        + image_titles[0] + "</h3><p>" + image_descriptions['observation_viz'] + "</p></li>")
    html_file.write("<li><img src='" +  item_list['forecast_viz'] + "' alt='forecast' /><h3>"
        + image_titles[1] + "</h3><p>" + image_descriptions['forecast_viz'] + "</p></li></ul>")
    html_file.write("<ul class='rig columns-2'>")
    html_file.write("<li><img src='" +  item_list['stdv_viz'] + "' alt='standard deviation'/><h3>"
        + image_titles[2] + "</h3><p>" + image_descriptions['stdv_viz'] + "</p></li>")
    html_file.write("<li><img src='" +  item_list['animated_diff_viz'] + "' alt='animated difference' /><h3>"
        + image_titles[3] + "</h3><p>" + image_descriptions['animated_diff_viz'] + "</p></li></u>")

    file_end = """</center></body></html>"""
    html_file.write(file_end)
    html_file.close()


  def convertToRelativePathsUnderDayDir(self, file_list):
    ##file_list is dictionary object
    for key, file in file_list.iteritems():
      arr = file.split('/')
      relative_path = '/'.join(arr[len(arr)-2:])
      file_list[key] = relative_path
    return file_list


  def getDataHour(self, file_name):
    arr = file_name.split('/')
    arr = arr[len(arr)-1].split('.')
    return arr[1]


  def parseDayDirectory(self, file_name):
    # file_name = "web/2017/04/23/hrrr_fcast/hrrr_fcast.20170423_t00z.2MT_DPT.IND90k.wrfsfcf01.heatmap.png"
    seg = file_name.split('/')
    directory = ''
    i = len(seg)-5
    for m in range(3):
      directory += seg[i] + '/'
      i += 1
    return directory


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
                      font-size: 1.2em;
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
