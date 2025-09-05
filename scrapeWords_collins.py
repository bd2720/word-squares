import requests
from bs4 import BeautifulSoup

DIRECTORY = 'words'

# only 2, 3, 4, and 5 work
numberWords = ['', '', 'two', 'three', 'four', 'five']

for N in range(2, 6):
  # list of n-letter words
  WORD_URL = f"https://scrabble.collinsdictionary.com/word-lists/{numberWords[N]}-letter-words-in-scrabble/"
  WORD_FILE = f"./{DIRECTORY}/words-collins-{N}.txt"

  page = requests.get(WORD_URL)
  soup = BeautifulSoup(page.content, "html.parser")
  #letter_tables = soup.find_all('ul', class_="letter-table")
  letter_tables = soup.find_all(class_=["letter-table", "letter_table"])
  words = []
  for table in letter_tables:
    word_elements = table.find_all('a')
    for word in word_elements:
      if not word:
        continue
      strippedWord = word.get_text().strip()
      if strippedWord:
        words.append(strippedWord)

  # write words to text file
  with open(WORD_FILE, "w") as file:
    for word in words:
      file.write(word + "\n")

  print(f"Scraped {len(words)} {N}-letter words!")
print("Done!")