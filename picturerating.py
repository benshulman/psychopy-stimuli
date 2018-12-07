#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:17:54 2017

@author: Ben Shulman
"""

#----------
# non psychopy initiation
import os # for listing

#-------------
# path to picture folder
stimpath = 'C:\\Users\\Robles Lab\\Dropbox\\RES Materials\\pyscripts\\baselinepictures\\'
# list of pictures
thepictures = os.listdir(stimpath)

#---------------
# psychopy initiation
from psychopy import visual, core, event
# initiate
# window
win = visual.Window(fullscr=True, color=[-1,-1,-1], size=[1100, 800], units='pix', monitor='testMonitor')
# rating scale initiation
# update to give only one response modality
picscale = visual.RatingScale(win, low = 1, high= 5,
	labels = [1,2,3,4,5],
	tickMarks=[1,2,3,4,5],
	scale="""Not at								  Very\n   all      							   much\n""",
	showAccept = False,
	pos = (0,-250))
# the how bad question
picq = visual.TextStim(win, text="How much do you like this picture?", pos = (0,-150))
# the slides
title1 = visual.TextStim(win, text='Picture Rating', pos=(0, 200))
instr1 = visual.TextStim(win, text='You will view a series of pictures, and rate how much you like each one. Each photo will be shown on screen for 15 s and then you will see the ratings scale shown below. Please try to sit up straight and keep still as we record your heart activity')
instr2 = visual.TextStim(win, text='Please let the research assistant know that this task has finished.')

scalebg = visual.Rect(win, width=1100, height=300, pos = (0,-275), fillColor = (0,0,0))

#-------------
# defining functions
def thequit():
	win.close()
	core.quit()
def thepause ():
	while True:
		thekeys = event.getKeys()
		if ('escape') in thekeys: thequit()
		if thekeys: break
def picloop(thepic, thewait=15):
	event.clearEvents()
	timer = core.CountdownTimer(thewait)
	while timer.getTime() > 0:
		thepic.draw()
		win.flip()
		if event.getKeys(['escape']): thequit()
	thepic.draw()
	picscale.reset()
	scalebg.draw()
	picq.draw()
	picscale.draw()
	win.flip()
	thepause()

#---------------
# instruction slide
title1.draw()
instr1.draw()
picscale.reset()
picq.draw()
picscale.draw()
win.flip()
thepause()
# pics
for trial in range(8):
	picpath = stimpath + thepictures[trial]
	thepic = visual.SimpleImageStim(win=win, image=picpath, units='pix', pos=[0, 0])
	picloop(thepic)
instr2.draw()
win.flip()
thepause()

#--------------
# clean up
thequit()