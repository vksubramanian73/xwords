import sys; args = sys.argv[1:]
# Varshini Subramanian, Period 7
import time
# a LOT faster! (only fails 15x15 and 5x5 one letter)
# changes made: 
# choosing the space w the least possible letters
# better block placement!! woot woot

height = -1
width = -1
blocking_squares_count = -1
pzl = ''
file_to_read = ''
start_time = time.process_time()
gLETTERPOSTOWORD = {}
wordLst = []
gLETTERS = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
poss_count = 0

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
        for i in range(3, len(args)):
            arg = args[i]
            orientation = arg[0].lower(); arg_x_index = arg.find('x')
            end_of_number_2 = -1; word = ''
            for j in range(len(arg) - 1, arg.find('x'), -1):
                if arg[j].isdigit(): end_of_number_2 = j; break
                else: word = word + arg[j]
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
            if i // width == 0: #000 from topmost row
                if lstPuzzle[i + width] == '-': lstPuzzle[i + width] = '0'
                if lstPuzzle[i + 2*width] == '-': lstPuzzle[i + 2*width] = '0'
            elif i // width == height - 1: #000 from bottommost row
                if lstPuzzle[i - width] == '-': lstPuzzle[i - width] = '0'
                if lstPuzzle[i - 2*width] == '-': lstPuzzle[i - 2*width] = '0'
            elif i // width == 1: #-00- from second to top row
                if lstPuzzle[i + width] == '-': lstPuzzle[i + width] = '0'
            elif i // width == height - 2: #-00- from second to bottom row
                if lstPuzzle[i - width] == '-': lstPuzzle[i - width] = '0'
            if i % width == 0: #000 from leftmost row
                if lstPuzzle[i + 1] == '-': lstPuzzle[i + 1] = '0'
                if lstPuzzle[i + 2] == '-': lstPuzzle[i + 2] = '0'
            elif i % width == width - 1: #000 from rightmost row
                if lstPuzzle[i - 1] == '-': lstPuzzle[i - 1] = '0'
                if lstPuzzle[i - 2] == '-': lstPuzzle[i - 2] = '0'
            elif i % width == 1: #000 from second to left row
                if lstPuzzle[i + 1] == '-': lstPuzzle[i + 1] = '0'
            elif i % width == width - 2: #000 from second to right row
                if lstPuzzle[i - 1] == '-': lstPuzzle[i - 1] = '0'
    for i,ch in enumerate(lstPuzzle): #symmetry
        if ch == '#': lstPuzzle[len(puzzle) - 1 - i] = '#'
        elif ch.isalpha() or ch == '0': 
            if lstPuzzle[len(puzzle) - 1 - i] == '-': lstPuzzle[len(puzzle) - 1 - i] = '0'
    return ''.join(lstPuzzle)

def bestSpaceBlockingSquare(puzzle):
    posToHeuristic = {}; pos = -1
    for pos in [i for i,ch in enumerate(puzzle) if ch == '-']:
        heuristic = block_heuristic(puzzle, pos)
        posToHeuristic[pos] = heuristic
    return sorted(posToHeuristic, key=posToHeuristic.get, reverse=True)

