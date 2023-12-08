from PIL import Image, ImageGrab
import cv2
import os
import pytesseract
import keyboard
import time
import pyperclip
import numpy as np
from collections import Counter
from langchain.llms import OpenAI
from langchain import PromptTemplate

tesseract_path = "C:\Program Files\Tesseract-OCR\\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = tesseract_path

import os

# Load environment variables from file
with open('.env') as f:
    for line in f:
        key, value = line.strip().split('=')
        os.environ[key] = value

# Use environment variables in your code
print(os.environ["OPENAI_API_KEY"])

def on_key_event(e): #Waits for shift + ctrl combination to start OCR process
    if e.event_type == keyboard.KEY_DOWN:
        if keyboard.is_pressed('shift') and keyboard.is_pressed("ctrl"):
            screenshot = ImageGrab.grabclipboard()
            if screenshot:
                bgColor =  detect_background_color(screenshot)
                img = processImage(screenshot,bgColor)
                extractText(img)
                print("Screenshot captured from clipboard and processed!")
                time.sleep(0.5)
                summarizeText(pyperclip.paste()) #Comment out to disable summarization
                print("Screenshot text summarized!") #Comment out to disable summarization
            else:
                text = pyperclip.paste()
                if(text == None):
                    print("Neither an image nor text was found in the clipboard")
                    return
                summarizeText(text) #Comment out to disable summarization
                print("Text copied from clipboard and summarized!") #Comment out to disable summarization
                
def detect_background_color(image): #Detects background color of the image and returns that information to be used in preprocessing
    img = np.array(image)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_flattened = img_gray.flatten()
    color_counts = Counter(img_gray_flattened)
    most_common_color = color_counts.most_common(1)[0][0]
    return most_common_color

def processImage(image, bgColor): #Applies preprocessing techniques to the image to improve prediction accuracy
    img = np.array(image)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if bgColor >= 128:
        bgColor = 255 - bgColor
        img_gray = cv2.bitwise_not(img_gray)
        
    thresh, img_bw = cv2.threshold(img_gray, bgColor + 10, 255, cv2.THRESH_BINARY)
    img_bw = cv2.bitwise_not(img_bw)

    kernel = np.ones((2,2),np.uint8)
    img_erode = cv2.erode(img_bw, kernel, iterations=1)
    
    return img_erode
    
def extractText(img): #Extracts text from image, automatically saves it into the clipboard and returns it
    ocr_result = pytesseract.image_to_string(img)
    ocr_result = ocr_result.replace("\n\n", "\n")
    ocr_result = ocr_result.replace("“", "\"").replace("”","\"") #Common error when extracting code syntax from screenshot
    pyperclip.copy(ocr_result)
    return ocr_result

def summarizeText(text): #Summarizes OCR text by sending sending the information to GPT-3.5 and asking for a summary
    llm = OpenAI(model_name="text-davinci-003", openai_api_key = os.environ['OPENAI_API_KEY'])
    template = """
    You will be provided with some text captured from a screenshot using OCR. I want you to summarize this text. The text may include some grammatical mistakes.
    The text you have to summarize is: {text}
    """
    prompt = PromptTemplate(input_variables=["text"], template=template)
    pyperclip.copy(llm(prompt.format(text=text)))

def main():
    print("Press Shift + Ctrl to load image from clipboard. Press Shift + Ctrl + alt to perform summarization on image or text in clipboard\n"+
          "You can keep the program running in the background, it'll terminate when you press esc")
    keyboard.hook(on_key_event)
    try:
        keyboard.wait('esc')
    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    main()