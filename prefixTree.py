from functools import reduce

class PrefixNode:
  def __init__(self, letter, position):
    self.letter = letter
    self.children = [None] * 26
    self.numChildren = 0
    self.position = position # 1-indexed
  
  def getLetter(self):
    return self.letter
  
  def getPosition(self):
    return self.position

  def getChildren(self):
    return self.children

  def getChild(self, letter):
    return self.children[ord(letter) - ord('A')]
  
  def addChild(self, letter):
    self.children[ord(letter) - ord('A')] = PrefixNode(letter, self.position+1)
    self.numChildren += 1

  def getNumChildren(self):
    return self.numChildren

  def hasChildren(self):
    return self.numChildren > 0

  # get all words of length n, in order, in the tree (recursive)
  def getWords(self, n):
    # Base Case: check that stopping depth has been reached
    if self.position >= n:
      return [self.letter]
    # Optimization: return empty word list if node has no children  
    if not self.hasChildren():
      return []
    return reduce(lambda words, nextChild: (words + [self.letter + childWord for childWord in nextChild.getWords(n)]) if nextChild else words, self.children, [])


class PrefixTree:
  def __init__(self, words, n):
    self.n = n # length of each word
    self.tree = PrefixNode('', 0)
    # add each word to the tree
    for word in words:
      # start at root of tree
      currNode = self.tree
      for letter in word:
        # try to index into that char
        if not currNode.getChild(letter):
          currNode.addChild(letter)
        # advance to next level of tree
        currNode = currNode.getChild(letter)
  
  def getTree(self):
    return self.tree
  
  def getN(self):
    return self.n

  # return a list of words that start with the given letter sequence
  def startsWith(self, letters):
    # index into tree for each given letter
    currNode = self.tree
    for letter in letters:
      currNode = currNode.getChild(letter)
      if not currNode:
        return []
    # construct the list of words inside PrefixNode
    return ["".join(letters[:-1]) + partialWord for partialWord in currNode.getWords(self.n)]