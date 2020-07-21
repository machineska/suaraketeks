# importing libraries
import os
from uuid import uuid4

import speech_recognition as sr

from pydub import AudioSegment, effects
from pydub.silence import split_on_silence

dataset_dir = '../datatest/'
filename = dataset_dir + '02.m4a'


myresult = str(uuid4().hex)
mychunk = myresult


# a function that splits the audio file into chunks
# and applies speech recognition
def silence_based_conversion(path=filename, silence_thresh=-33):

    try:
        os.mkdir('../results')
    except FileExistsError:
        pass

    listfname = filename.split(".")
    ext_file = listfname[-1]

    # song = AudioSegment.from_wav(path)
    #
    # if ext_file.lower() == 'mp3':
    #     song = AudioSegment.from_mp3(path)

    rawsound = AudioSegment.from_file(path, ext_file)
    song = effects.normalize(rawsound)

    # open a file where we will concatenate
    # and store the recognized text
    fh = open("../results/{0}.txt".format(myresult), "w+")

    # split track where silence is 0.5 seconds
    # or more and get chunks
    chunks = split_on_silence(song,
                              # must be silent for at least 0.5 seconds
                              # or 500 ms. adjust this value based on user
                              # requirement. if the speaker stays silent for
                              # longer, increase this value. else, decrease it.
                              min_silence_len=500,

                              # consider it silent if quieter than -16 dBFS
                              # adjust this per requirement
                              silence_thresh=silence_thresh
                              )

    # create a directory to store the audio chunks.
    try:
        os.chdir('..')
        os.mkdir('audio_chunks')
    except FileExistsError:
        pass

    # move into the directory to
    # store the audio files.
    os.chdir('audio_chunks')

    i = 0
    # process each chunk
    for chunk in chunks:

        # Create 0.5 seconds silence chunk
        chunk_silent = AudioSegment.silent(duration=10)

        # add 0.5 sec silence to beginning and
        # end of audio chunk. This is done so that
        # it doesn't seem abruptly sliced.
        audio_chunk = chunk_silent + chunk + chunk_silent

        # export audio chunk and save it in
        # the current directory.
        print("saving chunk{0}.wav".format(i))
        # specify the bitrate to be 192 k
        audio_chunk.export("./{0}-{1}.wav".format(mychunk, i), bitrate='192k', format="wav")

        # the name of the newly created chunk
        fl = mychunk + '-' + str(i) + '.wav'

        print("Processing chunk " + str(i))

        # get the name of the newly created chunk
        # in the AUDIO_FILE variable for later use.
        file = fl

        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(file) as source:
            # remove this if it is not working
            # correctly.
            # r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened, language='id-ID')
            # write the output to the file.
            fh.write(rec + ". ")
            print(rec)

        # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")
            fh.write("#######  ")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

        i += 1

    os.chdir('../src')


if __name__ == '__main__':
    silence_based_conversion(silence_thresh=-35)
