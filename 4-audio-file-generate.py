'''
STEP 4
This script will take the word lists previously generated and
generate .mp3 files for the Japanese, Japanese pronunciation
(with each syllable separated), and English pronunciation using
Google's text-to-speech.
'''

from gtts import gTTS
import os.path
from pydub import AudioSegment

# Number of words to convert to sound files:
no_of_words = 1000
# Pause length between the Japanese and English definitions:
all_pause_duration = 500
# Pause length after saying the English number:
numeral_pause_duration = 500
# Pause length between English definitions:
eng_pause_duration = 500
# Pause length after everything has been said:
end_pause_duration = 3000
# Pauses for between full hiragana and syllables:
kana_pause_duration = 500
# Pause between each syllable in the "slow pronunciation":
syl_pause_duration = 1

# Make the directories for each type of audio file.
pause_dir = "pauses"
kana_dir = "kana"
full_kana_dir = "full_kana"
combined_kana_dir = "combined_kana"
pronunciation_dir = "pronunciation"
numeral_dir = "numerals"
english_single_def_dir = "eng_single_def"
combined_eng_dir = "combined_eng"
final_dir = "final_audio"

# Check if the different directories for the audio files exist, and create them.
if os.path.isdir(pause_dir):
    print("Pause directory exists. Do not make.")
else:
    os.mkdir(pause_dir)
    print("Making Pause directory.")

if os.path.isdir(kana_dir):
    print("Kana directory exists. Do not make.")
else:
    os.mkdir(kana_dir)
    print("Making Kana directory.")

if os.path.isdir(full_kana_dir):
    print("Kana directory exists. Do not make.")
else:
    os.mkdir(full_kana_dir)
    print("Making Kana directory.")

if os.path.isdir(combined_kana_dir):
    print("Kana directory exists. Do not make.")
else:
    os.mkdir(combined_kana_dir)
    print("Making Kana directory.")

if os.path.isdir(pronunciation_dir):
    print("'Pronunciation' directory exists. Do not make.")
else:
    os.mkdir(pronunciation_dir)
    print("Making 'Pronunciation' directory.")

if os.path.isdir(english_single_def_dir):
    print(str(english_single_def_dir) + " directory exists. Do not make.")
else:
    os.mkdir(english_single_def_dir)
    print("Making " + str(english_single_def_dir) + " directory.")

if os.path.isdir(numeral_dir):
    print(str(numeral_dir) + " directory exists. Do not make.")
else:
    os.mkdir(numeral_dir)
    print("Making " + str(numeral_dir) + " directory.")

if os.path.isdir(combined_eng_dir):
    print(str(combined_eng_dir) + " directory exists. Do not make.")
else:
    os.mkdir(combined_eng_dir)
    print("Making " + str(combined_eng_dir) + " directory.")

if os.path.isdir(final_dir):
    print(str(final_dir) + " directory exists. Do not make.")
else:
    os.mkdir(final_dir)
    print("Making " + str(final_dir) + " directory.")

word_no = 1
word_no_str_pad = str(word_no).zfill(5)

# Generate pause files:
kana_pause = AudioSegment.silent(duration=kana_pause_duration)
kana_pause_filename = pause_dir + "/kana_pause.mp3"
kana_pause.export(out_f=kana_pause_filename)
print("Exporting + " + kana_pause_filename)

# Add pauses for between the hiragana syllables:
syl_pause = AudioSegment.silent(duration=syl_pause_duration)
syl_pause_filename = pause_dir + "/syl_silence.mp3"
syl_pause.export(out_f=syl_pause_filename)
print("Exporting + " + syl_pause_filename)

# Add pauses for between the Japanese and English sections of the final audio:
all_pause_filename = pause_dir + "/all_pause.mp3"
all_pause = AudioSegment.silent(duration=all_pause_duration)
all_pause.export(out_f=all_pause_filename)
print("Exporting + " + all_pause_filename)

# Add pause at the end of the final audio:
end_pause_filename = pause_dir + "/end_pause.mp3"
end_pause = AudioSegment.silent(duration=end_pause_duration)
end_pause.export(out_f=end_pause_filename)
print("Exporting + " + end_pause_filename)

