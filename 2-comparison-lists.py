'''
STEP 2
Using the Ordered Dictionaries of Japanese words produced in previous scripts,
we can order the words from most commonly used to least commonly used.

This works by:
1. We have a file called "unidic.csv" that contains Japanese words ordered from most
   to leased used (according to number of hits on Yahoo search). However, there are no
   English meanings included: only kanji and kana.
2. We need to compare the Japanese words in our Ordered Dictionaries we previously made to the
   order of the words in the unidic file. But, the Ordered Dictionaries are still very messy, and
   have lots of uncommon kanji and kana. The chance of not finding many results in Yahoo search for
   these uncommon words is high. However, the kanji and kana appear in the Ordered Dictionaries
   from most commonly used to least commonly used. i.e. the first kanji or kana to appear in each
   entry is the most commonly-used.
3. We need to make a series of four "comparison lists" that become less and less stringent with how many
   kanji or kana are included for each entry. For entries that more commonly use kana, we'll use the 'uk'
   tag to replace the kanji with the kana.
4. Using the unidic file, we compare the word on each line (from most common to least common) to the
   entries in our "comparison lists". If a match is found using the most stringent comparison list,
   then the corresponding entry in the "xml_import" or "xml_common_filt" list of Ordered Dictionaries
   is added to a "match_list". If no match is found, the word in the unidic file will then be compared
   to the words in each "comparison list" incrementally from most stringent to least stringent.
'''

import collections
import pandas

# Comparison list: create a regular (not Ordered) list of lists for making and comparing many different lists:
xml_comparison_list = []
for i_0 in range(len(xml_import)):
    child_list = []
    if 'k_ele' in xml_import[i_0]:
        if isinstance(xml_import[i_0]['k_ele'], dict):
            child_list.append(xml_import[i_0]['k_ele']['keb'])
        else:
            for i_1 in range(len(xml_import[i_0]['k_ele'])):
                child_list.append(xml_import[i_0]['k_ele'][i_1]['keb'])
    else:
        if isinstance(xml_import[i_0]['r_ele'], dict):
            child_list.append(xml_import[i_0]['r_ele']['reb'])
        else:
            for i_1 in range(len(xml_import[i_0]['r_ele'])):
                child_list.append(xml_import[i_0]['r_ele'][i_1]['reb'])
    xml_comparison_list.append(child_list)

# Create list with only one meaning per entry:
xml_comparison_list_one = [[i_0[0]] for i_0 in xml_comparison_list]
# Create list with only two meanings per entry:
xml_comparison_list_two = [[i_0[:2]] for i_0 in xml_comparison_list]

# Comparison list: for when kana is used more often, take only the most common kana form:
xml_comparison_list_one_uk = []
for i_0 in range(len(xml_import)):
    child_list = []
    is_kana = False
    if isinstance(xml_import[i_0]['sense'], dict):
        if 'misc' in xml_import[i_0]['sense']:
            if "uk;" in xml_import[i_0]['sense']['misc']:
                is_kana = True
                if isinstance(xml_import[i_0]['r_ele'], dict):
                    child_list.append(xml_import[i_0]['r_ele']['reb'])
                else:
                    child_list.append(xml_import[i_0]['r_ele'][0]['reb'])
    else:
        for i_1 in range(len(xml_import[i_0]['sense'][:2])):
            if 'misc' in xml_import[i_0]['sense'][i_1]:
                if "uk;" in xml_import[i_0]['sense'][i_1]['misc']:
                    is_kana = True
                    if isinstance(xml_import[i_0]['r_ele'], dict):
                        if xml_import[i_0]['r_ele']['reb'] not in child_list:
                            child_list.append(xml_import[i_0]['r_ele']['reb'])
                    else:
                        if xml_import[i_0]['r_ele'][0]['reb'] not in child_list:
                            child_list.append(xml_import[i_0]['r_ele'][0]['reb'])
    if is_kana == True:
        xml_comparison_list_one_uk.append(child_list)
    else:
        xml_comparison_list_one_uk.append(xml_comparison_list_one[i_0])

# Comparison list: for when kana is used more often, take the most common two kana:
xml_comparison_list_two_uk = []
for i_0 in range(len(xml_import)):
    child_list = []
    is_kana = False
    if isinstance(xml_import[i_0]['sense'], dict):
        if 'misc' in xml_import[i_0]['sense']:
            if "uk;" in xml_import[i_0]['sense']['misc']:
                is_kana = True
                if isinstance(xml_import[i_0]['r_ele'], dict):
                    child_list.append(xml_import[i_0]['r_ele']['reb'])
                else:
                    for i_1 in range(len(xml_import[i_0]['r_ele'][:2])):
                        child_list.append(xml_import[i_0]['r_ele'][i_1]['reb'])
    else:
        for i_1 in range(len(xml_import[i_0]['sense'][:2])):
            if 'misc' in xml_import[i_0]['sense'][i_1]:
                if "uk;" in xml_import[i_0]['sense'][i_1]['misc']:
                    is_kana = True
                    if isinstance(xml_import[i_0]['r_ele'], dict):
                        if xml_import[i_0]['r_ele']['reb'] not in child_list:
                            child_list.append(xml_import[i_0]['r_ele']['reb'])
                    else:
                        for i_2 in range(len(xml_import[i_0]['r_ele'][:2])):
                            if xml_import[i_0]['r_ele'][i_2]['reb'] not in child_list:
                                child_list.append(xml_import[i_0]['r_ele'][i_2]['reb'])
    if is_kana == True:
        xml_comparison_list_two_uk.append(child_list)
    else:
        xml_comparison_list_two_uk.append(xml_comparison_list_one[i_0])

