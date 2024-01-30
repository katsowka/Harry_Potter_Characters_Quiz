# module for making quizzes, including
# writing and processing True or False (TF)
# and Multiple Choice (MC) questions

import random as rd


# -- asking Y/N, number of rounds, username


def ask_YN(msg = ""):
    # asks for yes/no input until a clear answer is provided, returns choice as boolean
    # 'msg' is optional string input to be printed before the 'Y/N:' input request
    while True:
        print(msg, end=" ")
        ans = input("Y / N : ").upper()
        if ('Y' in ans) and not ('N' in ans):
            return True
        elif ('N' in ans) and not ('Y' in ans):
            return False
        else:
            print("Your response is not clear, try again. ")


def ask_rounds(max_rounds=10):
    while True:
        num = input("How many rounds would you like to play? ").strip()
        if not num.isdigit() or int(num) not in range(1, max_rounds+1):
            print(f"You can play 1 to {max_rounds} rounds. Please enter a number in that range.")
        else:
            return int(num)


# -- True or False (TF) related


def ask_TF():
    """
    asks for true or false input until a clear answer is provided
    :return: bool
    """
    while True:
        ans = input("Enter 'T' for True or 'F' for false: ").upper()
        if ('T' in ans) and not ('F' in ans):
            print("YOUR ANSWER: True")
            return True
        elif ('F' in ans) and not ('T' in ans):
            print("YOUR ANSWER: False")
            return False
        else:
            print("Your response is not clear, try again. ")


def process_TF(actual):
    """
    asks user for their answer to TF question and determines if they are correct
    :param actual: correct answer (bool)
    :return:
    given: answer provided by user (bool)
    is_correct: bool stating whether given answer is correct
    """
    given = ask_TF()
    is_correct = given == actual
    return given, is_correct


# -- Multiple Choice (MC) related

''' check these choices and consider changing
actual: correct answer
x, y, z: incorrect answers
a, b, c, d: shuffled answer options
A, B, C, D: letter choices corresponding to answer options
ACTUAL: correct letter choice
GIVEN: letter choice given by user
given: answer chosen by user based on their letter choice
'''


def mix_MC(actual, x, y, z):
    """
    shuffles options for a multiple choice question
    :param actual: correct answer (str)
    :param x: wrong answer 1 (str)
    :param y: wrong answer 2 (str)
    :param z: wrong answer 3 (str)
    :return:
    dict: dictionary with shuffled answers matched to letter options
    ACTUAL: letter corresponding to correct answer
    """
    lst = [actual, x, y, z]
    rd.shuffle(lst)
    LST = ['A', 'B', 'C', 'D']
    ACTUAL = LST[lst.index(actual)]
    dict = {LST[x]: lst[x] for x in range(len(lst))}
    return dict, ACTUAL


def print_MC(q, a, b, c, d):
    """
    creates a formatted string for a multiple choice question
    :param q: question being asked (str)
    :param a: text for option A (str)
    :param b: text for option B (str)
    :param c: text for option C (str)
    :param d: text for option D (str)
    :return:
    question: the full formatted question, with answer options (str)
    """
    question = f"QUESTION: {q}\n\tA: {a}\n\tB: {b}\n\tC: {c}\n\tD: {d}"
    return question


def ask_MC():
    """
    asks user for answer to multiple choice question (A, B, C or D)
    :return: user input (str)
    """
    while True:
        ans = input("Enter 'A', 'B', 'C' or 'D' to indicate your answer: ").upper()
        if (('A' in ans) and not (('B' or 'C' or 'D') in ans)):
            print("YOUR ANSWER: A")
            return 'A'
        elif (('B' in ans) and not (('A' or 'C' or 'D') in ans)):
            print("YOUR ANSWER: B")
            return 'B'
        elif (('C' in ans) and not (('B' or 'A' or 'D') in ans)):
            print("YOUR ANSWER: C")
            return 'C'
        elif (('D' in ans) and not (('B' or 'C' or 'A') in ans)):
            print("YOUR ANSWER: D")
            return 'D'
        else:
            print("Your response is not clear, try again. ")


def process_MC(q, actual, x, y, z):
    """
    processes MC question
    :param q: question being asked, without options (str)
    :param actual: correct answer (str)
    :param x: wrong answer 1 (str)
    :param y: wrong answer 2 (str)
    :param z: wrong answer 3 (str)
    :return:
    question: the full formatted question, with options (str)
    given: answer indicated by user (str)
    is_correct: bool stating whether given answer is correct
    GIVEN: letter answer provided by user (str)
    ACTUAL: letter corresponding to correct answer (str)
    """
    dict, ACTUAL = mix_MC(actual, x, y, z)
    a, b, c, d = dict.values()
    question = print_MC(q, a, b, c, d)
    print(question)
    GIVEN = ask_MC()
    given = dict[GIVEN]
    is_correct = given == actual
    return [question, given, is_correct, GIVEN, ACTUAL]