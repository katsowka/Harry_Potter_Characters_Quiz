'''
main author: Katarzyna Sowka (katsowka)
title: Harry Potter Characters Quiz

based on final project of CFG Python and Apps Kickstarter course
originally done in collaboration with Emma Jourzac (jourzy)
'''

# <editor-fold desc="----- IMPORT LIBRARIES AND DATA">


import requests as rq
# import pandas as pd
from pandas import json_normalize
# import numpy as np
import quizmaker as qm
import random as rd
import datetime
import csv

# -- importing Harry Potter characters data using API
url = 'https://hp-api.onrender.com/api/characters'
response = rq.get(url).json()
df = json_normalize(response)

# </editor-fold>


# <editor-fold desc="----- ORGANIZE DATA">

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

##### TEMPORARY SHORT DF
df = df.iloc[15:25]
# print("\n>>> full df:\n", df[['name', 'alternate_names']])

alts = df['alternate_names'].explode()
alts.dropna(inplace=True)
# print("\n>>> full alts:\n", alts)

# </editor-fold>


# <editor-fold desc="----- HELPER FUNCTIONS">


# -- file related


def read_csv(file):
    # opens csv file and reads in the data as a dictionary
    with open(file, 'r') as csv_file:
        object = csv.DictReader(csv_file)
        data = []
        for row in object: # each row is a dictionary
            data.append(row)
    return data # list of dictionaries


def write_csv(file, field_names, data):
    # saves data to existing file
    with open(file, 'w') as csv_file:
        object = csv.DictWriter(csv_file,
                                fieldnames=field_names,
                                lineterminator='\n')
        object.writeheader()
        object.writerows(data)


# field names as input?
# generalize "log" functions? instead of log_scores and log_stats?
def log_score(file, date, score, rounds):
    # adds the new score data to a csv file if it exists,
    # otherwise it creates a new file to store the data
    username = qm.ask_username(10)
    new_data = {'Date': date,
                'Username': username,
                'Score': score,
                'Rounds': rounds,
                'Percent': round(score/rounds*100, 1)}
    try:
        data = read_csv(file)
        data.append(new_data)
        write_csv(file, score_field_names, data)
    # if the file doesn't exist
    except (IOError, FileNotFoundError):
        write_csv(file, score_field_names, [new_data])


def log_stats(file, date, question_type, character, is_correct):
    # adds the new score data to a csv file if it exists,
    # otherwise it creates a new file to store the data
    new_data = {'Date': date,
                'Question.type': question_type,
                'Character.name': character,
                'Correct': is_correct}
    try:
        data = read_csv(file)
        data.append(new_data)
        write_csv(file, stats_field_names, data)
    # if the file doesn't exist
    except (IOError, FileNotFoundError):
        write_csv(file, stats_field_names, [new_data])


def update_qs_txt(qs_txt, round_, question, q, given, is_correct, correction, GIVEN = None):
    if question in MC_qs:
        qs_txt += f"{round_}. {q}\n\t\tyou answered {GIVEN}: {given} - "
        if is_correct:
            qs_txt += txt_correct + "\n\n"
        else:
            qs_txt += txt_wrong + "\n\t\t" + correction + "\n\n"

    else:
        qs_txt += f"{round_}. {q}\n\t\tyou answered {str(given)} - "
        if is_correct:
            qs_txt += txt_correct + "\n\n"
        else:
            qs_txt += txt_wrong + "\n\t\t" + correction + "\n\n"

    return qs_txt

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


# </editor-fold>


# <editor-fold desc="----- QUESTION TYPES">


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

    correction = ""

    actual = char['hogwartsStudent']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


def is_staff(df):
    """
    asks if a given character is a Hogwarts staff member, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"{char['name']} is a staff member at Hogwarts. True or False?"
    print(question)

    correction = ""

    actual = char['hogwartsStaff']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


def is_wizard(df):
    """
    asks if a given character is a wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"{char['name']} is a wizard. True or False?"
    print(question)

    correction = ""

    actual = char['wizard']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


def is_house(df):
    """
    asks if a given character belongs to a particular Hogwarts House, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind]
    """
    char = find_opts(df, 'house', '', True).iloc[0]
    ind = char.name

    rand_house = rd.choice(houses + [char['house']])  # 2 in 5 chance correct

    question = f"{char['name']} is in {rand_house} house. True or False?"
    print(question)

    correction = f"{char['name']} is in {char['house']} house."

    actual = char['house'] == rand_house
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


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

    correction = f"{char['name']}'s patronus is a/an {char['patronus']}."

    actual = char['patronus'] == rand_patronus
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


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

    correction = f"{char['name']} belongs to the {char['species']} species."

    actual = char['species'] == rand_species
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


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

    correction = f"{char['name']}'s alternate name/s is/are: {', '.join(x for x in char['alternate_names'])}"

    actual = rand_alt_name in char['alternate_names']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


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

    correction = f"{char['name']}'s wand is made of {char['wand.wood']}."

    actual = rand_wand_wood == char['wand.wood']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


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

    correction = f"The staff member at Hogwarts is {actual} (option {ACTUAL})."

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


