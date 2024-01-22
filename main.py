'''
Harry Potter Characters Quiz

main author: Katarzyna Sowka (katsowka)

based on final project of CFG Python and Apps Kickstarter course
originally done in collaboration with Emma Jourzac (jourzy)
'''


# ----- IMPORT LIBRARIES AND DATA


import requests as rq
import pandas as pd
from pandas import json_normalize  # 'unravels' nested columns, like wand
import numpy as np
import random as rd
import datetime
import csv

# importing Harry Potter characters data using API
url = 'https://hp-api.onrender.com/api/characters'
response = rq.get(url).json()

df = json_normalize(response)


# ----- ORGANIZE DATA

# 'name', 'alternate_names', 'species', 'gender', 'house', 'wizard',
# 'ancestry', 'patronus', 'hogwartsStudent', 'hogwartsStaff', 'actor',
# 'alternate_actors', 'alive', 'image', 'wand.wood', 'wand.core', 'wand.length'
# / df, df_remaining, alts, alts_remaining
# / species, houses, ancestries, patronuses, wand_woods, wand_cores

df.drop(columns=['id', 'dateOfBirth', 'yearOfBirth', 'eyeColour', 'hairColour'], inplace=True)

### previous spot for df and df_remaining
### now placed below cat values, but still not all fixed
### species MC main problem, just get to errors!!

species = [ x for x in df['species'].unique() if x != '']
houses = [ x for x in df['house'].unique() if x != '']
ancestries = [ x for x in df['ancestry'].unique() if x != '']
patronuses = [ x for x in df['patronus'].unique() if x != '']
wand_woods = [ x for x in df['wand.wood'].unique() if x != '']
wand_cores = [ x for x in df['wand.core'].unique() if x != '']



###### TEMOPORARY SHORT DF
df = df.iloc[0:100]

df_remaining = df.sample(frac=1)



alts = df['alternate_names'].explode()
alts.dropna(inplace = True)
alts_remaining = alts.sample(frac=1)

# ----- HELPER FUNCTIONS

# -- basic and True of False (TF) related


def check_ans(given, actual):
    """
    compares the given response to the actual answer to determine if correct
    :param given: given answer to check
    :param actual: actual answer
    :return: bool
    """
    if given == actual:
        #print("\t>>> Correct! :D")
        return True
    else:
        #print("\t>>> Sorry, wrong answer. :(")
        return False


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
    given = ask_TF()
    is_correct = check_ans(given, actual)
    return [given, is_correct]


# -- Multiple Choice (MC) related

''' go over these choices and consider changing
ans: correct answer -> change to 'actual'?
xyz: incorrect answers
ANS: correct letter choice -> change/d to 'ACTUAL'?
ABCD: letter choices
'''


def mix_MC(actual, x, y, z):
    """
    klxjhksj
    :param actual:
    :param x:
    :param y:
    :param z:
    :return:
    """
    lst = [actual, x, y, z]
    rd.shuffle(lst)
    LST = ['A', 'B', 'C', 'D']
    ACTUAL = LST[lst.index(actual)]
    dict = {LST[x]: lst[x] for x in range(len(lst))}
    return dict, ACTUAL


def print_MC(q, a, b, c, d):
    """
    kadjfhkasfh
    :param q:
    :param a:
    :param b:
    :param c:
    :param d:
    :return:
    """
    question = f"QUESTION: {q}\n\tA: {a}\n\tB: {b}\n\tC: {c}\n\tD: {d}"
    return question


