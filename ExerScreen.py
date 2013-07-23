#!/usr/bin/python
import time
import urllib
import commands
from bs4 import BeautifulSoup as bs

#User specific constants
factor = 20
user_id = 918702334


def fileio(fn, rw, val):
    f = open(fn, rw)
    if rw == 'w':
        f.write(str(val) + '\n')
    elif rw == 'r':
        return int(f.readline())
    f.close()

def get_score() :
    global score, scoreOld

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

    print "hi " + str(score) + " " + str(scoreOld)
    act = fileio("act_f", "r", 0)
    if act < activities:
        _ = fileio("act_f", "w", activities)

        score_new = ((score_pres * factor) - scoreOld) + score
        _ = fileio("score", "w", score_new)
        _ = fileio("scoreOld", "w", score)

        scoreOld = score
        score = score_new

def screen_state() :
    global count
    global score, scoreOld
    global state, startTime, timeDiff
    status = commands.getoutput('gnome-screensaver-command -q')
    print state
    if "inactive" in status:
        if state == "active":
            state = "inactive"
            startTime = commands.getoutput('date +"%s"')
            score = score - timeDiff
            commands.getoutput('notify-send "Time Left" ' + str(score))
            _ = fileio('score', 'w', score)
        if score < 0:
            commands.getoutput('notify-send "Switching off the screen" "Bob, you need to go exercise"')
            time.sleep(5)
            commands.getoutput('gnome-screensaver-command -l')
        else:
            time.sleep(2)
    else:
        if state == "active":
            time.sleep(2)
            count = count + 1
            if count == 20:
                get_score()
                count = 0
        else:
            state = "active"
            stopTime = commands.getoutput('date +"%s"')
            timeDiff = int(stopTime) - int(startTime)



score = 0
scoreOld = 0
count = 0
get_score()

state = "active"
startTime = commands.getoutput('date +"%s"')
timeDiff = 0

while True:
    screen_state()
