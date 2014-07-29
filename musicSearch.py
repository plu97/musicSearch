from __future__ import print_function
from music21 import stream, note, duration, interval, corpus


def hasNumber(inputString): 
    """
    # returns True if any of the char in the string is a digit
    """
    
    return any(char.isdigit() for char in inputString)


def isNumber(inputString): 
    """
    # returns True if the string is a number
    """
    try:
        float(inputString)
        return True
    except ValueError:
        return False


def stringToNotes(string):
    """
    # input: string of note names, separated by spaces
    # output: a stream with Note objects denoted by the string
    #
    # sharps are denoted by '#' and flats by '-'
    # octaves and rhythm are not supported in this function
    # see: stringToNotesWithOctave
    # 
    # example string: 'A B C# D E-'
    """
    
    s = stream.Stream() # create a new Stream
    
    
    for charNum in range(0, len(string)-1): # for every character except the last one in string 
        # the '-1' is so charNum + 1 doesn't go out of bounds
        # could probably change it to do a 'try catch'

        if string[charNum] in 'ABCDEFGabcdefg': # if char is a note name 
            newNote = note.Note() # create new Note object
            
            if string[charNum + 1] == '#' or string[charNum + 1] == '-': # if there's an accidental
                newNote.pitch.name = string[charNum:charNum + 2] # define the pitch of the Note object with the accidental
                charNum = charNum + 1 # advance the charNum 'pointer' forward to account for the accidental
            else: # there's no accidental
                newNote.pitch.name = string[charNum] # define the pitch of the Note object (no accidental)
            
            s.append(newNote) # put the Note object into the Stream
    
    
    if string[-1] in 'ABCDEFGabcdefg': #if the last character is a note name
        newNote = note.Note() # create new Note object
        newNote.pitch.name = string[-1] # pitch of the Note becomes the last character of string
        s.append(newNote) # append the new Note into Stream
            
    return s # return Stream


def stringToNotesWithOctave(string):
    """
    # input: string of note names, separated by spaces
    # output: a stream with Note objects denoted by the string
    #
    # sharps are denoted by '#' and flats by '-'
    # octaves ARE supported in this function as opposed to stringToNotes
    # 
    # example string: 'A3 B-3 C#4 D4 E4'
    """
    
    s = stream.Stream() # create a new Stream
    
    i = 0 # i is an integer that acts as a 'pointer' to the current char to be processed
    
    while (i < len(string) - 1):  # while there is still two or more characters to be processed
        if string[i] in 'ABCDEFGabcdefg': # if the first character is a note name
            newNote = note.Note() # create a new Note object
            if string[i + 1] == '#' or string[i + 1] == '-': # if the next character is an accidental
                newNote.pitch.name = string[i:i+3] # use all three characters to determine the pitch
                    # 1st: note name, 2nd: accidental, 3rd: octave
                i = i + 3 # advance 'pointer' by three
                
            else: # if there is no accidental
                newNote.pitch.name = string[i:i+2] # use the two charactersto determine the pitch
                i = i + 2 # advance 'pointer' by two
                
            s.append(newNote) # append the Note object to Stream
            
        else: # if the first character isn't a note name
            i = i + 1 # skip

    return s # return Stream


def stringToNotesRhythm(string):
    """
    # input: string of note rhythms, separated by spaces
    # output: a stream with Note objects denoted by the string
    #
    # sharps are denoted by '#' and flats by '-'
    # octaves ARE supported in this function as opposed to stringToNotes
    # 
    # example string: '8 8'
    """
    
    #rhythms
    s = stream.Stream()
    strList = []
    
    # going through string to add spaces to places that should have them
    # putting the "processed" string in strList as a list of characters
    for num in range(0, len(string)):
        strList.append(string[num])
        
        if string[num].isdigit(): 
            if num == len(string) - 1:
                continue
            
            elif string[num + 1].isalpha():
                strList.append(' ')
                num += 1
                
            elif string[num + 1].isdigit():
                continue
            
        elif string[num] == '.':
            if num == len(string) - 1:
                continue
            
            elif string[num + 1].isalpha():
                strList.append(' ')
                num += 1
        # else: do nothing
    newString = ''.join(strList)

    tokenList = newString.split() #tokenize the newString

    for token in tokenList:
        if token[1] == '#' or token[1] == '-':
            i = 2
            
        else:
            i = 1
            
        digits = 0
        dots = 0
        newNote = note.Note(token[0:i])
        while (i < len(token) and token[i].isdigit()):
            i = i + 1
            digits = digits + 1
        
        newNote.duration.type = duration.convertQuarterLengthToType(4. / int(token[i - digits:i]))
        
        
        while (i < len(token) and token[i] == '.'):
            i = i + 1
            dots = dots + 1
        
        newNote.duration.dots = dots
        
        s.append(newNote)
            
            
    return s
       
       
def contourToNotes(string):
    """
    # input: string of Parson's Code for Melodic Contours
    #    see https://en.wikipedia.org/wiki/Parsons_code
    #
    # output: a stream of Notes with the given contour
    #
    # 
    # example string: '*dduurrdrruur'
    """
    
    s = stream.Stream() # create new Stream
    
    nute = note.Note('g') # does not matter what note this is
        # we are going to create the contour by moving nute up and down
        
    assert string[0] == '*'
    s.append(nute) # append nute into Stream for first note
    
    string = string[1:] # take only the significant parts i.e. everything BUT the *
    
    
    for char in string: 
        
        nute = note.Note()
        
        if char == 'u' or char == 'U': 
            nute.ps = nute.ps + 1 # raise the pitch of nute
            
        elif char == 'd' or char == 'D':
            nute.ps = nute.ps - 1 # lower the pitch of nute
            
        elif char == 'r' or char == 'R':
            pass # the chicken
            
        else: # if char is not in 'uUdDrR'
            continue # skip the char 
        
        s.append(nute)  # append the note into Stream
    
    return s # return Stream

    
def sortByMeasure(streamList):
    """
    # input: a list of note excerpts to be sorted
    # output: sorted list by measure number of the first note in excerpt
    """
    return sorted(list, key = lambda x: x.notesAndRests[0].measureNumber)