def ask_MC():
    """
    kjhgjlhg
    :return:
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


def process_MC (q, actual, x, y, z):
    """
    jkhgjhggj
    :param q:
    :param actual:
    :param x:
    :param y:
    :param z:
    :return:
    """
    dict, ACTUAL = mix_MC(actual, x, y, z)
    a, b, c, d = dict.values()
    question = print_MC(q, a, b, c, d)
    print(question)
    GIVEN = ask_MC()
    given = dict[GIVEN]
    is_correct = check_ans(given, actual)
    return [question, given, is_correct, GIVEN, ACTUAL]


# -- dataframe related


def find_opts(df, cat_filter, val, flip=False):
    """
     find_opts(df, 'name', 'species', 'giant') -> series of names where species = giant
     find_opts(df, 'name', 'species', 'giant', False) -> series of names where species != giant
    :param df: dataframe, use full or partial
    :param cat_filter: category used to filter
    :param val: values in filter category
    :param flip: if filtering by cat_want != val
    :return: series with filter applied
    """
    if not flip:
        return df[df[cat_filter] == val]
    else:
        return df[df[cat_filter] != val]


# ----- QUESTION TYPES


# each question with the following form:
'''
INPUT: 
dataframe (shuffled list of remaining characters or full list of characters)
OR dataframe (as above) and series (of shuffled remaining alternate names) 

OUTPUT:
str ('question' being asked)
str or bool (the answer 'given' by user)
str or bool (the 'actual' / correct answer)
bool ('is_correct')
int (index 'ind' to remove from characters list, None if not removing one)
##### something for indicating error, like with insufficient data for question type
'''

# -- True or False (TF) types

def is_student(df):
    """
    asks if a given character is a Hogwarts students, True or False
    :param df: dataframe
    :return: [question, given, actual, check_ans(given, actual), ind]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"Is {char['name']} a student at Hogwarts?"
    print("QUESTION: " + question)

    actual = char['hogwartsStudent']
    ''' old, remove if fine
    given = ask_TF()
    is_correct = check_ans(given, actual)
    '''
    given, is_correct = process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_staff(df):
    """
    asks if a given character is a Hogwarts staff member, True or False
    :param df: dataframe
    :return: [question, given, actual, check_ans(given, actual), ind]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"Is {char['name']} a staff member at Hogwarts?"
    print("QUESTION: " + question)

    actual = char['hogwartsStaff']
    given, is_correct = process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_wizard(df):
    """
    asks if a given character is a wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, check_ans(given, actual), ind]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"Is {char['name']} a wizard?"
    print("QUESTION: " + question)

    actual = char['wizard']
    given, is_correct = process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_house(df):
    """
    asks if a given character belongs to a particular Hogwarts House, True or False
    :param df: dataframe
    :return: [question, given, actual, check_ans(given, actual), ind]
    """
    char = find_opts(df, 'house', '', True).iloc[0]
    ind = char.name

    rand_house = rd.choice(houses + [char['house']])  # 2 in 5 chance correct

    question = f"Is {char['name']} in {rand_house} house?"
    print("QUESTION: " + question)

    actual = char['house'] == rand_house
    given, is_correct = process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_patronus(df):
    """
    asks if a given patronus belongs to a particular wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, check_ans(given, actual), 0]
    """
    char = find_opts(df, 'patronus', '', True).iloc[0]
    ind = char.name

    rand_patronus = rd.choice(rd.sample(patronuses, k=3) + [char['patronus']])

    question = f"{char['name']}'s patronus is a/an: {rand_patronus}"
    print("QUESTION: " + question)

    actual = char['patronus'] == rand_patronus
    given, is_correct = process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_species(df):
    """
    asks if a given patronus belongs to a particular wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, check_ans(given, actual), 0]
    """
    char = df.iloc[0]
    ind = char.name

    rand_species = rd.choice(rd.sample(species, k=3) + [char['species']])

    question = f"{char['name']} belongs to the species: {rand_species}"
    print("QUESTION: " + question)

    actual = char['species'] == rand_species
    given, is_correct = process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_alt_name(df, alts):
    # asks if a given alternate name is that of a particular character, True or False
    alt_name = alts.iloc[0]
    ind = alts.index[0]
    char = df.loc[ind]

    rand_alt_name = rd.choice([rd.choice(alts.values), alt_name])

    question = f"One of {char['name']}'s alternate names is: {rand_alt_name}"
    print("QUESTION: " + question)

    actual = rand_alt_name in char['alternate_names']
    given, is_correct = process_TF(actual)

    return [question, given, actual, is_correct, ind]


### sample row of df returns df, need to use squeeze, better solution?
def is_wand_wood(df):
    # asks if a given wood type is used in a particular wizard's wand, True or False
    char = find_opts(df, 'wand.wood', '', True).sample().squeeze()
    ind = char.name

    other_wand_wood = rd.choice(wand_woods)
    rand_wand_wood = rd.choice([other_wand_wood, char['wand.wood']])

    question = f"The wood type of {char['name']}'s wand is: {rand_wand_wood}"
    print("QUESTION: " + question)

    actual = rand_wand_wood == char['wand.wood']
    given, is_correct = process_TF(actual)

    return [question, given, actual, is_correct, ind]

# -- Multiple Choice (MC) types

### MC_process returns 5, last two not used yet, so adding [0:3] to return

def MC_staff_1(df):
    """
    asks which character is a staff member at Hogwarts
    :param df:
    :return:
    """
    char = find_opts(df, 'hogwartsStaff', True).iloc[0]
    ind = char.name

    q = "Which of the following characters is a staff member at Hogwarts?"
    actual = char['name']

    opts = find_opts(df, 'hogwartsStaff', False).sample(frac=1)
    x, y, z = opts['name'].iloc[0:3].values

    question, given, is_correct = process_MC(q, actual, x, y, z)[0:3]

    return [question, given, actual, is_correct, ind]


def MC_student_1(df):
    char = find_opts(df, 'hogwartsStudent', True).iloc[0]
    ind = char.name

    q = "Which of the following characters is a student at Hogwarts?"
    actual = char['name']

    opts = find_opts(df, 'hogwartsStudent', False).sample(frac=1)
    x, y, z = opts['name'].iloc[0:3].values

    question, given, is_correct = process_MC(q, actual, x, y, z)[0:3]

    return [question, given, actual, is_correct, ind]


def MC_house_1(df):
    house = rd.choice(houses)
    char = find_opts(df, 'house', house).iloc[0]
    ind = char.name
    actual = char['name']

    opts = find_opts(df, 'house', house, True).sample(frac=1).iloc[0:3]
    x, y, z = opts['name'].values

    q = f"Which of the following characters is in {house} house?"

    question, given, is_correct = process_MC(q, actual, x, y, z)[0:3]

    return [question, given, actual, is_correct, ind]


