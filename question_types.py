
# <editor-fold desc="----- IMPORT LIBRARIES AND DATA">


import requests as rq
from pandas import json_normalize
import quizmaker as qm
import random as rd


# -- importing Harry Potter characters data using API
url = 'https://hp-api.onrender.com/api/characters'
response = rq.get(url).json()
df = json_normalize(response)

# </editor-fold>


# <editor-fold desc="----- ORGANIZE DATA">

df.drop(columns=['id', 'dateOfBirth', 'yearOfBirth', 'eyeColour', 'hairColour'], inplace=True)

species = [ x for x in df['species'].unique() if x != '']
houses = [ x for x in df['house'].unique() if x != '']
ancestries = [ x for x in df['ancestry'].unique() if x != '']
patronuses = [ x for x in df['patronus'].unique() if x != '']
wand_woods = [ x for x in df['wand.wood'].unique() if x != '']
wand_cores = [ x for x in df['wand.core'].unique() if x != '']

alts = df['alternate_names'].explode()
alts.dropna(inplace=True)


# </editor-fold>


# <editor-fold desc="----- HELPER FUNCTIONS">


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


def make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction):
    q_out = {"question": question,
                "given": given,
                "actual": actual,
                "is_correct": is_correct,
                "ind": ind,
                "GIVEN": GIVEN,
                "ACTUAL": ACTUAL,
                "correction": correction}
    return q_out


# </editor-fold>


# <editor-fold desc="----- QUESTION TYPES">


# each question with the following form:
'''
INPUT: 
dataframe (shuffled list of remaining characters)
OR dataframe (as above) and series (of shuffled remaining alternate names) 

OUTPUT:
question:  str ('question' being asked)
given:  str or bool (the answer 'given' by user)
actual:  str or bool (the 'actual' / correct answer)
is_correct:  bool ('is_correct')
ind:  int (index 'ind' to remove from characters list)
GIVEN:  str (given letter choice if MC, otherwise, None)
ACTUAL:  str (actual letter choice if MC, otherwise, None)
correction:  str (correction text for stating correct answer in context)
'''

# -- True or False (TF) types


