'''
main author: Katarzyna Sowka (katsowka)
title: Harry Potter Characters Quiz

based on final project of CFG Python and Apps Kickstarter course
originally done in collaboration with Emma Jourzac (jourzy)
'''

# ----- IMPORT LIBRARIES AND DATA


import requests as rq
import pandas as pd
from pandas import json_normalize
import numpy as np
import quizmaker as qm
import random as rd
import datetime
import csv

# -- importing Harry Potter characters data using API
url = 'https://hp-api.onrender.com/api/characters'
response = rq.get(url).json()
df = json_normalize(response)


# ----- ORGANIZE DATA

# NAMING REFERENCE:
# 'name', 'alternate_names', 'species', 'gender', 'house', 'wizard',
# 'ancestry', 'patronus', 'hogwartsStudent', 'hogwartsStaff', 'actor',
# 'alternate_actors', 'alive', 'image', 'wand.wood', 'wand.core', 'wand.length'
# / df, df_remaining, alts, alts_remaining
# / species, houses, ancestries, patronuses, wand_woods, wand_cores

df.drop(columns=['id', 'dateOfBirth', 'yearOfBirth', 'eyeColour', 'hairColour'], inplace=True)

species = [ x for x in df['species'].unique() if x != '']
houses = [ x for x in df['house'].unique() if x != '']
ancestries = [ x for x in df['ancestry'].unique() if x != '']
patronuses = [ x for x in df['patronus'].unique() if x != '']
wand_woods = [ x for x in df['wand.wood'].unique() if x != '']
wand_cores = [ x for x in df['wand.core'].unique() if x != '']

alts = df['alternate_names'].explode()
alts.dropna(inplace=True)
alts_remaining = alts.sample(frac=1)


##### TEMPORARY SHORT DF
df = df.iloc[0:100]
df_remaining = df.sample(frac=1)


# ----- HELPER FUNCTIONS

# -- dataframe related


