# Find 3-Letter Word Squares
# (Where every pair of horizontal and vertical words is unique)

# A L L
# W E E
# L I T

from prefixTree import PrefixTree 

N = 3
WORD_FILE = f"./words-{N}.txt"

def readWords():
  words = []
  with open(WORD_FILE, "r") as word_file:
    for line in word_file:
      words.append(line.strip())
  return words

def findSquares_unique_bf(words, limit=100):
  wordSet = set(words)
  wordSquares = []
  # choose first word
  for w1 in words:
    #print(f"w1:{w1}")
    # choose next word
    for w2 in words:
      if w2 == w1:
        continue
      # choose third word
      for w3 in words:
        if w3 == w2 or w3 == w1:
          continue
        # check that verticals are words
        valid = True
        vertWords = []
        for i in range(3):
          vert = w1[i] + w2[i] + w3[i]
          if vert not in wordSet or vert in [w1, w2, w3] or vert in vertWords:
            valid = False
            break
          vertWords.append(vert)
        if valid:
          wordSquares.append([w1, w2, w3])
          if len(wordSquares) >= limit:
            return wordSquares
          
          #print(f"Found: {wordSquares[-1]}")
  return wordSquares

def findSquares_prefixtree(words):
  squares = []
  # Choose words in columns, using prefix tree
  # 1. create prefix tree
  pftree = PrefixTree(words, 3)
  # 2. iterate through all starting words
  for word1 in words:
    # 3. Now our next starting letter is fixed. 
    # Iterate through all words that start with the second letter of the first word
    words2 = pftree.startsWith([word1[1]])
    for word2 in words2:
      # 4. Now our next 2 letters are fixed.
      # Can make word squares with all valid words that start with (word1[2]+word2[2])
      words3 = pftree.startsWith([word1[2], word2[2]])
      if len(words3) > 0:
        # record new squares
        squares += [[word1, word2, word3] for word3 in words3]
  # finally, return all the squares we found
  return squares

# call with partialSquares = [[w] for w in words]
def findSquares_prefixtree_r(ptree, depth, n, partialSquares):
  if depth >= n:
    return partialSquares
  # for each partial square: calculate
  newPartialSquares = []
  for psquare in partialSquares:
    # construct current prefix
    prefix = [psquare[i][depth] for i in range(depth)]
    # find list of words that begin with the prefix
    candidateWords = ptree.startsWith(prefix)
    # construct new partialSquares by pairing each candidate word with current partial square
    newPartialSquares += [psquare + [cword] for cword in candidateWords]
  return findSquares_prefixtree_r(ptree, depth+1, n, newPartialSquares)


def formatSquare(wordSquare):
  s = ""
  for horizontalWord in wordSquare:
    s += " ".join(horizontalWord) + "\n"
  return s


words = readWords()
pftree = PrefixTree(words, N)
# find all symmetrical word squares of size N
wordSquares = findSquares_prefixtree_r(pftree, 1, N, [[w] for w in words])
print(f"{len(wordSquares)} word squares found!")

#print(words)
#squares = findSquares_unique_bf(limit=10)
#for square in squares:
#  print(formatSquare(square))
#print(f"{len(squares)} unique squares were found.")