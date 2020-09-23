'''
  Created on 7. sep. 2020
  
  @author. joschua
'''

import argparse
import os
import re

def printGroup(group):
  print()
  print("************")
  print("***",group,"***")
  print("************")

groups = {
  "book-reports" :
  [ "boligkjoperboka",
   "hersketeknikker",
   "klok-paa-folelser",
   "mindfulness-medfolelse",
   "operasjon-sjolvdisiplin",
   "publications",
   "velvet-rage"
   ],
   "digital-work" :
   [ "digital-basics",
    "git-documentation"
    ],
   "kropp-sinn-sjel" :
   [ "ae-vil-bare-dans",
    "flora",
    "helse-trening",
    "meditasjon",
    "sovnheftet",
    "spraak-som-verktoy"
    ],
   "selles-und-jenes" :
   [ "rupaul-quotes",
    "stoff"
    ],
   "yoshis-liv" :
   [ "covid-19",
    "norsk-tysk-statsborgerskap",
    "yoshis-hjem",
    "yoshis-sjel",
    "yoshis-worth"]
}

class Action(object):
  
  actions = [
  "status",
  "fetch",
  "pull",
  "push"
  ]
  
  def __call__(self,value):
    if value not in self.actions:
      raise argparse.ArgumentTypeError("'{}' is not a valid option: {}".format(value,self.actions))
    return value

def cmds():
  # position arguments
  parser = argparse.ArgumentParser("A command line script to check status, fetch, pull and push git repositories")
  parser.add_argument("action", help="Action for the git request.", type=Action())

  args = parser.parse_args()

  # Starting here
  print("Starting {}ing in: {}".format(args.action,os.getcwd()))
    
  # Looping through groups
  for group, repos in groups.items():
    #print("Now, we are in: ",os.getcwd())
    os.chdir(group)
    printGroup(group)
    # Looping through repositories
    for repo in repos:
      os.chdir(repo)
      if args.action=="status":
        print("\n* Checking status of repository: ",repo)
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
      os.chdir("..")
      
    os.chdir("..")
    
  # Ending here
  print("Ending in: ",os.getcwd())


if __name__=='__main__':
  cmds()
