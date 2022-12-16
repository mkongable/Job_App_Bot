from gtts import gTTS
tts = gTTS('Hi, I am Megan, an aspiring software engineer', lang='en')
tts.save('intro.mp3')