''' 
Psych 403 - Computer Programming for Psychology Final Project
Python Script file name: 403Project_VisualSearch_MP
Coded by: Mae Pacificar

This project is an example of the Visual Search Paradigm commonly used in Attention research to investigate how people search for targets among distractors.
A classic example of the Visual Search Paradigm is the game Where's Waldo (Wally)?
This is applicable to everyday life in different ways. 
For example, trying to find your keys among a very messy bedroom during finals - how long does it take for you to find it?

Specifically, this experiment is serial search task (a.k.a. conjunction search) which requires people to consider at least 2 features of the target (colour and letter).
In this task, I wanted to see how long participants are able to find the current target per trial.

Before the experiment, instructions are shown to participants. 
There are 3 blocks of 10 trials in total.
Prior to the search display, a fixation cross is shown for 250 ms.
For the search display, there are 25 stimuli shown in a 5x5 grid
The letters used as stimuli are "L" and "T" and the colours of the letters are either red or blue.
In each trial, participants are asked to find and identify the 1 odd coloured letter target from 24 distractors.
The target letter and colour per trial is drawn at random.
The 24 distractors are composed of 20 opposite letters (in both possible colours) and 4 same letters (in the opposite colour).
For example, if the target is a red L, then the 20 distractors are composed of red and blue Ts and 4 blue Ls.
The search display is shown until the participant has given their response.

If the letter is L and red, the participant is asked to press the UP arrow key.
If the letter is L and blue, the participant is asked to press the DOWN arrow key.
If the letter is T and red, the participant is asked to press the LEFT arrow key.
If the letter is T and blue, the participant is asked to press the RIGHT arrow key.

The participant data I've collected consists of:
    (1) the participant number,
    (2) the session number,
    (3) the age of the participant,
    (4) the participant's handedness,
    (5) the participant's gender,
    (6) if the participant has given consent (real experiments ask for consent per ethics guidelines)
    (7) and the date the experiment was ran.
The experiment data I've collected consists of: 
    (1) the target letter and (2) colour per trial, 
    (3) the participant's response per trial (up, down, left, right),
    (4) if the participant correctly identified the target (accuracies),
    (5) the response time per trial(from onset of search display to participant's key press,
    (6) and the trial number and the block number.

Both participant data and experiment data are saved into a csv file with a filename consisting of participant number, session number, and date. 
The first 2 rows of the CSV file consists of the participant data and the rest of the rows consists of the experiment data.
'''
#=====================
#IMPORT MODULES
#=====================
#-import numpy and/or numpy functions: 
import numpy as np
#-import psychopy functions:
from psychopy import core, gui, visual, event, monitors
#-import file save function:
import pandas as pd
#-import other functions as necessary:
import os
import random
from datetime import datetime

#=====================
#PATH SETTINGS
#=====================
#-define the main directory where you will keep all of your experiment files:
directory = os.getcwd()
#-define the directory where you will save your data:
path = os.path.join(directory, 'dataFiles')
if not os.path.exists(path): #-if path doesn't exist, make the path
   os.makedirs(path)
   
#=====================
#COLLECT PARTICIPANT INFO
#=====================
#-preset participant info needed:
exp_info = {'participant_nr': 00, 
            'session': 00, 
            'age': 18, 
            'handedness':('right','left','ambi'), 
            'gender':'', 
            'consent given': False}
#-participant info dialog box:
my_dlg = gui.DlgFromDict(dictionary = exp_info, 
                         title = "Participant Information", 
                         order = ['consent given', 'participant_nr', 'session', 'age', 'gender', 'handedness'])
#-date when experiment occurred:
date = datetime.now()
exp_info['date'] = str(date.month) + '-' + str(date.day) + '-' + str(date.year)
#-file name setup for participant data collected
filename = ('Participant' + 
            str(exp_info['participant_nr']) + '_' +
            exp_info['date'] + 
            '_VS_Session' +
            str(exp_info['session']) +
            '.csv')
print(filename)

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
#-number of trials and blocks 
nTrials = 10
nBlocks = 3
totalTrials = nTrials*nBlocks

