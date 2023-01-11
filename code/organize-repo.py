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


def organize_repo():
    
   parser = argparse.ArgumentParser("A command line script to organize a git repository containing images organized by year, month, and day.")
 
   parser.add_argument("-p", "--path", help="Path to the target git repository. Default: Current folder.", default='.')

   #parser.add_argument('-s', '--source_dir', help="Path to the source folder, in which the images are located. Default: Current folder.", default=".")
   #parser.add_argument('-th', '--has_thumbs', help="Indicates if the image(s) has/have thumbnails. Default: False", action='store_true')
  
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
   if os.path.exists(os.path.join(target_path,'DUMP.JSON')):
       print('The DUMP.JSON file already exists.')
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
                        week['days'][days[i]]['tags'] = list(tags_day) # JSON does not like sets.
                  i+=1 # mMve on to next paragraph and thus day. 
               if tags_week:
                  week['tags'] = list(tags_week) #JSON does not like sets. 
            
            '''
            Preparing for JSON
            '''
            
            week['file'] = os.path.relpath(md[1],rootdir)
            years['years'][year_num]['weeks'][week_num] = week
    if tags_global:
       years['tags'] = tags_global

    '''
    3. Dumping into JSON file
    '''
    
    json_file = os.path.join(rootdir,'DUMP.JSON')
    obj = json.dumps(years, indent=3) 
    
    with open(json_file,"w") as outfile:
       json.dump(years,outfile)
    
    print('Ending script')

if __name__=='__main__':
  organize_repo()