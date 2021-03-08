'''
STEP 5
This script will use the audio files generated in the previous script
to automatically read the length of all mp3 files and generate an .srt
subtitle file that can be imported into a video editing software along
with the audio files.
'''

import os.path
from mutagen.mp3 import MP3

def secToSrt(time_sec):
    if type(time_sec) != float:
        time_sec = float(time_sec)
    time_sec_str = str(time_sec)
    sec_str = ""
    msec_str = ""
    for i in range(len(time_sec_str)):
        if time_sec_str[i] != ".":
            sec_str += time_sec_str[i]
        else:
            msec_str += time_sec_str[(i + 1):(len(time_sec_str) + 1)]
            break
    # Minutes and seconds:
    min_sec = int(sec_str)
    sec = min_sec % 60
    sec_str = str(sec).zfill(2)
    min = int((min_sec - sec) / 60)
    # Hours
    if min > 59:
        hr_min = min
        min = min % 60
        hr = int((hr_min - min) / 60)
    else:
        hr = 0
    min_str = str(min).zfill(2)
    hr_str = str(hr).zfill(2)
    # Microseconds:
    while len(msec_str) < 3:
        msec_str += "0"
    if len(msec_str) > 3:
        msec_int = int(msec_str[:3])
        if int(msec_str[3]) >= 5:
            msec_int += 1
        msec_str = str(msec_int)
    while len(msec_str) < 3:
        msec_str += "0"
    srt_final = hr_str + ":" + min_str + ":" + sec_str + "," + msec_str
    return(srt_final)

# Start with the kanji:
srt_file_dir = "srt_files/"

# Make the .srt file directory:
if os.path.isdir(srt_file_dir):
    print(srt_file_dir + " directory exists. Do not make.")
else:
    os.mkdir(srt_file_dir)
    print("Making " + srt_file_dir + " directory.")

srt_filename_list = [(srt_file_dir + "kanji.srt"),
                     (srt_file_dir + "kana.srt"),
                     (srt_file_dir + "english.srt")]

srt_filename_kanji = srt_file_dir + "kanji.srt"
srt_filename_kana = srt_file_dir + "kana.srt"
srt_filename_english = srt_file_dir + "english.srt"

# List the full audio files currently made and sort them numerically:
audio_filename_list_pre = os.listdir(final_dir) # final_dir should already be declared from previous script.
# Exclude hidden files and folders:
audio_filename_list = []
for i in range(len(audio_filename_list_pre)):
    if audio_filename_list_pre[i][-4:len(audio_filename_list_pre[i])] == ".mp3":
        audio_filename_list.append(audio_filename_list_pre[i])
audio_filename_list.sort()

srt_counter = 1
for i in range(len(audio_filename_list)):
    # Determine lengths of audio files:
    if srt_counter == 1:
        prev_time = 0
        prev_time_str = "00:00:00,000"
        audio = MP3(final_dir + "/" + audio_filename_list[i])
        next_time = audio.info.length
        next_time_str = secToSrt(next_time)
    else:
        prev_time = next_time
        prev_time_str = secToSrt(prev_time)
        audio = MP3(final_dir + "/" + audio_filename_list[i])
        next_time = prev_time + audio.info.length
        next_time_str = secToSrt(next_time)
        print(srt_counter)
        print("prev_time = " + str(prev_time))
        print("next_time = " + str(next_time))
    time_str = prev_time_str + " --> " + next_time_str
    print("time_str = " + time_str)
    # Add srt_counter and the time:
    for i_one in range(len(srt_filename_list)):
        print(srt_counter, file = open(srt_filename_list[i_one], "a"))
        print(time_str, file = open(srt_filename_list[i_one], "a"))
    print(kanji_list[i], end = "\n\n", file = open(srt_filename_kanji, "a"))
    print(kana_list_filt[i], end = "\n\n", file = open(srt_filename_kana, "a"))
    # Print English
    if (len(eng_list_filt[i])) > 1:
        srt_eng_no = 1
        for i_one in range(len(eng_list_filt[i])):
            eng_srt_str = str(srt_eng_no) + ". "
            srt_eng_no += 1
            for i_two in range(len(eng_list_filt[i][i_one])):
                eng_srt_str += eng_list_filt[i][i_one][i_two] + "; "
            eng_str = eng_srt_str[:-2]
            print(eng_str, file = open(srt_filename_english, "a"))
        print("\n", end = "", file = open(srt_filename_english, "a"))
    else:
        for i_one in range(len(eng_list_filt[i])):
            for i_two in range(len(eng_list_filt[i][i_one])):
                if i_two == 0:
                    eng_srt_str = eng_list_filt[i][i_one][i_two] + "; "
                else:
                    eng_srt_str += eng_list_filt[i][i_one][i_two] + "; "
            eng_str = eng_srt_str[:-2]
            print(eng_str, file=open(srt_filename_english, "a"))
        print("\n", end="", file=open(srt_filename_english, "a"))
    # Increment the counter
    srt_counter += 1
