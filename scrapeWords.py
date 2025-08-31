import requests
from bs4 import BeautifulSoup
# list of 3-letter words
WORD_URL = "https://scrabble.collinsdictionary.com/word-lists/three-letter-words-in-scrabble/"
WORD_FILE = "./words-3.txt"

page = requests.get(WORD_URL)
soup = BeautifulSoup(page.content, "html.parser")
letter_tables = soup.find_all('ul', class_="letter-table")
words = []
for table in letter_tables:
  for word in table:
    if not word:
      continue
    strippedWord = word.strip()
    if strippedWord:
      words.append(strippedWord)

# write words to text file
with open(WORD_FILE, "w") as file:
  for word in words:
    file.write(word + "\n")

print("Done!")