#!/usr/bin/env python
import json
import glob
import os
import shutil
from zipfile import ZipFile
from datetime import datetime

# Options
m_backup  = False
m_restore = True
m_make_local_list = True
m_make_global_list = True
m_archive_all = True

# Directories
user_name = os.getlogin()
dir_local  = "/Users/"+user_name+"/Library/Containers/net.wargaming.wotblitz.macos/Data/Documents/DAVAProject/replays/"
dir_global = "/Users/"+user_name+"/Google Drive File Stream/My Drive/WOTB/replays/"

configFile = "/Users/"+user_name+"/Library/Containers/net.wargaming.wotblitz.macos/Data/Documents/DAVAProject/localOptions.bin"
configFile2 = "/Users/"+user_name+"/Library/Containers/net.wargaming.wotblitz.macos/Data/Documents/DAVAProject/localOptions.bin.bak"
backupFile = "/Users/"+user_name+"/.wotb_config_backup"

# Output file
filename_html = "/Users/"+user_name+"/Desktop/wotb_replays.html"

def backup():
  if(os.path.exists(configFile)):
    shutil.copy2(configFile, backupFile)
    
  else:
    print "Config file not exist"
  # End backup
    
def restore():
  if(os.path.exists(backupFile)):
    shutil.copy2(backupFile, configFile)
    shutil.copy2(backupFile, configFile2)
  else:
    print "Please backup first"
  # End restore
    
def make_html_header():
  file_html = open(filename_html, "w")
  file_html.write("<!DOCTYPE html> \n")
  file_html.write("<html lang=\"en\"> \n") 
  file_html.write("<meta charset=\"UTF-8\"> \n")
  file_html.write("<head> \n")
  file_html.write("<link href=\"http://mottie.github.io/tablesorter/css/theme.default.css\" rel=\"stylesheet\"> \n")
  file_html.write("<script src=\"http://cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js\" type=\"text/javascript\"></script> \n")
  file_html.write("<script src=\"http://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.9.1/jquery.tablesorter.min.js\" type=\"text/javascript\"></script> \n")
  file_html.write("</head> \n")
  file_html.write("<script type=\"text/javascript\"> \n")
  file_html.write("$(document).ready(function() \n")
  file_html.write("{ \n")
  file_html.write("$(\"#local\").tablesorter(); \n")
  file_html.write("$(\"#global\").tablesorter(); \n")
  file_html.write("} \n")
  file_html.write("); \n")
  file_html.write("</script> \n")
  file_html.write("<script type=\"text/javascript\"> \n")
  file_html.write("function copy_archive(filename){ \n")
  file_html.write(" \n")
  file_html.write("ret = confirm(\"archive ?\"); \n")
  file_html.write("if (ret == true){ \n")
  file_html.write("alert(\"Sorry, not implemented yet\"); \n")
  file_html.write("} \n")
  file_html.write("if(ret == false){ \n")
  file_html.write("alert(\"Cancelled\"); \n")
  file_html.write("} \n")
  file_html.write("} \n")
  file_html.write("</script> \n")
  
  file_html.write("<body> \n")
  # End make_html_header

def make_table_local():
  file_html = open(filename_html, "a")
  file_html.write("<font size=\"7\">Local files</font> \n")
  local_replays = glob.glob( (dir_local+"*.wotbreplay") )

  print_header = True

  for replay in local_replays:
    source = ZipFile(replay, 'r')

    for file in source.filelist:
      if file.filename != 'meta.json':
        continue

      meta = source.extract('meta.json')
      meta_fh = open(meta,'r')
      data = json.load(meta_fh)
      meta_fh.close()
      data.update({u'Link': source.filename})
      data.update({u'Archive': ""})
      os.remove('meta.json')

      if print_header: 
        file_html.write("<table border=\"1\" id=\"local\" class=\"tablesorter\"> \n")
        file_html.write("<thead> \n")
        file_html.write("<tr> \n")
        for key,value in sorted(data.iteritems(), reverse=True):
          if("version" in key):
            key = "Wotb version"
          elif("vehicleCompDescriptor" in key):
            continue
          elif("title" in key):
            continue
          elif("playerVehicleName" in key):
            key = "Player tank name"
          elif("playerName" in key):
            key = "Player name"
          elif("mapName" in key):
            key = "Map"
          elif("mapId" in key):
            continue
          elif("dbid" in key):
            continue
          elif("camouflageId" in key):
            continue
          elif("battleStartTime" in key):
            key = "Battle start at"
          elif("battleDuration" in key):
            key = "Battle duration (sec)"
          elif("arenaUniqueId" in key):
            continue
          elif("arenaBonusType" in key):
            continue
          file_html.write("<th>"+ str(key) +"</th> \n")
          print_header = False
        file_html.write("</tr> \n")
        file_html.write("</thead> \n")
        file_html.write("<tbody> \n")
        # header
        
      file_html.write("<tr> \n")
      for key,value in sorted(data.iteritems(), reverse=True):
        if( "battleStartTime" in key):
          value = datetime.fromtimestamp(int(value))
        elif("vehicleCompDescriptor" in key):
          continue
        elif("title" in key):
          continue
        elif("mapId" in key):
          continue
        elif("dbid" in key):
          continue
        elif("camouflageId" in key):
          continue
        elif("arenaUniqueId" in key):
          continue
        elif("arenaBonusType" in key):
          continue
        elif("Link" in key):
          value = "<a href=\""+str(value)+"\">link</a>"
        elif("Archive" in key):
          value = "<input type=\"button\" value=\"copy\" onclick=\"copy_archive('"+source.filename+"')\";>"
        file_html.write("<td>"+ str(value) +"</td> \n")
      file_html.write("</tr> \n")

  file_html.write("</tbody> \n")
  file_html.write("</table> \n")
    
  # End of make_table_local

