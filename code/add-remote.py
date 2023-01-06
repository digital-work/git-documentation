'''
  Created on 9. sep. 2020
  
  Last updated on 6. jan. 2023
  
  @author. joschua
'''

import argparse
import os
import pathlib

user = "joschuaos"

def repos():
  # position arguments
  parser = argparse.ArgumentParser("A command line script to add remote origin to GitHub( and GitLab).")
  
  # optional arguments
  parser.add_argument('-r', '--repo', help="Repository name.", default=None)
  parser.add_argument('-g', '--group', help="Group/organization name.")
  parser.add_argument('-p', '--protocol', help="Protocol of the repository (https or ssh)", default="ssh")
  
  args = parser.parse_args()
  
  repo = args.repo
  if not repo:
     print("None repository name chosen. Choosing folder name instead.")
     repo = pathlib.Path(os.getcwd()).name
  
  os.system("git remote remove origin")
  os.system("git remote remove origin-gitlab")
  
  path_gitlab = ""
  if args.protocol.upper()=="SSH":
    path_gitlab = "git@gitlab.com:{}/{}.git".format(args.group if args.group else user,repo)
  elif args.protocol.upper()=="HTTPS":
    path_gitlab = "https://gitlab.com/{}/{}.git".format(args.group if args.group else user,repo)
  
  path_github = ""
  if args.protocol.upper()=="SSH":
    path_github = "git@github.com:{}/{}.git".format(args.group if args.group else user,repo)
  elif args.protocol.upper()=="HTTPS":
    path_github = "https://github.com/{}/{}.git".format(args.group if args.group else user,repo)
  
  print("GitHub:{};\nGitLab:{}.".format(path_github,path_gitlab))
  
  print("Adding origin.")
  os.system("git remote add origin {}".format(path_github))
  os.system("git remote set-url origin --add {}".format(path_gitlab))
  
  print("Adding origin-gitlab.")
  os.system("git remote add origin-gitlab {}".format(path_gitlab)) 
  
if __name__=='__main__':
  repos()