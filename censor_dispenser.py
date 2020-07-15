# Codecademy Project: Censor Dispenser
# Jul 2020
# Agnes Bi

# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

import re   # regular expression

def convert_to_censored(word):
    censoredversion = ''
    for l in word:
        if l.isalnum():
            censoredversion += '*'
        else:
            censoredversion += l
    return censoredversion

#print(convert_to_censored("learning algorithms"))


# Q1: Write a function that can censor a specific word or phrase from a body of text, and then return the text.

def censor1(word, email):
#    word_rg = "\W(?=" + re.escape(word) + ")(?<=\W)"
    caseinsensitive_word = re.compile(re.escape(word), re.IGNORECASE)
    return caseinsensitive_word.sub(convert_to_censored(word), email)

email_one = censor1("learning algorithms", email_one)
print(email_one)

# Q2: Write a function that can censor not just a specific word or phrase from a body of text, but a whole list of words and phrases, and then return the text.
def censor2(lst, email):
    for item in lst:
        email = censor1(item, email)
    return email

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself", "Helena"]

email_two = censor2(proprietary_terms, email_two)
#print(email_two)

# Q3: Write a function that can censor any occurance of a word from the “negative words” list after any “negative” word has occurred twice, as well as censoring everything from the list from the previous step as well

def censor3(negwlst, censoredlst, email):
    # process the text
    lines = email.split("\n")
    content = []
    for line in lines:
        content += line.split(" ")
    emailwords = []     # cleaned-up (i.e., special characters deleted, all lower-cased) list of words
    for word in content:
        updated = ''
        for letter in word:
            if letter.isalnum() == True:
                updated += letter.lower()
        if not updated == '':
            emailwords.append(updated)
    wordsfreq = {}   # calculate the number of times each word occur in the text
    for word in emailwords:
        if word in wordsfreq:
            wordsfreq[word] += 1
        else:
            wordsfreq[word] = 1
    # list the negative words that are repeated more than twice in the text
    repeated = []
    for word in negwlst:
        if wordsfreq.get(word, 0) > 2:
            repeated.append(word)
    for negw in repeated:
        segments = re.split(negw, email, flags=re.IGNORECASE)    # spilt email by the key words (case-incensitive)
        email = negw.join(segments[:2]) + (convert_to_censored(negw)).join(segments[2:])    # glue texts back together replacing the key word with *** after two occurances
    return censor2(censoredlst, email)     # deal with the usual censoring

negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]

email_three = censor3(negative_words, proprietary_terms, email_three)
#print(email_three)

# Q4: Write a function that censors not only all of the words from the negative_words and proprietary_terms lists, but also censor any words in email_four that come before AND after a term from those two lists.

def censor4(negwlst, censoredlst, email):
    email = censor3(negwlst, censoredlst, email)   # apply the Q3 censor rules
    segments = email.split(" ")
    interim_segments = segments[:]   # updated to censor the preceding words
    for i in range(len(segments)-1):
        if "*" in segments[i+1]:
            interim_segments[i] = convert_to_censored(segments[i])
    finalsegments = interim_segments[:]  # updated to censor the following words
    for i in range(1, len(interim_segments)):
        if ("*" in interim_segments[i-1] and not "\n" in interim_segments[i-1]) and (not "*" in interim_segments[i]): # assuming when there is a line break, tracking the next word stops
            finalsegments[i] = convert_to_censored(interim_segments[i])
    return " ".join(finalsegments)


email_four = censor4([], negative_words + proprietary_terms, email_four)
#print(email_four)

# As a challenge, make sure the functions:
#   1) Handle upper and lowercase letters.      (check)
#   2) Handle punctuation.      (check)
#   3) Censor words while preserving their length.  (check)

# Q: how to solve the issue of over-matching??? e.g., censored "here" because "her" was on the list
# Attempt 1: using regular expression \W, impplmented in censor1 but doesn't quite work
