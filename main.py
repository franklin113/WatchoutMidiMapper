#!/usr/bin/env python

"""
This small app uses pygame to read midi input data and copy the channel name to the clipboard.

The idea is, you create a dictionary of midi channels where the values of each key are the names
you assigned in watchout.

For example,

_1a - channel 21
_2b - channel 30
ect...

The way I created the dictionary, this only really works with Korg nanoKontrol Studio, but you can
just go in and change the dictionary to match.

I've mapped each button to a row and column. Starting from the left, the columns run 1-8, rows a-d.

In Watchout I added an underscore because you cannot begin an input with a number in the task window.

"""

import pyperclip
import pygame
import pygame.midi
from pygame.locals import *




def build_midi_dict():
	finalDict={}
	numRows= 4
	numColumns=8

	midiCols = [x for x in range(1,9)]
	midiRows = ['a','b','c','d']
	midiAssignments = [x for x in range(21,54)]
	midiMap = []

	curCounter = 21
	for i in midiCols:
		newCol = []
		rowCounter = 0
		skipCounter = 0

		#print('column: ',i)
		for j in midiRows:


			newCount = curCounter + rowCounter
			if newCount <= 31:
				skipCounter = 0
				countWithSkip = newCount

			else:
				skipCounter = 1
				countWithSkip = newCount + skipCounter
			newCol.append((str(i)+j,countWithSkip))
			finalDict[countWithSkip]='_'+str(i)+j
			rowCounter += 8
			#print(countWithSkip)

		curCounter += 1
	return finalDict

def print_device_info():
	pygame.midi.init()
	_print_device_info()
	pygame.midi.quit()

def _print_device_info():
	for i in range( pygame.midi.get_count() ):
		r = pygame.midi.get_device_info(i)
		(interf, name, input, output, opened) = r

		in_out = ""
		if input:
			in_out = "(input)"
		if output:
			in_out = "(output)"

		print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
			   (i, interf, name, opened, in_out))


def input_main(midiDict,device_id = None):
	pygame.init()
	pygame.fastevent.init()
	event_get = pygame.fastevent.get
	event_post = pygame.fastevent.post

	pygame.midi.init()

	_print_device_info()


	if device_id is None:
		input_id = pygame.midi.get_default_input_id()
	else:
		input_id = device_id

	print ("using input_id :%s:" % input_id)
	i = pygame.midi.Input( input_id )

	pygame.display.set_mode((1,1))


	buttonDown = 0
	buttonUp = 127
	going = True
	while going:
		events = event_get()
		for e in events:
			if e.type in [QUIT]:
				going = False
			if e.type in [KEYDOWN]:
				going = False
			if e.type in [pygame.midi.MIDIIN]:
				print (e)

		if i.poll():
			midi_events = i.read(10)
			midiChannelNum = midi_events[0][0][1]
			midiPress = midi_events[0][0][2]
			if midiPress == buttonDown:
				print(midiChannelNum)
				pyperclip.copy(midiDict[midiChannelNum])

			# convert them into pygame events.
			# midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
			# for m_e in midi_evs:
			# 	event_post( m_e )

	del i
	pygame.midi.quit()


if __name__ == '__main__':


	midiDict = build_midi_dict()

	device_id = 1 #assumes a device ID of 1

	input_main(midiDict,device_id)

