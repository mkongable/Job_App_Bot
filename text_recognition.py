import pytesseract
import cv2
import numpy as np
from PIL import Image

# this method should check if a job is suitable for the bot to apply to, given the extracted text from the screenshot of the job info
# we only want to apply to jobs that include the keywords in [software, developer, engineer, product, rotation]
# also returns the keyword that was successfully matched if applicable
def is_job_suitable(job_image):
    extracted_text = pytesseract.image_to_string(job_image)
    keywords = ['software', 'developer', 'engineer', 'product', 'rotation', 'quality']
    for keyword in keywords:
        if keyword in extracted_text.lower():
            return True, keyword
    return False, None


# processes an image to enhance text recognition. Assumes image is inputted as RGB
def process_image(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])  # sharpen convolution
    image = cv2.filter2D(image, -1, kernel)

    # upsample
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # apply simple binary threshold to get image with only b/w pixels
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