#-stimuli properties for the search display and other stimuli
textHeight = 27 # instruction text height
letterT = 'T' # search display letter stimulus
letterL = 'L' # search display letter stimulus
letterHeight = 60 # search display letter height
letterFont = 'Open Sans' # all text font

# possible x-coordinates and y-coordinates for the 25 stimuli (target + 24 distractors), numbers chosen so they will show in a 5x5 grid
xCoords = [-600,-300,0,300,600]*5 
yCoords = [-400,-400,-400,-400,-400] + [-200,-200,-200,-200,-200] + [0,0,0,0,0] + [200,200,200,200,200] + [400,400,400,400,400]
stimCoords = list(zip(xCoords,yCoords)) # list of all x- and y-coordinates for the 25 stimuli

# number of opposite letter distractors and their possible colours
distractor_opp_count = 20
distractor_opp_colours = ['red']*distractor_opp_count + ['blue']*distractor_opp_count

# number of same letter distractors 
distractor_same_count = 4

# colour of the target as index[0] and same letter distractor as index[1]
target_same_colours = ['red','blue']

#-list of instructions/messages for the experiment
experiment_msg = [
    ('Welcome to the Visual Search Task!\n\n\n'
     'Press SPACE to begin'),
    ('In this experiment, you will search for \n\n''THE ODD COLOURED LETTER \n\n\n'
     'The letter will either be "T" or "L".\n' 'The colour will either be RED or BLUE.\n'
     'Each trial will begin with a fixation cross followed by a display of letters. \n\n\n\n'
     'Press SPACE to continue instructions'),
    ('EXAMPLE: \n''if the target in a trial is a RED "T":\n'
     '1 RED "T" will be among DIFFERENT coloured "L"s and BLUE "T"s.\n\n\n'
     'Once you found the target, click the corresponding key for the target\n'
     'AS FAST AS YOU CAN: \n\n\n'
     'RED "L"  =  UP arrow key\n'
     'BLUE "L"  =  DOWN arrow key\n\n'
     'RED"T"  =  LEFT arrow key\n'
     'BLUE "T"  =  RIGHT arrow key\n\n\n\n'
     'Press SPACE to continue'),
    ('Reminder: \n\n\n'
     'RED "L"  =  UP\n'
     'BLUE "L"  =  DOWN \n\n'
     'RED "T"  =  LEFT \n'
     'BLUE "T"  =  RIGHT \n\n\n'
     'Once you are ready,\n press SPACE to continue')]

#=====================
#PREPARE CONDITION LISTS
#=====================
#-create counterbalanced list of all conditions: each tuple represents a trial condition where the target letter is index[0] and opposite letter is index[1]
targetLetter = [letterT, letterL]*5
distractorLetter = [letterL, letterT]*5
blockCondition = list(zip(targetLetter,distractorLetter))

#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
targets = [0]*totalTrials #-prefill list of the target letter per trial
target_colours = [0]*totalTrials #-prefill list of target colour per trial
responses = [0]*totalTrials #-prefill list of participant response per trial
accuracies = [0]*totalTrials #-prefill list of accuracy per trial
responseTimes = [0]*totalTrials #-prefill list of response time per trial
trialNumbers = [0]*totalTrials #-prefill list of the trial number
blockNumbers = [0]*totalTrials #-prefill list of the block number for the trial

#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
#-define the monitor settings using psychopy functions
mon = monitors.Monitor('myMonitor', width=38.3, distance=60) # this is my screen's width 
mon.setSizePix([1920,1080])

#-define the window (size, color, units, fullscreen mode) using psychopy functions
win = visual.Window(
 monitor=mon,
 size = (1920,1080), # this is my screen's size
 color='black', 
 units='pix',
 fullscr=True) # I set the screen to fullscreen 

#-define experiment messages
start_msg = experiment_msg[0] # first message in the experiment_msg list
instruct_first_msg = experiment_msg[1] # second message in the experiment_msg list
instruct_next_msg = experiment_msg[2] # third message in the experiment_msg list

