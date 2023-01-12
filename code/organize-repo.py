'''
  Created on 10. jan 2023.
  
  Last updated on 11. jan. 2023.
  
  @author. joschua
'''

import argparse

import os
from subprocess import call, STDOUT
import re

import pathlib
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

def as_posix(path):
    
   path = pathlib.PurePath(path).as_posix()
   
   return path

def organize_repo():
    
   parser = argparse.ArgumentParser("A command line script to organize a git repository containing images organized by year, month, and day.")
 
   parser.add_argument("-p", "--path", help="Path to the target git repository. Default: Current folder.", default='.')
   parser.add_argument('-f', '--force', help="Forces the recomputation of the JSON.DUMP file. Default: False", action='store_true')
   #parser.add_argument()
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
  
   force=args.force # if True, compute DUMP.JSON
   json_file = os.path.join(target_path,'DUMP.JSON')
   
   if force or not os.path.exists(json_file): 
      explanation = ""
      if not os.path.exists(json_file):
         explanation = "Creating new DUMP.JSON file."
      elif force: 
         explanation = "Recomputing DUMP.JSON as requested by the user."
      print(explanation)
      create_JSON_representation(target_path)
   else:
      print('The DUMP.JSON file already exists. Reading data from file.')
      
      f        = open(json_file,'r')
      json_obj = json.loads(f.read())
      f.close()
      
      '''
      Update week files
      '''
      update_UKEXX_files(json_file,target_path)
      
      '''
      Update overview in README.md file
      '''
      update_GLOSSARY_file(json_file, target_path)
      
      '''
      Update overview in README.md file
      '''
      update_ARKIV_file(json_file, target_path)      
      
      '''
      Update overview in README.md file
      '''
      update_README_file(json_file, target_path)

def find_paragraphs(h_level,header,repl_string,text):
   
   regex_pars = re.compile(r"(?:#{"+str(h_level)+"}\s+"+header+")([\s\S]*?)(?=\n{2}#{2}\s+|\Z)", re.MULTILINE) # 
   res_pars   = re.findall(regex_pars,text)
   res        = ""
   if res_pars:
      #print(repl_string) 
      res = re.sub(regex_pars,repl_string,text)
   else: 
      res = text + "\n\n" + repl_string
      
   return res
    

def update_UKEXX_files(json_file,target_path):
    
   f        = open(json_file,'r')
   json_obj = json.loads(f.read())
   f.close()
   
   '''
   Update navigation after H1
   ''' 
   
   archive_file = os.path.join(target_path,'dokumenter','ARKIV.md')
   archive_string  = ""
   navigation_string = ""
   git_string = ""
   
   '''
   Update weekly overview.
   We have to loop through all weeks twice to make the navigation at the top of the file.
   '''

   
   week_count = 0
   week_list = []
   if 'years' in json_obj:
      for year in json_obj['years']:
         if 'weeks' in json_obj['years'][year]:
            for week in json_obj['years'][year]['weeks']:
               
               if 1:
                   week_file = as_posix(os.path.join(target_path,json_obj['years'][year]['weeks'][week]['file']))
                   
                   week_count += 1
                   week_list.append((week,week_file))
                   
                   git_string = "## Oversikt\n\n" 
                   if 'days' in json_obj['years'][year]['weeks'][week]:
                      days =  json_obj['years'][year]['weeks'][week]['days']
                      i = 0
                      for k,v in days.items():
                          git_string += "* [{}](#{})".format(k,k)+ ("\n" if i!=len(days.items())-1 else "")
                          i += 1 
                   
                   f  = open(week_file,"r",encoding="utf-8")
                   text = f.read()
                   f.close()
                   
                   overview_string = find_paragraphs(2,r'Oversikt',git_string,text)
                   
                   f = open(week_file,"w",encoding="utf-8")
                   f.write(overview_string)
                   f.close()
    
   #print(week_list)               
   uke_string = "" 
   i = 0
   archive_file = os.path.join(target_path,"dokumenter/ARKIV.md")
   for week in week_list:
      
      week_num  = week[0] 
      week_file = week[1]
      navigation_string = ""
   
      header_string = "# Uke {}\n\n".format(week_num)
   
      if i:
         print("hiersimmer")
         prev_week_file = week_list[i-1][1]
         print(prev_week_file,"    ",week_file)
         rel_path       = as_posix(os.path.relpath(prev_week_file, os.path.dirname(week_file))) # Rel path to previous week
         navigation_string += "[< Back]({}) |\n".format(rel_path)
         
      rel_path = as_posix(os.path.relpath(archive_file, os.path.dirname(week_file))) # Rel path to ARKIV.md
      navigation_string += "[Home]({})".format(rel_path) 
      
      if i < len(week_list)-1:
         next_week_file = week_list[i+1][1]
         #print(prev_week_file,"    ",week_file)
         rel_path       = as_posix(os.path.relpath(next_week_file, os.path.dirname(week_file))) # Rel path to next week
         navigation_string += " |\n[Next >]({})\n\n".format(rel_path) 
      else:
         navigation_string += "\n\n" 
         
          
      header_string += navigation_string+'[This header has been computed automatically.]'
      
      f = open(week_file,"r",encoding="utf-8")
      text = f.read()
      f.close()
    
      uke_string = find_paragraphs(1,r'Uke \d{1,2}',header_string,text)

      f = open(week_file,"w",encoding="utf-8")
      f.write(uke_string)
      f.close()
      i += 1
   
   
   
