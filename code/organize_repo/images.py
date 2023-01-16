'''
  Created on 16. jan 2023. 
  
  Last updated on 16. jan. 2023.
  
  @author. joschua
  
  This module contains functions focusing on the inclusion and presentation of images. 
'''

import os

import datetime

import json
import re

from organize_repo.tools import as_posix, find_paragraphs

def update_images(json_file,target_path):
   
   if not os.path.exists(json_file):
      print("Error. JSON file does not exist. This is needed for updating images.")
      return 
   
   f        = open(json_file,'r')
   json_obj = json.loads(f.read())
   f.close()
   
   rootdir = target_path
   regex_imgs   = re.compile(r'(.+\.jpg$)|(.+\.png)',re.IGNORECASE)
   regex_thumbs = re.compile(r'.+(_thumb).+',re.IGNORECASE) # Exclude all thumbs for now.
   
   weekly_img_files        = {} # Contains all images without thumbnails
   weekly_img_files_thumbs = {} # Contains all images with thumbnails
   for root, dirs, files in os.walk(rootdir):
      for file in files:
         if regex_imgs.match(file):# and not regex_thumbs.match(file):
            img_path = as_posix(os.path.join(root,file))
            #rel_path = os.path.relpath(img_path,target_path)
            rel_path = img_path
            date_str = re.findall(r'(\d{4}-\d{2}-\d{2})',root)#[-1] # Find date from folder since images might have different dates.
            hasThumb = False
            
            if regex_thumbs.match(file):
               check_path = re.sub(r'_thumb','',img_path)
               if os.path.exists(check_path): 
                  continue # Moving on because image file will be handled elsewhere.
               else:
                  hasThumb = False # The file is the file and thumbnail at once.
            else:
               stem,ext   = os.path.splitext(img_path)
               check_path = os.path.join(stem+"_thumb"+ext)  
               hasThumb = True if os.path.exists(check_path) else False    
            
            if not date_str: continue
            date_str = date_str[-1] # Only get the last one.
            try: 
               date  = datetime.datetime.strptime(date_str,'%Y-%m-%d')
            except Exception as e:
               print("Something went wrong: {}".format(e))
               continue
            
            year      = str(date.year)
            week      = str(date.isocalendar()[1])
            year      = str(date.isocalendar()[0])
            view_file = ''
            if 'years' in json_obj:
               if str(year) in json_obj['years']:
                  if 'weeks' in json_obj['years'][year]:
                     if week in json_obj['years'][year]['weeks']:
                        if 'file' in json_obj['years'][year]['weeks'][week]:
                           view_file = json_obj['years'][year]['weeks'][week]['file']
                        else: 
                           print('"file" could not be found in ',json_obj['years'][year]['weeks'][week])
                           continue
                     else: 
                        print(week,' could not be found in ',json_obj['years'][year]['weeks'])
                        continue
                  else: 
                     print('"weeks" could not be found in ',json_obj['years'][year])
                     continue
               else: 
                  print(year, ' could not be found in ', json_obj['years'])
                  continue
               
            if not view_file:
               print("The week file could not be found: {}.".format(json_obj['years'][year]['weeks'][week]))
               continue
            
            view_file = os.path.join(target_path,view_file) 
            
            if hasThumb:
               if not year in weekly_img_files_thumbs:
                  weekly_img_files_thumbs[year] = {}
               
               if not week in weekly_img_files_thumbs[year]:
                  img_files = []
                  img_files.append(rel_path)
                  weekly_img_files_thumbs[year][week] = {'file': view_file, 'images': img_files}
               else:
                  weekly_img_files_thumbs[year][week]['file'] = view_file
                  weekly_img_files_thumbs[year][week]['images'].append(rel_path)
   
            else:
               if not year in weekly_img_files:
                  weekly_img_files[year] = {}
               
               if not week in weekly_img_files[year]:
                  img_files = []
                  img_files.append(rel_path)
                  weekly_img_files[year][week] = {'file': view_file, 'images': img_files}
               else:
                  weekly_img_files[year][week]['file'] = view_file
                  weekly_img_files[year][week]['images'].append(rel_path)
   
   if not weekly_img_files: 
      print("No images without thumbnails have been found.")
   else: 
      for year,weeks in weekly_img_files.items():
         for week,imgs in weeks.items():
            file = imgs['file']
            for img in imgs['images']:
               pass
            
   if not weekly_img_files_thumbs:
      print("No images with thumbnails have been found.")
   else: 
      for year,weeks in weekly_img_files_thumbs.items():
         for week,imgs in weeks.items():
            view_file = imgs['file']
            
            new_imgs_string  = ""
            paragraph_string = "## New images\n\n" 
            f  = open(view_file,"r",encoding="utf-8")
            text = f.read()
            f.close()
            
            text = find_paragraphs(2,r'New images',"",text).strip()

            git_string = ""
            for img in imgs['images']:
               rel_path  = as_posix(os.path.relpath(img, os.path.dirname(view_file))) 
               regex_img = re.compile(r'.+{}.+'.format(rel_path),re.IGNORECASE)
               if regex_img.findall(text):
                  continue
               else:
                  title      = os.path.splitext(os.path.basename(rel_path))[0]
                  regex_desc = r'^\d{4}-\d{2}-\d{2}_(.+)$'
                  descs      = re.findall(r'^(\d{4}-\d{2}-\d{2})_(.+)$',title)
                  if descs:
                     title = "{} ({})".format(descs[0][0],descs[0][1])
                  title = title.replace('.jpg','').replace('.png','')
                  rel_thumb   = rel_path.replace('.jpg','_thumb.jpg').replace('.png','_thumb.png')
                  git_string += "[![{}]({})]({})\n".format(title,rel_thumb,rel_path) 
            
            if not git_string:
               continue
            else:
               print("New images will be added for week {}.".format(week))

            paragraph_string += git_string + "\n[This list has been generated automatically.]" 
            new_imgs_string = find_paragraphs(2,r'New images',paragraph_string,text)

            f = open(view_file,"w",encoding="utf-8")
            f.write(new_imgs_string)     
            f.close()

