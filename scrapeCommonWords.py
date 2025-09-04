# Scrape a list of all "common" words from Webster, store each list by word length

import requests
from bs4 import BeautifulSoup

WORD_URL = "https://www.merriam-webster.com/wordfinder/classic/begins/common/-1"

wordsByLength = dict()
# make a request for each letter in the alphabet
for i in range(ord('a'), ord('z')+1):
  # get current letter
  letter = chr(i)
  # request all common words like 'letter%'
  pageNumber = 1
  while True:
    # request all common words like 'letter%' on the current page
    print(f'requesting page for letter {letter}, pageNumber {pageNumber}...')
    page = requests.get(f"{WORD_URL}/{letter}/{pageNumber}")
    soup = BeautifulSoup(page.content, "html.parser")
    # find paginated result table
    result_table = soup.find('ul', class_='paginated-list-results')
    # if results not found, no more pages (go to next letter)
    if not result_table or not result_table.findChild():
      print(f'"{letter}" pages processed: {pageNumber-1}')
      break
    # process each word
    for result in result_table.findChildren('a'):
      word = result.getText()
      if len(word) < 2:
        continue
      if len(word) in wordsByLength:
        wordsByLength[len(word)].append(word)
      else:
        wordsByLength[len(word)] = [word]
    # next result page
    pageNumber += 1
print('Done processing! Printing to files...')
# Done processing, now write each to a file
for length in wordsByLength.keys():
  words = wordsByLength[length]
  with open(f"words-common-{length}.txt", "w") as file:
    for word in words:
      file.write(word + "\n")
print('Done!')