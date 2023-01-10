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
    regex   = re.compile(r'(UKE.*\.md$)')
    
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
            for line in f:
                regex = re.compile(r"^\#.+?(?=Uke).*\d+$", re.IGNORECASE)
                #if a = regex.search(line):
                #   print(line)
                if regex.search(line):
                   res = re.findall(r'\d+',line)
                   if res:
                       week      = {}
                       week['file'] = md 
                       week['days'] = []
                       weeks[int(res[0])] = week
                       
    print(weeks)

if __name__=='__main__':
  finding_tags()