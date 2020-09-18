# Helpful git scripts

[Home](../README.md)

This folder contains git scripts writen in Python that will help you to execute common git tasks:
* [add-remote.py](#add-remote-py)

## add-remote.py

 A command line script to add remote origin to GitHub and GitLab. 
 The script will first remove existing remote addresses, before it will add two remote called origin (pointing to GitHub), and origin-gitlab (pointing to GitLab).
 
### Usage 
 
 Use this from the folder where your .git folder is located.
 `add-remote.py` can be located in a parent folder.
 
 ```
 py add-remote.py [-h] [-g GROUP] [-p PROTOCOL] repo
 ```
 
 __Input__:  
 
* `repo`: name of the repository. OBS :warning: : Make sure that the name is the same on GitHub and GitLab.
* `GROUP`: 
 name of the group on GitLab / organization on GitHub. 
 :warning: OBS :warning: : Make sure that the group and organization name is the same on GitHub and GitLab.
 * `PROTOCOL`:
 protocol of the remote address. 
 Can be either HTTPS or SSH. 
 