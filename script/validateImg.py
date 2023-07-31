import requests
import os
import time

def downLoadImage(url):
    response = requests.get(url)

    if not os.path.exists("images"):
        os.makedirs("images")

    filename = f"vcodeImg_{int(time.time())}.jpg"
    image_path = f"images/{filename}"

    with open(image_path, "wb") as f:
        f.write(response.content)

    return filename