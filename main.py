import os
import sys
import requests
import json


#음성녹음 후 저장
os.system('arecord -D plughw:2,0 -d 5 mic_data/micTest.mp3')
#저장한 음성 불러오기
data = open('mic_data/micTest.mp3', 'rb')


client_id = "uqxuk1o1n2"
client_secret = "ZZ5R25thKHgDUat5oVIHbNjKliT6uZA4HtryiaqH"

#네이버 클라우드 플랫폼 접속을 위한 두개의 url과 headers 지정
lang = "Kor" # 언어 코드 ( Kor, Jpn, Eng, Chn )
csr_url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
csr_headers = {
		"X-NCP-APIGW-API-KEY-ID": client_id,
		"X-NCP-APIGW-API-KEY": client_secret,
		"Content-Type": "application/octet-stream"
}

sentiment_url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
sentiment_headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}

response = requests.post(csr_url,  data=data, headers=csr_headers)#서버에 보낸후 데이터 받기
rescode = response.status_code
content = response.text[9:-2]# 쓸데없는 부분을 짜르고 사용자가 말한 부분만 저장

#오류가 아닐시 문자열 데이터 출력 오류라면 오류 코드와 오류번호 출력
if(rescode == 200):
    print(content)
else:
    print("Error : " + rescode + "\n 출력문 : " + response.text)


data = {
    "content":content
}

#print(json.dumps(data,indent=4, sort_keys=True))
response = requests.post(sentiment_url,  data=json.dumps(data), headers=sentiment_headers)
rescode = response.status_code
dict = json.loads(response.text)
#print(type(dict))

if(rescode == 200):
    print(json.dumps(dict, indent="\t"))
    print(dict)
else:
    print("Error : " + response.text)