#-default message text (start with the first message)
instruct_text = visual.TextStim(win, text = start_msg, height = textHeight)

#-define block text
block_msg = experiment_msg[3]
block_text = visual.TextStim(win, text = block_msg, height = textHeight)

#-define fixation, target, and distractors
fixation = visual.TextStim(win, text = '+', color = 'white', height = letterHeight)

target = visual.TextStim(win, text = 'L', font = letterFont,
                pos = (0,0), height = letterHeight,
                color = 'white') # target stim
                
distractor_same = visual.TextStim(win, text = 'L', font = letterFont,
                pos = (0,0), height = letterHeight,
                color = 'white') # distractor same target stim
                
distractor_opposite = visual.TextStim(win, text = 'L', font=letterFont,
                pos = (0,0), height = letterHeight,
                color = 'white') # distractor opposite stim

#-frame timing info:
#-set durations
refresh = 1.0/60.00 #-monitor refresh rate of the monitor
fix_dur = 0.250 # 250 ms
display_dur = refresh # show indefinitely (arbitrary)

#-set frame counts
fix_frames = int(fix_dur/refresh) # number of fixation frames
display_frames = int(display_dur/refresh)  # number of display frames (indefinite until press)
last_frame = 1 # add another frame after all drawn
# total number of frames to be presented per trial:
total_frames = int(fix_frames + display_frames + last_frame)

#-set clock timer for response 
resp_clock = core.Clock()

#=====================
#START EXPERIMENT
#=====================
#-present start message 
instruct_text.draw() # draw experiment start message
win.flip() # show experiment start message
event.waitKeys(keyList=['space']) # wait and allow participant to begin experiment by pressing SPACE bar

#-present first instruction message
instruct_text.text = instruct_first_msg # first part of instruction
instruct_text.draw() # draw
win.flip() # show
event.waitKeys(keyList=['space']) # allow participant to move to next part of instruction by pressing SPACE bar

#-present next instruction message
instruct_text.text = instruct_next_msg # second part of instruction
instruct_text.draw() # draw
win.flip() # show
event.waitKeys(keyList=['space']) # allow participant to start experiment by pressing SPACE bar

