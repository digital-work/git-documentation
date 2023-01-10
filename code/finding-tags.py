'''
  Created on 10. jan 2023.
  
  Last updated on 10. jan. 2023.
  
  @author. joschua
'''

import os
import re

def finding_tags():
    
    '''
    1. step: Find all the .md-files in the directory
    '''
    rootdir = "."
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
        with open(md) as f:
            week_num     = 0
            week         = {}
            week['file'] = md
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
  finding_tags()