def sortTupleByMeasure(tuplelist):
    """
    # input: a list of tuples (note excerpts, partNumber it was from) to be sorted
    # output: sorted list by measure number of the first note in note excerpt of the tuple
    """
    return sorted(list, key = lambda x: x[0].notesAndRests[0].measureNumber)

        
def approxInterval(interval1, interval2):
    """
    # input: two intervals
    # output: True if the two intervals are 'approximately the same', False otherwise
    #
    # To be 'approximately the same', the direction of the intervals must match
    #     i.e. ascending intervals will never be the same as descending ones
    # The 'function' of the interval must be the same. They are grouped as the following:
    #     'steps': 2nds and 3rds
    #     'perfect': 4ths and 5ths
    #     'leaps': 6ths and 7ths
    # 
    # A case can be made to equate 5ths and octaves, but has not been put into practice here yet
    """
    
    # creation of the Interval objects
    ascending2 = interval.GenericInterval('ascending second')
    descending2 = interval.GenericInterval('descending second')
    ascending3 = interval.GenericInterval('ascending third')
    descending3 = interval.GenericInterval('descending third')
    ascending4 = interval.GenericInterval('ascending fourth')
    descending4 = interval.GenericInterval('descending fourth')
    ascending5 = interval.GenericInterval('ascending fifth')
    descending5 = interval.GenericInterval('descending fifth')
    ascending6 = interval.GenericInterval('ascending sixth')
    descending6 = interval.GenericInterval('descending sixth')
    ascending7 = interval.GenericInterval('ascending seventh')
    descending7 = interval.GenericInterval('descending seventh')
    
    if interval1 == interval2:
        return True
    
    if interval1 == ascending2 or interval1 == ascending3:
        if interval2 == ascending2 or interval2 == ascending3:
            return True
        
    if interval1 == descending2 or interval1 == descending3:
        if interval2 == descending2 or interval2 == descending3:
            return True
        
    if interval1 == ascending4 or interval1 == ascending5:
        if interval2 == ascending4 or interval2 == ascending5:
            return True
        
    if interval1 == descending4 or interval1 == descending5:
        if interval2 == descending4 or interval2 == descending5:
            return True
    
    if interval1 == ascending6 or interval1 == ascending7:
        if interval2 == ascending6 or interval2 == ascending7:
            return True
        
    if interval1 == descending6 or interval1 == descending7:
        if interval2 == descending6 or interval2 == descending7:
            return True

    return False


def exactNoteSearch(score, motifPart, motifStart, motifEnd, notes = None, print_ = 0, octave = 1, show = 0):
    """
    # input:
    #    score - the parsed score to search in
    #
    #    motiPart - integer indicating the part in the score to grab the notes from
    #
    #    motifStart - integer indicating first note of the query
    #
    #    motifEnd - integer indicating the note after the last note of query
    #
    #    notes - string to be converted to a Stream with Notes via stringToNotes()
    #        The given Stream will be used to find matches instead.
    #        If notes isn't None, then motifPart, motifStart, and motifEnd will be ignored.
    #        Default value is None
    #
    #    print_ - If True, print extra information that may be useful in the terminal
    #        Default value is False (0)
    #
    #    octave - If True, match algorithm will ignore octaves, only matching note names
    #        If False, match algorithm will match both octaves and note names
    #        Default value is True
    #
    #    show - If True, color matches to score, and use music21's show('musicxml') to visualize score
    #        Default value is False
    #
    # output: comparing the motif/theme against the score,
    #    returns a list of matching Streams, excerpted from the score
    #    A stream is a match iff all the notes match both in pitch and rhythm to the given motif/theme
    #
    """

    print ('\nSearching by exact note...')
    
    flatParts = [] 
    for part in score.parts:
        flatParts.append(part.flat) # flatten each Parts in the score
        
        
    noteParts = []
    for part in flatParts: # extract notes and rests for each flattened Parts
        noteParts.append(part.notesAndRests)
    
    if notes != None: # if there exists a string for notes
        print ('\tCustom motif used')
        # a very crude way of differentiating strings with octave info and those without
        if hasNumber(notes): # if the string has numbers
            motif = stringToNotesWithOctave(notes) # convert string to Notes via stringToNotesWithOctave*()
        else: # if the string has no numbers
            motif = stringToNotes(notes) # convert string to Notes via stringToNotes()
    else: # if notes == None
        print ('\tMotif defined from score')
        motif = flatParts[motifPart].notes[motifStart:motifEnd] # get match query from score
                            
    
    if print_:
        print ('\tMotif is defined as follows:')
        for thisNote in motif:
            print ('\t\t' + thisNote.nameWithOctave + ' ' + thisNote.duration.type + ' note')
        print()         
        
    matchList = [] # list of matches found
    matchTupleList = [] # tuple of (Stream match, integer listNum)
    matchQ = False
        
    for listNum in range(0, len(noteParts)): # for all parts in the piece
        for noteNum in range(0, len(noteParts[listNum]) - len(motif)): # for all notes in the part
            for motifNoteNum in range(0, len(motif)): # for all notes in the motif
                if octave: # different octaves are acceptable
                    if motif[motifNoteNum].name == noteParts[listNum][noteNum + motifNoteNum].name:
                        #matching pitch (not by octave)
                        if motif[motifNoteNum].duration.type == noteParts[listNum][noteNum + motifNoteNum].duration.type: 
                            #we're also matching length
                            #might not be a good idea to usenote.type, since it groups all complex into 'complex'
                            if motifNoteNum == len(motif) - 1: # if this is the last note to match 
                                matchQ = True # flag as a match
                                
                        else: # note types are different, match failed
                            break
                    else: # note pitches are different, match failed
                        break
                else: # notes with different octaves are different
                    if motif[motifNoteNum] == noteParts[listNum][noteNum + motifNoteNum]: # if note1 = note2
                        if motifNoteNum == len(motif) - 1:
                            matchQ = True
                    else:
                        break
                    
            if matchQ: # if after the forloops, matchQ is True
                match = noteParts[listNum][noteNum : noteNum + len(motif)] # get the matching notes from the score
                match.insert(0, flatParts[listNum].getClefs().elements[0]) # get the clef of the respective part
                    # NOTE! This will fail to give the correct clef if the clef changes in the middle of the piece!
                    # this is literally getting the first clef of the Part where the match is found
                    # works for Art of the Fugue though
                matchList.append(match) # insert match into matchList
                matchTuple = (match, listNum) # define matchTuple as (Stream, integer)
                matchTupleList.append(matchTuple) # insert matchTuple into its separate list
                matchQ = False # reset the match flag
                
        
    print (str(len(matchTupleList)) + ' match(es) found:')
    for entry in matchTupleList: # for all the tuples in matchtupleList
        print ('\tPart ' + str(entry[1]) + ' from measure ' + str(entry[0].notes[0].measureNumber), end = ' ')
        print ('to ' + str(entry[0].notes[-1].measureNumber))
        
    if show: 
        score = colorScore(score, matchTupleList) # color the score with the matches
        score.show('musicxml') # show() the score in musicxml
    
    return matchList #should be list of exact matches


