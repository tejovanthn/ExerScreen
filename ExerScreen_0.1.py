#!/usr/bin/env python
import urllib
import commands
from bs4 import BeautifulSoup as bs

#Python scipt to scrub runkeeper for user and get total calories.
#This is mapped with a factor and a file "calorieCount" is updated

#User specific constants
factor = 20
user_id = 918702334

#Using bsoup to get tags
page = bs(urllib.urlopen('http://runkeeper.com/user/' + str(user_id)), "lxml")

#Total Calories
line = str(page.find_all('h1')[2])
loc = line.find("</")
score_pres = int(line[line.find(">", loc - 10) + 1:loc])

#Total Activity
line = str(page.find_all('h1')[0])
loc = line.find("</")
activities = int(line[line.find(">", loc - 10) + 1:loc])


def fileio(fn, rw, val):
    f = open(fn, rw)
    if rw == 'w':
        f.write(str(val) + '\n')
    elif rw == 'r':
        return int(f.readline())
    f.close()


#If number of total activity has not changed, nothing is done.
#else the score is updated
act = fileio("act_f", "r", 0)
if act < activities:
    _ = fileio("act_f", "w", activities)
    #
    score = fileio("score", "r", 0)
    score_old = fileio("scoreOld", "r", 0)

    score_new = ((score_pres * factor) - score_old) + score
    _ = fileio("score", "w", score_new)
    _ = fileio("scoreOld", "w", score)


print "Starting service"

#Uses gnome-screensaver-command to poll for screensaver state
#When inactive (user is at the system), it updates the score if it comes
#out of active state

state = "active"
startTime = commands.getoutput('date +"%s"')
timeDiff = 0

while True:
    status = commands.getoutput('gnome-screensaver-command -q')

    if "inactive" in status:
        if state == "active":
            state = "inactive"
            startTime = commands.getoutput('date +"%s"')
            scoreSession = fileio('score', 'r', 0) - timeDiff
            commands.getoutput('notify-send "Time Left" ' + str(scoreSession))
            _ = fileio('score', 'w', scoreSession)
        if scoreSession < 0:
            commands.getoutput('notify-send "Switching off the screen" "Bob, you need to go exercise"')
            commands.getoutput('sleep 5')
            commands.getoutput('gnome-screensaver-command -l')
        else:
            commands.getoutput('sleep 2')
    else:
        if state == "active":
            commands.getoutput('sleep 2')
        else:
            state = "active"
            stopTime = commands.getoutput('date +"%s"')
            timeDiff = int(stopTime) - int(startTime)

