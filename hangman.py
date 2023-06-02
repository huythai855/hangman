"""
Python basics, Problem Set, hangman.py
Name: Nguyen Huy Thai
Collaborators: No one
Time spent: 3 hours
"""

# ---------------------------------------------------------------------------- #
#                                 Hangman Game                                 #
# ---------------------------------------------------------------------------- #

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    with open(WORDLIST_FILENAME, "r") as inFile:
        # line: string
        line = inFile.readline()
        # wordlist: list of strings
        wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# Load the list of words into the variable wordlist
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are lowercase
    letters_guessed: list (of letters), which letters have been guessed so far, assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed, False otherwise
    """
    flag = True
    for c in secret_word:
        if c not in letters_guessed:
            flag = False
    return flag


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
        which letters in secret_word have been guessed so far.
    """
    guessed_word = ''
    for c in secret_word:
        if c in letters_guessed:
            guessed_word += c
        else:
            guessed_word += '_ '
    return guessed_word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not yet been guessed.
    """
    flag = [True for i in range(26)]

    for letter in letters_guessed:
        flag[ord(letter) - 97] = False

    available_letters = []

    for i in range(0, 26):
        if flag[i] is True:
            available_letters.append(chr(i + 97))

    return ''.join(available_letters)


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.
    """
    vowels = ['u', 'e', 'o', 'a', 'i']
    number_of_guess = 6
    number_of_warning = 3
    guessed = False

    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')

    letters_guessed = []

    while not guessed and number_of_guess >= 1:
        print('------------')

        # Determine that we should use the singular or the plural form of nouns 'guess'
        guess_word_form = 'guesses' if (number_of_guess > 1) else 'guess'

        print('You have', number_of_guess, guess_word_form, 'left.')
        available_letters = get_available_letters(letters_guessed)
        print('Available letters:', available_letters)
        guess_letter = input("Please guess a letter: ")

        # Guess an invalid character
        if len(guess_letter) == 1 and not guess_letter.isalpha():
            # Decrease the number of guess if there's no number of warning left.
            if number_of_warning > 0:
                number_of_warning -= 1
            else:
                number_of_guess -= 1
            # Determine that we should use the singular or the plural form of nouns 'guess'
            warning_word_form = 'warnings' if (number_of_warning > 1) else 'warning'
            print('Oops! That is not a valid letter.')
            print('You have', number_of_warning, warning_word_form, 'left:',
                  get_guessed_word(secret_word, letters_guessed))
            continue

        # Guess a duplicated character
        if guess_letter in letters_guessed:
            print('Oops! You\'ve already guessed that letter.')
            # Decrease the number of guess if there's no number of warning left.
            if number_of_warning > 0:
                number_of_warning -= 1
            else:
                number_of_guess -= 1
            warning_word_form = 'warnings' if (number_of_warning > 1) else 'warning'
            print('You now have', number_of_warning, warning_word_form, 'left:',
                  get_guessed_word(secret_word, letters_guessed))
            continue

        # Guess a correct character
        if guess_letter in secret_word:
            letters_guessed.append(guess_letter)
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            if get_guessed_word(secret_word, letters_guessed) == secret_word:
                guessed = True
            continue

        # Guess an incorrect character
        print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
        if guess_letter in vowels:
            number_of_guess -= 2
        else:
            number_of_guess -= 1

    print('------------')
    # Win the game
    if guessed:
        number_of_unique_character = len(set(secret_word))
        score = number_of_guess * number_of_unique_character
        print('Congratulations, you won!')
        print('Your total score for this game is:', score)
    # Lose the game
    else:
        print('Sorry, you ran out of guesses. The word was ' + secret_word + '.')


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the /
     corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    if len(my_word) is not len(other_word):
        return False
    # Check if are there any mismatches
    is_same = True
    for i in range(len(my_word)):
        if my_word[i] != '_' and my_word[i] != other_word[i]:
            is_same = False
            break
    return is_same


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
    """

    matching_words = []
    match_found = True

    for word in wordlist:
        if match_with_gaps(my_word, word):
            matching_words.append(word)
            match_found = True

    if match_found:
        all_matching_worlds = ' '.join(matching_words)
        print('Possible words matched are:', all_matching_worlds)
    else:
        print('No matches found')


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.
    """
    vowels = ['u', 'e', 'o', 'a', 'i']
    number_of_guess = 6
    number_of_warning = 3
    guessed = False

    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')

    letters_guessed = []

    while not guessed and number_of_guess >= 1:
        print('------------')

        # Determine that we should use the singular or the plural form of nouns 'guess'
        guess_word_form = 'guesses' if (number_of_guess > 1) else 'guess'

        print('You have', number_of_guess, guess_word_form, 'left.')
        available_letters = get_available_letters(letters_guessed)
        print('Available letters:', available_letters)
        guess_letter = input("Please guess a letter: ")

        # In case the player want to get hint
        if guess_letter == '*':
            # Remove whitespace in the word returned from the method
            current_word = get_guessed_word(secret_word, letters_guessed).replace(' ', '')
            show_possible_matches(current_word)
            continue

        # Guess an invalid character
        if len(guess_letter) == 1 and not guess_letter.isalpha():
            # Decrease the number of guess if there's no number of warning left.
            if number_of_warning > 0:
                number_of_warning -= 1
            else:
                number_of_guess -= 1
            # Determine that we should use the singular or the plural form of nouns 'guess'
            warning_word_form = 'warnings' if (number_of_warning > 1) else 'warning'
            print('Oops! That is not a valid letter.')
            print('You have', number_of_warning, warning_word_form, 'left:',
                  get_guessed_word(secret_word, letters_guessed))
            continue

        # Guess a duplicated character.
        if guess_letter in letters_guessed:
            print('Oops! You\'ve already guessed that letter.')
            # Decrease the number of guess if there's no number of warning left.
            if number_of_warning > 0:
                number_of_warning -= 1
            else:
                number_of_guess -= 1
            warning_word_form = 'warnings' if (number_of_warning > 1) else 'warning'
            print('You now have', number_of_warning, warning_word_form, 'left:',
                  get_guessed_word(secret_word, letters_guessed))
            continue

        # Guess a correct character
        if guess_letter in secret_word:
            letters_guessed.append(guess_letter)
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            if get_guessed_word(secret_word, letters_guessed) == secret_word:
                guessed = True
            continue

        # Guess an incorrect character
        print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
        if guess_letter in vowels:
            number_of_guess -= 2
        else:
            number_of_guess -= 1

    print('------------')
    # Win the game
    if guessed:
        number_of_unique_character = len(set(secret_word))
        score = number_of_guess * number_of_unique_character
        print('Congratulations, you won!')
        print('Your total score for this game is:', score)
    # Lose the game
    else:
        print('Sorry, you ran out of guesses. The word was ' + secret_word + '.')


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
