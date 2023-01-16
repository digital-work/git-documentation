'''
  Created on 16. jan 2023. 
  
  Last updated on 16. jan. 2023.
  
  @author. joschua
  
  This module contains functions focusing on the inclusion and presentation of images. 
'''

from itertools import chain

types    = ["IMAGE", "MD"]
subtypes = {
      "IMAGE": ["JPG", "PNG", "GIF"],
      "MD"   : ["WEEK", "ADMIN", "OTHER"],
      "ADMIN": ["README", "ARCHIVE", "GLOSSARY"]
   }
ending_to_type = {
      'JPG': 'image'
   }

from itertools import chain

class FileType:
   
   def __init__(self,file_type,subtype=None):
      
      assert(self.asserting(file_type,subtype))
      
      self.file_type = file_type.upper()   
      self.subtype   = subtype
        
   def asserting(self,file_type,subtype):
      
      isAsserted = True 
      
      if not file_type: return False # Assert that string is not empty
      if not file_type.upper() in types: return False # Assert that type is valid.
      if not (isinstance(subtype,SubFileType) or subtype is None): return False
      
      return isAsserted
   
   def __str__(self):
      unicode = ""
      if self.subtype: 
         unicode += "{}>{}".format(self.file_type,str(self.subtype))
      else:
         unicode += "{}".format(self.file_type,str(self.subtype))
      return unicode#repr(self)

   def __repr__(self):
      unicode = ""
      if self.subtype:
         unicode = "<Type: {}; {}>".format(self.file_type,str(self.subtype))
      else:
         unicode = "<Type: {}>".format(self.file_type)
      return unicode

   def __eq__(self,other):
      if not isinstance(other,FileType):
         return NotImplemented
      return str(self) == str(other)  
   
class SubFileType(FileType):
   
   def __init__(self,file_type,subtype=None):
      FileType.__init__(self,file_type,subtype)
    
   def asserting(self,file_type,subtype):
      
      isAsserted = True 
      
      if not file_type: return False # Assert that string is not empty
      if not file_type.upper() in chain(*subtypes.values()): return False # Assert that subtype is valid.
      if not (isinstance(subtype,SubFileType) or subtype is None): return False
      
      return isAsserted
    
   def __repr__(self):
      unicode = ""
      if self.subtype:
         unicode = "<Subtype: {}; {}>".format(self.file_type,str(self.subtype))
      else:
         unicode = "<Subtype: {}>".format(self.file_type)
      return unicode

def update_navigation(target_path):
   """
   Updating navigation in the project.
   
   Navigation contains the follwoing the elements:
   * Update Navigation between files. 
   * Update Overview for each file.
   * Update ARKIV.md file.
   * Update README.md-file.
   """
   
   """
   Get list of all files in repository.
   """
   files = get_all_files(target_path)
   
   """
   Loop through all files
   """
   if not files:
      print("No files have been found in: {}.".format(target_path))
   for file in files:
      
      f    = open(file,"r")
      text = f.read()
      f.close()
      
      """
      Extract main header from the file.
      """
      header_main = "Dummy"
      headers = get_headers(1,text) 
      if headers:
         header_main = headers[0]
      
      """
      Extract type of the file.
      """
      type = get_type(file,text)
      
   
   #type =  
   
   """
   Inter
   """
   
   """
   """
   
   """
   """
   
   """
   """
   
   """
   """
   
   """
   """
   
   """
   """
   
   """
   """
   
def get_all_files(target_path):
   """
   Returns all relevant files in target_path.
   """
      
   files = []
   return files

def get_headers(level,text):
   """
   Returns all header on the respective level.
   """
   
   headers = []
   return headers

def get_type(file,text):
   """
   Extract type of a file.
   The type candidates are:
   * md: admin, image, or  
   * admin: Files like README, ARKIV, GLOSSARY, etc.
   * week: Files like UKE-XX, etc.
   * image: Files like JPG, PNG, GIF, etc.
   * md: All other MD files.
   """
   
   type = None
   return type