def exactPitchSearch(score, motifPart, motifStart, motifEnd, notes = None, print_ = 0, octave = 1, show = 0):
    """
    # input:
    #    score - the parsed score to search in
    #
    #    motiPart - integer indicating the part in the score to grab the notes from
    #
    #    motifStart - integer indicating first note of the query
    #
    #    motifEnd - integer indicating the note after the last note of query
    #
    #    notes - string to be converted to a Stream with Notes via stringToNotes()
    #        The given Stream will be used to find matches instead.
    #        If notes isn't None, then motifPart, motifStart, and motifEnd will be ignored.
    #        Default value is None
    #
    #    print_ - If True, print extra information that may be useful in the terminal
    #        Default value is False (0)
    #
    #    octave - If True, match algorithm will ignore octaves, only matching note names
    #        If False, match algorithm will match both octaves and note names
    #        Default value is True
    #
    #    show - If True, color matches to score, and use music21's show('musicxml') to visualize score
    #        Default value is False
    #
    # output: comparing the motif/theme against the score,
    #    returns a list of matching Streams, excerpted from the score
    #    A stream is a match iff all the notes match both in pitch (ignores rhythm/duration) to the given motif/theme
    #
    """    
    
    # if notes != None, use notes as motif, and ignore motifPart, motifStart, and motifEnd
    print ('\nSearching by exact pitch...')
    
    flatParts = []
    for part in score.parts:
        flatParts.append(part.flat) # flatten each Parts in the score
        
        
    noteParts = []
    for part in flatParts: # extract notes and rests for each flattened Parts
        noteParts.append(part.notesAndRests)
    
    if notes != None: # if there exists a string for notes
        print ('\tCustom motif used')
        # a very crude way of differentiating strings with octave info and those without        
        if hasNumber(notes):
            motif = stringToNotesWithOctave(notes)
        else:
            motif = stringToNotes(notes)
    else: # if notes == None
        print ('\tMotif defined from score')
        motif = flatParts[motifPart].notes[motifStart:motifEnd]
                            
    
    if print_:
        print ('\tMotif is defined as follows:')
        for thisNote in motif:
            print ('\t\t' + thisNote.nameWithOctave + ' ' + thisNote.duration.type + ' note')
        print ('')               
        
    matchList = []
    matchTupleList = []    
    matchQ = False
        
    for listNum in range(0, len(noteParts)): # for all parts in the piece
        for noteNum in range(0, len(noteParts[listNum]) - len(motif)): # for all notes in the part
            for motifNoteNum in range(0, len(motif)): # for all notes in the motif
                
                if motif[motifNoteNum].name == noteParts[listNum][noteNum + motifNoteNum].name: 
                    #if the note names are the same
                    
                    if octave: #allow different octaves
                        if motifNoteNum == len(motif) - 1:
                            matchQ = True
                    else: #don't allow different octaves
                        if motif[motifNoteNum].octave == noteParts[listNum][noteNum + motifNoteNum].octave:
                            #make sure octaves work
                            if motifNoteNum == len(motif) - 1:
                                matchQ = True

                            
                else:
                    break

                    
            if matchQ:# if after the forloops, matchQ is True
                match = noteParts[listNum][noteNum : noteNum + len(motif)] # get the matching notes from the score
                match.insert(0, flatParts[listNum].getClefs().elements[0]) # get the clef of the respective part
                    # NOTE! This will fail to give the correct clef if the clef changes in the middle of the piece!
                    # this is literally getting the first clef of the Part where the match is found
                    # works for Art of the Fugue though
                matchList.append(match) # insert match into matchList
                matchTuple = (match, listNum) # define matchTuple as (Stream, integer)
                matchTupleList.append(matchTuple) # insert matchTuple into its separate list
                matchQ = False # reset the match flag
                
        
    print (str(len(matchTupleList)) + ' match(es) found:')
    for entry in matchTupleList:
        print ('\tPart %d from measure %d to %d' % (entry[1], entry[0].notes[0].measureNumber, entry[0].notes[-1].measureNumber))
        
    if show:
        score = colorScore(score, matchTupleList) # color the score with the matches
        score.show('musicxml') # show() the score in musicxml
    
    
    return matchList #should be list of exact matches


