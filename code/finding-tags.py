'''
  Created on 10. jan 2023.
  
  Last updated on 10. jan. 2023.
  
  @author. joschua
'''

import argparse

import os
from subprocess import call, STDOUT
import re


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
                md_files.append(os.path.join(root,file))
                
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
    
    weeks = {}
    
    for md in md_files:
        with open(md,encoding="latin-1") as f:
            week_num     = 0
            week         = {}
            week['file'] = os.path.relpath(md,rootdir)
            days         = [] 
            for line in f:
                regex_week = re.compile(r"^\#.+?(?=Uke).*\d+$", re.IGNORECASE)
                #if a = regex.search(line):
                #   print(line)
                if not week_num and regex_week.search(line):
                   res = re.findall(r'\d+',line)
                   if res:
                       week_num = int(res[0])
                        
                       weeks[int(res[0])] = week
                       
                regex_days = re.compile(r"^\#\#.+\d{4}\-\d{2}-\d{2}$", re.IGNORECASE)
                if regex_days.match(line):
                    res = re.findall(r'\d{4}\-\d{2}-\d{2}',line)
                    if res:
                       days.append(res[0])
            week['days']    = days
            weeks[week_num] = week
                       
    print(weeks)

if __name__=='__main__':
  organize_repo()