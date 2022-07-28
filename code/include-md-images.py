'''
  Created on 28. jul. 2022
  
  @author. joschua
'''

import argparse
import os

def include_images():
 parser = argparse.ArgumentParser("A command line script to add remote origin to GitHub( and GitLab).")
 
 parser.add_argument("target_file", help="Path to the target file, in which the images will be shown")

 parser.add_argument('-s', '--source_dir', help="Path to the source folder, in which the images are located. Default: Current folder.", default=".")
 parser.add_argument('-th', '--has_thumbs', help="Indicates if the image(s) has/have thumbnails. Default: False", action='store_true')
  
 args = parser.parse_args()
 
 target_file = args.target_file
 if not os.path.exists(target_file):
    raise Exception('FileError. Chosen target file does not exist: {}'.format(target_file))
 
 # File containing the final image strings. Stored in the same folder as the target file.
 
 
 image_strings_dir = os.path.join(os.path.dirname(target_file),"images.txt")
 print(image_strings_dir)
 
 source_dir = args.source_dir
 if not os.path.exists(source_dir):
    raise Exception('PathError. Chosen source folder does not exist: {}'.format(source_dir))

 has_thumbs=args.has_thumbs
 if has_thumbs:
    print("The source directory does contain thumbnails.".format(has_thumbs))
 else:
    print("The source directory does not contain thumbnails.".format(has_thumbs))

 # list to store files
 res = []
 # Iterate directory
 for file in os.listdir(source_dir):
   # check only text files
   if (file.endswith('.jpg') or file.endswith('.png')) and file.find("_thumb") == -1:
     res.append(file)
 
 with open(image_strings_dir, 'a') as image_strings_file:
   for file in res:
     # Compute relative path from target file
     rel_file = os.path.relpath(file, start=target_file)
      
     # Compute the github mockdown string
     md_string = ""
      
     title = file.replace('.jpg','').replace('.png','')
     if has_thumbs:
       rel_thumb = file.replace('.jpg','_thumb.jpg').replace('.png','_thumb.png')
       md_string = "[![{}]({})]({})".format(title,rel_thumb,rel_file)
     else:
       md_string = "![{}]({})".format(title,rel_file)
      
     image_strings_file.write(md_string)
 
if __name__=='__main__':
  include_images()