def exactRhythmSearch(score, motifPart, motifStart, motifEnd, rhythm = None, print_ = 0, context = 0, sort = 'part', show = 0):
    """
    # input:
    #    score - the parsed score to search in
    #
    #    motiPart - integer indicating the part in the score to grab the notes from
    #
    #    motifStart - integer indicating first note of the query
    #
    #    motifEnd - integer indicating the note after the last note of query
    #
    #    rhythm - string to be converted to a Stream with Notes via stringToRhythm()
    #        The given Stream will be used to find matches instead.
    #        If rhythm isn't None, then motifPart, motifStart, and motifEnd will be ignored.
    #        Default value is None
    #
    #    print_ - If True, print extra information that may be useful in the terminal
    #        Default value is False (0)
    #
    #    context - If True, matches will include the 3 notes before or after the actual match
    #
    #    sort - determines the sorting algorithm for printing matches in terminal
    #        Accepts either 'part' or 'measure'
    #        Default value is 'part'
    #
    #    show - If True, color matches to score, and use music21's show('musicxml') to visualize score
    #        Default value is False
    #
    # output: comparing the motif/theme against the score,
    #    returns a list of matching Streams, excerpted from the score
    #    A stream is a match iff all the notes match both in rhythm (not pitch) to the given motif/theme
    #
    """    
    print ('\nSearching by rhythm...')
    
    flatParts = []
    for part in score.parts:
        flatParts.append(part.flat) # flatten each Parts in the score
        
    noteParts = []
    for part in flatParts: # extract notes and rests for each flattened Parts
        noteParts.append(part.notesAndRests)
    
    if rhythm != None: # if there exists a string for rhythm
        motif = stringToNotesRhythm(rhythm)
        if print_:
            print('Searching from string')
    else: # if rhythm == None
        motif = flatParts[motifPart].notes[motifStart:motifEnd]
        if print_:
            print('Motif taken from score')

            
    if print_:
        for note in motif:
            print('\t%s note' % (note.duration.fullName))
        print('')
            
    
    matchList = []
    matchTupleList = []
    matchQ = False
    
    for listNum in range(0, len(noteParts)): # for all parts in the piece
        for noteNum in range(0, len(noteParts[listNum]) - len(motif)): # for all notes in the part
            for motifNoteNum in range(0, len(motif)): # for all notes in the motif
                
                if motif[motifNoteNum].duration.quarterLength == noteParts[listNum][noteNum + motifNoteNum].duration.quarterLength:
                    # if the duration (in quarter length) of the first note is the same as that of the second:
                    if motifNoteNum == len(motif) - 1: # if this is the last notes to be matched
                        matchQ = True # switch match flag to True
                else: # if duration doesn't equate
                    break
            
            if matchQ: # if after the forloops, matchQ is True
                match = noteParts[listNum][noteNum : noteNum + len(motif)] # get the matching notes from the score
                match.insert(0, flatParts[listNum].getClefs().elements[0]) # get the clef of the respective part
                    # NOTE! This will fail to give the correct clef if the clef changes in the middle of the piece!
                    # this is literally getting the first clef of the Part where the match is found
                    # works for Art of the Fugue though
                matchList.append(match) # insert match into matchList
                matchTuple = (match, listNum) # define matchTuple as (Stream, integer)
                matchTupleList.append(matchTuple) # insert matchTuple into its separate list
                matchQ = False # reset the match flag
    
        
        
    print(str(len(matchTupleList)) + ' match(es) found:')
    
    if sort == 'part':
        print('Sorting by parts:')
        
    elif sort == 'measure':
        print('Sorting by measures: ')
        matchList = sortByMeasure(matchList) # sort matchList by measure via sortByMeasure()
        matchTupleList = sortTupleByMeasure(matchTupleList) # sort matchTupleList via sortTupleByMeasure()
        
    for entry in matchTupleList: # print all the matches found
        print('\tPart %d from measure %d to %d' % (entry[1],entry[0].notes[0].measureNumber,entry[0].notes[-1].measureNumber))
        
    if show:
        score = colorScore(score, matchTupleList) # color the score with the matches
        score.show('musicxml') # show() the score in musicxml
    
    return matchList #should be list of exact matches


def exactIntervalSearch(score, motifPart, motifStart, motifEnd, notes = None, print_ = 0, context = 0, show = 0):
    """
    # input:
    #    score - the parsed score to search in
    #
    #    motiPart - integer indicating the part in the score to grab the notes from
    #
    #    motifStart - integer indicating first note of the query
    #
    #    motifEnd - integer indicating the note after the last note of query
    #
    #    notes - string to be converted to a Stream with Notes via stringToNotes()
    #        The given Stream will be used to find matches instead.
    #        If notes isn't None, then motifPart, motifStart, and motifEnd will be ignored.
    #        Default value is None
    #
    #    print_ - If True, print extra information that may be useful in the terminal
    #        Default value is False (0)
    #
    #    context - If True, matches will include the 3 notes before or after the actual match
    #        Default value is False
    #
    #    show - If True, color matches to score, and use music21's show('musicxml') to visualize score
    #        Default value is False
    #
    # output: comparing the motif/theme against the score,
    #    returns a list of matching Streams, excerpted from the score
    #    A Stream is a match iff all the intervals of the Stream match that of the motif
    #
    """    
    
    print('\nSearching by exact intervals...')
    
    flatParts = []
    for part in score.parts:
        flatParts.append(part.flat) # flatten each Parts in the score
    
    noteParts = []
    for part in flatParts: # extract notes and rests for each flattened Parts
        noteParts.append(part.notesAndRests)
    
    if notes != None: # if there exists a string for notes
        print('\tCustom motif used')
        # a very crude way of differentiating strings with octave info and those without
        if hasNumber(notes):
            motif = stringToNotesWithOctave(notes)
        else:
            motif = stringToNotes(notes)
    else: # if notes == None
        print('\tMotif taken from score')
        motif = flatParts[motifPart].notes[motifStart:motifEnd]
    
    
    mIntervalList = []
    matchList = []
    matchTupleList = []

    
    if print_: 
        print('Matching the following intervals:')
        
    for num in range(0, len(motif) - 1):
        mIntervalList.append(interval.notesToChromatic(motif[num], motif[num+1]))
        if print_: 
            print('\t' + str(mIntervalList[num]))
            
            
    # the actual checking
    matchQ = False; # initialization of the match flag
    i = 0 # i and j are both used for context (see below)
    j = 0 
        
    for listNum in range(0, len(noteParts)): # for all parts in the piece
        for noteNum in range(0, len(noteParts[listNum]) - len(mIntervalList)): # for all notes in the part
            for mIntervalNum in range(0, len(mIntervalList)): # for all notes in the motif

                if noteParts[listNum][noteNum + mIntervalNum].isNote:
                    if noteParts[listNum][noteNum + mIntervalNum + 1].isNote : #check if both notes are notes at all
                        #if yes, make interval of this and next note, and use that to compare with motif
                        intervalCandidate = interval.notesToChromatic(noteParts[listNum][noteNum + mIntervalNum], noteParts[listNum][noteNum + mIntervalNum + 1])

                else:  # if not, break
                    #matchQ == False
                    break
            
                
                if (intervalCandidate == mIntervalList[mIntervalNum]): 
                    if mIntervalNum == len(mIntervalList) - 1:
                        matchQ = True
                
                else:
                    break  #candidate interval =/= motif interval

            if matchQ: #if intervalCandidate matches motif
                
                if context: # getting the closest three surrounding notes for the match
                    previousNote = noteParts[listNum][noteNum].previous() # previousNote = the element before the first note of the match
                    nextNote = noteParts[listNum][noteNum + len(mIntervalList) + 1].next() 
                        # nextNote = the element after the last note of the match
                    
                    for num in range(0, 3): # for 3 times
                        if 'Barline' in previousNote.classes: # if the previousNote is a barline
                            num = num - 1 # ignore it (move the pointer num back)
                            
                        elif 'note' in previousNote.classes or 'rest' in previousNote.classes: # if previousNote is a note or rest
                            previousNote = previousNote.previous() # move previousNote to the previous note of the original previousNote
                            i = i + 1 # increment i
                            
                        else : break # if previousNote is neither barline nor note, break
                        
                    for num in range(0, 3):
                        if 'Barline' in nextNote.classes: # if the nextNote is a barline
                            num = num - 1 # ignore it (move the pointer num back)
                        elif 'note' in nextNote.classes or 'rest' in nextNote.classes:# if nextNote is a note or rest
                            nextNote = nextNote.next() # move nextNote to the next note of the original nextNote
                            j = j + 1 # increment j
                            
                        else : break # if nextNote is neither barline nor note, break
                
    
                match = noteParts[listNum][noteNum - i: noteNum + len(mIntervalList) + 1 + j]
                    # match takes in also i notes before and j notes after match
                
    
                match.insert(0, flatParts[listNum].getClefs().elements[0]) # get the clef of the respective part
                    # NOTE! This will fail to give the correct clef if the clef changes in the middle of the piece!
                    # this is literally getting the first clef of the Part where the match is found
                    # works for Art of the Fugue though
                matchTuple = (match, listNum)
                matchList.append(match)
                matchTupleList.append(matchTuple) 
                i = 0 # reset i, j, and matchQ
                j = 0
                matchQ = False

        
    if (print_):
        print('\nMATCHES:') 
        for num in range(0,len(matchList)): # print out all the elements within the matches
            print('Match #' + str(num))
            print(matchList[num])
            matchList[num].show('text')    
            print('')
    
    print(str(len(matchTupleList)) + ' match(es) found:')
    

    for matchTuple in matchTupleList: # print all the matches found
        print('\tPart ' + str(matchTuple[1]) + ' from measure ' + str(matchTuple[0].notes[0].measureNumber), end = ' ')
        print('to ' + str(matchTuple[0].notes[-1].measureNumber))

    if show:
        score = colorScore(score, matchTupleList) # color the score with the matches
        score.show('musicxml') # show() the score in musicxml

    
    return matchList


