'''
STEP 3
Filter the Ordered dictionaries and turn them into regular lists. There is a kanji list,
a kana list, and an English list with a certain number of definitions.
'''

# MAKE LISTS:

import pandas

# Decide which word list to use for further processing:
word_list = match_list

# Get Hiragana for all words:
kana_list = []
kana_filename = "kana.txt"

for i in range(len(word_list)):
    if isinstance(word_list[i]['r_ele'], dict):
        child_kana_list = []
        child_kana_list.append(word_list[i]['r_ele']['reb'])
        kana_list.append(child_kana_list)
    elif isinstance(word_list[i]['r_ele'], list):
        child_kana_list = []
        for i_one in range(len(word_list[i]['r_ele'])):
            child_kana_list.append(word_list[i]['r_ele'][i_one]['reb'])
        kana_list.append(child_kana_list)

# 2 - Get Kanji for most words. If k_ele exists, grab it. Otherwise don't:
kanji_list = []
kanji_filename = "kanji.txt"

for i in range(len(word_list)):
    child_kanji_list = []
    if 'k_ele' in word_list[i]:
        if isinstance(word_list[i]['k_ele'], dict):
            if ('misc' in word_list[i]['sense']) and \
                    ("uk;" in word_list[i]['sense']['misc']):
                child_kanji_list.append("")
            else:
                child_kanji_list.append(word_list[i]['k_ele']['keb'])
        else:
            for i_one in range(len(word_list[i]['k_ele'])):
                if ('misc' in word_list[i]['sense']) and \
                        ("uk;" in word_list[i]['sense']['misc']):
                    child_kanji_list.append("")
                else:
                    child_kanji_list.append(word_list[i]['k_ele'][i_one]['keb'])
    else:
        child_kanji_list = []
        child_kanji_list.append("")
    kanji_list.append(child_kanji_list)

# 3 - English meanings - sense, gloss, #text
english_filename = "english.txt"
eng_list = []
parent_eng = []
child_eng = []

for i in range(len(word_list)):
    parent_eng = []
    if isinstance(word_list[i]['sense'], list): # More than one English meaning.
        for i_one in range(len(word_list[i]['sense'])):
            child_eng = []
            if isinstance(word_list[i]['sense'][i_one]['gloss'], list):
                child_eng = []
                for i_two in range(len(word_list[i]['sense'][i_one]['gloss'])):
                    child_eng.append(word_list[i]['sense'][i_one]['gloss'][i_two]["#text"])
            elif isinstance(word_list[i]['sense'][i_one], dict):
                child_eng.append(word_list[i]['sense'][i_one]['gloss']["#text"])
            parent_eng.append(child_eng)
    elif isinstance(word_list[i]['sense'], dict): # One English meaning
        child_eng = []
        if isinstance(word_list[i]['sense']['gloss'], list):
            child_eng = []
            for i_one in range(len(word_list[i]['sense']['gloss'])):
                child_eng.append(word_list[i]['sense']['gloss'][i_one]["#text"])
        elif isinstance(word_list[i]['sense']['gloss'], dict):
            child_eng.append(word_list[i]['sense']['gloss']["#text"])
        parent_eng.append(child_eng)
    eng_list.append(parent_eng)

# Make a pandas dataframe:
all_lists_dict = {"Kana": kana_list, "Kanji": kanji_list, "English": eng_list}
word_list_dataframe = pandas.DataFrame(all_lists_dict)

# All list:
all_words = []
if len(kana_list) == \
        len(kanji_list) == \
        len(eng_list):
    for i in range(len(kana_list)):
        all_words.append([])
        all_words[i].append(kana_list[i])
        all_words[i].append(kanji_list[i])
        all_words[i].append(eng_list[i])

### Filter the kanji, kana and english lists to reduce only to the most commonly used.

# Filter kana to just use first pronunciation:
kana_list_filt = []
no_of_kana = 1

for i in range(len(kana_list)):
    kana_list_filt.append(kana_list[i][:(no_of_kana)])

### Filter English words:
# Takes a full list of English words and cuts down the number of synonyms and meanings.
eng_list_filt_first = []
no_of_synonyms = 2
no_of_meanings = 2

for i in range(len(eng_list)):
    if len(eng_list[i]) > no_of_meanings:
        eng_list_filt_first.append(eng_list[i][:no_of_meanings])
    else:
        eng_list_filt_first.append(eng_list[i])

eng_list_filt = []

for i in range(len(eng_list_filt_first)):
    child_eng_list_filt = []
    for i_one in range(len(eng_list_filt_first[i])):
        if len(eng_list_filt_first[i][i_one]) > 2:
            child_eng_list_filt.append(eng_list_filt_first[i][i_one][:no_of_synonyms])
        else:
            child_eng_list_filt.append(eng_list_filt_first[i][i_one])
    eng_list_filt.append(child_eng_list_filt)

# Make all_words_filt:
all_words_filt = []
if len(kana_list) == len(kanji_list) == len(eng_list):
    for i in range(len(kana_list)):
        all_words_filt_child = []
        all_words_filt_child.append(kana_list[i])
        all_words_filt_child.append(kanji_list[i])
        all_words_filt_child.append(eng_list[i])
        all_words_filt.append(all_words_filt_child)
    print("All word lists are equal.")
else:
    print("Length of kana, kanji, and English lists are not equal.")