def is_student_1(df):
    """
    asks if a given character is a Hogwarts students, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"{char['name']} is a student at Hogwarts. True or False?"
    print(question)

    correction = ""

    actual = char['hogwartsStudent']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def is_staff_1(df):
    """
    asks if a given character is a Hogwarts staff member, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"{char['name']} is a staff member at Hogwarts. True or False?"
    print(question)

    correction = ""

    actual = char['hogwartsStaff']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def is_wizard_1(df):
    """
    asks if a given character is a wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
    """
    char = df.iloc[0]
    ind = char.name

    question = f"{char['name']} is a wizard. True or False?"
    print(question)

    correction = ""

    actual = char['wizard']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def is_species_1(df):
    """
    asks if a given character belongs to a certain species, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
    """
    char = df.iloc[0]
    ind = char.name

    rand_species = rd.choice(rd.sample(species, k=3) + [char['species']])

    question = f"{char['name']} is a/an {rand_species}. True or False?"
    print(question)

    correction = f"{char['name']} is a/an {char['species']}."

    actual = rand_species == char['species']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def is_house_1(df):
    """
    asks if a given character belongs to a particular Hogwarts House, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
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

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def is_patronus_1(df):
    """
    asks if a given patronus belongs to a particular wizard, True or False
    :param df: dataframe
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
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

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def is_alt_name_1(df, alts):
    """
    asks if a given alternate name belongs to a particular wizard
    :param df: dataframe of HP characters
    :param alts: series of alternate names of HP characters
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
    """
    # asks if a given alternate name is that of a particular character, True or False
    alt_name = alts.iloc[0]
    ind = alts.index[0]
    char = df.loc[ind]

    rand_alt_name = rd.choice([rd.choice(alts.values), alt_name])

    question = f"One of {char['name']}'s alternate names is {rand_alt_name}. True or False?"
    print(question)

    correction = f"{char['name']} is also known as: {', '.join(x for x in char['alternate_names'])}"

    actual = rand_alt_name in char['alternate_names']
    given, is_correct = qm.process_TF(actual)

    ACTUAL, GIVEN = None, None

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def is_wand_wood_1(df):
    """
    asks if a particular wood is used in a given characters wand
    :param df: dataframe of HP characters
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
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

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


# -- Multiple Choice (MC) types


def MC_staff_1(df):
    """
    asks which character is a staff member at Hogwarts
    :param df:
    :return: [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
    """
    char = find_opts(df, 'hogwartsStaff', True).iloc[0]
    ind = char.name

    q = "Which of the following characters is a staff member at Hogwarts?"
    actual = char['name']

    opts = find_opts(df, 'hogwartsStaff', False).sample(frac=1)
    x, y, z = opts['name'].iloc[0:3].values

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"The staff member at Hogwarts is {actual} (option {ACTUAL})."

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def MC_student_1(df):
    char = find_opts(df, 'hogwartsStudent', True).iloc[0]
    ind = char.name

    q = "Which of the following characters is a student at Hogwarts?"
    actual = char['name']

    opts = find_opts(df, 'hogwartsStudent', False).sample(frac=1)
    x, y, z = opts['name'].iloc[0:3].values

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"The student at Hogwarts is {actual} (option {ACTUAL})."

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


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

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def MC_house_2(df):
    char = find_opts(df, 'house', '', True).iloc[0]
    ind = char.name

    q = f"Which house is {char['name']} in?"
    actual = char['house']
    x, y, z = rd.sample([x for x in houses if x != actual], k=3)

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"{char['name']} is in {actual} house (option {ACTUAL})."

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def MC_species_1(df):
    char = find_opts(df, 'species', 'human', True).iloc[0]
    ind = char.name

    q = f"Which species does {char['name']} belong to?"
    actual = char['species']
    x, y, z = rd.sample([x for x in species if x != actual], k=3)

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"{char['name']} is a/an {actual} (option {ACTUAL})."

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


def MC_alt_name_1(df, alts):
    actual = alts.iloc[0]
    ind = alts.index[0]
    char = df.loc[ind]

    q = f"By which name is {char['name']} also known as?"
    x, y, z = alts[alts.index != ind].iloc[0:3].values

    question, given, is_correct, GIVEN, ACTUAL = qm.process_MC(q, actual, x, y, z)

    correction = f"{char['name']} is also known as: {', '.join(x for x in char['alternate_names'])}"

    q_out = make_q_out(question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction)

    return q_out


# </editor-fold>


# <editor-fold desc="----- TESTING">


### My Questions:
'''
- can the questions be put in a module? (with dataframes)

- how to simplify the output of questions?
   [question, given, actual, is_correct, ind, GIVEN, ACTUAL, correction]
   
   - a tuple / dictionary? (like a template version?)
   
   - OR make question types into objects? (two types? since two types of input?)
   so class will be Q_type (with function as parent class?), 
   and each instance is a specific question type?

if OOP:

class Q_type(function):
    def __init__(self, ??? ): ??? data for making question? OR outputs?
                            ??? = type? (MC or TF) - helpful, but not necessary
                                the outputs?? 
        self.type = type


'''

# question = is_wand_wood_1

# list of question types for reference
# TF_qs = [is_student_1, is_staff_1, is_wizard_1, is_species_1, is_house_1, is_patronus_1, is_alt_name_1, is_wand_wood_1]
# MC_qs = [MC_student_1, MC_staff_1, MC_house_1, MC_house_2, MC_species_1, MC_alt_name_1]
# alts_qs = [is_alt_name_1, MC_alt_name_1]  # require df and alts as input
# question_types = TF_qs + MC_qs
#
#
#
#
#
# for question in question_types:
#     if question in alts_qs:
#         q_out = question(df, alts)
#     else:
#         q_out = question(df)
#     print(f"is_correct: {q_out['is_correct']}")