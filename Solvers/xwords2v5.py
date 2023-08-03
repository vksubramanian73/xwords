import sys; args = sys.argv[1:]
# Varshini Subramanian, Period 7
import time
# FINAL VERSION: RECEIVED A 100 AND VERY FAST :)
# changes made:
# set intersections for valid words of all constraints
# checking how many words have letter replacing star (word[space]), and sorting based on that 

height = -1
width = -1
blocking_squares_count = -1
pzl = ''
file_to_read = ''
start_time = time.process_time()
gLETTERPOSTOWORD = {}
wordLst = []
gLETTERS = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}

def setGlobals():
    global height, width, blocking_squares_count, pzl, file_to_read, gLETTERPOSTOWORD, wordLst
    if args:
        x_index = args[0].find('x')
        height = int(args[0][0:x_index])
        width = int(args[0][x_index+1:])
        pzlList = ['-']*(height*width)
        blocking_squares_count = int(args[1])
        file_to_read = args[2]
        if blocking_squares_count % 2 == 1: pzlList[len(pzlList)//2] = '#'
        #parsing through the seed strings depending on how many there are
        for i in range(3, len(args)):
            arg = args[i]
            #finding the position of the seed string
            orientation = arg[0].lower(); arg_x_index = arg.find('x')
            end_of_number_2 = -1; word = ''
            for j in range(len(arg) - 1, arg.find('x'), -1):
                if arg[j].isdigit(): end_of_number_2 = j; break
                else: word = word + arg[j]
            #finding exactly what the seed string is and placing it horizontally/vertically depending on orientation
            word = word[::-1]
            row = int(arg[1:arg_x_index])
            column = int(arg[arg_x_index+1:end_of_number_2+1])
            if end_of_number_2 == len(arg) - 1: 
                if orientation == 'v': pzlList[row*width + column] = '#'
                else: pzlList[row*width + column] = '#'
            for x in range(0, len(word)):
                if orientation == 'v':
                    if word[x] == '#': pzlList[(row+x)*width + column] = '#'
                    else: pzlList[(row+x)*width + column] = word[x].upper()
                else: 
                    if word[x] == '#': pzlList[row*width + column + x] = '#'
                    else: pzlList[row*width + column + x] = word[x].upper()
        pzl = ''.join(pzlList)
        wordLst = open(file_to_read, 'r').read().splitlines()
        greater = max(height, width)
        #adding words to lookup table
        #lookup table: (letter, position):word
        for word in wordLst:
            if len(word) > greater: continue
            for i,ch in enumerate(word):
                if (ch.upper(), i) in gLETTERPOSTOWORD: gLETTERPOSTOWORD[(ch.upper(), i)].add(word.upper())
                else: gLETTERPOSTOWORD[(ch.upper(), i)] = {word.upper()}
        
def strPuzzle(puzzle):
    newstr = ''
    for i, v in enumerate(puzzle):
        newstr += v
        if (i+1) % width == 0 and i != len(puzzle) - 1: newstr += '\n'
    return newstr

def fixSquares(puzzle):
    lstPuzzle = [*puzzle]
    for i,ch in enumerate(lstPuzzle):
        if ch.isalpha() or ch == '0': 
            #general: i check if the position has a '-' so that i don't override fixed letters
            #top down conditions: only one of the four needs to be satisfied
            #000 from topmost row
            if i // width == 0:
                if lstPuzzle[i + width] == '-': lstPuzzle[i + width] = '0'
                if lstPuzzle[i + 2*width] == '-': lstPuzzle[i + 2*width] = '0'
            #000 from bottommost row
            elif i // width == height - 1:
                if lstPuzzle[i - width] == '-': lstPuzzle[i - width] = '0'
                if lstPuzzle[i - 2*width] == '-': lstPuzzle[i - 2*width] = '0'
            #-00- from second to top row
            elif i // width == 1: 
                if lstPuzzle[i + width] == '-': lstPuzzle[i + width] = '0'
            #-00- from second to bottom row
            elif i // width == height - 2:
                if lstPuzzle[i - width] == '-': lstPuzzle[i - width] = '0'
            
            #left right conditions: only one of the four needs to be satisfied
            #000 from leftmost row
            if i % width == 0: 
                if lstPuzzle[i + 1] == '-': lstPuzzle[i + 1] = '0'
                if lstPuzzle[i + 2] == '-': lstPuzzle[i + 2] = '0'
            #000 from rightmost row
            elif i % width == width - 1:
                if lstPuzzle[i - 1] == '-': lstPuzzle[i - 1] = '0'
                if lstPuzzle[i - 2] == '-': lstPuzzle[i - 2] = '0'
            #-00- from second to left row
            elif i % width == 1: 
                if lstPuzzle[i + 1] == '-': lstPuzzle[i + 1] = '0'
            #-00- from second to right row
            elif i % width == width - 2: 
                if lstPuzzle[i - 1] == '-': lstPuzzle[i - 1] = '0'
    #ensuring symmetry for the whole puzzle
    for i,ch in enumerate(lstPuzzle):
        if ch == '#': lstPuzzle[len(puzzle) - 1 - i] = '#'
        elif ch.isalpha() or ch == '0': 
            if lstPuzzle[len(puzzle) - 1 - i] == '-': lstPuzzle[len(puzzle) - 1 - i] = '0'
    return ''.join(lstPuzzle)

#finding an empty space with the highest block heuristic (below)
#high heuristic = better
def bestSpaceBlockingSquare(puzzle):
    posToHeuristic = {}; pos = -1
    for pos in [i for i,ch in enumerate(puzzle) if ch == '-']:
        heuristic = block_heuristic(puzzle, pos)
        posToHeuristic[pos] = heuristic
    #returning spaces based on decreasing heuristic
    return sorted(posToHeuristic, key=posToHeuristic.get, reverse=True)

def block_heuristic(puzzle, space):
    up = 0; down = 0; left = 0; right = 0
    #finding number of empty spaces/letters below index param
    for i in range(space, len(puzzle), width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '0': down += 1
        elif puzzle[i] == '#': break 
    #finding number of empty spaces/letters above index param
    for i in range(space-width, -1, -width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '0': up += 1
        elif puzzle[i] == '#': break
    #finding number of empty spaces/letters to the right of index param
    for i in range(space, space+width-space%width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '0': right += 1
        elif puzzle[i] == '#': break
    #finding number of empty spaces/letters to the left of index param
    for i in range(space-1, space-space%width-1, -1):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '0': left += 1
        elif puzzle[i] == '#': break
    return left*right + up*down

def placeBlockingSquares(puzzle): #similar to brute force
    if puzzle.count('#') == blocking_squares_count: return puzzle
    elif puzzle.count('#') > blocking_squares_count: return ''
    #need to make a copy because floodfill changes the board
    lstPuzzleWithIsolations = [*puzzle]
    identifyIsolatedRegions(lstPuzzleWithIsolations, puzzle.find('-'))
    #floodfill algorithm replaces connected squares w a '$'
    #so if there are '-' or '0' that means there are still disconnected regions
    if '-' in lstPuzzleWithIsolations or '0' in lstPuzzleWithIsolations: return ''
    #print(strPuzzle(puzzle)); print() --> debugging 
    for pos in bestSpaceBlockingSquare(puzzle): #bestSpaceBlockingSquare sorts by heuristic
        lstPuzzle = [*puzzle]
        #symmetry
        lstPuzzle[pos] = lstPuzzle[len(puzzle) - pos - 1] = '#'
        block_positions = [pos, len(puzzle) - pos - 1]
        #placing forced blocking squares until there are no more blocking squares to be placed
        #ensures that the board is always valid
        while(block_positions):
            pos_to_input = block_positions.pop(0)
            lstPuzzle, block_positions = placeForcedBlocks(lstPuzzle, pos_to_input, block_positions)
        #only places forced letters for the index (pos)
        lstPuzzle = placeForcedLetters(lstPuzzle, pos)
        subPzl = ''.join(lstPuzzle)
        #print(strPuzzle(subPzl)); print() --> debugging 
        bF = placeBlockingSquares(subPzl)
        if bF: return bF
    return ''

def placeForcedBlocks(lstPuzzle, pos, block_positions):
    #in general: lstPuzzle[pos] is guaranteed to be a blocking square
    #left right conditions: only one of the following four conditions needs to be satisfied
    # --# condition from leftmost column
    if pos % width == 2:
        if lstPuzzle[pos - 1] != '#' and lstPuzzle[pos - 2] != '#': 
            lstPuzzle[pos - 1] = lstPuzzle[pos - 2] = '#'
            block_positions.append(pos-1); block_positions.append(pos-2)
    # #-- condition from rightmost column
    elif pos % width == width - 3:
        if lstPuzzle[pos + 1] != '#' and lstPuzzle[pos + 2] != '#': 
            lstPuzzle[pos + 1] = lstPuzzle[pos + 2] = '#'
            block_positions.append(pos+1); block_positions.append(pos+2)
    # -# condition from leftmost column
    elif pos % width == 1: 
        if lstPuzzle[pos - 1] != '#': lstPuzzle[pos - 1] = '#'; block_positions.append(pos-1)
    # #- condition from rightmost column
    elif pos % width == width - 2:
        if lstPuzzle[pos + 1] != '#': lstPuzzle[pos + 1] = '#'; block_positions.append(pos+1)
    
    #top down conditions: only one of the following four conditions needs to be satisfied
    # #-- condition from topmost row
    if pos // width == 2: # #-- condition from topmost row
        if lstPuzzle[pos - width] != '#' and lstPuzzle[pos - 2*width] != '#': 
            lstPuzzle[pos - width] = lstPuzzle[pos - 2*width] = '#'
            block_positions.append(pos-width); block_positions.append(pos-2*width)
    # #-- condition from bottommost row
    elif pos // width == height - 3:
        if lstPuzzle[pos + width] != '#' and lstPuzzle[pos + 2*width] != '#': 
            lstPuzzle[pos + width] = lstPuzzle[pos + 2*width] = '#'
            block_positions.append(pos+width); block_positions.append(pos+2*width)
    # -# condition from topmost row
    elif pos // width == 1:
        if lstPuzzle[pos - width] != '#': lstPuzzle[pos - width] = '#'; block_positions.append(pos-width)
    # #- condition from bottommost row
    elif pos // width == height - 2:
        if lstPuzzle[pos + width] != '#': lstPuzzle[pos + width] = '#'; block_positions.append(pos+width)
    
    # #--# condition across rows in general (left to right)
    if pos // width == (pos + 1) // width == (pos + 2) // width == (pos + 3) // width:
        if lstPuzzle[pos + 3] == '#' and lstPuzzle[pos + 2] != '#' and lstPuzzle[pos + 1] != '#': 
            lstPuzzle[pos + 1] = lstPuzzle[pos + 2] = '#'
            block_positions.append(pos+1); block_positions.append(pos+2)
    # #--# condition across rows in general (right to left)
    if pos // width == (pos - 1) // width == (pos - 2) // width == (pos - 3) // width: 
        if lstPuzzle[pos - 3] == '#' and lstPuzzle[pos - 2] != '#' and lstPuzzle[pos - 1] != '#': 
            lstPuzzle[pos - 1] = lstPuzzle[pos - 2] = '#'
            block_positions.append(pos-1); block_positions.append(pos-2)
    # #--# condition across columns in general (top to bottom)
    if pos + 3*width < len(lstPuzzle): 
        if lstPuzzle[pos + 3*width] == '#' and lstPuzzle[pos + 2*width] != '#' and lstPuzzle[pos + width] != '#': 
            lstPuzzle[pos + width] = lstPuzzle[pos + 2*width] = '#'
            block_positions.append(pos+width); block_positions.append(pos+2*width)
    # #--# condition across columns in general (bottom to top)
    if pos - 3*width > 0:
        if lstPuzzle[pos - 3*width] == '#' and lstPuzzle[pos - 2*width] != '#' and lstPuzzle[pos - width] != '#': 
            lstPuzzle[pos - width] = lstPuzzle[pos - 2*width] = '#'
            block_positions.append(pos-width); block_positions.append(pos-2*width)
    
    # #-# condition across rows in general (left to right)
    if pos // width == (pos + 1) // width == (pos + 2) // width: 
        if lstPuzzle[pos + 2] == '#' and lstPuzzle[pos + 1] != '#': lstPuzzle[pos + 1] = '#'; block_positions.append(pos+1)
    # #-# condition across rows in general (right to left)
    if pos // width == (pos - 1) // width == (pos - 2) // width: 
        if lstPuzzle[pos - 2] == '#' and lstPuzzle[pos - 1] != '#': lstPuzzle[pos - 1] = '#'; block_positions.append(pos-1)
    # #-# condition across columns in general (top to bottom)
    if pos + 2*width < len(lstPuzzle): 
        if lstPuzzle[pos + 2*width] == '#' and lstPuzzle[pos + width] != '#': lstPuzzle[pos + width] = '#'; block_positions.append(pos+width)
    # #-# condition across columns in general (bottom to top)
    if pos - 2*width > 0: 
        if lstPuzzle[pos - 2*width] == '#' and lstPuzzle[pos - width] != '#': lstPuzzle[pos - width] = '#'; block_positions.append(pos-width)
    
    #ensuring symmetry for the whole puzzle
    for i,ch in enumerate(lstPuzzle):
        if ch == '#': lstPuzzle[len(lstPuzzle) - 1 - i] = '#'
        elif ch.isalpha() or ch == '0': 
            if lstPuzzle[len(lstPuzzle) - 1 - i] == '-': lstPuzzle[len(lstPuzzle) - 1 - i] = '0'
    return lstPuzzle, block_positions

def placeForcedLetters(lstPuzzle, pos):
    #in general: lstPuzzle[pos] is guaranteed to be a blocking square
    # #000 condition across rows (left to right, leading to an edge)
    if pos // width == (pos + 1) // width == (pos + 2) // width == (pos + 3) // width:
        if (lstPuzzle[pos + 1].isalpha() or lstPuzzle[pos + 1] == '0') and (lstPuzzle[pos + 2].isalpha() or lstPuzzle[pos + 2] == '0'):
            if lstPuzzle[pos + 3] == '-': lstPuzzle[pos + 3] = '0'
        if lstPuzzle[pos + 1] == lstPuzzle[pos + 2] == lstPuzzle[pos + 3] == '-':
            if (pos + 3) % width == width - 1:
                lstPuzzle[pos + 1] = lstPuzzle[pos + 2] = lstPuzzle[pos + 3] = '0'
        if (lstPuzzle[pos + 1].isalpha() or lstPuzzle[pos + 1] == '0'):
            if lstPuzzle[pos + 2] == '-': lstPuzzle[pos + 2] = '0'
            if lstPuzzle[pos + 3] == '-': lstPuzzle[pos + 3] = '0'
        if (lstPuzzle[pos + 2].isalpha() or lstPuzzle[pos + 2] == '0'):
            if lstPuzzle[pos + 1] == '-': lstPuzzle[pos + 1] = '0'
            if lstPuzzle[pos + 3] == '-': lstPuzzle[pos + 3] = '0'
        if (lstPuzzle[pos + 3].isalpha() or lstPuzzle[pos + 3] == '0'):
            if lstPuzzle[pos + 1] == '-': lstPuzzle[pos + 1] = '0'
            if lstPuzzle[pos + 2] == '-': lstPuzzle[pos + 2] = '0'
    
    # #000# condition across rows in general (left to right)
    if pos // width == (pos + 1) // width == (pos + 2) // width == (pos + 3) // width == (pos + 4) // width:
        if lstPuzzle[pos + 4] == '#':
            if lstPuzzle[pos + 1] == '-': lstPuzzle[pos + 1] = '0'
            if lstPuzzle[pos + 2] == '-': lstPuzzle[pos + 2] = '0'
            if lstPuzzle[pos + 3] == '-': lstPuzzle[pos + 3] = '0'
    
    # #000 condition across columns (top to bottom, leading to an edge)
    if pos + 3*width < len(lstPuzzle):
        if (lstPuzzle[pos + width].isalpha() or lstPuzzle[pos + width] == '0') and (lstPuzzle[pos + 2*width].isalpha() or lstPuzzle[pos + 2*width] == '0'):
            if lstPuzzle[pos + 3*width] == '-': lstPuzzle[pos + 3*width] = '0'
        if lstPuzzle[pos + width] == lstPuzzle[pos + 2*width] == lstPuzzle[pos + 3*width] == '-':
            if (pos + 3*width) // width == width - 1:
                lstPuzzle[pos + width] = lstPuzzle[pos + 2*width] = lstPuzzle[pos + 3*width] = '0'
        if (lstPuzzle[pos + width].isalpha() or lstPuzzle[pos + width] == '0'):
            if lstPuzzle[pos + 2*width] == '-': lstPuzzle[pos + 2*width] = '0'
            if lstPuzzle[pos + 3*width] == '-': lstPuzzle[pos + 3*width] = '0'
        if (lstPuzzle[pos + 2*width].isalpha() or lstPuzzle[pos + 2*width] == '0'):
            if lstPuzzle[pos + width] == '-': lstPuzzle[pos + width] = '0'
            if lstPuzzle[pos + 3*width] == '-': lstPuzzle[pos + 3*width] = '0'
        if (lstPuzzle[pos + 3*width].isalpha() or lstPuzzle[pos + 3*width] == '0'):
            if lstPuzzle[pos + width] == '-': lstPuzzle[pos + width] = '0'
            if lstPuzzle[pos + 2*width] == '-': lstPuzzle[pos + 2*width] = '0'
    
    # #000# across columns in general (top to bottom)
    if pos + 4*width < len(lstPuzzle):
        if lstPuzzle[pos + 4*width] == '#':
            if lstPuzzle[pos + width] == '-': lstPuzzle[pos + width] = '0'
            if lstPuzzle[pos + 2*width] == '-': lstPuzzle[pos + 2*width] = '0'
            if lstPuzzle[pos + 3*width] == '-': lstPuzzle[pos + 3*width] = '0'
    
    #ensuring symmetry for the whole puzzle
    for i,ch in enumerate(lstPuzzle):
        if ch == '#': lstPuzzle[len(lstPuzzle) - 1 - i] = '#'
        elif ch.isalpha() or ch == '0': 
            if lstPuzzle[len(lstPuzzle) - 1 - i] == '-': lstPuzzle[len(lstPuzzle) - 1 - i] = '0'
    return lstPuzzle

#floodfill/areafill algorithm
def identifyIsolatedRegions(lstPuzzle, pos):
    #checking if the position is out of bounds
    if pos < 0 or pos >= len(lstPuzzle): return
    #further checking if the position is out of bounds
    if pos // width < 0 or pos // width >= height or pos % width < 0 or pos % width >= width: return
    #checking if the position is either a blocking square or already visited
    if lstPuzzle[pos] == '#' or lstPuzzle[pos] == '$': return
    #marking the position as visited
    lstPuzzle[pos] = '$'
    #recursive call for above position
    identifyIsolatedRegions(lstPuzzle, pos - width)
    #recursive call for below position
    identifyIsolatedRegions(lstPuzzle, pos + width)
    #recursive call for right position IF right position is on the same row as position
    if (pos + 1) // width == pos // width: identifyIsolatedRegions(lstPuzzle, pos + 1)
    #recursive call for left position IF left position is on the same row as position
    if (pos - 1) // width == pos // width: identifyIsolatedRegions(lstPuzzle, pos - 1)

#called only once --> before bruteForce is called
def fillIsolatedRegions(puzzle, pzlListWithIsolations):
    pzlList = [*puzzle]
    #isolated regions must have '0' or '-' because they have not been visited in floodfill
    isolated = [i for i,ch in enumerate(pzlListWithIsolations) if ch == '-' or ch == '0']
    for i in isolated:
        #replacing each isolated square w a blocking square
        pzlList[i] = '#'
    return ''.join(pzlList)

def placeLetters(puzzle, wordsUsed):
    if puzzle.count('-') == 0: return puzzle
    lstPuzzle = [*puzzle]
    #LOL idk why but bestSpace does not work for 5x5 so heres some special casing :)
    if height == width == 5: space = puzzle.find('-'); letters, letterToWord = findLetters(lstPuzzle, wordsUsed, space)
    else: space, letters, letterToWord = findBestSpace(puzzle, wordsUsed)
    #print(strPuzzle(puzzle)); print() #--> debugging
    if space == -1: return ''
    for letter in letters:
        #print(strPuzzle(puzzle)); print() --> debugging
        #making a copy of wordsUsed dict so i dont have to remove words if theyre eventually not used
        wordsUsedCopy = {*wordsUsed}
        lstPuzzle[space] = letter
        #letterToWord is returned in findLetters --> if a full word is made, it's added to the set 
        if letter in letterToWord:
            for word in letterToWord[letter]:
                wordsUsedCopy.add(word)
        #print(strPuzzle(''.join(lstPuzzle))); print() --> debugging
        pL = placeLetters(''.join(lstPuzzle), wordsUsedCopy)
        if pL: return pL
    return ''

def findBestSpace(puzzle, wordsUsed):
    smallest, minspace = 27, -1
    lettersToRet = set(); lettersToWordToRet = {}
    for index in [i for i,ch in enumerate(puzzle) if ch == '-']:
        letters, lettersToWord = findLetters([*puzzle], wordsUsed, index)
        #if there are no possible letters, the board is invalid, so back out immediately
        if len(letters) == 0: return -1, set(), {}
        #trying to find the space for placing a letter w the least number of possible letters
        if len(letters) < smallest: 
            smallest = len(letters); minspace = index
            lettersToRet = letters; lettersToWordToRet = lettersToWord
    return minspace, lettersToRet, lettersToWordToRet

def findLetters(puzzle, wordsUsed, space):
    #letterToWord is only applicable when full words are made (letter placed:word made)
    #replacing the puzzle[space] (params) with a '*' for easier reference later on
    letterToWord = {}; puzzle[space] = '*'
    vword = ''; hword = ''
    #finding the letters in the vertical word including the space param and indices below that
    for i in range(space, len(puzzle), width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '*': vword = vword + puzzle[i]
        elif puzzle[i] == '#': break
    #finding the letters in the vertical words including the indices above space param
    for i in range(space-width, -1, -width):
        if puzzle[i].isalpha() or puzzle[i] == '-': vword = puzzle[i] + vword
        elif puzzle[i] == '#': break
    
    #finding the letters in the horizontal word including the space param and indices below that
    for i in range(space, space+width-space%width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '*': hword = hword + puzzle[i]
        elif puzzle[i] == '#': break
    #finding the letters in the horizontal word including the indices above space param
    for i in range(space-1, space-space%width-1, -1):
        if puzzle[i].isalpha() or puzzle[i] == '-': hword = puzzle[i] + hword
        elif puzzle[i] == '#': break
    
    #finding the constraints (existing letters) in both the horizontal and vertical words
    vConstraints = []; hConstraints = []
    for i,ch in enumerate(vword):
        if ch.isalpha():
            vConstraints.append((ch, i))
    for i,ch in enumerate(hword):
        if ch.isalpha():
            hConstraints.append((ch, i))
    
    #letters dicts: letter:number of words w that letter @ space param
    vLetters = {}; hLetters = {}
    #if there are no constraints: all letters are possible with an equal weight
    if len(vConstraints) == 0: vLetters = {i:26 for i in gLETTERS}
    if len(hConstraints) == 0: hLetters = {i:26 for i in gLETTERS}
    #finding words that satisfy the horizontal and vertical constraints (which is why 2 things are returned)
    vValidWords, hValidWords = findConstraintWords(vConstraints, hConstraints)
    #finding where the space position fits in w the whole word (vertically and horizontally)
    hSpace = hword.find('*'); vSpace = vword.find('*')
    for word in vValidWords:
        if len(word) != len(vword): continue
        #finding the letter at the space position and adding it to letters dict
        if word[vSpace] in vLetters: vLetters[word[vSpace]] += 1
        else: vLetters[word[vSpace]] = 1
        #checking if the addition of one letter makes a full word
        if vword.count('-') == 0:
            #print(strPuzzle(puzzle)); print(wordsUsed) --> debugging
            if word in wordsUsed: 
                #print(vLetters) --> debugging
                #deleting the letter if it makes a word that's alr been used, bc its invalid
                del vLetters[word[vSpace]]; continue
            #adding the letter + word made to the letterToWord dict
            if word[vSpace] in letterToWord: letterToWord[word[vSpace]].append(word)
            else: letterToWord[word[vSpace]] = [word]
    #same thing as vertical: look above for comments
    for word in hValidWords:
        if len(word) != len(hword): continue
        if word[hSpace] in hLetters: hLetters[word[hSpace]] += 1
        else: hLetters[word[hSpace]] = 1
        if hword.count('-') == 0:
            #print(strPuzzle(puzzle)); print(wordsUsed)
            if word in wordsUsed: 
                #print(hLetters)
                del hLetters[word[hSpace]]; continue
            if word[hSpace] in letterToWord: letterToWord[word[hSpace]].append(word)
            else: letterToWord[word[hSpace]] = [word]
    #checking the intersection of the valid letters vertically and the valid letters horizontally
    letters = {}
    for i in vLetters:
        #the total heuristic (word frequency) is just the vertical + horizontal word frequency LOL
        if i in hLetters: letters[i] = vLetters[i] + hLetters[i]
    #returning letters based on decreasing word frequency
    return sorted(letters, key=letters.get, reverse=True), letterToWord

def findConstraintWords(vConstraints, hConstraints):
    vValidWords = set(); hValidWords = set()
    for i,c in enumerate(vConstraints):
        #if we're looking at the first constraint: there's no intersection needed bc the existing set is empty
        if c in gLETTERPOSTOWORD and i == 0:
            vValidWords = gLETTERPOSTOWORD[c]
        #finding an intersection between the alr existing valid words and the valid words for the constraint
        elif c in gLETTERPOSTOWORD:
            vValidWords = vValidWords.intersection(gLETTERPOSTOWORD[c])
    #check vertical: same concept
    for i,c in enumerate(hConstraints):
        if c in gLETTERPOSTOWORD and i == 0:
            hValidWords = gLETTERPOSTOWORD[c]
        elif c in gLETTERPOSTOWORD:
            hValidWords = hValidWords.intersection(gLETTERPOSTOWORD[c])
    return vValidWords, hValidWords

def main():
    setGlobals()
    newPzl = ''
    #print(pzl) --> made it easier to debug
    #no blocking squares
    if blocking_squares_count == 0:
        newPzl = pzl
    #the whole thing is blocking squares
    elif blocking_squares_count == height*width:
        newPzl = ''.join(['#']*(height*width))
    else:
        #first, fix squares based on what's originally on the board
        newPzl = fixSquares(pzl)
        newPzlLst = [*newPzl]
        #placing forced blocks for every blocking square
        for pos in [i for i, ch in enumerate(newPzl) if ch == '#']:
            newPzlLst, blocking_positions = placeForcedBlocks(newPzlLst, pos, [])
        newPzl = ''.join(newPzlLst)
        #checking for isolated/separated regions
        newPzlListWithIsolations = [*newPzlLst]; tempPzl = ''
        for i in [index for index, ch in enumerate(newPzl) if ch == '-']:
            identifyIsolatedRegions(newPzlListWithIsolations, i)
            if '-' in newPzlListWithIsolations: 
                #filling the isolations and then checking if the blocking square count is satisfied
                tempPzl = fillIsolatedRegions(newPzl, newPzlListWithIsolations)
                #if blocking square count is satisfied: we are good
                if tempPzl.count('#') <= blocking_squares_count:
                    newPzl = tempPzl; newPzlLst = [*newPzl]; break
                #else: replace all the '$' (connected stuff) with '-' 
                #repeat floodfill until blocking square count is satisfied
                else:
                    tempPzl = ''
                    for pos, ch in enumerate(newPzlListWithIsolations):
                        if ch == '$': newPzlListWithIsolations[pos] = '-'
            #if there are no isolations: break after the first check
            else: break
        #placing forced letters for each initial blocking square
        for pos in [i for i, ch in enumerate(newPzl) if ch == '#']:
            newPzlLst = placeForcedLetters(newPzlLst, pos)
        newPzl = ''.join(newPzlLst)
        newPzl = placeBlockingSquares(newPzl)
        newPzl = newPzl.replace('0', '-')
    print(strPuzzle(newPzl))
    print(f"puzzle formation time: {time.process_time() - start_time}")
    newPzl = placeLetters(newPzl, set())
    print(strPuzzle(newPzl))
    print(f"total time: {time.process_time() - start_time}")

if __name__ == '__main__': main()