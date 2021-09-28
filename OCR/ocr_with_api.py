import cv2
import requests
import io
import json
import ocrspace


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    img = cv2.imread(filename)

    # Calling the OCR API to send our image.
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)
    # Sending data to the server in bytes.
    result = requests.post(url_api,
                           files={filename: file_bytes},
                           data={"apikey": "f67955701b88957",
                                 "language": "eng"})

    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    return text_detected


def ocr_core2(filename):
    api = ocrspace.API(endpoint='https://api.ocr.space/parse/image', api_key='f67955701b88957',
                       language=ocrspace.Language.English)
    text = api.ocr_file(filename)
    return text