def genericIntervalSearch(score, motifPart, motifStart, motifEnd, 
                          notes = None, print_ = 0, approx = 0, context = 0, 
                          sort = 'part', show = 0, inverse = 0, retrograde = 0):
    """
    # input:
    #    score - the parsed score to search in
    #
    #    motiPart - integer indicating the part in the score to grab the notes from
    #
    #    motifStart - integer indicating first note of the query
    #
    #    motifEnd - integer indicating the note after the last note of query
    #
    #    notes - string to be converted to a Stream with Notes via stringToNotes()
    #        The given Stream will be used to find matches instead.
    #        If notes isn't None, then motifPart, motifStart, and motifEnd will be ignored.
    #        Default value is None
    #
    #    print_ - If True, print extra information that may be useful in the terminal
    #        Default value is False (0)
    #
    #    approx - If True, match by approxInterval() instead of music21.genericInterval()
    #        Default value is False
    #
    #    context - If True, matches will include the 3 notes before or after the actual match
    #        Default value is False
    #
    #    sort - determines the sorting algorithm for printing matches in terminal
    #        Accepts either 'part' or 'measure'
    #        Default value is 'part'
    #
    #    show - If True, color matches to score, and use music21's show('musicxml') to visualize score
    #        Default value is False
    #
    #    inverse - If True, finds matches for inverses as well
    #        Program will color inverse matches blue for visualization
    #        Default value is False
    #    
    #    retrograde - Unimplemented. 
    #       To be made into a parameter that would allow searches for retrograde melody.
    #
    # output: comparing the motif/theme against the score,
    #    returns a list of matching Streams, excerpted from the score
    #    A Stream is a match iff all the generic intervals of the Stream matches that of the motif
    #
    """        
    
    
    print('\nSearching by generic intervals...')

    
    flatParts = []
    for part in score.parts:
        flatParts.append(part.flat) # flatten each Parts in the score
    
    noteParts = []
    for part in flatParts: # extract notes and rests for each flattened Parts
        noteParts.append(part.notesAndRests)
    
    if notes != None: # if there exists a string for notes
        print('\tCustom motif used')
        # a very crude way of differentiating strings with octave info and those without
        if hasNumber(notes):
            motif = stringToNotesWithOctave(notes)
        else:
            motif = stringToNotes(notes)
    else: # if notes == None
        print('\tMotif taken from score')
        motif = flatParts[motifPart].notes[motifStart:motifEnd]
    
    
    mIntervalList = [] # list of intervals in the motif
    matchList = [] 
    matchTupleList = []
    inverseMatchList = []
    inverseMatchTupleList = []

    currentlyMatching = 'none'
    
    if print_: 
        print('Matching the following intervals:')
        
    for num in range(0, len(motif) - 1):
        mIntervalList.append(interval.notesToGeneric(motif[num], motif[num+1]))
        if print_: 
            print('\t' + str(mIntervalList[num]))
            
            
    # the actual checking
    matchQ = False;
    i = 0
    j = 0
        
    for listNum in range(0, len(noteParts)): # for all parts in the piece
        for noteNum in range(0, len(noteParts[listNum]) - len(mIntervalList)): # for all notes in the part
            for mIntervalNum in range(0, len(mIntervalList)): # for all notes in the motif

                if noteParts[listNum][noteNum + mIntervalNum].isNote:
                    if noteParts[listNum][noteNum + mIntervalNum + 1].isNote : #check if both notes are notes at all
                        #if yes, make interval of this and next note, and use that to compare with motif
                        intervalCandidate = interval.notesToGeneric(noteParts[listNum][noteNum + mIntervalNum], noteParts[listNum][noteNum + mIntervalNum + 1])

                else:  # if not, break
                    #matchQ == False
                    break
                
                
                if mIntervalNum == 0: # when matching the first interval
                    if intervalCandidate == mIntervalList[mIntervalNum]: # if first interval match
                        currentlyMatching = 'regular'
                        
                    elif inverse and intervalCandidate.reverse() == mIntervalList[mIntervalNum]: # if intervals are inverted
                        currentlyMatching = 'inverse'
                        
                    elif approx:
                        if approxInterval(intervalCandidate, mIntervalList[mIntervalNum]): 
                            currentlyMatching = 'regular'
                        
                        elif inverse and approxInterval(intervalCandidate.reverse(), mIntervalList[mIntervalNum]):
                            currentlyMatching = 'inverse'
                        
                        else:
                            currentlyMatching = 'none'
                            break
                    
                    else: # if intervals don't match
                        currentlyMatching = 'none' # reset currentlyMatching
                        break
                    
                    if mIntervalNum == len(mIntervalList) - 1: # if matching the last interval
                        matchQ = True
            
                
                elif (intervalCandidate == mIntervalList[mIntervalNum]): # if interval matches
                    if currentlyMatching == 'regular':
                        if mIntervalNum == len(mIntervalList) - 1: # if matching last interval
                            matchQ = True
                    else: # currentlyMatching != 'regular'
                        currentlyMatching = 'none' # reset currentlyMatching
                        break
                    
                elif inverse and intervalCandidate.reverse() == mIntervalList[mIntervalNum]:
                    # if interval is inverted
                    if currentlyMatching == 'inverse':
                        if mIntervalNum == len(mIntervalList) - 1: # if matching last interval
                            matchQ = True
                    else:
                        currentlyMatching = 'none' # reset currentlyMatching
                        break
                        
                elif approx:
                    if approxInterval(intervalCandidate, mIntervalList[mIntervalNum]):
                        # if the two intervals are approximately the same (see approxInterval())
                        if currentlyMatching == 'regular':
                            if mIntervalNum == len(mIntervalList) - 1: # if matching last interval
                                matchQ = True
                        else:
                            currentlyMatching = 'none' # reset currentlyMatching
                            break
                            
                    elif inverse and approxInterval(intervalCandidate.reverse(), mIntervalList[mIntervalNum]):
                        # if the inverted interval of one is approximately the same as the other (see approxInterval())
                        if currentlyMatching == 'inverse':
                            if mIntervalNum == len(mIntervalList) - 1: # if matching last interval
                                matchQ = True
                        else:
                            currentlyMatching = 'none' # reset currentlyMatching
                            break 
                            
                    else:
                        break
                
                else:
                    break  #candidate interval != motif interval

            if matchQ: #if intervalCandidate matches motif
                
                if context: # getting the closest three surrounding notes for the match
                    previousNote = noteParts[listNum][noteNum].previous() # previousNote = the element before the first note of the match
                    nextNote = noteParts[listNum][noteNum + len(mIntervalList) + 1].next() 
                        # nextNote = the element after the last note of the match
                    
                    for num in range(0, 3): # for 3 times
                        if 'Barline' in previousNote.classes: # if the previousNote is a barline
                            num = num - 1 # ignore it (move the pointer num back)
                            
                        elif 'note' in previousNote.classes or 'rest' in previousNote.classes: # if previousNote is a note or rest
                            previousNote = previousNote.previous() # move previousNote to the previous note of the original previousNote
                            i = i + 1 # increment i
                            
                        else : break # if previousNote is neither barline nor note, break
                        
                    for num in range(0, 3):
                        if 'Barline' in nextNote.classes: # if the nextNote is a barline
                            num = num - 1 # ignore it (move the pointer num back)
                        elif 'note' in nextNote.classes or 'rest' in nextNote.classes:# if nextNote is a note or rest
                            nextNote = nextNote.next() # move nextNote to the next note of the original nextNote
                            j = j + 1 # increment j
                            
                        else : break # if nextNote is neither barline nor note, break                
                
                
                match = noteParts[listNum][noteNum - i: noteNum + len(mIntervalList) + 1 + j]             
    
                match.insert(0, flatParts[listNum].getClefs().elements[0]) # get the clef of the respective part
                    # NOTE! This will fail to give the correct clef if the clef changes in the middle of the piece!
                    # this is literally getting the first clef of the Part where the match is found
                    # works for Art of the Fugue though
                matchTuple = (match, listNum)
                
                if currentlyMatching == 'regular':
                    matchList.append(match)
                    matchTupleList.append(matchTuple)
                    
                elif inverse and currentlyMatching == 'inverse':
                    inverseMatchList.append(match)
                    inverseMatchTupleList.append(matchTuple)
                
                i = 0 # i, j, matchQ, and currentlyMatching
                j = 0
                matchQ = False 
                currentlyMatching = 'none'

        
    if (print_):
        
        print('\nMATCHES:') # print all the intervals of every match
        
        for num in range(0,len(matchList)):
            print('Match #' + str(num))
            for stuff in range(1, len(matchList[num].elements) - 1): # for all the note pairs
                if matchList[num].elements[stuff].isNote and matchList[num].elements[stuff + 1].isNote:
                    interval.notesToGeneric(matchList[num].elements[stuff], matchList[num].elements[stuff + 1])
                    # convert notes to intervals
            matchList[num].show('text')    
            print('')
    
    
    print(str(len(matchTupleList)) + ' match(es) found:')   
    
    for matchTuple in matchTupleList: # print all the matches found
        print('\tPart', str(matchTuple[1]) + ' from measure ' + str(matchTuple[0].notes[0].measureNumber), end = '')
        print(' to ' + str(matchTuple[0].notes[-1].measureNumber))
    
    if inverse:
        print('\nINVERSE MATCHES:')
        print(str(len(inverseMatchTupleList)) + ' match(es) found:')
        for inverseMatchTuple in inverseMatchTupleList: # print all the inverse matches found
            print('\tPart ' + str(inverseMatchTuple[1]) + ' from measure ' + str(inverseMatchTuple[0].notes[0].measureNumber), end = '')
            print(' to ' + str(inverseMatchTuple[0].notes[-1].measureNumber))

    if show:
        print('Coloring matches...')
        score = colorScore(score, matchTupleList)
        score = colorScore(score, inverseMatchTupleList, noteColor = '#0000FF')
        print('Coloring finished')
        score.show('musicxml') # show() the score in musicxml

    return matchList