def make_table_global():
  file_html = open(filename_html, "a")
  file_html.write("<font size=\"7\">Archived files</font> \n")
  if(not os.path.exists(dir_global)):
    os.mkdir(dir_global)
  global_replays = glob.glob( (dir_global+"*.wotbreplay") )

  print_header = True

  for replay in global_replays:
    source = ZipFile(replay, 'r')

    for file in source.filelist:
      if file.filename != 'meta.json':
        continue

      meta = source.extract('meta.json')
      meta_fh = open(meta,'r')
      data = json.load(meta_fh)
      meta_fh.close()
      data.update({u'Link': source.filename})
      os.remove('meta.json')

      if print_header: 
        file_html.write("<table border=\"1\" id=\"global\" class=\"tablesorter\"> \n")
        file_html.write("<thead> \n")
        file_html.write("<tr> \n")
        for key,value in sorted(data.iteritems(), reverse=True):
          if("version" in key):
            key = "Wotb version"
          elif("vehicleCompDescriptor" in key):
            continue
          elif("title" in key):
            continue
          elif("playerVehicleName" in key):
            key = "Player tank name"
          elif("playerName" in key):
            key = "Player name"
          elif("mapName" in key):
            key = "Map"
          elif("mapId" in key):
            continue
          elif("dbid" in key):
            continue
          elif("camouflageId" in key):
            continue
          elif("battleStartTime" in key):
            key = "Battle start at"
          elif("battleDuration" in key):
            key = "Battle duration (sec)"
          elif("arenaUniqueId" in key):
            continue
          elif("arenaBonusType" in key):
            continue
          file_html.write("<th>"+ str(key) +"</th> \n")
          print_header = False
        file_html.write("</tr> \n")
        file_html.write("</thead> \n")
        file_html.write("<tbody> \n")
        # header
        
      file_html.write("<tr> \n")
      for key,value in sorted(data.iteritems(), reverse=True):
        if( "battleStartTime" in key):
          value = datetime.fromtimestamp(int(value))
        elif("vehicleCompDescriptor" in key):
          continue
        elif("title" in key):
          continue
        elif("mapId" in key):
          continue
        elif("dbid" in key):
          continue
        elif("camouflageId" in key):
          continue
        elif("arenaUniqueId" in key):
          continue
        elif("arenaBonusType" in key):
          continue
        elif("Link" in key):
          value = "<a href=\""+str(value)+"\">link</a>"
        elif("Archive" in key):
          value = "<input type=\"button\" value=\"copy\" onclick=\"copy_archive('"+source.filename+"')\";>"
        file_html.write("<td>"+ str(value) +"</td> \n")
      file_html.write("</tr> \n")

  file_html.write("</tbody> \n")
  file_html.write("</table> \n")

  
if __name__ == '__main__':
  if m_backup and m_restore:
    print "ERROR: Both backup and restore enabled"
    exit()

  if m_backup:
    backup()
    print "Config file backuped"

  if m_restore:
    restore()
    print "Config file restored from backup"

  make_html_header()

  if m_archive_all:
    for thisFile in glob.glob((dir_local+"*.wotbreplay")):
      shutil.copy2( thisFile, dir_global) 
    print "All local files archived"
      
  if m_make_local_list:
    make_table_local()

  if m_make_global_list:
    make_table_global()

  file_html = open(filename_html, "a")
  file_html.write("</body> \n")
  file_html.write("</html> \n")
