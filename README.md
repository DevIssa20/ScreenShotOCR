# ScreenShotOCR

## About
This is a python program that awaits input from the user,then loads an image saved in the user's clipboard and extracts the text from it, then saves the text in clipboard.Very useful for quick OCR usage ! The program will then send the
output to OpenAI for summarization. In order to disable that functionality, comment out the lines of code having the comment : #Comment out to disable summarization

## Limitations
The program works extremely well for images where the background and text colors are clearly segmented, and when the image is just a block of text. Moreover, it's best to be specific in your screen snips, only snip the area of your screen which you want to extract from (Try not to include, lines, images, columns, etc...)

## Potential Improvements
- Feeding the OCR output to a language model for grammar and syntax correction
- More complex image preprocessing techniques
