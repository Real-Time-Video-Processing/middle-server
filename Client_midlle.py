import requests
import json
import subprocess
import threading

rtspLinkList=[] 

def ffmpeg(connect_url, out_url): #ffmpeg 실행 ex) ffmpeg -i "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov" http://localhost:8090/monitoring1.ffm
    command = 'ffmpeg -i "' + connect_url + '" ' + out_url
    arg = list()
    arg.append(command)
    proc = subprocess.call(arg, shell=True)

def ffserver(): #ffserver 실행
    proc = subprocess.call(["ffserver", "-f" ,"ffserver.conf"])

def get(url):
    response = requests.get(url)

    # print(response.text)
    # print(response.json())
    return response

def polling_web():
    url = "http://localhost:3000/" # 웹서버 주소(url)

    response = get(url) #해당 url로 get 함수 호출

    rasberryPIjson = response.json() #get으로 얻은 json string
    rasberryPIinfo = json.loads(rasberryPIjson) #json string을 python dict 로 변환

    if rasberryPIinfo["rtspLink"] in rtspLinkList : # rtspLinkList 에 해당 링크가 존재하는지 유무
        return # 존재하면 이미 실행하고 있는 중이므로 리턴
    else : # 존재하지 않으면 rtspLinkList에 추가하고 ffserver, ffmpeg 실행
        rtspLinkList.append(rtspLinkList)
        t1 = threading.Thread(target=ffserver) #ffserver 실행
        t1.start()

        t1 = threading.Thread(target=ffmpeg, args=(rasberryPIinfo["rtspLink"], "http://localhost:8090/monitoring1.ffm")) # ffmpeg 실행
        t1.start()

def startPolling(interval_sec): # interval_sec 마다 polling web 실행
    print("start Polling")
    poll = threading.Timer(interval_sec, polling_web)
    poll.start()

def post(url, newItem): # 해당 url에 new Item post
    response = requests.post(url, data=newItem)

if __name__ == '__main__':
    startPolling(10)

# post 함수 예시

# newItem = {
#     "port":1234,
#     "address":"127.0.0.1",
#     "rtspLink":"rtsp://localhost:8554/test",
#     "gps":""
#     }
# post("http://localhost:3000/", newItem)

# print(response.text)