def block_heuristic(puzzle, space):
    up = 0; down = 0; left = 0; right = 0
    for i in range(space, len(puzzle), width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '0': down += 1
        elif puzzle[i] == '#': break 
    for i in range(space-width, -1, -width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '0': up += 1
        elif puzzle[i] == '#': break
    for i in range(space, space+width-space%width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '0': right += 1
        elif puzzle[i] == '#': break
    for i in range(space-1, space-space%width-1, -1):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '0': left += 1
        elif puzzle[i] == '#': break
    return left*right + up*down

def placeBlockingSquares(puzzle): #similar to brute force
    if puzzle.count('#') == blocking_squares_count: return puzzle
    elif puzzle.count('#') > blocking_squares_count: return ''
    lstPuzzleWithIsolations = [*puzzle]
    identifyIsolatedRegions(lstPuzzleWithIsolations, puzzle.find('-'))
    if '-' in lstPuzzleWithIsolations or '0' in lstPuzzleWithIsolations: return ''
    #print(strPuzzle(puzzle)); print()
    for pos in bestSpaceBlockingSquare(puzzle):
        lstPuzzle = [*puzzle]
        lstPuzzle[pos] = lstPuzzle[len(puzzle) - pos - 1] = '#'
        block_positions = [pos, len(puzzle) - pos - 1]
        while(block_positions):
            pos_to_input = block_positions.pop(0)
            lstPuzzle, block_positions = placeForcedBlocks(lstPuzzle, pos_to_input, block_positions)
        lstPuzzle = placeForcedLetters(lstPuzzle, pos)
        subPzl = ''.join(lstPuzzle)
        #print(strPuzzle(subPzl)); print()
        bF = placeBlockingSquares(subPzl)
        if bF: return bF
    return ''

def placeForcedBlocks(lstPuzzle, pos, block_positions):
    if pos % width == 2: # --# condition from leftmost column
        if lstPuzzle[pos - 1] != '#' and lstPuzzle[pos - 2] == '#': 
            lstPuzzle[pos - 1] = lstPuzzle[pos - 2] = '#'
            block_positions.append(pos-1); block_positions.append(pos-2)
    elif pos % width == width - 3: # #-- condition from rightmost column
        if lstPuzzle[pos + 1] != '#' and lstPuzzle[pos + 2] != '#': 
            lstPuzzle[pos + 1] = lstPuzzle[pos + 2] = '#'
            block_positions.append(pos+1); block_positions.append(pos+2)
    elif pos % width == 1: # -# condition from leftmost column
        if lstPuzzle[pos - 1] != '#': lstPuzzle[pos - 1] = '#'; block_positions.append(pos-1)
    elif pos % width == width - 2: # #- condition from rightmost column
        if lstPuzzle[pos + 1] != '#': lstPuzzle[pos + 1] = '#'; block_positions.append(pos+1)
    if pos // width == 2: # #-- condition from topmost row
        if lstPuzzle[pos - width] != '#' and lstPuzzle[pos - 2*width] != '#': 
            lstPuzzle[pos - width] = lstPuzzle[pos - 2*width] = '#'
            block_positions.append(pos-width); block_positions.append(pos-2*width)
    elif pos // width == height - 3: # #-- condition from bottommost row
        if lstPuzzle[pos + width] != '#' and lstPuzzle[pos + 2*width] != '#': 
            lstPuzzle[pos + width] = lstPuzzle[pos + 2*width] = '#'
            block_positions.append(pos+width); block_positions.append(pos+2*width)
    elif pos // width == 1: # -# condition from topmost row
        if lstPuzzle[pos - width] != '#': lstPuzzle[pos - width] = '#'; block_positions.append(pos-width)
    elif pos // width == height - 2: # #- condition from bottommost row
        if lstPuzzle[pos + width] != '#': lstPuzzle[pos + width] = '#'; block_positions.append(pos+width)
    if pos // width == (pos + 1) // width == (pos + 2) // width == (pos + 3) // width: # #--# condition across rows
        if lstPuzzle[pos + 3] == '#' and lstPuzzle[pos + 2] != '#' and lstPuzzle[pos + 1] != '#': 
            lstPuzzle[pos + 1] = lstPuzzle[pos + 2] = '#'
            block_positions.append(pos+1); block_positions.append(pos+2)
    if pos // width == (pos - 1) // width == (pos - 2) // width == (pos - 3) // width: # #--# condition across rows
        if lstPuzzle[pos - 3] == '#' and lstPuzzle[pos - 2] != '#' and lstPuzzle[pos - 1] != '#': 
            lstPuzzle[pos - 1] = lstPuzzle[pos - 2] = '#'
            block_positions.append(pos-1); block_positions.append(pos-2)
    if pos + 3*width < len(lstPuzzle): # #--# condition across columns
        if lstPuzzle[pos + 3*width] == '#' and lstPuzzle[pos + 2*width] != '#' and lstPuzzle[pos + width] != '#': 
            lstPuzzle[pos + width] = lstPuzzle[pos + 2*width] = '#'
            block_positions.append(pos+width); block_positions.append(pos+2*width)
    if pos - 3*width > 0: # #--# condition across columns
        if lstPuzzle[pos - 3*width] == '#' and lstPuzzle[pos - 2*width] != '#' and lstPuzzle[pos - width] != '#': 
            lstPuzzle[pos - width] = lstPuzzle[pos - 2*width] = '#'
            block_positions.append(pos-width); block_positions.append(pos-2*width)
    if pos // width == (pos + 1) // width == (pos + 2) // width: # #-# condition across rows
        if lstPuzzle[pos + 2] == '#' and lstPuzzle[pos + 1] != '#': lstPuzzle[pos + 1] = '#'; block_positions.append(pos+1)
    if pos // width == (pos - 1) // width == (pos - 2) // width: # #-# condition across rows
        if lstPuzzle[pos - 2] == '#' and lstPuzzle[pos - 1] != '#': lstPuzzle[pos - 1] = '#'; block_positions.append(pos-1)
    if pos + 2*width < len(lstPuzzle): # #-# condition across columns
        if lstPuzzle[pos + 2*width] == '#' and lstPuzzle[pos + width] != '#': lstPuzzle[pos + width] = '#'; block_positions.append(pos+width)
    if pos - 2*width > 0: # #-# condition across columns
        if lstPuzzle[pos - 2*width] == '#' and lstPuzzle[pos - width] != '#': lstPuzzle[pos - width] = '#'; block_positions.append(pos-width)
    for i,ch in enumerate(lstPuzzle): #symmetry
        if ch == '#': lstPuzzle[len(lstPuzzle) - 1 - i] = '#'
        elif ch.isalpha() or ch == '0': 
            if lstPuzzle[len(lstPuzzle) - 1 - i] == '-': lstPuzzle[len(lstPuzzle) - 1 - i] = '0'
    return lstPuzzle, block_positions

def placeForcedLetters(lstPuzzle, pos):
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
    if pos // width == (pos + 1) // width == (pos + 2) // width == (pos + 3) // width == (pos + 4) // width:
        if lstPuzzle[pos + 4] == '#':
            if lstPuzzle[pos + 1] == '-': lstPuzzle[pos + 1] = '0'
            if lstPuzzle[pos + 2] == '-': lstPuzzle[pos + 2] = '0'
            if lstPuzzle[pos + 3] == '-': lstPuzzle[pos + 3] = '0'
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
    if pos + 4*width < len(lstPuzzle):
        if lstPuzzle[pos + 4*width] == '#':
            if lstPuzzle[pos + width] == '-': lstPuzzle[pos + width] = '0'
            if lstPuzzle[pos + 2*width] == '-': lstPuzzle[pos + 2*width] = '0'
            if lstPuzzle[pos + 3*width] == '-': lstPuzzle[pos + 3*width] = '0'
    for i,ch in enumerate(lstPuzzle):
        if ch == '#': lstPuzzle[len(lstPuzzle) - 1 - i] = '#'
        elif ch.isalpha() or ch == '0': 
            if lstPuzzle[len(lstPuzzle) - 1 - i] == '-': lstPuzzle[len(lstPuzzle) - 1 - i] = '0'
    return lstPuzzle

def identifyIsolatedRegions(lstPuzzle, pos):
    if pos < 0 or pos >= len(lstPuzzle): return
    if pos // width < 0 or pos // width >= height or pos % width < 0 or pos % width >= width: return
    if lstPuzzle[pos] == '#' or lstPuzzle[pos] == '$': return
    lstPuzzle[pos] = '$'
    identifyIsolatedRegions(lstPuzzle, pos - width)
    identifyIsolatedRegions(lstPuzzle, pos + width)
    if (pos + 1) // width == pos // width: identifyIsolatedRegions(lstPuzzle, pos + 1)
    if (pos - 1) // width == pos // width: identifyIsolatedRegions(lstPuzzle, pos - 1)

def fillIsolatedRegions(puzzle, pzlListWithIsolations):
    pzlList = [*puzzle]
    isolated = [i for i,ch in enumerate(pzlListWithIsolations) if ch == '-']
    for i in isolated:
        pzlList[i] = '#'
    return ''.join(pzlList)

def placeLetters(puzzle, wordsUsed):
    if puzzle.count('-') == 0: return puzzle
    lstPuzzle = [*puzzle]
    if height == width == 5: space = puzzle.find('-'); letters, letterToWord = findLetters(lstPuzzle, wordsUsed, space)
    else: space, letters, letterToWord = findBestSpace(puzzle, wordsUsed) 
    #space, letters, letterToWord = findBestSpace(puzzle, wordsUsed) 
    if space == -1: return ''
    #print(strPuzzle(puzzle)); print()
    for letter in letters:
        wordsUsedCopy = {*wordsUsed}
        lstPuzzle[space] = letter
        if letter in letterToWord:
            for word in letterToWord[letter]:
                wordsUsedCopy.add(word)
        pL = placeLetters(''.join(lstPuzzle), wordsUsedCopy)
        if pL: return pL
    return ''

def findBestSpace(puzzle, wordsUsed):
    smallest, minspace = 27, -1
    lettersToRet = set(); lettersToWordToRet = {}
    for index in [i for i,ch in enumerate(puzzle) if ch == '-']:
        letters, lettersToWord = findLetters([*puzzle], wordsUsed, index)
        if len(letters) == 0: return -1, set(), {}
        #elif len(letters) == 1: return minspace, letters, lettersToWord
        if len(letters) < smallest: 
            smallest = len(letters); minspace = index
            lettersToRet = letters; lettersToWordToRet = lettersToWord
    return minspace, lettersToRet, lettersToWordToRet

def findLetters(puzzle, wordsUsed, space):
    global poss_count
    poss_count += 1
    vLettersToRet = set(); hLettersToRet = set(); letterToWord = {}; puzzle[space] = '*'
    vword = ''; hword = ''
    for i in range(space, len(puzzle), width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '*': vword = vword + puzzle[i]
        elif puzzle[i] == '#': break
    for i in range(space-width, -1, -width):
        if puzzle[i].isalpha() or puzzle[i] == '-': vword = puzzle[i] + vword
        elif puzzle[i] == '#': break
    for i in range(space, space+width-space%width):
        if puzzle[i].isalpha() or puzzle[i] == '-' or puzzle[i] == '*': hword = hword + puzzle[i]
        elif puzzle[i] == '#': break
    for i in range(space-1, space-space%width-1, -1):
        if puzzle[i].isalpha() or puzzle[i] == '-': hword = puzzle[i] + hword
        elif puzzle[i] == '#': break
    vLetterIndex = -1; hLetterIndex = -1
    for i,ch in enumerate(vword):
        if ch.isalpha(): vLetterIndex = i; break
    for i,ch in enumerate(hword):
        if ch.isalpha(): hLetterIndex = i; break
    vValidWords = set(); hValidWords = set(); hSpace = hword.find('*'); vSpace = vword.find('*')
    if vLetterIndex == -1: vLettersToRet = {*gLETTERS}
    else:
        if (vword[vLetterIndex], vLetterIndex) in gLETTERPOSTOWORD:
            for word in gLETTERPOSTOWORD[(vword[vLetterIndex], vLetterIndex)]:
                validWord = True
                if len(word) != len(vword): continue
                for i,ch in enumerate(vword):
                    if ch == '-' or ch == '*': continue
                    elif word[i] != ch.upper(): validWord = False; break
                if validWord: vValidWords.add(word)
            for word in vValidWords:
                if vword.count('-') == 1:
                    if word in wordsUsed: continue
                    if word[vSpace] in letterToWord: letterToWord[word[vSpace]].append(word)
                    else: letterToWord[word[vSpace]] = [word]
                vLettersToRet.add(word[vSpace])
    if hLetterIndex == -1: hLettersToRet = {*gLETTERS}
    else:
        if (hword[hLetterIndex], hLetterIndex) in gLETTERPOSTOWORD:
            for word in gLETTERPOSTOWORD[(hword[hLetterIndex], hLetterIndex)]:
                validWord = True
                if len(word) != len(hword): continue
                for i,ch in enumerate(hword):
                    if ch == '-' or ch == '*': continue
                    elif word[i] != ch.upper(): validWord = False; break
                if validWord: hValidWords.add(word)
            for word in hValidWords:
                if hword.count('-') == 1:
                    if word in wordsUsed: continue
                    if word[hSpace] in letterToWord: letterToWord[word[hSpace]].append(word)
                    else: letterToWord[word[hSpace]] = [word]
                hLettersToRet.add(word[hSpace])
    return hLettersToRet.intersection(vLettersToRet), letterToWord

def main():
    setGlobals()
    newPzl = ''
    print(pzl)
    if blocking_squares_count == 0:
        newPzl = pzl
    elif blocking_squares_count == height*width:
        newPzl = ''.join(['#']*(height*width))
    else:
        newPzl = fixSquares(pzl)
        newPzlLst = [*newPzl]
        for pos in [i for i, ch in enumerate(newPzl) if ch == '#']:
            newPzlLst, blocking_positions = placeForcedBlocks(newPzlLst, pos, [])
        newPzl = ''.join(newPzlLst)
        newPzlListWithIsolations = [*newPzlLst]; tempPzl = ''
        for i in [index for index, ch in enumerate(newPzl) if ch == '-']:
            identifyIsolatedRegions(newPzlListWithIsolations, i)
            if '-' in newPzlListWithIsolations: 
                tempPzl = fillIsolatedRegions(newPzl, newPzlListWithIsolations)
                if tempPzl.count('#') <= blocking_squares_count:
                    newPzl = tempPzl; newPzlLst = [*newPzl]; break
                else:
                    tempPzl = ''
                    for pos, ch in enumerate(newPzlListWithIsolations):
                        if ch == '$': newPzlListWithIsolations[pos] = '-'
            else: break
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
    print(f"poss count: {poss_count}")

if __name__ == '__main__': main()