#=====================
#BLOCK SEQUENCE
#=====================
#-for loop for nBlocks 
for iblock in range(nBlocks):
    instruct_text.text = 'Block ' + str(iblock+1)+ ' of the experiment'# show what number of block the participant is in
    instruct_text.draw() # draw
    win.flip() # show
    core.wait(2) # show for 2 seconds then,
    block_text.draw() # draw block message consisting of target:key to press
    win.flip() # show 
    event.waitKeys(keyList=['space']) # wait for user to press SPACE to start the trials
    
    np.random.shuffle(blockCondition) # shuffle the list of conditions for what is each trial's target and opposite letter
    
    #=====================
    #TRIAL SEQUENCE
    #=====================    
    for itrial in range(nTrials): 
        #-count overall number of trials:
        overallTrial = iblock*nTrials+itrial
        
        #-shuffle necessary lists that needs to be determined per trial
        np.random.shuffle(stimCoords) # shuffle where the target and distractors are going to show per trial
        np.random.shuffle(target_same_colours) # shuffle what colour the target will be per trial
        np.random.shuffle(distractor_opp_colours) # shuffle what colour each distractor will be per trial
        
        #-collect data information about block, trial, and target for the trial, respectively:
        blockNumbers[overallTrial] = iblock+1
        trialNumbers[overallTrial] = itrial+1
        targets[overallTrial] = blockCondition[itrial][0] #-prefill list of 
        
        #-stimuli properties for current trial:
        target.text = blockCondition[itrial][0] # target letter for the trial
        distractor_same.text = blockCondition[itrial][0] # distractor same letter as target
        distractor_opposite.text = blockCondition[itrial][1] # distractor opposite letter as target
        
        target.pos = (stimCoords[24][0], stimCoords[24][1]) # position of target for the trial (last indexed tuple)
        
        target.color = target_same_colours[0] # colour of target for the trial
        target_colours[overallTrial] = target_same_colours[0] # colour of target/trial for data collection
        
        distractor_same.color = target_same_colours[1] # colour of distractor that is the same letter as target
        
        #=====================
        #START TRIAL
        #=====================   
        for frameN in range(total_frames): # for all the frames
            if 0 <= frameN <= fix_frames: # for the number of frames for fixation:
                fixation.draw() # draw fixation
                win.flip() #-show fixation
            
            if fix_frames < frameN <= (fix_frames + display_frames): # after fixation show display:
                for i in range(distractor_opp_count): # loop through the number of opposite letter distractors to be shown, start from index 0-19
                    distractor_opposite.pos = (stimCoords[i][0], stimCoords[i][1]) # set each distractor's position
                    distractor_opposite.color = distractor_opp_colours[i] # set each distractor's colour
                    distractor_opposite.draw() # draw each distractor 
                for i in range(distractor_same_count):
                    i += 20 # loop through the number of same letter distractor, start from next index [20-23]
                    distractor_same.pos = (stimCoords[i][0], stimCoords[i][1]) # set each distractor's colour
                    distractor_same.draw() # draw each distractor
                target.draw() # draw the target 
                win.flip() # show the search display: 1 target, 20 opposite letter distractors, 4 same letter distractors
                resp_clock.reset() # reset timer at onset of search display
                keys = event.waitKeys(keyList=['up', 'down', 'left', 'right']) # collect arrow keypress for response, once pressed, trial is over
                if keys: # if user pressed up, down, left, or right arrow keys
                    responses[overallTrial] = keys[0] # collect first key pressed after search display shown
                    responseTimes[overallTrial] = resp_clock.getTime() # collect time of response after search display shown = RT
                    if target_same_colours[0] == 'red' and blockCondition[itrial][0] == letterL: # target red L
                        if keys[0] == 'up': 
                            accuracies[overallTrial] = 'Correct' # if key pressed is up for target red L, they are correct
                        else:
                            accuracies[overallTrial] = 'Incorrect' # otherwise, they are wrong
                    elif target_same_colours[0] == 'blue' and blockCondition[itrial][0] == letterL: # target blue L
                        if keys[0] == 'down':
                            accuracies[overallTrial] = 'Correct' # if key pressed is down for target blue L, they are correct
                        else: 
                            accuracies[overallTrial] = 'Incorrect' # otherwise, they are wrong
                    elif target_same_colours[0] == 'red' and blockCondition[itrial][0] == letterT: # target red T
                        if keys[0] == 'left':
                            accuracies[overallTrial] = 'Correct' # if key pressed is left for target red T, they are correct
                        else: 
                            accuracies[overallTrial] = 'Incorrect' # otherwise, they are wrong
                    else: # target blue T
                        if keys[0] == 'right':
                            accuracies[overallTrial] = 'Correct' # if key pressed is right for target blue T, they are correct
                        else: 
                            accuracies[overallTrial] = 'Incorrect' # otherwise, they are wrong
        #-print info about subject's response for the trial:
        print(
         'Block:',
         iblock+1,
         ', Trial:', 
         itrial+1, 
         ', Target:', 
         blockCondition[itrial][0],
         ', Colour:',
         target_same_colours[0],
         '=', 
         accuracies[overallTrial], 
         ', RT:', 
         responseTimes[overallTrial])
#======================
# END OF EXPERIMENT
#======================        
#-write data to a file
df1 = pd.DataFrame(data=exp_info, index=[0]) # participant info
df2 = pd.DataFrame(data={
 "Block Number": blockNumbers, 
 "Trial Number": trialNumbers,
 "Target Letter": targets,
 "Target Colour": target_colours,
 "Response": responses,
 "Accuracy": accuracies, 
 "Response Time": responseTimes}) # experiment data 
# filename as determined at the start of the experiment using participant info 
df1.to_csv(os.path.join(path, filename), sep=',') # save into csv the participant info first
df2.to_csv(os.path.join(path, filename), sep=',', index=False, mode = 'a') # save into the same csv the experiment data

#-close window
win.close()

#-quit experiment
core.quit()