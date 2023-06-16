# TODO
from cs50 import get_string

# ask user to prompt the phrase
phrase = get_string("Phrase: ")

length = 0

# calculate length of the input
for i in phrase:
    length += 1

# variable counters
letters = 0
words = 0
sentences = 0

# counting letters
for i in range(length):
    if phrase[i].isalpha():
        letters += 1
    # counting words
    # option 1 : letter plus space
    elif phrase[i].isspace() and not(phrase[i - 1] == "?" or phrase[i - 1] == "." or phrase[i - 1] == "!"):
        words += 1
    # option 2 : letter followed by punctuation
    elif phrase[i] == "?" or phrase[i] == "." or phrase[i] == "!":
        words += 1
        sentences += 1

# calculate av number of letters per 100 words
avlet = (letters * 100) / words

# average number of sentences
avsen = (sentences * 100) / words

# coleman index
coleman = round(0.0588 * avlet - 0.296 * avsen - 15.8)

if coleman > 16:
    print("Grade 16+")
elif coleman < 1:
    print("Before Grade 1")
else:
    print(f"Grade {coleman}")