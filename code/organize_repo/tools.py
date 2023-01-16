'''
  Created on 16. jan 2023. 
  
  Last updated on 16. jan. 2023.
  
  @author. joschua
  
  This module contains several helper tools. 
'''

import pathlib

import re

def as_posix(path):
    
   path = pathlib.PurePath(path).as_posix()
   
   return path

def find_paragraphs(h_level,header,repl_string,text):
   
   regex_pars = re.compile(r"(?:#{"+str(h_level)+"}\s+"+header+")([\s\S]*?)(?=\n{2}#{2}\s+|\Z)", re.MULTILINE) # 
   res_pars   = re.findall(regex_pars,text)
   res        = ""
   if res_pars:
      res = re.sub(regex_pars,repl_string,text)
   else: 
      res = text + "\n\n" + repl_string
      
   return res