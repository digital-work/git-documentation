'''
  Created on 9. sep. 2020
  
  @author. joschua
'''

import argparse
import os

user = "joschuaos"

def repos():
  # position arguments
  parser = argparse.ArgumentParser("A command line script to add remote origin to GitHub( and GitLab).")
  parser.add_argument("repo", help="Repository name.")
  
  # optional arguments
  parser.add_argument('-g', '--group', help="Group/organization name.")
  parser.add_argument('-p', '--protocol', help="Protocol of the repository (https or ssh)", default="ssh")
  
  args = parser.parse_args()
  
  os.system("git remote remove origin")
  os.system("git remote remove origin-gitlab")
  
  path_gitlab = ""
  if args.protocol.upper()=="SSH":
    path_gitlab = "git@gitlab.com:{}/{}.git".format(args.group if args.group else user,args.repo)
  elif args.protocol.upper()=="HTTPS":
    path_gitlab = "https://gitlab.com/{}/{}.git".format(args.group if args.group else user,args.repo)
  
  path_github = ""
  if args.protocol.upper()=="SSH":
    path_github = "git@github.com:{}/{}.git".format(args.group if args.group else user,args.repo)
  elif args.protocol.upper=="HTTPS":
    path_github = "https://github.com/{}/{}.git".format(args.group if args.group else user,args.repo)
  
  print("GitHub:{};\nGitLab:{}.".format(path_github,path_gitlab))
  
  print("Adding origin.")
  os.system("git remote add origin {}".format(path_github))
  os.system("git remote set-url origin --add {}".format(path_gitlab))
  
  print("Adding origin-gitlab.")
  os.system("git remote add origin-gitlab {}".format(path_gitlab)) 
  
if __name__=='__main__':
  repos()