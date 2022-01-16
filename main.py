import streamlit as st
from PIL import Image
import requests
from PIL import ImageDraw
from PIL import ImageFont
import io

st.title("顔認識アプリ")


subscription_key = "f27a694900a145b99a6eb9e1565c964a"

assert subscription_key

face_api_url = "https://2022112.cognitiveservices.azure.com/face/v1.0/detect"


uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()
        
    headers = {
        "Content-Type":"application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    params = {
        "returnFaceId": "true",
        "returnFaceAttributes":"age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise"
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    results = res.json()

    fnt = ImageFont.truetype("YuGothL.ttc", 30)



    for result in results:
        
        
        rect = result["faceRectangle"]

        rec_age = int(result["faceAttributes"]["age"])
        rec_gender = result["faceAttributes"]["gender"]

        text = f"{rec_gender} {rec_age}"
        
        
        draw = ImageDraw.Draw(img)

        draw.rectangle([(rect["left"], rect["top"]), (rect["left"]+rect["width"], rect["top"]+rect["height"])], fill=None, outline="green", width=5)
        draw.text((rect["left"], rect["top"]-40) , text , font=fnt , align="center", fill='red')

    st.image(img, caption="Uploaded image", use_column_width=True)