def exactContourSearch(score, motifPart, motifStart, motifEnd, 
                       contour = None, print_ = 0, approx = 0, context = 0, sort = 'part', show = 0, inverse = 0):
    """
    # Given a score, which part the motif occurs (motifPart), where it starts (motifStart) and ends (motifEnd) by notes,
    #    returns a list of Part excerpts that contain a matching contour line to the theme
    #
    # contour is a string that will be used to match contour lines. motifPart, motifStart, and motifEnd will be ignored
    #
    # print_ is a boolean value that, if true, make the program print out additional information (what notes are in the matches)
    #
    # approx is not used (transferred over from genericIntervalSearch). 
    #    TODO: make approx match excerpts based on looser criteria?
    #
    # context is a boolean value that, if true, will grab surrounding measures for context when returning the matchList
    #    justification: might want to use this function if you are using matchList to print out each matches separately?
    #
    # sort is a string of values either 'part' or 'measure'
    #    the printed list will be sorted by either part or measure, respectively
    #    TODO: sort the returned matchList as well
    #
    # show is a boolean value that, if true, will export the score (using music21's show() function)
    #    the exported score will have all the matches colored in red
    #    if inverse is also True, the exported score will have all inverse matches colored in green
    #
    """
    
    print('\nSearching by contour...')
    
    matchList = []
    matchTupleList = []
    inverseMatchList = []
    inverseMatchTupleList = []
    
    motifContour = []
    
    
    flatParts = []
    for part in score.parts: # flatten each part of the score and put it in a list
        flatParts.append(part.flat) 
    
    noteParts = []
    for part in flatParts: # extract only notes and rests of the list of flat parts
        noteParts.append(part.notesAndRests)


    if contour != None: # if there exists a custom contour
        print('\tCustom motif used')
        motif = contourToNotes(contour) # gives notes with the given contour from string
         
    else: # if no custom contour found (contour == None)
        print('\tMotif taken from score')
        motif = flatParts[motifPart].notes[motifStart:motifEnd] # get the notes pointed by motifPart, motifStart & End
    
    # append contour information into motifConour list
    for num in range(0, len(motif) - 1): # for every interval/pairs of notes
        if motif[num].ps < motif[num + 1].ps: # if first note is lower than the second
            motifContour.append('up')
            
        elif motif[num].ps > motif[num + 1].ps: # if first note is higher than the second
            motifContour.append('down')
            
        elif motif[num].ps == motif[num + 1].ps: # if the first note is the same as the second
            motifContour.append('repeat')
            
        else: # should never happen
            print('SOMERTHING HAS GONER RONG')
            pass # the bacon, please
        
        
    if print_: # verbose
        print('Contour is defined as follows:')
        for stuff in motifContour:
            print(stuff)
        print('')

    matchQ = False #initializing match flag
    currentlyMatching = 'none' 
        
    for partNum in range(0, len(noteParts)): # for every part in the score
        for noteNum in range(0, len(noteParts[partNum]) - len(motif)): # for all notes in the part
            for motifNum in range(0, len(motif) - 1): #for all the notes in the motif
                #compare noteNumth note with the next one in the part
                if not noteParts[partNum][noteNum + motifNum].isNote: # if first element isn't a note
                    break
                if not noteParts[partNum][noteNum + motifNum + 1].isNote: # if second element isn't a note
                    break

                
                if currentlyMatching == 'none': # if we're not currentlyMatching anything 
                    # this should only be run for the first note comparison
                    if noteParts[partNum][noteNum + motifNum].ps < noteParts[partNum][noteNum + motifNum + 1].ps:
                        # if the first pair of notes is going up
                        if motifContour[motifNum] == 'up': # if it matches the respective query area
                            currentlyMatching = 'regular' 
                        elif inverse and motifContour[motifNum] == 'down': # if it is inverted to the query area
                            currentlyMatching = 'inverse'
                        else: #motifContour[motifNum] == 'repeat' 
                            # might do some approximation to allow repeats to be equal 'up'
                            break
                        
                            
                    elif noteParts[partNum][noteNum + motifNum].ps > noteParts[partNum][noteNum + motifNum + 1].ps:
                        # if the first pair of notes is going down
                        if motifContour[motifNum] == 'down': # if it matches the respective query area
                            currentlyMatching = 'regular'
                        elif inverse and motifContour[motifNum] == 'up': # if it is inverted to the query area
                            currentlyMatching = 'inverse'
                        else: #motifContour[motifNum] == 'repeat'
                            break
                            
                            
                    elif noteParts[partNum][noteNum + motifNum].ps == noteParts[partNum][noteNum + motifNum + 1].ps:
                        # if the first two notes are the same
                        if motifContour[motifNum] != 'repeat': 
                            break
                        else: # motifContour[motifNum] == 'repeat'
                            pass
                        
                    else:
                        print('this realllly shouldn\'t happen') # this really shouldn't happen
                        
                        
                    if motifNum == len(motif) - 2: # if comparing the last contour element
                        # note: this is to catch the degenerative case where we're only matching for two notes
                        matchQ = True   # match flag = True
                            # this is because if the contours doesn't match, the forloop breaks
                            # if it reaches here that means the forloop hasn't broken yet                                 
                            
                    # after this, we'll have currentlyMatching information
                
                
                elif currentlyMatching == 'regular':
                    if noteParts[partNum][noteNum + motifNum].ps < noteParts[partNum][noteNum + motifNum + 1].ps:
                        # if first note is lower than second note (going up)
                        if motifContour[motifNum] == 'up': 
                            if motifNum == len(motif) - 2: # if comparing the last contour element
                                matchQ = True
    
                        else: # if contour element isn't 'up'
                            currentlyMatching = 'none' # reset currentlyMatching
                            break
                        
                    elif noteParts[partNum][noteNum + motifNum].ps > noteParts[partNum][noteNum + motifNum + 1].ps:
                            # if first note is higher than second note (going down)
                        if motifContour[motifNum] == 'down':
                            if motifNum == len(motif) - 2: # if comparing the last contour element
                                matchQ = True 
                        else: # if contour element isn't 'up'
                            currentlyMatching = 'none' # reset currentlyMatching
                            break
                        
                    elif noteParts[partNum][noteNum + motifNum].ps == noteParts[partNum][noteNum + motifNum + 1].ps:
                        # if first note is the same as the second note (repeat)
                        if motifContour[motifNum] == 'repeat':
                            if motifNum == len(motif) - 2: # if comparing the last contour element
                                matchQ = True
                        else:
                            currentlyMatching = 'none' # reset currentlyMatching
                            break
                        
                elif currentlyMatching == 'inverse':
                    if noteParts[partNum][noteNum + motifNum].ps < noteParts[partNum][noteNum + motifNum + 1].ps:
                        # if first note is lower than second note (going up)
                        if motifContour[motifNum] == 'down':
                            if motifNum == len(motif) - 2:
                                matchQ = True
    
                        else:
                            currentlyMatching = 'none' # reset currentlyMatching
                            break
                        
                    elif noteParts[partNum][noteNum + motifNum].ps > noteParts[partNum][noteNum + motifNum + 1].ps:
                        # if first note is higher than second note (going down)
                        if motifContour[motifNum] == 'up':
                            if motifNum == len(motif) - 2:
                                matchQ = True
                        else:
                            currentlyMatching = 'none' # reset currentlyMatching
                            break
                        
                    elif noteParts[partNum][noteNum + motifNum].ps == noteParts[partNum][noteNum + motifNum + 1].ps:
                        if motifContour[motifNum] == 'repeat':
                            if motifNum == len(motif) - 2:
                                matchQ = True
                        else:
                            currentlyMatching = 'none' # reset currentlyMatching
                            break                    
                
                    
            if matchQ:
                
                match = noteParts[partNum][noteNum: noteNum + len(motif)]
                match.insert(0, flatParts[partNum].getClefs().elements[0])                
                matchTuple = (match, partNum)
                
                if currentlyMatching == 'regular':
                    matchList.append(match)
                    matchTupleList.append(matchTuple)
                
                elif currentlyMatching == 'inverse': 
                    inverseMatchList.append(match)
                    inverseMatchTupleList.append(matchTuple)
                
                
                matchQ = False
                currentlyMatching = 'none'

                
    if (print_):
        print('\nMATCHES:')
        for num in range(0,len(matchList)):
            print('Match #' + str(num))
            print(matchList[num])
            matchList[num].show('text')    
            print('')
    
    
    
    print(str(len(matchTupleList)) + ' match(es) found:')
    
    if sort == 'part':
        pass
            
    elif sort == 'measure':
        print('Sorting by measures: ')
        matchList = sortByMeasure(matchList)
        matchTupleList = sortTupleByMeasure(matchTupleList)
    
    for matchTuple in matchTupleList:
        print('\tPart %d from measure %d to %d' % (matchTuple[1], matchTuple[0].notes[0].measureNumber, matchTuple[0].notes[-1].measureNumber))

    
    if inverse:
        print(str(len(matchTupleList)) + ' inverse match(es) found:')  
        for inverseMatchTuple in inverseMatchTupleList:
            print('\tPart %d from measure %d to %d' % (inverseMatchTuple[1], inverseMatchTuple[0].notes[0].measureNumber, inverseMatchTuple[0].notes[-1].measureNumber))      
    
    if show:
        score = colorScore(score, matchTupleList)
        score = colorScore(score, inverseMatchTupleList, noteColor = '#00FF00')
        score.show('musicxml')
        
    
    return matchList