def get_md_files_tree(path_):
   '''
   Source: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
   '''
   
   file_token  = ''
   regex_files = re.compile(r'(.+\.md$)',re.IGNORECASE)
   regex_dirs  = re.compile(r'^\..+|^media',re.IGNORECASE)
   
   tree = []
   for root, dirs, files in os.walk(path_):
      for d in dirs:
         if not regex_dirs.match(d):
            #tree.update({d: get_md_files_tree(os.path.join(root, d))})
            tree += get_md_files_tree(as_posix(os.path.join(root, d)))
      for f in files:
         if regex_files.match(f):
            #print(os.path.join(root,f))
            tree.append(as_posix(os.path.join(root,f)))
      return tree  # note we discontinue iteration trough os.walk     

def update_image_tables(json_file,target_path):
   
   '''
   Get a list of all .md fils
   ''' 
   
   rootdir = target_path
   regex   = re.compile(r'(.+\.md$)',re.IGNORECASE) # Only list .md and .pdf files
            
   file_tree = get_md_files_tree(target_path)
   git_string = ""
   
   for file in file_tree:
      
      success = 0
      f       = open(file,"r",encoding="utf-8")
      text    = f.read()
      f.close()
      
      regex = r'.jpg\)\n\[!\['
      if re.findall(regex,text):
         success = 1
         text    = re.sub(regex,'.jpg)|[![',text)
      regex = r'\n\[!\['
      if re.findall(regex,text):
         success = 1
         text    = re.sub(regex,'\n|[![',text)
      regex = r'.jpg\)\Z'
      if re.findall(regex,text):
         success = 1
         text = re.sub(regex,'.jpg)|',text)
      regex = r'.jpg\)\n'
      if re.findall(regex,text):
         success = 1
         text = re.sub(regex,'.jpg)|\n',text)
      
      # Do not put single images in tables.
      text = re.sub(r'\n\|([^|]*)\|\Z',r'\n\1',text) # Mid text
      text = re.sub(r'\n\|([^|]*)\|\n',r'\n\1\n',text) # End text
      
      text = re.sub(r'\)\|\n\n\|\[',r')|\n|[',text) # Remove new line between table rows.
      
      text = re.sub(r'\n\n(\|[^|]+\.jpg[^|]+\|[^|]+\.jpg[^|]+\|\n)',r'\n\n|||\n|:-:|:-:|\n\1',text) # Make prefix for two column tables
      text = re.sub(r'\n\n(\|[^|]+\.jpg[^|]+\|[^|]+\.jpg[^|]+\|[^|]+\.jpg[^|]+\|\n)',r'\n\n||||\n|:-:|:-:|:-:|\n\1',text) # Make prfix for three column tables.
      
      f = open(file,"w",encoding="utf-8")
      f.write(text)
      f.close()