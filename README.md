# Psych 403 - Computer Programming for Psychology Final Project
## Coded by: Mae Pacificar

Python Script file name: 403Project_VisualSearch_MP

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

- If the letter is L and red, the participant is asked to press the UP arrow key.
- If the letter is L and blue, the participant is asked to press the DOWN arrow key.
- If the letter is T and red, the participant is asked to press the LEFT arrow key.
- If the letter is T and blue, the participant is asked to press the RIGHT arrow key.

The participant data I've collected consists of:
1. the participant number,
2. the session number,
3. the age of the participant,
4. the participant's handedness,
5. the participant's gender,
6. if the participant has given consent (real experiments ask for consent per ethics guidelines)
7. the date the experiment was ran

The experiment data I've collected consists of: 
1. the target letter per trial,
2. the target colour per trial, 
3. the participant's response per trial (up, down, left, right),
4. if the participant correctly identified the target (accuracies),
5. the response time per trial,
6. and the trial number and the block number.

Both participant data and experiment data are saved into a csv file with a filename consisting of participant number, session number, and date. 
The first 2 rows of the CSV file consists of the participant data and the rest of the rows consists of the experiment data.
