'''
main author: Katarzyna Sowka (katsowka)
title: Harry Potter Characters Quiz

based on final project of CFG Python and Apps Kickstarter course
originally done in collaboration with Emma Jourzac (jourzy)
'''

# <editor-fold desc="----- IMPORT LIBRARIES">
from HP_char_type import HP_char_type as ct # from file name import class
import random as rd
import datetime
import csv
import quizmaker as qm  # custom
import question_types as qt  # custom


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


def update_qs_txt(qs_txt, round_, question, q_out):
    if question in MC_qs:
        qs_txt += f'{round_}. {q_out["question"]}\n\t\tYou answered {q_out["given"]} (option {q_out["GIVEN"]}) - '
        if q_out["is_correct"]:
            qs_txt += txt_correct + "\n\n"
        else:
            qs_txt += txt_wrong + "\n\t\t" + q_out["correction"] + "\n\n"

    else:
        qs_txt += f'{round_}. {q_out["question"]}\n\t\tYou answered {str(q_out["given"])} - '
        if q_out["is_correct"]:
            qs_txt += txt_correct + "\n\n"
        else:
            qs_txt += (txt_wrong
                       + (("\n\t\t" + q_out["correction"]) if q_out["correction"] else "")
                       + "\n\n")

    return qs_txt


# -- game play related

##### put try_another in module???

def try_another_q (df_remaining, question_types, question):
# finds and executes another question type that doesn't throw an error
# (when error caused by too few characters remaining)

    ### (should ohly happen if forcing only a limited selection of question types
    if len(question_types) == 0:
        print(">>>>> chosen question types too limited, choosing from another list!")
        new_question = rd.choice(unrestricted_qs)
        q_out = new_question(df_remaining)
        return q_out

    else:
        new_question_types = [x for x in question_types if x not in alts_qs + [question]]
        new_question = rd.choice(new_question_types)

    try:
        q_out = new_question(df_remaining)
        return q_out

    except (IndexError, ValueError):
        print("\n\n>>>>> got another error - going deeper!")
        return try_another_q(df_remaining, new_question_types, new_question)


# </editor-fold>


# <editor-fold desc="----- SETTING UP FOR GAME PLAY">


# list of question types to be chosen from randomly
#TF_qs = [qt.is_character(qt.df, ct.STUDENT), qt.is_character(qt.df, ct.STAFF), qt.is_wizard_1, qt.is_species_1, qt.is_house_1, qt.is_patronus_1, qt.is_alt_name_1, qt.is_wand_wood_1]
# TF_qs = [qt.is_student_1, qt.is_staff_1, qt.is_wizard_1, qt.is_species_1, qt.is_house_1, qt.is_patronus_1, qt.is_alt_name_1, qt.is_wand_wood_1]
MC_qs = [qt.MC_student_1, qt.MC_staff_1, qt.MC_house_1, qt.MC_house_2, qt.MC_species_1, qt.MC_alt_name_1]
# all_qs = TF_qs + MC_qs

alts_qs = [qt.is_alt_name_1, qt.MC_alt_name_1]  # require df and alts as input
unrestricted_qs = [qt.is_student_1, qt.is_staff_1, qt.is_wizard_1, qt.is_species_1] # work on just one and any character

question_types = [qt.is_character, qt.is_character]

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
    alts_remaining = alts.sample(frac=1)

    # asking for number of rounds
    rounds = qm.ask_rounds(max_rounds)

    # creating random selection of question types
    questions = rd.choices(question_types, k=rounds)

    # initializing items
    score = 0
    round_ = 1
    qs_txt = qs_intro

    # -- going through each question
    for question in questions:

        if round_ == rounds:
            print(f"\n***** Round {round_} - Last One! *****")
        else:
            print(f"\n***** Round {round_} *****")

        # questions requiring alternative names series
        if question in alts_qs:
            try:
                q_out = question(df_remaining, alts_remaining)

            except (IndexError, ValueError):
                q_out = try_another_q(df_remaining, question_types, question)

        # 'regular' questions, only requiring characters dataframe
        else:
            try:
                q_out = question(qt.df, ct.STUDENT)

            except (IndexError, ValueError) as e:
                q_out = try_another_q(df_remaining, question_types, question)

        # adding question to text and stats files
        qs_txt = update_qs_txt(qs_txt, round_, question, q_out)
        log_stats(stats_file, date_short, question.__name__, df_remaining.loc[q_out["ind"]]['name'], q_out["is_correct"])

        # question feedback and updating score and round
        if q_out["is_correct"]:
            print(txt_correct)
            score += 1
        else:
            print(txt_wrong)
            if show_answer and q_out["correction"]:
                print(q_out["correction"])
        round_ += 1

        ### why ignore errors in df_ramaining?
        # dropping used character and refreshing character lists if needed
        df_remaining.drop(q_out["ind"], inplace=True, errors='ignore')
        alts_remaining.drop(q_out["ind"], inplace=True, errors='ignore')

        if len(df_remaining) == 0:
            # print(">>> refreshing lists!")
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

    # logging score if 5 or more rounds
    if rounds >= 5:
        save_score = qm.ask_YN("Would you like to save your score?")
        if save_score:
            log_score(score_file, date_short, score, rounds)
    else:
        print("If you play 5 or more rounds you have a chance to appear on the leaderboard!")


def leaderboard(N=10):
    # creates a top N leaderboard (default is top 10) from scores file
    try:
        data = read_csv(score_file)
    except (IOError, FileNotFoundError):
        print("No leaderboard yet! Here's your chance to be #1!")
        return

    # converting to integers
    for each in data:
        each['Rounds'] = int(each['Rounds'])
        each['Percent'] = float(each['Percent'])

    # sorting and trimming to max N rows
    sorted_data = sorted(sorted(data, key=lambda x: x['Rounds'], reverse=True),
                         key=lambda x: x['Percent'], reverse=True)
    lb_data = sorted_data[:min(N, len(sorted_data))]

    # saving file
    write_csv(lb_file, score_field_names, lb_data)

    # displaying
    print("\n***************  LEADERBOARD  ***************\n")
    for x in range(len(lb_data)):
        print(f"{x + 1:3}: {lb_data[x]['Username']:12} "
              f"Score: {lb_data[x]['Score']} / {lb_data[x]['Rounds']} "
              f"= {lb_data[x]['Percent']} %\n")


# </editor-fold>


# ----- MAIN


while True:
    play(qt.df, qt.alts, question_types, qs_intro)
    leaderboard()
    play_again = qm.ask_YN("\nWould you like to play again?")
    if not play_again:
        print("Goodbye!")
        break

# q_out = qt.is_character(qt.df, ct.STUDENT )
# print(f"is_correct: {q_out['is_correct']}")

# for question in question_types:
#     if question in alts_qs:
#         q_out = question(qt.df, qt.alts)
#     else:
#         q_out = question(qt.df)
#     print(f"is_correct: {q_out['is_correct']}")