def MC_student_1(df):
    char = find_opts(df, 'hogwartsStudent', True).iloc[0]
    ind = char.name

    q = "Which of the following characters is a student at Hogwarts?"
    actual = char['name']

    opts = find_opts(df, 'hogwartsStudent', False).sample(frac=1)
    x, y, z = opts['name'].iloc[0:3].values

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"The student at Hogwarts is {actual} (option {ACTUAL})."

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


def MC_house_1(df):
    house = rd.choice(houses)
    char = find_opts(df, 'house', house).iloc[0]
    ind = char.name
    actual = char['name']

    opts = find_opts(df, 'house', house, True).sample(frac=1).iloc[0:3]
    x, y, z = opts['name'].values

    q = f"Which of the following characters is in {house} house?"

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"The character in {house} house is {actual} (option {ACTUAL})."

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


def MC_house_2(df):
    char = find_opts(df, 'house', '', True).iloc[0]
    ind = char.name

    q = f"Which house is {char['name']} in?"
    actual = char['house']
    x, y, z = rd.sample([x for x in houses if x != actual], k=3)

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"{char['name']} is in {actual} house (option {ACTUAL})."

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


# needs FULL df?
def MC_species_1(df):
    char = find_opts(df, 'species', 'human', True).iloc[0]
    ind = char.name

    q = f"Which species does {char['name']} belong to?"
    actual = char['species']
    x, y, z = rd.sample([x for x in species if x != actual], k=3)

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"{char['name']} is a/an {actual} (option {ACTUAL})."

    return [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]


# </editor-fold>


# <editor-fold desc="----- SETTING UP FOR GAME PLAY">


# list of question types to be chosen from randomly
TF_qs = [is_student, is_staff, is_wizard, is_house, is_patronus, is_alt_name, is_wand_wood]
MC_qs = [MC_student_1, MC_staff_1, MC_house_1, MC_house_2, MC_species_1]
all_qs = TF_qs + MC_qs

unrestricted_TF_qs = [is_student, is_staff, is_wizard]
unrestricted_MC_qs = [MC_student_1, MC_staff_1, MC_species_1]
restricted_qs = [x for x in all_qs if x not in (unrestricted_TF_qs + unrestricted_MC_qs)]

alts_qs = [is_alt_name]

question_types = TF_qs

# date and time formats
now = datetime.datetime.now()
now_short = now.strftime("%d-%m-%Y, %H:%M")
date_short = now.strftime("%d-%m-%Y")

# for writing files
score_file = "scores.csv"
lb_file = "leaderboard.csv"
score_field_names = ['Date', 'Username', 'Score', 'Rounds', 'Percent']

stats_file = "stats.csv"
stats_field_names = ['Date', 'Question.type', 'Character.name', 'Correct']

qs_file = "HPquiz_qs.txt"

### add all print statements here? then put in list that feed into play?
# print statements
txt_correct = "Correct!"
txt_wrong = "Incorrect!"
qs_intro = f"\t\t\t~~*~** Harry Potter Quiz: Your Questions and Answers **~*~~ \n\ndate: {date_short}\n\n"

# restricting number of rounds
max_rounds = 100

# other custom variables
show_answer = True

# </editor-fold>


# <editor-fold desc="----- GAME PLAY AND LEADERBOARD">


def play(df, alts, question_types, qs_txt):

    # creating shuffled character lists
    df_remaining = df.sample(frac=1)
