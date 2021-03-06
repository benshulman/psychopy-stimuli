﻿#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:17:54 2017
 
@author: Ben Shulman
"""

#----------
# non psychopy initiation
import pandas as pd
import numpy as np
from random import shuffle
import time

#-------------
# path to picture folder
stimpath = 'C:\\Users\\Robles Lab\\Dropbox\\RES Materials\\pyscripts\\emopictures\\'
# list of pictures
stimlist = pd.read_csv('C:\\Users\\Robles Lab\\Dropbox\\RES Materials\\pyscripts\\stimlist.csv', dtype={'image': 'str'})

#---------------
# randomize pictures to trial type and block
# randomize trial order
trialtypes = ['lneg','lneu','reap'] #look negative, look neutral, and reappraise trials
trialorder = []
for _ in range(4):
    shuffle(trialtypes)
    if len(trialorder) != 0:
        while trialtypes[0] == trialorder[-1]:
            shuffle(trialtypes)
    trialorder.extend(trialtypes)
# expand trial order into trials and blocks
triallist = np.array([np.repeat(trialorder,4),
    np.repeat(range(4),12),
    range(4*12)]).T
triallist = pd.DataFrame(triallist, columns = ['type','block','trialnumber'])
# assign pictures to trials
picorder = []
negind = stimlist[stimlist.neg == 1].index.tolist()
neuind = stimlist[stimlist.neg == 0].index.tolist()
shuffle(negind)
shuffle(neuind)
for i in range(len(triallist)):
    if triallist.type[i] == 'lneu':
        thepic = neuind.pop()
    else:
        thepic = negind.pop()
    picorder.append(thepic)
triallist = triallist.assign(image = stimlist.image[picorder].reset_index().image)

'''
Participants will complete 4 blocks of 12 trials, which will take 4 minutes each.
Participants will rest for 30 seconds between blocks.
Within each block, participants will complete 4 consecutive trials of each of the 3 conditions.
The order of conditions in blocks will be randomized with the constraint that conditions do not repeat consecutively between blocks.
'''
triallist = triallist.assign(rating = None, choiceHistory = None)

#---------------
# psychopy initiation
from psychopy import visual, core, event
# initiate
# window
win = visual.Window(fullscr=True, color=[-1,-1,-1], size=[1100, 800], units='pix', monitor='testMonitor')
# rating scale initiation
# update to give only one response modality
scalebad = visual.RatingScale(win, low = 1, high= 5,
    labels = [1,2,3,4,5],
    tickMarks=[1,2,3,4,5],
    scale="""Not at                               Very\nall badly                             badly\n""",
    showAccept = False)
# first instruction slide
instr = visual.TextStim(win, pos=(0,0), height=.1, units='norm', text="When you see the word Look, just look at the picture and let yourself feel whatever emotions you have in response to it.\n\nWhen you see the word Decrease, try to change the meaning of the emotional event in the picture to minimize how badly you feel.\n\nPlease enter your rating quickly after each picture, because after 3 seconds the task will continue.")
# second instruction slide
instr2 = visual.TextStim(win, pos=(0,0), height=.1, units='norm', text="This task will take a little more than 15 minutes, and you'll have a 30 s break every 5 minutes.\n\nTry to sit up straight while we record your heart activity.\n\nPlease leave your fingers resting over the number keys, and your arms resting on the desk.")
# third instruction slide
instr3 = visual.TextStim(win, pos=(0,0), height=.1, units='norm', text="Please let the research assistant know you have finished with this task.")
# When you see the word Look, just look at the picture and let yourself respond to what you see. Just let yourself feel whatever emotions you have in response to it.\nWhen you see the word Decrease, try to change the meaning of the emotional event in the picture to minimize how badly you feel. Tell yourself something about what’s going on in the picture to minimize how badly you feel about it.\nPlease enter your rating quickly after each picture, because after 3 seconds the task will continue.
# the how bad question
qbad = visual.TextStim(win, text="How badly do you feel?", height=.12, units='norm')
# PID initiation
# pid instructions
pIDinst = visual.TextStim(win, text='enter participant number', height=.12, units='norm', pos=(0, 0.5))
CapturedResponseString = visual.TextStim(win, 
                        units='norm',height = 0.1,
                        pos=(0, 0.0), text='',
                        alignHoriz = 'center',alignVert='center',
                        color='BlanchedAlmond')
#will be used to show the text they are typing: will update every 
# time they type a letter
captured_string = '' #empty for now.. this is a string of zero length that 
                                 # we will append our key presses to in sequence
# countdown for break
countdown = visual.TextStim(win, 
                        units='norm',height = 0.1,
                        pos=(0, 0.0), text='',
                        alignHoriz = 'center',alignVert='center',
                        color='BlanchedAlmond')

#-------------
# drawing functions
# text drawing function
def thepause ():
	while True:
		thekeys = event.getKeys()
		if ('escape') in thekeys: savequit()
		if thekeys: break
def showtext (thetext):
    thetext.draw()
    win.flip()
    if ('escape') in event.getKeys():
        savequit()
# picture drawing function
def showpic (thepic, thecue, thewait = 6):
    thepic.draw()
    thecue = visual.TextStim(win, text=thecue, height = .15, units = 'norm', pos = (0,-0.9))
    thecue.draw()
    win.flip()
    core.wait(thewait)
    if event.getKeys(['escape']):
            savequit()
# scale drawing function
def showscale(thewait = 3):
    scalebad.reset()
    timer = core.CountdownTimer(thewait)
    while timer.getTime() > 0:
        qbad.draw()
        scalebad.draw()
        win.flip()
        if event.getKeys(['escape']):
            savequit()
# trial instruction cue
def showcue(thecue, thewait = 2):
    # event.clearEvents()
    thecue = visual.TextStim(win, text=thecue, height = .15, units = 'norm')
    showtext(thecue)
    core.wait(thewait)
    if event.getKeys(['escape']):
        savequit()
# intertrialstim break
def interbreak (thewait):
    win.flip()
    core.wait(thewait)
    if event.getKeys(['escape']):
        savequit()
# break between blocks
def showbreak (thewait = 30):
    timer = core.CountdownTimer(thewait)
    while timer.getTime() > 0:
        # minutes = int(timer.getTime()/60.0) # the integer number of minutes 
        # seconds = int(timer.getTime() - (minutes * 60.0)) 
        seconds = int(timer.getTime())
        # timeText = str(minutes) + ':' + str(seconds) # create a string of characters representing the time
        # timer.text=timeText
        timetext = visual.TextStim(win,str(seconds), height = 0.12, pos = (0,-0.25), units = 'norm')
        timetext.draw()
        timeheading = visual.TextStim(win, '30 s Break', height = 0.15, pos = (0,0.25), units ='norm')
        timeheading.draw()
        win.flip()
        if event.getKeys(['escape']):
            savequit()
# a routine to update the string on the screen as the participant types
def updateTheResponse(captured_string):
    CapturedResponseString.setText(captured_string)
    CapturedResponseString.draw()
    pIDinst.draw()
    win.flip()
# savequit
def savequit():
    # save out
    triallist.to_csv(stimpath + pID + '_' + thedate + '_' + thetime + '_' + 'triallog.csv')
    win.close()
    core.quit()

#---------------
# set pID
pidEntered = 0
while pidEntered == 0:
    pIDinst.draw()  # draw instruction
    win.flip() # show instruction
     
    # now we will keep tracking what's happening on the keyboard
    # until the participant hits the return key
     
    #check for Esc key / return key presses each frame
    while pidEntered == 0:
        for key in event.getKeys():
            #quit at any point
            if key in ['escape']: 
                win.close()
                core.quit()
                 
            #if the participant hits return, save the string so far out 
            #and reset the string to zero length for the next trial
            elif key in ['return']:
                print 'participant typed %s' %captured_string #show in debug window
                pID=captured_string #store for later
                captured_string = '' #reset to zero length 
                pidEntered = 1 #finishes
                 
            #allow the participant to do deletions too , using the 
            # delete key, and show the change they made
            elif key in ['delete','backspace']:
                captured_string = captured_string[:-1] #delete last character
                updateTheResponse(captured_string)
#if any other key is pressed, add it to the string and 
            # show the participant what they typed
            else: 
                captured_string = captured_string+key
                #show it
                updateTheResponse(captured_string)

#---------------
# store pID and date in log
thedate = time.strftime("%b%d%Y", time.localtime())
thetime = time.strftime("%H-%M", time.localtime())
triallist = triallist.assign(pID = pID, date = thedate, time = thetime)

#---------------
# first instruction slide
showtext(instr)
thepause()

#---------------
# second instruction slide
showtext(instr2)
thepause()

#---------------
# run a block
for block in range(4):
    # for trial in range(12):
    for trial in range(12):
        trialn = block * 12 + trial
        picpath = stimpath + triallist.image[trialn] + '.jpg'
        thepic = visual.SimpleImageStim(win=win, image=picpath, units='pix', pos=[0, 0])
        if triallist.type[trialn] == 'reap':
            thecue = 'Decrease'
        else:
            thecue = 'Look'
        # show the cue
        showcue(thecue)
        # show the picture
        showpic(thepic, thecue)
        # interstim interval
        interbreak(1)
        # show the scale
        showscale()
        # thisExp.addData('final_rating', your_ratingscale_name.getHistory()[-1][0])
        triallist.rating[trialn] = scalebad.getRating()
        triallist.choiceHistory[trialn] = scalebad.getHistory()
        # interstim interval
        interbreak(3)
    if block < 3:
        showbreak()

#--------------
# save out
triallist.to_csv(stimpath + pID + '_' + thedate + '_' + thetime + '_' + 'triallog.csv')

#---------------
# third instruction slide
showtext(instr3)
thepause()

#--------------
# clean up
win.close()
core.quit()