def rhythmContourSearch(score, motifPart, motifStart, motifEnd, contour = None, print_ = 0, approx = 0, context = 0, sort = 'part'):
    """
    # Unimplemented
    #
    # This search would search for contours over relative rhythm
    #     Not all the notes will be used, just an approximation
    #
    """
    matchList = []
    
    return matchList


def colorScore(score, matchTupleList, noteColor = '#FF0000'):
    """
    # Given a score and a matchTupleList (Stream, int)
    #    for all the matchTuples: color its respective part in the score
    #
    # noteColor defines the color, red by default
    """
    
    flatParts = []
    matchPlace = -1
    offsetMapList = []
    
    for part in score.parts: # for every part in the score
        flatParts.append(part.flat) # flatten part in the score
        offsetMapList.append(part.flat.notesAndRests.offsetMap) # extract notes and rests from the flattened part
    
    for match in matchTupleList: # for every match in matchTupleList
        targetOffset = match[0].flat.notesAndRests[0].offset 
            # define targetOffset as the offset (distance from the front) of the first element in match
        partNum = match[1]
        
        for checkNoteNum in range(0, len(score.parts[partNum].flat.notesAndRests)): # for every note in the respective Part of the score

            if offsetMapList[partNum][checkNoteNum]['offset'] == targetOffset: # if the offset of the note from match is the same from score
                matchPlace = checkNoteNum # we've found the first note to be colored
                break
            

        
        if matchPlace != -1: # if we found a note at the given offset
            
            for num in range(0, len(match[0].notesAndRests)):
                score.parts[partNum].flat.notesAndRests[checkNoteNum + num].color = noteColor
                
            matchPlace = -1
                
        else: # if we didn't find any note at the given offset
            print('Cannot color score as %s cannot be found' % match[0])
            
    
    return score


def demo():
    number = input('Art of the Fugue #?: ')
    
    header = 'bach/artOfFugue_bwv1080/'
    tailer = '.zip'
    
    if number >= 1 and number < 10:
        location = '{0}{1}{2}{3}'.format(header, '0', str(number), tailer)
    
    elif number >= 10 and number < 22:
        location = '{0}{1}{2}'.format(header,str(number), tailer)
        
    sBach = (corpus.parse(location))
    
    part = input('Where is the theme? ')
    
# Uncomment for an example
# sBach6 = corpus.parse('bach/artOfFugue_bwv1080/06.zip')
# test = genericIntervalSearch(sBach6, 4, 0, 10, show = 1, approx = 1, inverse = 1, sort = 'part')
    
