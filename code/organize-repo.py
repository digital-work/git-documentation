'''
  Created on 10. jan 2023.
  
  Last updated on 11. jan. 2023.
  
  @author. joschua
'''

import argparse

import os
from subprocess import call, STDOUT
import re

import json

import datetime
from dateutil.relativedelta import relativedelta
import locale

def get_month_str(year,week):
   
   month_str = ""
   
   date = datetime.date(int(year), 1, 1) + relativedelta(weeks=+int(week))
   
   locale.setlocale(locale.LC_TIME, 'no_NO.UTF-8')
   month_id  = date.strftime("%m")
   month     = date.strftime("%B").capitalize()
   month_str = "{}_{}".format(month_id,month)
   
   return month_id, month_str

def organize_repo():
    
   parser = argparse.ArgumentParser("A command line script to organize a git repository containing images organized by year, month, and day.")
 
   parser.add_argument("-p", "--path", help="Path to the target git repository. Default: Current folder.", default='.')

   args = parser.parse_args()
 
   target_path = args.path
   try: 
       if not os.path.exists(target_path):
          raise Exception("PathError. Chosen target path does not exist: {}".format(target_path))
       if call(["git", "branch"], cwd=target_path, stderr=STDOUT, stdout=open(os.devnull, 'w')) != 0:
          raise Exception("TypeError. Chosen directory is not a git repository: {}".format(target_path))
       else:
           print("Repo git check passed: {}.".format(target_path))
   except Exception as e:
       print("An error occured: {}.".format(e))    
       return
   
   '''
   Check if JSON representation already exists.
   '''
  
   
   json_file = os.path.join(target_path,'DUMP.JSON')
   if os.path.exists(json_file):
      print('The DUMP.JSON file already exists. Reading data from file.')
      
      f        = open(json_file,'r')
      json_obj = json.loads(f.read())
      
      '''
      Creating glossary file.
      '''
       
      glossar_file = os.path.join(target_path,'GLOSSARY.md')
      git_string = ""
      
      if 'tags' in json_obj:
         for tag in json_obj['tags']:
             git_string += "* \#{}\n".format(tag)
             day_string = ""
             for year in json_obj['tags'][tag]['years']:
                for week in json_obj['tags'][tag]['years'][year]['weeks']:
                    for day in json_obj['tags'][tag]['years'][year]['weeks'][week]['days']:
                       '''
                       Get rel path to .md file.
                       '''
                       md_file = json_obj['years'][year]['weeks'][week]['file'] 
                       
                       day_string += "[{}]({}#{}) ".format(day,md_file,day)
             day_string = day_string.strip().replace(" ", ", ")
             git_string += "    * {}\n".format(day_string)
      glossar_string = "# Glossary\n\nThis glossary has been computed automatically.\n\n## Overview\n\n{}".format(git_string)
      g = open(glossar_file,"w")
      g.write(glossar_string)
      g.close()
      
      """
      Creating archive file.
      """
      #datetime.datetime.strptime("2023-01-01","%Y-%m-%d").isocalendar()[1]
      
      archive_file = os.path.join(target_path,'dokumenter','ARKIV.md')
      archive_string = "# Archive\n\n##  Overview\n\nThis overview has been computed automatically.\n\n"
      git_string = ""
      
      if 'years' in json_obj:
         for year in json_obj['years']:
            git_string += "* {}/\n".format(year)
            month_count = 0
            if 'weeks' in json_obj['years'][year]:
               for week in json_obj['years'][year]['weeks']:
                  month,month_str = get_month_str(year, week)
                  if month_count!=month:
                     git_string += "    * {}/\n".format(month_str)
                     month_count=month
                  week_file = ""
                  if 'file' in json_obj['years'][year]['weeks'][week]:
                     week_file = json_obj['years'][year]['weeks'][week]['file']
                     week_file = os.path.join(target_path,week_file) # Week file has to start from same point as archive file.
                     week_file = os.path.relpath(week_file,os.path.dirname(archive_file)) # Start must be directory
                  git_string += "       * [UKE-{:02d}.md]({})\n".format(int(week),week_file)
                  
                  if 'days'in json_obj['years'][year]['weeks'][week]:
                     for day in json_obj['years'][year]['weeks'][week]['days']:
                        git_string += "          * [{}]({}#{})\n".format(day,week_file,day)
      
      archive_string += git_string
      
      g = open(archive_file,"w")
      g.write(archive_string)
      g.close()
      
   else: 
      print("Creating new DUMP.JSON file.")
      create_JSON_representation(target_path)

