import speech_recognition as sr

dataset_dir = '../datatest/'
filename = dataset_dir + '15062020_wav.wav'

r = sr.Recognizer()
# open the file
with sr.AudioFile(filename) as source:

    r.adjust_for_ambient_noise(source)

    # listen for the data (load audio to memory)
    audio_data = r.record(source)

    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data, language='id-ID', show_all=True)
    print(text)
