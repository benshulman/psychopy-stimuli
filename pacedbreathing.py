#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:17:54 2017

@author: Ben Shulman
"""

#---------------
# psychopy initiation
from psychopy import visual, core, event, sound

thesound = sound.Sound('C:\\Users\\Robles Lab\\Dropbox\\RES Materials\\pyscripts\\sweepad.wav')

# initiate
# window
win = visual.Window(fullscr=True, color=[-1,-1,-1], size=[1100, 800], units='pix', monitor='testMonitor')
# first instruction slide
title1 = visual.TextStim(win, text='Paced Breathing: Practice', pos=(0, 200))
instr11 = visual.TextStim(win, text='You will hear a tone rising and falling. Please inhale as the tone rises, and exhale as the tone falls. Please do your best to match your breathing to the rhythm of the tone. Please try to sit up straight and keep still as we record your heart activity')
instr12 = visual.TextStim(win, text='30 s Practice Round')
title2 = visual.TextStim(win, text='Paced Breathing: Full', pos=(0, 200))
instr21 = visual.TextStim(win, text='You will now continue with the same task for 2 minutes. Again, try to match your breathing to the rhythm of the tone. Remember, please sit up straight and keep still as we record your heart activity.')
instr22 = visual.TextStim(win, text='2 min Round')
instr3 = visual.TextStim(win, pos=(0,0), height=.1, units='norm', text="Please let the research assistant know you have finished with this task.")

#-------------
def thequit():
	win.close()
	core.quit()
def thewait (thewait):
	event.clearEvents()
	timer = core.CountdownTimer(thewait)
	while timer.getTime() > 0:
		if event.getKeys(['escape']):
			thequit()
def thepause ():
	event.clearEvents()
	while True:
		thekeys = event.getKeys()
		if ('escape') in thekeys: thequit()
		if thekeys: break

#---------------
# practice instruction slide
title1.draw()
instr11.draw()
win.flip()
thepause()

# practice round slide
title1.draw()
instr12.draw()
win.flip()
thesound.play()
thewait(35)

# core.wait(35)
thesound.stop()

# full instruction slide
title2.draw()
instr21.draw()
win.flip()
thepause()

# full round slide
event.clearEvents()
title2.draw()
instr22.draw()
win.flip()
thesound.play()
thewait(130)
thesound.stop()
instr3.draw()
win.flip()
thepause()

#--------------
# clean up
thequit()