def MC_house_2(df):
    char = find_opts(df, 'house', '', True).iloc[0]
    ind = char.name

    q = f"Which house is {char['name']} in?"
    actual = char['house']
    x, y, z = rd.sample([x for x in houses if x != actual], k=3)

    question, given, is_correct = process_MC(q, actual, x, y, z)[0:3]

    return [question, given, actual, is_correct, ind]


# needs FULL df?
def MC_species_1(df):
    char = find_opts(df, 'species', 'human', True).iloc[0]
    ind = char.name

    q = f"Which species does {char['name']} belong to?"
    actual = char['species']
    x, y, z = rd.sample([x for x in species if x != actual], k=3)

    question, given, is_correct = process_MC(q, actual, x, y, z)[0:3]

    return [question, given, actual, is_correct, ind]


# ----- SETTING UP FOR GAME PLAY (questions, files etc.)


# list of question types to be chosen from randomly
TFqs = [is_student, is_staff, is_wizard, is_house, is_patronus, is_alt_name, is_wand_wood]
MCqs = [MC_student_1, MC_staff_1, MC_house_1, MC_house_2, MC_species_1]
question_types = TFqs + MCqs
# question_types = [is_alt_name]

# print statements
txt_correct = "Correct!"
txt_wrong = "Incorrect!"

# for writing files
today = datetime.datetime.now()
date_short = today.strftime("%d-%m-%Y")
qs_txt = f"\t\t\t~~*~** Harry Potter Quiz: Your Questions and Answers **~*~~ \n\ndate: {date_short}\n\n"


# ----- GAME PLAY


# -- setting up rounds and questions
# asking for number of rounds
while True:
    num = input("\n>>> Welcome to the Harry Potter Characters Quiz! <<< "
                "\n\nHow many rounds would you like to play? ").strip()
    if not num.isdigit() or int(num) not in range(1, 51):
        print("You can play 1 to 50 rounds. Please enter a number in that range.")
    else:
        max_rounds = int(num)
        break

# initializing score and starting round
score = 0
round_ = 1

# creating selection of questions
questions = rd.choices(question_types, k=max_rounds)

# -- going through questions
for question in questions:

    if round_ == max_rounds:
        print(f"\n***** Round {round_} - Last One! *****")
    else:
        print(f"\n***** Round {round_} *****")

    # questions requiring alternative names series
    if question in [is_alt_name]:  # ADD MC_'alts' when done
        if len(alts_remaining) == 0:
            question = rd.choice([is_student, is_staff, is_wizard])
            q, given, actual, is_correct, ind = question(df_remaining)
        else:
            q, given, actual, is_correct, ind = question(df_remaining, alts_remaining)

    ### is this required? NOT if questions skipping implemented
    # questions requiring full dataframe
    elif question in [is_wand_wood]:
        q, given, actual, is_correct, ind = question(df)

    # standard questions
    else:
        ### MC qs when df_remaining is low - Add Error returns!!
        if len(df_remaining) < 10 and question in [MCqs]:
            print("df_remaining getting low for MC!=")
            break
        q, given, actual, is_correct, ind = question(df_remaining)

    qs_add = (f"{round_}. {q}\n\tyour answer:\t{str(given)}"
              f"\n\tcorrect answer:\t{str(actual)}\n\n")
    qs_txt += qs_add

    if is_correct:
        print(txt_correct)
        score += 1
    else:
        print(txt_wrong)

    round_ += 1

    if ind is not None:
        df_remaining.drop(ind, inplace=True, errors='ignore')
        alts_remaining.drop(ind, inplace=True, errors='ignore')

    if len(df_remaining) == 0:
        print("### no chars left!!") ###
        df_remaining = df.sample(frac=1)
        alts_remaining = alts.sample(frac=1)

    ###
    # print(df_remaining['name'])
    # print(alts_remaining)


# -- after final round

end_text = f"\nYou scored {score} out of {max_rounds}."

qs_txt += f"{end_text}"

print(end_text)

with open('HPquiz_qs.txt', 'w') as file:
    file.write(qs_txt)



# ----- OLD STUFF (not used)

# --- examples of exploring dataframes
# print(df.columns)
# print(df.index)
# print(df.dtypes)
# print(df.head())
# print(df.info())
# print(df.describe())
# print(df['species'].unique())
# print(df['species'].value_counts())
# print(df[df['wizard']==False]['patronus']) # patronus column of dataframe where wizard is False
# print(df.at[3, 'patronus']=='') # unknown / missing patronus values are empty strings

# --- trials of getting df
# print(type(response)) -> list [of JSONS??
# print(response[0])
# print(type(response[0])) # -> dict

# resp_j = json.dumps(response)

# df = pd.DataFrame(response)
# Xdf = pd.read_json(response, orient='records')
# Xdf = pd.read_json(response.text)
# Xdf = pd.read_json(str(response))

# works but wand nested
# df = pd.read_json(resp_j)
