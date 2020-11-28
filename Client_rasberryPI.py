import requests
import json
import socket
import sys

def post(url, newItem): # 해당 url에 new Item post
    response = requests.post(url, data=newItem)

if __name__ == '__main__':
    web_server_url = "http://localhost:3000/"
    newItem = {
        "port":1234,
        "address":"127.0.0.1",
        "rtspLink":"rtsp://localhost:8554/test",
        "gps":""
    }
    if(len(sys.argv) < 2) :
        print("port를 인자로 입력하세요 ex) python3 Client_rasberryPI.py 4567")
        sys.exit()

    port = sys.argv[1]
    newItem["port"] = port

    address = socket.gethostbyname(socket.gethostname())
    newItem["address"] = address

    rtspLink = "rtsp://" + address + ":" + port + "/test.mp4"
    newItem["rtspLink"] = rtspLink
    post(web_server_url, newItem)

    #print(newItem)
    
# post 함수 예시

# newItem = {
#     "port":1234,
#     "address":"127.0.0.1",
#     "rtspLink":"rtsp://localhost:8554/test",
#     "gps":""
#     }
# post("http://localhost:3000/", newItem)

# print(response.text)
