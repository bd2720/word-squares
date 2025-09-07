# Find 3-Letter Word Squares
# (Where every pair of horizontal and vertical words is unique)

# A L L
# W E E
# L I T

from prefixTree import PrefixTree 
import sys

WORD_DIRECTORY = 'words' # fixed directory name where word files are read from
SQUARE_DIRECTORY = 'squares' # fixed directory name where word squares files are saved to
VALID_WORD_SETS = {"collins", "webster", "webster-common"}
DEFAULT_WORD_SET = "webster-common"

wordSquares = []

# print the word square with the letters spaced out
def formatSquare(wordSquare):
  return "\n".join(" ".join(word) for word in wordSquare)

# print multiple word squares, each separated by an empty line
def formatSquares(wordSquares):
  return "\n\n".join(formatSquare(sq) for sq in wordSquares)

# read words in from the given filename, ensure uppercase
def readWords(filename):
  words = []
  with open(filename, "r") as word_file:
    for line in word_file:
      words.append(line.strip().upper())
  return words

# write squares to a file
def writeSquares(filename, wordSquares):
  with open(filename, "w") as square_file:
    square_file.write(formatSquares(wordSquares))

# Find symmetrical word squares using a prefix tree (non-recursive)
def findSquares_prefixtree(ptree, words, n, startingSquares=None, shouldPrint=False):
  # build squares starting with each word
  partialSquares = startingSquares if startingSquares else [[w] for w in words] 
  # add on n-1 new words to each square, or remove it
  for depth in range(1, n):
    if shouldPrint:
      print(f"{len(partialSquares)} partial squares of length {depth}...")
    if not partialSquares:
      break
    # Just for fun, see how close we got
    if shouldPrint and len(partialSquares) <= 10:
      print(formatSquares(partialSquares))
    newPartialSquares = []
    for psquare in partialSquares:
      # construct current prefix
      prefix = [psquare[i][depth] for i in range(depth)]
      # find list of words that begin with the prefix
      candidateWords = ptree.startsWith(prefix)
      # construct new partialSquares by pairing each candidate word with current partial square
      # without pruning, this is simply: newPartialSquares += [psquare + [cword] for cword in candidateWords]
      for cword in candidateWords:
        # attempt to prune this entry by ensuring that words exist for each partial column
        shouldPrune = False
        for i in range(depth+1, n):
          # construct partial column
          pcol = [psquare[j][i] for j in range(depth)]
          # add letter from candidate word
          pcol.append(cword[i])
          # prune candidate word if no words exist starting with this partial column
          if not ptree.hasWordStartingWith(pcol):
            shouldPrune = True
            break
        if not shouldPrune:
        # add new partial square to the list if not already pruned
          newPartialSquares.append(psquare + [cword])
      
    # overwrite old partialSquares with new ones
    partialSquares = newPartialSquares
  # return all squares found
  return partialSquares 

# Usage:
#   $ python ./findSquares.py <WORD_SET> <N*> <STARTING_WORD>
#   (* == required)
#   (can replace optional params with _)
def main():
  # try to read WORD_SET
  try:
    WORD_SET = sys.argv[1]
    if WORD_SET not in VALID_WORD_SETS:
      raise
  except:
    WORD_SET = DEFAULT_WORD_SET
    print(f"Warning: WORD_SET is invalid, defaulting to {DEFAULT_WORD_SET}...")
  # try to read N
  try:
    N = int(sys.argv[2])
  except:
    print("Error: N is invalid.")
    return
  # assemble word file name
  WORD_FILE = f"./{WORD_DIRECTORY}/words-{WORD_SET}-{N}.txt"
  # read in list of N-length words
  try:
    words = readWords(WORD_FILE)
  except:
    print("Error: Word file does not exist.")
    return
  if not words:
    print("Error: Words were not read successfully.")
    return
  # try to read starting word
  STARTING_WORD = None
  try:
    STARTING_WORD = sys.argv[3].upper()
  except:
    pass
  if STARTING_WORD:
    if len(STARTING_WORD) != N:
      print("Error: STARTING_WORD is not a valid length.")
      return
    elif STARTING_WORD not in words:
      print("Error: STARTING_WORD is not a valid word.")
      return
  # assemble PrefixTree
  pftree = PrefixTree(words, N)
  # find all symmetrical word squares of size N
  global wordSquares
  wordSquares = []
  wordsToSearch = [STARTING_WORD] if STARTING_WORD else words
  for i, word in enumerate(wordsToSearch):
    print(f"{word} ({i+1} / {len(wordsToSearch)}) [{len(wordSquares)} Found So Far]")
    newSquares = findSquares_prefixtree(pftree, words, N, startingSquares=[[word]])
    if newSquares:
      print("!!! FOUND WORD SQUARES !!!")
      #print((formatSquares(newSquares)))
      wordSquares += newSquares
  # print size of results
  print(f"{len(wordSquares)} word squares of size {N} found" + (f" starting with {STARTING_WORD}!" if STARTING_WORD else "!"))

if __name__ == "__main__":
  main()