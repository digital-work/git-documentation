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
    
    years = {'years': {}, 'tags': {}}
    
    for md in md_files:
        with open(md[1],encoding="utf-8") as f:
            year         = md[0]
            #print(year)
            if not year in years['years']:
                years['years'][year] = {"weeks": {}}
            
            week_num     = 0
            week         = {}
            week['file'] = os.path.relpath(md[1],rootdir)
            days         = [] 
            tags         = set({})
            for line in f:
                line = line.strip()
                '''
                Finding week number.
                '''
                if not week_num:
                   regex_week = re.compile(r"^\#.+?(?=Uke)\D*(\d+).*", re.IGNORECASE)
                   res = re.findall(regex_week,line)
                   if res:
                      week_num = int(res[0])
                
                '''
                Finding all days listed in file.
                '''       
                regex_days = re.compile(r"^\#\#.+(\d{4}\-\d{2}-\d{2})$", re.IGNORECASE)
                res = re.findall(regex_days, line)
                if res:
                    days.append(res[0])
                    
                '''
                Finding all tags listed in file.
                '''
                #regex_tags = re.compile(r"^Tags:.*#(\w+).+", re.IGNORECASE)
                regex_tags = re.compile(r"Tags:.*")
                
                res = re.search(regex_tags,line)
                if res:
                   tags.update(re.findall('#(\w+)',line))
                   #p = re.compile(r"#\w+", re.IGNORECASE)
                   #res = re.findall(p,line)
                   #print(res.group())
            
            if days: 
               week['days'] = days
            if tags:
               week['tags'] = list(tags)
               for tag in tags:
                  if not tag in years['tags']:
                      years['tags'][tag] = {}
                  if not year in years['tags'][tag]:
                      years['tags'][tag][year] = []
                  years['tags'][tag][year].append(week_num)
                  years['tags'][tag][year].sort()
            
            years['years'][year]['weeks'][week_num] = week
    #print(years)

    '''
    3. Dumping into JSON file
    '''
    
    json_file = os.path.join(rootdir,'DUMP.JSON')
    obj = json.dumps(years, indent=3)
    print(obj)        
    
    with open(json_file,"w") as outfile:
       json.dump(years,outfile)
    
    print('Ending')

if __name__=='__main__':
  organize_repo()