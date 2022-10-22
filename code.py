# Install and Import Dependencies
#pip install youtube-dl # it allows you to grap any video if it was needed 
#after installing it drop the video link to download it and put it at the home directory
!pip install ibm_watson
!brew install ffmpeg #used to extract the audio and outputting it as txt file
#format transcoding, basic editing (trimming and concatenation), video scaling, video post-production effects and standards compliance (SMPTE, ITU). 
#FFmpeg also includes other tools: ffplay ,a simple media player and ffprobe , a command-line tool to display media information

import subprocess
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Extract Audio
command = 'ffmpeg -i aiml.mkv -ab 160k -ar 44100 -vn audio.wav' #aiml.mkv is the file name 
subprocess.call(command, shell=True)

# Setup STT Service
apikey = ''
url = ''

# Setup service
authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

# Open Audio Source and Convert
with open('audio.wav', 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/wav', model='en-AU_NarrowbandModel', continuous=True).get_result()
res

# Process Results and Output to Text
len(res['results'])

text = [result['alternatives'][0]['transcript'].rstrip() + '.\n' for result in res['results']]

text = [para[0].title() + para[1:] for para in text]
transcript = ''.join(text) #join all text in one
with open('output.txt', 'w') as out: 
    out.writelines(transcript)

transcript