### Start working with the unidic file from here:
colnames = ['lexeme', 'newspaper', 'reading']

# Import Unidic CSV file:
unidic_df = pandas.read_csv('unidic.csv', names=colnames)

# 1. Skip only-English words (e.g. ｐｌａｙｓｔａｔｉｏｎ, ａｄｄｒｅｓｓ, etc.)
# 2. Search each word in lexeme and compare to kanji of wwwjdic.
#       If there is an exact match, add that wwwjdic to the word_list
# 3. If still no matches, do a search on jisho.org and grab the first result.
#       Ask for confirmation from the user however to avoid dodgy result.
#       Add to list if okay, add to reject list if not okay.
# 4. Continue until 25,000 words is reached.

lexeme_list = unidic_df.lexeme.tolist()
main_reading_list = unidic_df.newspaper.tolist()
reading_list = unidic_df.reading.tolist()

lexeme_list_sub = []
for i in range(len(lexeme_list)):
    word_build = ""
    for i_one in range(len(lexeme_list[i])):
        if lexeme_list[i][i_one] != "鱻": # This kanji appears for unknown reasons and needs to be deleted.
            word_build += lexeme_list[i][i_one]
        else:
            break
    lexeme_list_sub.append(word_build)
lexeme_list = lexeme_list_sub

# Produce a list of matches
no_of_matches = 30_000
match_list = []
no_match_list = []
for i in range(len(lexeme_list)):
    matches_found = 0
    if len(match_list) < no_of_matches:
        # Look for a direct match in first kanji or hiragana only:
        print("Searching for " + lexeme_list[i] + ". " + \
              str(len(match_list)) + " matches found.")
        for i_one in range(len(xml_comparison_list_one)):
            for i_two in range(len(xml_comparison_list_one[i_one])):
                if lexeme_list[i] == xml_comparison_list_one[i_one][i_two]:
                    matches_found += 1
                    if xml_import[i_one] not in match_list:
                        match_list.append(xml_import[i_one])
                        print(lexeme_list[i])
                        print(xml_comparison_list_one[i_one])
                        print(xml_comparison_list_one[i_one][i_two])
        # Now look for a match in the first 2 kanji:
        for i_one in range(len(xml_comparison_list_two)):
            for i_two in range(len(xml_comparison_list_two[i_one])):
                if lexeme_list[i] == xml_comparison_list_two[i_one][i_two]:
                    matches_found += 1
                    if xml_import[i_one] not in match_list:
                        match_list.append(xml_import[i_one])
        # If usually kana, look for only the first kana entry:
        for i_one in range(len(xml_comparison_list_one_uk)):
            for i_two in range(len(xml_comparison_list_one_uk[i_one])):
                if lexeme_list[i] == xml_comparison_list_one_uk[i_one][i_two]:
                    matches_found += 1
                    if xml_import[i_one] not in match_list:
                        match_list.append(xml_import[i_one])
                        print(lexeme_list[i])
                        print(xml_comparison_list_one_uk[i_one])
                        print(xml_comparison_list_one_uk[i_one][i_two])
        # If no matches still, look using the newspaper form of the word (i.e. kanji form that is not used so much):
        if matches_found == 0:
            escape = False
            for i_one in range(len(xml_comparison_list_one)):
                for i_two in range(len(xml_comparison_list_one[i_one])):
                    if main_reading_list[i] == xml_comparison_list_one[i_one][i_two]:
                        matches_found += 1
                        if xml_import[i_one] not in match_list:
                            match_list.append(xml_import[i_one])
                            escape = True
            #
            if escape == False:
                for i_one in range(len(xml_comparison_list_two)):
                    for i_two in range(len(xml_comparison_list_two[i_one])):
                        if main_reading_list[i] == xml_comparison_list_two[i_one][i_two]:
                            matches_found += 1
                            if xml_import[i_one] not in match_list:
                                match_list.append(xml_import[i_one])
                                escape = True
            #
            if escape == False:
                for i_one in range(len(xml_comparison_list_one_uk)):
                    for i_two in range(len(xml_comparison_list_one_uk[i_one])):
                        if main_reading_list[i] == xml_comparison_list_one_uk[i_one][i_two]:
                            matches_found += 1
                            if xml_import[i_one] not in match_list:
                                match_list.append(xml_import[i_one])
                                escape = True
        if matches_found == 0:
            print("No match found. Adding now to 'NO MATCHES' list.")
            no_match_list.append(lexeme_list[i])

# Ensure to check the no_match_list for words for which matches were not find.

# Export "match_list" to json file:
# Export json file:
json_filename = "match_list.json"
json_xml_import = json.dumps(match_list)
with open(json_filename, 'w') as jsonfile:
    json.dump(json_xml_import, jsonfile)
# Re-import json file of xml_import to save time when running script many times:
with open(json_filename, 'r') as jsonfile:
    json_load = json.load(jsonfile)
json_od = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(json_load)
match_list_import = json_od
