#!/bin/python

import sys
from subprocess import call

print("This command is not compatible with any scp flags. Set up the ssh connection in your ssh config first.\n")
if len(sys.argv) == 0:
  print("usage: mvkey <key> <ssh-connection>:<remote_dir>")
  decider = False

elif sys.argv[1][:3] != "pub":

  yn = raw_input(sys.argv[1] + " doesn't have a .pub ending and may not be a public key. Do you want to continue? [Y/n] ")
  if len(yn) == 0 or (yn[0] != "n" and yn[0] != "N"):
    decider = True
  else:
    decider = False

else:
  decider = True

if decider and not call(["scp", sys.argv[1], sys.argv[2]]):
  #call(["rm", sys.argv[1]])

  yn = raw_input("Do you want to directly append the key to the remote authorized_keys? [y/N] ")
  if len(yn) == 0 or (yn[0] != "y" and yn[0] != "Y"):
    print("connecting to " + sys.argv[1])
    command = "ssh " + sys.argv[2].split(":")[0] + " -t " + "\'cd " + sys.argv[2].split(":")[1] + "; $SHELL -l\'"
    print  command
    call([command], shell = True)
  else:
    command = "ssh " + sys.argv[2].split(":")[0] + " -t " + "\'cd " + sys.argv[2].split(":")[1] + "; cat " + sys.argv[1] + ">> authorized_keys; rm " + sys.argv[1] + "\'"
    if not call([command], shell = True):
      print("appended " + sys.argv[1] + " to remote authorized_keys")