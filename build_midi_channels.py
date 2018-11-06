
# written for Watchout 6.1.6, but may work in 6.2+
'''
run this to create the mappings for the nanoKontrol Studio.
It uses pyperclip to copy the returned data to the clipboard.
Just open Watchout and paste in the new midi inputs.

'''

import pyperclip

midiText = '''UTF8 DATATON_DFC_DATA_590925_620721_AUC069 {
	"Structure and File Format (C) Copyright Dataton AB" 2016 1
	"WATCHMAKER" 6 1 6 0
	ObjTransferable ObjTransferable struct extends {
		TextTransferable struct extends {
			Transferable struct {
			}
		} {
		}
	} {
		mObjData list object true,
		mClassName string
	} {
		{ // mObjData
			MIDIControllerVariable struct extends {
				MIDIVariable struct extends {
					Variable struct extends {
						VarListItem struct {
							mName string
						}
					} {
						mValue variant,
						mLimit float
					}
				} {
					mChannel int
				}
			} {
				mController int,
				mHighRes bool
			} { "test", 0, 1, 1, 1, false // mName mValue mLimit mChannel mController mHighRes
			},
			%s
		},
		"VarListItem" // mClassName
	}
}
'''


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
		newCol.append(('_'+str(i)+j,countWithSkip))
		rowCounter += 8
		#print(countWithSkip)


	midiMap.append(newCol[:])

	curCounter += 1


#print(midiMap)
newChannels = ''
for cols in midiMap:
	for rows in cols:
		midiButtonTemplate = 'MIDIControllerVariable {{ \
		"{title}", 0, 1, 1, \
		{channel}, false }}, // mName mValue mLimit mChannel mController mHighRes,\n'.format(
			title = rows[0],
			channel = rows[1])

		newChannels += midiButtonTemplate

#print(newChannels)
finalText = midiText  % newChannels[:-2]
pyperclip.copy(finalText)
print(finalText)