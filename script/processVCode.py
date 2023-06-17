from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image, ImageOps
import os


def getVCode():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    chrome = webdriver.Chrome('./chromedriver', options=options)

    url = 'https://course.fcu.edu.tw/validateCode.aspx'
    chrome.get(url)

    for i in range(49, 50):
        with open(f'./images/{i}.png', 'wb') as file:
            captcha = chrome.find_element(By.XPATH, '/html/body/img')
            file.write(captcha.screenshot_as_png)  # write to folder
        time.sleep(1)
        chrome.refresh()


def cutVCode():
    for j in range(1000):
        image = Image.open(f'./data/validateCode/photo/{j}.png')
        image = image.convert('L')

        width, height = image.size

        part_width = (width - 12) // 4

        for i in range(4):
            left = i * part_width + 6
            upper = 0
            right = (i + 1) * part_width + 6
            lower = height

            part = image.crop((left, upper, right, lower))
            part.save(f'./data/validateCode/digit/{j}-{i}.png')


def resizeVCode():
    for i in range(10):
        # Define the folder path containing the PNG images
        folder_path = f'data/digit/{i}'

        # Loop through each file in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                # Open the image file
                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path).convert("RGB")

                # Resize the image
                size = (224, 224)
                resized_image = ImageOps.fit(image, size, Image.LANCZOS)

                # Save the resized image with the new file name
                resized_image.save(os.path.join(
                    folder_path + '_resized', filename))

                # Close the image file
                image.close()