#    print("\n>>> in play:\n",df_remaining[['name', 'alternate_names']])
    alts_remaining = alts.sample(frac=1)

    # asking for number of rounds
    rounds = qm.ask_rounds(max_rounds)

    # creating random selection of question types
    questions = rd.choices(question_types, k=rounds)

    # initializing items
    score = 0
    round_ = 1
    qs_txt = qs_intro

    # going through questions
    for question in questions:

        if round_ == rounds:
            print(f"\n***** Round {round_} - Last One! *****")
        else:
            print(f"\n***** Round {round_} *****")

        # questions requiring alternative names series
        if question in alts_qs:
            try:
                q, given, actual, is_correct, ind, GIVEN, ACTUAL, correction = question(df_remaining, alts_remaining)

            except (IndexError) as e:
                print(f">>> alt_qs: got {e} for question {question.__name__}")
                if len(df_remaining) > 3:
                    question = rd.choice(unrestricted_TF_qs + unrestricted_MC_qs)
                else:
                    question = rd.choice(unrestricted_TF_qs)
                q, given, actual, is_correct, ind, GIVEN, ACTUAL, correction = question(df_remaining)

        else:
            try:
                q, given, actual, is_correct, ind, GIVEN, ACTUAL, correction = question(df_remaining)

            except (IndexError, ValueError) as e:
                print(f">>> got {e} for question {question.__name__}")
                if len(df_remaining) > 3:
                    question = rd.choice(unrestricted_TF_qs + unrestricted_MC_qs)
                else:
                    question = rd.choice(unrestricted_TF_qs)
                q, given, actual, is_correct, ind, GIVEN, ACTUAL, correction = question(df_remaining)

#        print("\n>>> to log and to drop: ", df_remaining.loc[ind]['name'], "\n") ###

        # adding to qs stats file
        log_stats(stats_file, date_short, question.__name__, df_remaining.loc[ind]['name'], is_correct)

        # adding to qs text file
        update_qs_txt(qs_txt, round_, question, q, given, is_correct, correction, GIVEN)
        # if question in MCqs:
        #     qs_txt += f"{round_}. {q}\n\t\tyou answered {GIVEN}: {given} - "
        #     if is_correct:
        #         qs_txt += (txt_correct + "\n\n")
        #     else:
        #         qs_txt += (txt_wrong + "\n"
        #                    + "\t\t" + correction + "\n\n")
        #                    # + f"\n\t\tcorrect answer is {ACTUAL}: {actual}\n\n")
        # else:
        #     qs_txt += (f"{round_}. {q}\n\t\tyou answered {str(given)} - "
        #                + (txt_correct if is_correct else
        #                   txt_wrong + "\n\t\t" + correction)
        #                + "\n\n")

        if is_correct:
            print(txt_correct)
            score += 1

        else:
            print(txt_wrong)
            if show_answer and correction:
                print(correction)

        round_ += 1

        ### took out "if ind is not None"
        ### why ignore errors in df_ramaining?
        # dropping used character and refreshing character lists if needed
        df_remaining.drop(ind, inplace=True, errors='ignore')
        alts_remaining.drop(ind, inplace=True, errors='ignore')

        if len(df_remaining) == 0:
            print(">>> refreshing lists!")
            df_remaining = df.sample(frac=1)
            alts_remaining = alts.sample(frac=1)


    # -- after final round

    # generating end text
    end_text = f"\nYou scored {score} out of {rounds}."
    qs_txt += f"{end_text}"
    print(end_text)

    # generating questions file
    with open(qs_file, 'w') as file:
        file.write(qs_txt)
    print(f"\nSee the file {qs_file} if you'd like to see your questions and answers.\n")

    # logging score is 5 or more rounds
    if rounds >= 5:
        save_score = qm.ask_YN("Would you like to save your score?")
        if save_score:
            log_score(score_file, date_short, score, rounds)
    else:
        print("If you play 5 or more rounds you have a chance to appear on the leaderboard!")


def leaderboard():

    try:
        data = read_csv(score_file)
    # if the file doesn't exist
    except (IOError, FileNotFoundError):
        print("No leaderboard yet! Here's your chance to be #1!")
        return

    # converting to integers
    for each in data:
        each['Rounds'] = int(each['Rounds'])
        each['Percent'] = float(each['Percent'])


    # sorting and trimming to max 10 rows
    sorted_data = sorted(sorted(data, key=lambda x: x['Rounds'], reverse=True),
                         key=lambda x: x['Percent'], reverse=True)
    lb_data = sorted_data[:min(10, len(sorted_data))]

    # saving file
    write_csv(lb_file, score_field_names, lb_data)

    # for display
    print("\n***************  LEADERBOARD  ***************\n")
    for x in range(len(lb_data)):
        print(f"{x + 1:3}: {lb_data[x]['Username']:12} "
              f"Score: {lb_data[x]['Score']} / {lb_data[x]['Rounds']} "
              f"= {lb_data[x]['Percent']} %\n")

# </editor-fold>


# ----- MAIN


while True:
    play(df, alts, question_types, qs_intro)
    # leaderboard()
    play_again = qm.ask_YN("\nWould you like to play again?")
    if not play_again:
        print("Goodbye!")
        break