def find_opts(df, cat_filter, val, flip=False):
    """
     find_opts(df, 'name', 'species', 'giant') -> series of names where species = giant
     find_opts(df, 'name', 'species', 'giant', False) -> series of names where species != giant
    :param df: dataframe, use full or partial
    :param cat_filter: category used to filter
    :param val: values in filter category
    :param flip: if filtering by cat_want != val
    :return: dataframe with filter applied
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
    :return: [question, given, actual, is_correct, ind]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"{char['name']} is a student at Hogwarts. True or False?"
    print(question)

    actual = char['hogwartsStudent']
    given, is_correct = qm.process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_staff(df):
    """
    asks if a given character is a Hogwarts staff member, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"{char['name']} a staff member at Hogwarts. True or False?"
    print(question)

    actual = char['hogwartsStaff']
    given, is_correct = qm.process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_wizard(df):
    """
    asks if a given character is a wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"{char['name']} a wizard. True or False?"
    print(question)

    actual = char['wizard']
    given, is_correct = qm.process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_house(df):
    """
    asks if a given character belongs to a particular Hogwarts House, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind]
    """
    char = find_opts(df, 'house', '', True).iloc[0]
    ind = char.name

    rand_house = rd.choice(houses + [char['house']])  # 2 in 5 chance correct

    question = f"Is {char['name']} in {rand_house} house. True or False?"
    print(question)

    actual = char['house'] == rand_house
    given, is_correct = qm.process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_patronus(df):
    """
    asks if a given patronus belongs to a particular wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind]
    """
    char = find_opts(df, 'patronus', '', True).iloc[0]
    ind = char.name

    rand_patronus = rd.choice(rd.sample(patronuses, k=3) + [char['patronus']])

    question = f"{char['name']}'s patronus is a/an {rand_patronus}. True or False?"
    print(question)

    actual = char['patronus'] == rand_patronus
    given, is_correct = qm.process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_species(df):
    """
    asks if a given patronus belongs to a particular wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind]
    """
    char = df.iloc[0]
    ind = char.name

    rand_species = rd.choice(rd.sample(species, k=3) + [char['species']])

    question = f"{char['name']} belongs to the {rand_species} species. True or False?"
    print(question)

    actual = char['species'] == rand_species
    given, is_correct = qm.process_TF(actual)

    return [question, given, actual, is_correct, ind]


def is_alt_name(df, alts):
    """
    asks if a given alternate name belongs to a particular wizard
    :param df: dataframe of HP characters
    :param alts: series of alternate names of HP characters
    :return: [question, given, actual, is_correct, ind]
    """
    # asks if a given alternate name is that of a particular character, True or False
    alt_name = alts.iloc[0]
    ind = alts.index[0]
    char = df.loc[ind]

    rand_alt_name = rd.choice([rd.choice(alts.values), alt_name])

    question = f"One of {char['name']}'s alternate names is {rand_alt_name}. True or False?"
    print(question)

    actual = rand_alt_name in char['alternate_names']
    given, is_correct = qm.process_TF(actual)

    return [question, given, actual, is_correct, ind]


### sample row of df returns df, need to use squeeze, better solution?
def is_wand_wood(df):
    """
    asks if a particular wood is used in a given characters wand
    :param df: dataframe of HP characters
    :return: [question, given, actual, is_correct, ind]
    """
    # asks if a given wood type is used in a particular wizard's wand, True or False
    char = find_opts(df, 'wand.wood', '', True).sample().squeeze()
    ind = char.name

    other_wand_wood = rd.choice(wand_woods)
    rand_wand_wood = rd.choice([other_wand_wood, char['wand.wood']])

    question = f"{char['name']}'s wand is made of {rand_wand_wood}. True or False?"
    print(question)

    actual = rand_wand_wood == char['wand.wood']
    given, is_correct = qm.process_TF(actual)

    return [question, given, actual, is_correct, ind]


# -- Multiple Choice (MC) types

### MC_process returns 5 items, last 2 not used yet, so adding [0:3] to return

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

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL]


def MC_student_1(df):
    char = find_opts(df, 'hogwartsStudent', True).iloc[0]
    ind = char.name

    q = "Which of the following characters is a student at Hogwarts?"
    actual = char['name']

    opts = find_opts(df, 'hogwartsStudent', False).sample(frac=1)
    x, y, z = opts['name'].iloc[0:3].values

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL]


def MC_house_1(df):
    house = rd.choice(houses)
    char = find_opts(df, 'house', house).iloc[0]
    ind = char.name
    actual = char['name']

    opts = find_opts(df, 'house', house, True).sample(frac=1).iloc[0:3]
    x, y, z = opts['name'].values

    q = f"Which of the following characters is in {house} house?"

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL]


def MC_house_2(df):
    char = find_opts(df, 'house', '', True).iloc[0]
    ind = char.name

    q = f"Which house is {char['name']} in?"
    actual = char['house']
    x, y, z = rd.sample([x for x in houses if x != actual], k=3)

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL]


# needs FULL df?
def MC_species_1(df):
    char = find_opts(df, 'species', 'human', True).iloc[0]
    ind = char.name

    q = f"Which species does {char['name']} belong to?"
    actual = char['species']
    x, y, z = rd.sample([x for x in species if x != actual], k=3)

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL]


# ----- SETTING UP FOR GAME PLAY (questions, files etc.)


# restricting number of rounds
max_rounds = 100

# list of question types to be chosen from randomly
TFqs = [is_student, is_staff, is_wizard, is_house, is_patronus, is_alt_name, is_wand_wood]
MCqs = [MC_student_1, MC_staff_1, MC_house_1, MC_house_2, MC_species_1]
question_types =  MCqs + TFqs
# question_types = [is_student]

### add all print statements here? then put in list that feed into play?
# print statements
txt_correct = "Correct!"
txt_wrong = "Incorrect!"

# for writing files
now = datetime.datetime.now()
now_short = now.strftime("%d-%m-%Y, %H:%M")
date_short = now.strftime("%d-%m-%Y")

qs_intro = f"\t\t\t~~*~** Harry Potter Quiz: Your Questions and Answers **~*~~ \n\ndate: {date_short}\n\n"


# ----- GAME PLAY

def play(df, alts, question_types, qs_txt):

    # refreshing character lists
    df_remaining = df.sample(frac=1)
    alts_remaining = alts.sample(frac=1)

    # asking for number of rounds
    rounds = qm.ask_rounds(max_rounds)

    # creating selection of questions
    questions = rd.choices(question_types, k=rounds)

    # initializing score and starting round
    score = 0
    round_ = 1

    # intitializing questions file
    qs_txt = qs_intro

    # going through questions
    for question in questions:

        if round_ == rounds:
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

        # MC questions
        elif question in MCqs:
            ### MC qs when df_remaining is low - Add Error return!!
            if len(df_remaining) < 10 and question in [MCqs]:
                ###
                print("df_remaining getting low for MC!=")
                break
            q, given, actual, is_correct, ind, GIVEN, ACTUAL = question(df_remaining)

        else:
            q, given, actual, is_correct, ind = question(df_remaining)

        # adding to text file
        if question in MCqs:
            qs_add = (f"{round_}. {q}\n\t\tyou answered - {GIVEN}: {given}"
                      f"\n\t\tcorrect answer - {ACTUAL}: {actual}\n\n")
        else:
            qs_add = (f"{round_}. {q}\n\t\tyou answered - {str(given)}"
                      f"\n\t\tcorrect answer - {str(actual)}\n\n")
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
            ###
            print("### no chars left!!")
            df_remaining = df.sample(frac=1)
            alts_remaining = alts.sample(frac=1)

        ###
        # print(df_remaining['name'])
        # print(alts_remaining)


    # -- after final round

    end_text = f"\nYou scored {score} out of {rounds}."

    qs_txt += f"{end_text}"

    print(end_text)

    with open('HPquiz_qs.txt', 'w') as file:
        file.write(qs_txt)


while True:
    play(df, alts, question_types, qs_intro)
    play_again = qm.ask_YN("\nWould you like to play again?")
    if not play_again:
        print("Goodbye!")
        break