def create_JSON_representation(target_path):
    
    '''
    1. step: Find all the .md-files in the directory
    '''
    rootdir = target_path
    regex   = re.compile(r'(UKE-\d{2}\.md$)')
    
    md_files = []
    
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                reldir = os.path.relpath(root,rootdir)
                year   = re.findall(r'\d{4}',reldir,0)
                md_files.append([year[0],os.path.join(root,file)])
                
    '''
    2. Make a representation of the timeline of all files and their contents
    { <week#>:
       [ { <day>: 
            [ <tags> ],
         },
       'file'
       ]
    }
    '''
    
    years = {'years': {}}
    tags_global = {}#years['tags']
    
    for md in md_files:
        with open(md[1],encoding="utf-8") as f:
            '''
            Each .md file represents a week.
            '''
            
            text = f.read()
            
            year_num  = 0  
            week_num  = 0
            days      = []  
            tags_week = set({})
            
            '''
            Finding year number.
            '''
            year_num     = md[0]
            if not year_num in years['years']: # Check for JSON object
               years['years'][year_num] = {"weeks": {}}
            
            '''
            Finding week number.
            '''
            week_num = 0
            if not week_num:
               regex_week = re.compile(r"^\#.+?(?=Uke)\D*(\d+).*", re.IGNORECASE)
               res = re.findall(regex_week,text)
               if res:
                  week_num = int(res[0])
            if not week_num in years['years'][year_num]['weeks']: # Check for JSON object
               years['years'][year_num]['weeks'][week_num] = {'days': {}}
            week = years['years'][year_num]['weeks'][week_num]
            
            '''
            Finding all the days of the week.
            '''
            
            regex_days = re.compile(r"^#{2}\s+(\d{4}-\d{2}-\d{2})$", re.IGNORECASE and re.MULTILINE)
            days = re.findall(regex_days, text)
            for day in days:
               if not day in week: # Check for JSON object
                  week['days'][day] = None

            '''
            Finding the corresponding paragraph for each day.
            Each paragraph starts with an h2 following the pattern YYYY-MM-DD.
            Each paragraph finishes at the next date or the end of the file.
            '''            
            regex_pars = re.compile(r"(?:#{2}\s+\d{4}-\d{2}-\d{2})([\s\S]*?)(?=#{2}\s+\d{4}-\d{2}-\d{2}|\Z)", re.MULTILINE)
            res_pars = re.findall(regex_pars,text)
            if res_pars:
               # There should be as many paragraphs as days above. 
               i = 0;
               for par in res_pars:
                  # Each paragraph corresponds to a day extracted above. 
                  tags_day = set({})
                  
                  '''
                  Find all the lines with tags.
                  It is possible to have multiple lines with tags.
                  '''
                  regex_tags = re.compile(r"(Tags:.*(?=\n|$))+")
                
                  res_tags = re.findall(regex_tags,par)
                  if res_tags:
                     for r in res_tags:
                        '''
                        Extract all individual tag from each tags line.
                        '''
                        
                        tags = re.findall('#(\w+)',r)
                        if tags:
                           tags_day.update(tags) # Daily tags. Avoid duplicate tags for each day.
                           tags_week.update(tags_day) # Weekly tags. Avoid duplicate tagss for each week.
                           
                           for tag in tags: # Global tags.
                              if not tag in tags_global:
                                 tags_global[tag] = {'years': {}}
                              
                              if not year_num in tags_global[tag]['years']:
                                 tags_global[tag]['years'][year_num] = {'weeks': {}}
                              
                              if not week_num in tags_global[tag]['years'][year_num]['weeks']:
                                 tags_global[tag]['years'][year_num]['weeks'][week_num] = {'days': []}
                                 
                              if not days[i] in tags_global[tag]['years'][year_num]['weeks'][week_num]['days']: # Avoid duplicate days for each tag.
                                 tags_global[tag]['years'][year_num]['weeks'][week_num]['days'].append(days[i]) 
                     
                     if tags_day:
                        if not week['days'][days[i]]:
                            week['days'][days[i]] = {}
                        week['days'][days[i]]['tags'] = list(sorted(tags_day)) # JSON does not like sets.
                  i+=1 # mMve on to next paragraph and thus day. 
               if tags_week:
                  week['tags'] = list(sorted(tags_week)) #JSON does not like sets. 
            
            '''
            Preparing for JSON
            '''
            
            week['file'] = os.path.relpath(md[1],rootdir)
            years['years'][year_num]['weeks'][week_num] = week
    if tags_global:
       tags_global = dict(sorted(tags_global.items()))
       years['tags'] = tags_global

    '''
    3. Dumping into JSON file
    '''
    
    json_file = os.path.join(rootdir,'DUMP.JSON')
    json_obj = json.dumps(years, indent=3) 
    
    with open(json_file,"w") as outfile:
       json.dump(years,outfile,indent=3)
    
    print('Ending script')

if __name__=='__main__':
  organize_repo()