'''
  Created on 10. jan 2023.
  
  Last updated on 10. jan. 2023.
  
  @author. joschua
'''

import os
import re

def finding_tags():
    
    print("hello world")
    '''
    1. step: Find all the .md-files in the directory
    '''
    rootdir = "."
    regex   = re.compile(r'(UKE.*\.md$)')
    
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                print(os.path.join(root,file))
            
    
    

if __name__=='__main__':
  finding_tags()