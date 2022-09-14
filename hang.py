''' Hang.py - okd game in a new style '''

import sys
import linecache
import string
import secrets as scrt
import webbrowser as wb

# Hang is my attempt to rescue an old game with a new concept, as I use random picked words
# from a dictionary an at the end Itry to find the word meaning using the internet.

def save_scores(nruns, nwins, nfails):
    ''' Function to save data from the runs, wins and fails '''
    try:
        score_file = open('hang_scores.txt', 'w', encoding="utf-8")
    except FileNotFoundError:
        print("Erro opening file hang_scores.txt")
    else:
        with score_file:
            score_file.write(f"{nruns},{nwins},{nfails}")

def get_scores():
    ''' Function to get previous data from the runs, wins and fails '''
    val_scores = []
    try:
        score_file = open("hang_scores.txt", 'r', encoding="utf-8")
    except FileNotFoundError:
        val_scores = [0,0,0]
    else:
        with score_file:
            line = score_file.readline()
            val_scores = line.split(',')
    return (int(val_scores[0]),int(val_scores[1]),int(val_scores[2]))

def get_available_letters(availableletters, guessed_letter):
    ''' Function to remove the guessed letter from the still available letters to use '''
    idx = availableletters.index(guessed_letter)
    availableletters = availableletters[:idx] + availableletters[idx+1:]
    return availableletters

def get_word():
    ''' Function to get a random word from the dictionary file. '''
    line_index = scrt.randbelow(172823)
    new_word = linecache.getline("dictionary.txt",line_index)
    linecache.clearcache()
    return new_word

def list_of_index(str_word, some_letter):
    ''' Function to get a list of the possible indexes of a letter in the word. '''
    list_index = []

    while str_word.count(some_letter) > 0:
        letter_index = str_word.index(some_letter)
        list_index.append(letter_index)
        str_word = str_word[:letter_index] + some_letter.upper() + str_word[letter_index+1:]

    return list_index

def actual_guess(str_guess, idx, guessed_letter):
    ''' Function to set a guessed letter on the showed word. '''
    str_guess[idx] = guessed_letter
    return str_guess

def show_guess(list_guess):
    ''' Function receives a list and return it as a string. '''
    str_guess = ""
    for actual_letter in enumerate(list_guess):
        str_guess = str_guess + actual_letter[1]

    return str_guess

def try_letter(guess_word, actual_word, guessed_letter):
    ''' Function to get a list of the possible indexes of a letter in the word. '''
    list_idx = list_of_index(actual_word, guessed_letter)
    if len(list_idx) != 0:
        for letter_index in enumerate(list_idx):
            guessed_word = actual_guess(guess_word,letter_index[1],guessed_letter)
    return guessed_word

def player_guess():
    ''' Function to ask for a new letter to guess. '''
    lowercaseletters = string.ascii_lowercase
    new_letter = ''
    while(new_letter == '' or new_letter not in lowercaseletters):
        new_letter = input("Pick a lowercase letter between a and z.")
    return new_letter

# Start the game getting a new word from dictionary
the_word = get_word()
guess = ['_']*(len(the_word)-1)
guessOK = []
errors = []

letters = list(string.ascii_lowercase)

#for i in range(len(the_word) - 1):
#    guess.append('_')

guessOK.append(the_word[0])
guess = try_letter(guess, the_word, the_word[0])
word = show_guess(guess)
print(f"Your next word has {str(len(the_word)-1)} characters: {word}")

remainingletters = get_available_letters(letters, the_word[0])

runs, wins, fails = get_scores()

CT=10
while CT > 0:
    letter = player_guess()

    while (letter in guessOK or letter in errors):
        print(f"This letter '{letter}' was already used. Please try another one,")
        letter = player_guess()

    if the_word.count(letter.lower()) > 0:
        guessOK.append(letter)
        guess = try_letter(guess, the_word, letter.lower())

        word = show_guess(guess)

        if word.count('_') == 0:
            print(f"You have correctly guessed the word: {word}")
            wins +=1
            break
        print(f"\nYou still have {str(CT)} chances to guess the word. [{word}].")
    else:
        errors.append(letter)
        word = show_guess(guess)
        CT -= 1
        print(f"\nYou still have {str(CT)} chances to guess the word. [{word}].")
        #print(f"\nActual tries: OK {guessOK} - Errors {errors}")

    remainingletters = get_available_letters(remainingletters, letter)
    print(f"Available letters to your next choice: {remainingletters}")

if CT == 0:
    print(f"You have failed to guess the word. Your attempt: [{word}], the word is: {the_word}")
    fails +=1

runs +=1

res=f"{(wins / runs) * 100:.2f}"
print(f"\nYou have played hang.py {runs} times, with {res}% of wins.")
print(f"You winned {wins} times and failed {fails} times.")

save_scores(runs, wins, fails)

url = f"https://www.thefreedictionary.com/{the_word}"
wb.open(url)

sys.exit(0)
