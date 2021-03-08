'''
STEP 1
Read the "JMdict_e" - the JMdict file with only English glosses and
extract all the kanji, kana, and English meanings.
The meanings are also filtered by commonly used words and words where
kana is used more often than the corresponding kanji.

Useful websites:
http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project
http://nihongo.monash.edu/wwwjdicinf.html#code_tag
'''

import xmltodict
import json
import collections

# Open the WWWJDIC dictionary xml file and convert to an Ordered Dictionary:
# "JMdict_e" is renamed to "JMdict_e_amp.xml" and only contains the "<JMdict>" tagged contents.
with open("JMdict_e_amp.xml", "r+") as xml_file:
    xml_str = xml_file.read()
    xml_import = xmltodict.parse(xml_str)
xml_import_list = []
for i in range(len(xml_import['JMdict']['entry'])):
    xml_import_list.append(xml_import['JMdict']['entry'][i])
oldest_xml_import = xml_import
xml_import = xml_import_list

# Optionally make the xml human-readable using BeautifulSoup and export it:
from bs4 import BeautifulSoup
soup = BeautifulSoup(xml_str, 'html.parser')
soup_pretty = soup.prettify()
print(soup_pretty, file=open("JMdict_e_amp_pretty.xml", "w"))

# List for tags that we don't want, such as obscure words:
unwanted_tags = ["obs", "obsc", "arch"]

# List for tags that we do want, such as for common words:
common_tags = ["news1", "news2", "ichi1", "ichi2", "spec1", "spec2", "gai1", "gai2",
               "nf01", "nf02", "nf03", "nf04", "nf05", "nf06", "nf07", "nf08", "nf09",
               "nf10", "nf11", "nf12", "nf13", "nf14", "nf15", "nf16", "nf17", "nf18",
               "nf19", "nf20", "nf21", "nf22", "nf23", "nf24", "nf25", "nf26", "nf27",
               "nf28", "nf29", "nf30", "nf31", "nf32", "nf33", "nf34", "nf35", "nf36",
               "nf37", "nf38", "nf39", "nf40", "nf41", "nf42", "nf43", "nf44", "nf45",
               "nf46", "nf47", "nf48"]

# Remove all non-common definitions. If no definitions are left, then delete entry:
# Makes a list of words containing only common words within wwwjdic dictionary:
xml_common_filt = []
for i_0 in range(len(xml_import)):
    print("Filtering common words. Word " + str(i_0 + 1) + " of "  + str(len(xml_import)) + ".")
    child_list = []
    # k_ele and ke_pri refer to kanji readings:
    if 'k_ele' in xml_import[i_0]:
        # If there's more than one definition, it's a dictionary:
        if isinstance(xml_import[i_0]['k_ele'], dict):
            if 'ke_pri' in xml_import[i_0]['k_ele']:
                for i_1 in range(len(common_tags)):
                    if common_tags[i_1] in xml_import[i_0]['k_ele']['ke_pri']:
                        if xml_import[i_0] not in xml_common_filt:
                            xml_common_filt.append(xml_import[i_0])
        else:
            # If it's a list (not dict), then there's only one definition:
            for i_1 in range(len(xml_import[i_0]['k_ele'])):
                if 'ke_pri' in xml_import[i_0]['k_ele'][i_1]:
                    for i_2 in range(len(common_tags)):
                        if common_tags[i_2] in xml_import[i_0]['k_ele'][i_1]['ke_pri']:
                            if xml_import[i_0] not in xml_common_filt:
                                xml_common_filt.append(xml_import[i_0])
    else:
        # If there's no kanji reading, do the same treatment but with the kana:
        # Kana or "reading" is r_ele and re_pri:
        if isinstance(xml_import[i_0]['r_ele'], dict):
            if 're_pri' in xml_import[i_0]['r_ele']:
                for i_1 in range(len(common_tags)):
                    if common_tags[i_1] in xml_import[i_0]['r_ele']['re_pri']:
                        if xml_import[i_0] not in xml_common_filt:
                            xml_common_filt.append(xml_import[i_0])
        else:
            for i_1 in range(len(xml_import[i_0]['r_ele'])):
                if 're_pri' in xml_import[i_0]['r_ele'][i_1]:
                    for i_2 in range(len(common_tags)):
                        if common_tags[i_2] in xml_import[i_0]['r_ele'][i_1]['re_pri']:
                            if xml_import[i_0] not in xml_common_filt:
                                if xml_import[i_0] not in xml_common_filt:
                                    xml_common_filt.append(xml_import[i_0])

# Export "xml_import" to json file:
# Export json file:
json_filename = "xml_import.json"
json_xml_import = json.dumps(xml_import)
with open(json_filename, 'w') as jsonfile:
    json.dump(json_xml_import, jsonfile)
# Re-import json file of xml_import to save time when running script many times:
with open(json_filename, 'r') as jsonfile:
    json_load = json.load(jsonfile)
json_od = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(json_load)
xml_import = json_od

# Export "xml_common_filt" to json file:
# Export json file:
json_filename = "xml_common_filt.json"
json_xml_import = json.dumps(xml_common_filt)
with open(json_filename, 'w') as jsonfile:
    json.dump(json_xml_import, jsonfile)
# Re-import json file of xml_import to save time when running script many times:
with open(json_filename, 'r') as jsonfile:
    json_load = json.load(jsonfile)
json_od = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(json_load)
xml_common_filt = json_od