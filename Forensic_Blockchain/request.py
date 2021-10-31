import requests
import cv2
import base64

img = cv2.imread('corgi.jpg')
string_img = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
req = {
  "case_id": 1,
  "evid_id": 1,
  "handler": "vernon",
  "new_status": "Checked In",
  "purpose": "Storage",
  "image": string_img
}

res = requests.post('http://167.71.205.211:5000/api/check_evidence/',
                    json=req)
if res.ok:
    print(res.json())
