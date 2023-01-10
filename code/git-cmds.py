'''
  Created on 7. sep. 2020
  
  Last updated on 10. jan. 2023
  
  @author. joschua
'''

import argparse
import os
import re
import json

import subprocess

def printGroup(group):
  print()
  print("************")
  print("***",group,"***")
  print("************")

class Action(object):
  
  actions = [
  "status",
  "fetch",
  "pull",
  "push",
  "update"
  ]
  
  def __call__(self,value):
    if value not in self.actions:
      raise argparse.ArgumentTypeError("'{}' is not a valid option: {}".format(value,self.actions))
    return value

def cmds():

  # position arguments
  parser = argparse.ArgumentParser("A command line script to check status, fetch, pull and push git repositories")
  parser.add_argument("action", help="Action for the git request.", type=Action())
  
  parser.add_argument('-a', '--archive', help="Update archived repositories.", action="store_true")
  
  args = parser.parse_args()
  
  groups = []
  try: 
    if not args.archive:
       print("data")
       with open('data.json','r') as filehandler:
         groups = json.load(filehandler)
    else:
       print("arkiv")
       with open('arkiv.json','r') as filehandler:
         groups = json.load(filehandler)
  except:
    raise Exception('FileError. There is no repo data file. Please create a file called "data.json" with the relevant repositories.')

  # Starting here
  print("Starting {}ing in: {}".format(args.action,os.getcwd()))
    
  # Looping through groups
  for group, repos in groups.items():
    #print("Now, we are in: ",os.getcwd())
    os.chdir(group)
    printGroup(group)
    # Looping through repositories
    
    pull = args.action=="pull"
    push = args.action=="push"
    
    for repo in repos:
       os.chdir(repo)
       if args.action=="status":
          print("* Checking status of repository: ",repo)
          os.system("git status")
       elif args.action=="pull":
          print("\n* Pulling repository: ",repo)
          os.system("git pull --all")
       elif args.action=="fetch":
          print("\n* Fetching origin-gitlab of repository: ",repo)
          os.system("git fetch origin-gitlab")
          os.system("git merge origin-gitlab/master")
       elif args.action=="push":
          print("\n* Pushing repository: ",repo)
          os.system("git push --all")
       elif args.action=="update":
          #os.system("git pull --all --dry-run")
          os.system("git remote update")
          os.system("git status -uno")
       if not repo==".":
          os.chdir("..")
    os.chdir("..")
    
  # Ending here
  print()
  print("Ending in: ",os.getcwd())

if __name__=='__main__':
  cmds()