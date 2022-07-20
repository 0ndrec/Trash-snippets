import sys
import subprocess

# Get the system argument with the path to the file
# This file contains the pathes to the files to be compared
targetlist = sys.argv[1]

#Open the file and read the lines
with open(targetlist, 'r') as f:
    for line in f.readlines():
        oldstring = line.strip()
        newstring = oldstring.replace("target_string", "replacement_string")

        #Call subprocess to rename the file
        subprocess.run("mv " + "~" + oldstring + " " + "~" + newstring, shell=True)

#Close the file
f.close()