def update_GLOSSARY_file(json_file,target_path):
    
   f        = open(json_file,'r')
   json_obj = json.loads(f.read())
   f.close()
   
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
                  md_file = os.path.join(target_path,json_obj['years'][year]['weeks'][week]['file']) 
                  rel_path = os.path.relpath(md_file, target_path)
                  
                  day_string += "[{}]({}#{}) ".format(day,as_posix(rel_path),day)
         day_string = day_string.strip().replace(" ", ", ")
         git_string += "    * {}\n".format(day_string)
   glossar_string = "# Glossary\n\nThis glossary has been computed automatically.\n\n## Overview\n\n{}".format(git_string)
   
   g = open(glossar_file,"w")
   g.write(glossar_string)
   g.close()
 
def update_ARKIV_file(json_file,target_path):
    
   f        = open(json_file,'r')
   json_obj = json.loads(f.read())
   f.close()
   
   """
   Creating archive file.
   """
   #datetime.datetime.strptime("2023-01-01","%Y-%m-%d").isocalendar()[1]

   archive_file = os.path.join(target_path,'dokumenter','ARKIV.md')
   archive_string  = ""
   if not os.path.exists(archive_file):
      f = open(archive_file,"w")
      f.close()
      archive_string += "# Archive \n\n"
   overview_string = "##  Overview\n\n"
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
                  week_file = os.path.join(target_path,json_obj['years'][year]['weeks'][week]['file']) # Week file has to start from same point as archive file for computation of rel path.
                  week_file = as_posix(os.path.relpath(week_file,os.path.dirname(archive_file))) # Start must be directory
               git_string += "       * [UKE-{:02d}.md]({})\n".format(int(week),week_file)
               
               if 'days'in json_obj['years'][year]['weeks'][week]:
                  for day in json_obj['years'][year]['weeks'][week]['days']:
                     git_string += "          * [{}]({}#{})\n".format(day,week_file,day)

   overview_string += git_string+'\n[This overview has been computed automatically.]'

   f = open(archive_file,"r",encoding="utf-8")
   text = f.read()
   f.close()

   regex_pars = re.compile(r"(?:#{2}\s+Overview)([\s\S]*?)(?=\n{2}#{2}\s+|\Z)", re.MULTILINE)
   res_pars = re.findall(regex_pars,text)
   if res_pars:
      archive_string = re.sub(regex_pars,overview_string,text)
   else: 
      archive_string += text + '\n\n'+overview_string
   
   f = open(archive_file,"w",encoding="utf-8")
   f.write(archive_string)
   f.close()
      
def update_README_file(json_file,target_path):
   
   f        = open(json_file,'r')
   json_obj = json.loads(f.read())
   f.close()
   
   readme_file = os.path.join(target_path,'README.md')
   readme_string  = ""
   if not os.path.exists(readme_file):
      print("README.md does not exist. Please create file in: {}.".format(target_path))
      return
   overview_string = "##  Overview\n\n"
   git_string = ""
   
   '''
   Creating overview string by traversing all folders again
   ''' 
   
   rootdir = target_path
   regex   = re.compile(r'(.+\.md$)|(.+\.pdf)',re.IGNORECASE) # Only list .md and .pdf files
            
   file_tree = get_README_overview_tree(target_path)
   b = walk_for_README_overview([],file_tree,".")
   git_string = ""
   for v in b:
      ind = v[1].count('/')
      if ind:
         git_string += " "+ind*"   "
      path_from_root = as_posix(os.path.join(target_path,v[1]))
      rel_path = as_posix(os.path.relpath(path_from_root,target_path)) # Make it consistent on Mac and PC
      url       = v[0]
      if os.path.isfile(path_from_root): 
         git_string += "* [{}]({})\n".format(url,rel_path) # Only files have links.
      else:
         git_string += "* {}/\n".format(url) # Directories do not have links.
   
   overview_string += git_string+'\n[This overview has been computed automatically.]'
      
   '''
   Replace existing overview section indicated by "## Overview"
   '''

   f = open(readme_file,"r",encoding="utf-8")
   text = f.read()
   f.close()
    
   regex_pars = re.compile(r"(?:#{2}\s+Overview)([\s\S]*?)(?=\n{2}#{2}\s+|\Z)", re.MULTILINE)
   res_pars = re.findall(regex_pars,text)
   if res_pars:
      readme_string = re.sub(regex_pars,overview_string,text)
   else: 
      readme_string += text + '\n\n'+overview_string
  
   f = open(readme_file,"w",encoding="utf-8")
   f.write(readme_string)
   f.close()

def walk_for_README_overview(arr,d,path):
   
   for k, v in d.items():
      file_path = os.path.join(path,k)
      file_path = as_posix(file_path)
      arr.append((k,file_path)) 
      if type(v) == dict:   # option 1 with "type()"
      #if isinstance(v, dict):   # option 2 with "isinstance()"
         new_path = os.path.join(path,k)
         new_path = as_posix(new_path)
         walk_for_README_overview(arr,v,new_path)
      
   return arr 

def get_README_overview_tree(path_):
   '''
   Source: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
   '''
   
   file_token  = ''
   regex_files = re.compile(r'(.+\.md$)|(.+\.pdf)',re.IGNORECASE)
   regex_dirs  = re.compile(r'^\..+|^media',re.IGNORECASE)
   
   for root, dirs, files in os.walk(path_):
      tree = {}
      for d in dirs:
         if not regex_dirs.match(d):
            tree.update({d: get_README_overview_tree(os.path.join(root, d))})
      for f in files:
         if regex_files.match(f):
            tree.update({f: file_token})
      return tree  # note we discontinue iteration trough os.walk

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
            
            week['file'] = as_posix(os.path.relpath(md[1],rootdir))
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