# Add pause for between the English numerals corresponding each individual meaning:
numeral_pause_filename = pause_dir + "/numeral_pause.mp3"
numeral_pause = AudioSegment.silent(duration=numeral_pause_duration)
numeral_pause.export(out_f=numeral_pause_filename)
print("Exporting + " + numeral_pause_filename)

# Add pause for between the English gloss definitions:
eng_pause_filename = pause_dir + "/eng_pause.mp3"
eng_pause = AudioSegment.silent(duration=eng_pause_duration)
eng_pause.export(out_f=eng_pause_filename)
print("Exporting + " + eng_pause_filename)

# Generate "1" and "2" English audio:
audio_one = gTTS(text="one", lang="en", slow=False)
audio_one.save(numeral_dir + "/1_numeral.mp3")
audio_two = gTTS(text="two", lang="en", slow=False)
audio_two.save(numeral_dir + "/2_numeral.mp3")

### Generate word files:
final_file_list = []

for i in range(len(all_words_filt[:no_of_words])):
    # Kana files made first:
    for kana in range(len(kana_list_filt[i])):
        print("Word no. is " + str(word_no) + ".")
        kana_audio_full = gTTS(text=kana_list_filt[i][kana], lang="ja", slow=False)
        kana_full_filename = full_kana_dir + "/" + kana_list_filt[i][kana] + ".mp3"
        if os.path.isfile(kana_full_filename):
            print("File exists. Do nothing.")
        else:
            kana_audio_full.save(kana_full_filename)
            print("Full kana saved")
        # Split hiragana string:
        kana_split = list(kana_list_filt[i][kana])
        print(kana_split)
        # Join small ゃ　ょ　ゅ　ャ　ョ　ュ　ァ　ィ　ェ　ォ　and ー to previous character:
        exc_list = ['ゃ', 'ょ', 'ゅ', 'ャ', 'ョ', 'ュ', 'ァ', 'ィ', 'ェ', 'ォ', 'ー']
        filt_kana = []
        for i_one in range(len(kana_split)):
            if kana_split[i_one] in exc_list:
                kana_split[i_one - 1] = kana_split[i_one - 1] + kana_split[i_one]
        for i_one in range(len(kana_split)):
            if kana_split[i_one] not in exc_list:
                filt_kana.append(kana_split[i_one])
        print(filt_kana)
        ## Make the fragments audio:
        # Save each item in list as separate audio file:
        for i_one in range(len(filt_kana)):
            if os.path.isfile(kana_dir + "/" + filt_kana[i_one] + ".mp3"):
                print("File exists. Do nothing.")
            else:
                print("File not exist. Make it.")
                kana_audio_syl = gTTS(text=filt_kana[i_one], lang="ja", slow=False)
                filename_syl = kana_dir + "/" + filt_kana[i_one] + ".mp3"
                kana_audio_syl.save(filename_syl)
        # Find the files corresponding to each individual syllable and add them together:
        for i_one in range(len(filt_kana)):
            # append .mp3 to each item in string and add together:
            filt_kana[i_one] = kana_dir + "/" + filt_kana[i_one] + ".mp3"
        print(filt_kana)
        pause_kana = []
        for i_one in range(len(filt_kana)):
            pause_kana.append(filt_kana[i_one])
            pause_kana.append(syl_pause_filename)
        pause_kana = pause_kana[:-1]
        # Make the final file:
        # Loop through the list, and sequentially add each mp3 file to each other:
        for i_one in range(len(pause_kana)):
            if i_one == 0:
                combine_syl = AudioSegment.from_mp3(pause_kana[0])
            else:
                next_syl = AudioSegment.from_mp3(pause_kana[i_one])
                combine_syl += next_syl
        combined_syl_filename = pronunciation_dir + "/" + kana_list_filt[i][kana] + "_combined.mp3"
        if os.path.isfile(combined_syl_filename):
            print("File exists. Do nothing.")
        else:
            combine_syl.export(out_f=combined_syl_filename)
        ## Finalise the kana section audio file for the particular word entry:
        kana_audio_full_file = AudioSegment.from_mp3(kana_full_filename)
        combine_syl_file = AudioSegment.from_mp3(combined_syl_filename)
        kana_pause_file = AudioSegment.from_mp3(kana_pause_filename)
        combine_kana = kana_audio_full_file + kana_pause_file + combine_syl_file + kana_pause_file + kana_audio_full_file
        combine_kana_filename = combined_kana_dir + "/" + kana_list_filt[i][kana] + "_combined_kana.mp3"
        if os.path.isfile(combine_kana_filename):
            print("File exists. Do nothing.")
        else:
            combine_kana.export(out_f=combine_kana_filename)
            print("Exporting " + combine_kana_filename)
    ##### ENGLISH #####
    # ENGLISH - GENERATING AUDIO FILES FOR EACH WORD:
    # For all English definitions stored in all_words, get the list
    # of definitions, make the filename string, and add each to the eng_filename_list
    eng_filename_list = []
    for i_one in range(len(eng_list_filt[i])):
        eng_filename_list.append([])
        for i_two in range(len(eng_list_filt[i][i_one])):
            eng_single_def = (eng_list_filt[i][i_one][i_two])
            filename_eng = english_single_def_dir + "/" + eng_single_def + ".mp3"
            eng_filename_list[i_one].append(filename_eng)
            if os.path.isfile(filename_eng):
                print(eng_single_def + " file exists. Do nothing.")
            else:
                print("English file for '" + eng_single_def + "' does not exist. Creating now.")
                eng_audio = gTTS(text=eng_list_filt[i][i_one][i_two], lang="en", slow=False)
                eng_audio.save(filename_eng)
    # If the list of definitions is more than 1,
    # add a number to each list, otherwise don't add any number:
    if len(eng_filename_list) > 1:
        numeral = 1
        for i_one in range(len(eng_filename_list)):
            numeral_str = numeral_dir + "/" + str(numeral) + "_numeral.mp3"
            eng_filename_list[i_one].insert(0, numeral_str)
            numeral += 1
    # Add appropriate pauses to eng_filename_list, in a new
    # separate list called eng_filename_list_pause:
    eng_filename_list_pause = []
    if len(eng_list_filt[i]) > 1:
        for i_one in range(len(eng_filename_list)):
            num_count = 0
            for i_two in range(len(eng_filename_list[i_one])):
                if i_two == 0:
                    eng_filename_list_pause.append(eng_filename_list[i_one][i_two])
                    eng_filename_list_pause.append(numeral_pause_filename)
                else:
                    eng_filename_list_pause.append(eng_filename_list[i_one][i_two])
                    eng_filename_list_pause.append(eng_pause_filename)
        eng_filename_list_pause = eng_filename_list_pause[:-1]
    else:
        for i_one in range(len(eng_filename_list[0])):
            eng_filename_list_pause.append(eng_filename_list[0][i_one])
            eng_filename_list_pause.append(eng_pause_filename)
        eng_filename_list_pause = eng_filename_list_pause[:-1]
    # Use eng_filename_list_pause to join all the listed
    # audio files together:
    for i_one in range(len(eng_filename_list_pause)):
        if i_one == 0:
            print("Printing " + eng_filename_list_pause[0])
            combine_eng = AudioSegment.from_mp3(eng_filename_list_pause[0])
        else:
            print("Printing " + eng_filename_list_pause[i_one])
            next_eng = AudioSegment.from_mp3(eng_filename_list_pause[i_one])
            combine_eng += next_eng
    combined_eng_filename = combined_eng_dir + "/" + kana_list_filt[i][kana] + "_eng_combined.mp3"
    if os.path.isfile(combined_eng_filename):
        print("File exists. Do nothing.")
    else:
        combine_eng.export(out_f=combined_eng_filename)
        print("Exporting " + combined_eng_filename)
    # Combine the Japanese and English together:
    combine_all = AudioSegment.from_mp3(combine_kana_filename) + AudioSegment.from_mp3(all_pause_filename) + AudioSegment.from_mp3(combined_eng_filename) + AudioSegment.from_mp3(all_pause_filename) + AudioSegment.from_mp3(kana_full_filename) + AudioSegment.from_mp3(end_pause_filename)
    combined_all_filename = final_dir + "/" + word_no_str_pad + "_all_" + kana_list_filt[i][kana] + "_combined.mp3"
    if os.path.isfile(combined_all_filename):
        print("File exists. Do nothing.")
    else:
        combine_all.export(out_f=combined_all_filename)
        print("Exporting " + combined_all_filename)
    # Increment word number:
    word_no += 1
    word_no_str_pad = str(word_no).zfill(5)
    final_file_list.append(word_no_str_pad)
