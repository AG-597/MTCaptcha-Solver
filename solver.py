import base64
import io
import random
import string
from pydub import AudioSegment, effects
import speech_recognition as sr
import requests
import time
import datetime

#https://t.me/csolver
#https://discord.gg/csolver

#BEST Captcha solver ^^^

def reconize(b64MP3):
    ffmpeg = './ffmpeg.exe'

    AudioSegment.converter = ffmpeg

    AudData = base64.b64decode(b64MP3)
    aaudio = AudioSegment.from_file(io.BytesIO(AudData), format="mp3")

    audio = effects.normalize(aaudio)

    mp3Bytes = io.BytesIO(AudData)
    audio = AudioSegment.from_mp3(mp3Bytes)

    wavBytes = io.BytesIO()
    audio.export(wavBytes, format="wav")

    recognizer = sr.Recognizer()

    wavBytes.seek(0)
    with sr.AudioFile(wavBytes) as source:
        AudData = recognizer.record(source)

    try:
        text = recognizer.recognize_google(AudData)
        procText = ''.join(text.split())
        return procText
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def getChal(ssid, headers):
    ts = int(time.time() * 1000)
    r = requests.get(
        "https://service.mtcaptcha.com/mtcv1/api/getchallenge.json", 
        params={
            "sk": "MTPublic-DemoKey9M",
            "bd": "service.mtcaptcha.com",
            "rt": ts,
            "tsh": "TH[83568921fa4dc8f6b855adf836d4ef49]",
            "act": "$",
            "ss": ssid,
            "lf": "1",
            "tl": "$",
            "lg": "en",
            "tp": "s"
        },
        headers=headers
    )
    return r.json() 

def getAudio(ssid, headers):
    ct = getChal(ssid, headers)
    r = requests.get(
        'https://service.mtcaptcha.com/mtcv1/api/getaudio.json', 
        params={
            "sk": "MTPublic-DemoKey9M",
            "ct": ct['result']['challenge']['ct'],
            "fa": "$",
            "ss": ssid
        },
        headers=headers
    )
    fseed = ct['result']['challenge']['foldChlg']['fseed']
    return r.json(), ct['result']['challenge']['ct'], fseed

def solve(sk, site, tsh):
    ssid = 'S' + ''.join(random.choices(string.ascii_letters + string.digits, k=9))
    headers = {
        'authority': 'service.mtcaptcha.com',
        'method': 'GET',
        'path': f'/mtcv1/api/getchallenge.json?sk={sk}&bd={site}&rt={int(time.time() * 1000)}&tsh={tsh}&act=%24&ss={ssid}&lf=1&tl=%24&lg=en&tp=s',
        'scheme': 'https',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,de;q=0.9',
        'Cookie': 'jsV=2024-03-24.15.25.36; mtv1ConfSum={v:01|wdsz:std|thm:basic|lan:en|chlg:std|clan:1|cstyl:1|afv:0|afot:0|}; mtv1Pulse=0001VdfJPyhISbfNra4WcbfR6o',
        'Dnt': '1',
        'Priority': 'u=1, i',
        'Referer': f'https://service.mtcaptcha.com/mtcv1/client/iframe.html?v=2024-03-24.15.25.36&sitekey={site}&iframeId=mtcaptcha-iframe-1&widgetSize=standard&custom=false&widgetInstance=mtcaptcha&challengeType=standard&theme=basic&lang=en&action=&autoFadeOuterText=false&host=https%3A%2F%2Fservice.mtcaptcha.com&hostname=service.mtcaptcha.com&serviceDomain=service.mtcaptcha.com&textLength=0&lowFrictionInvisible=&enableMouseFlow=false',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Avast Secure Browser";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Avast/126.0.0.0',
    }
    audio, ct, fseed = getAudio(ssid, headers)
    
    ans = reconize(audio['result']['aud']['audio64'])
    newheaders = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en,de;q=0.9",
    "Cookie": f"jsV={datetime.now().strftime('%Y-%m-%d.%H.%M.%S')}; mtv1ConfSum={{v:01|wdsz:std|thm:basic|lan:en|chlg:std|clan:1|cstyl:1|afv:0|afot:0|}}; mtv1Pulse=0001hovhjfxCjzvl1nKOImvZZZ",
    "Dnt": "1",
    "Priority": "u=1, i",
    "Referer": f"https://service.mtcaptcha.com/mtcv1/client/iframe.html?v={datetime.now().strftime('%Y-%m-%d.%H.%M.%S')}&sitekey={sk}&iframeId=mtcaptcha-iframe-1&widgetSize=standard&custom=false&widgetInstance=mtcaptcha&challengeType=standard&theme=basic&lang=en&action=&autoFadeOuterText=false&host={f'https://{site}'}&hostname={site}&serviceDomain={site}&textLength=0&lowFrictionInvisible=&enableMouseFlow=false",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Avast Secure Browser";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Avast/126.0.0.0"
}
    r = requests.get(
        'https://service.mtcaptcha.com/mtcv1/api/solvechallenge.json',
        params = {
            "ct": ct,
            "sk": sk,
            "st": ans,
            "lf": 1,
            "bd": site,
            "rt": int(time.time() * 1000),
            "tsh": tsh,
            "fa": "ziXXcJpQ5PGRKq_fMza2Ahq9wARv0_qvGsOOVeNE0vyaJqpkWuSMItGei3f",
            "qh": "$",
            "act": "$",
            "ss": ssid,
            "tl": "$",
            "lg": "en",
            "tp": "s",
            "kt": "H0khTUIqiIwwTmV9kTXQfvDf-oXhrGYcZSDZaCnJewoE9z7d-VXvCJtw6NW5ayNf",
            "fs": fseed
        },
        headers=newheaders
    )
        
    return r.json

try:
    print(solve('MTPublic-DemoKey9M', 'service.mtcaptcha.com', 'TH[83568921fa4dc8f6b855adf836d4ef49]')) # replace with site (domain NOT url) & sitekey & TH values
except:
    pass
