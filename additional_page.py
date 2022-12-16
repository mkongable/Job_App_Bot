import pyautogui
import pytesseract
from text_recognition import *


BLANK_BOX_KEYWORD_DICT = {
    "Linked": "https://www.linkedin.com/in/mkongable/",
    "AWS": "2",
    "Github": "https://github.com/mkongable",
    "Website": "https://github.com/mkongable",
    "Most recent company": "NASA",
    "Most recent job title": "Rover Engineer",
    "Name": "Megan",
    "Pronouns": "She/Her",
    "Salary": "75000",
    "Compensation": "75000",
    "referral": "N/A",
    "refer": "LinkedIn",
    "related to": "N/A",
    "location": "Center Point, Iowa",
    "City": "Center Point, Iowa",
    "API": "4",
    "Remote": "Yes",
    "Java": "4",
    "Python": "4",
    "C++": "4",
    "C#": "1",
    "Programming": "5",
    "JavaScript": "2",
    "HTML": "2",
    "React": "2",
    "CSS": "2",
    "SQL": "2",
    "MongoDB": "2",
    "Software": "3",
    "Unity": "1",
    "Git": "3",
    "Linux": "2",
    "CI/CD": "2",
    "Azure": "2",
    "AGILE": "4",
    "Report": "3",
    "Microsoft": "4",
    "Name": "Megan",
    "hear": "LinkedIn",
    "C": "1"
}

SELECT_OPTION_KEYWORD_DICT = {
    "Sponsorship": "images/dropdowns/no.png",
    "legally": "images/dropdowns/yes.png",
    "backend": "images/dropdowns/yes.png",
    "first hear": "images/dropdowns/linkedin.png",
    "currently an employee": "images/dropdowns/no.png",
    "referral": "images/dropdowns/no.png",
    "API": "images/dropdowns/yes.png",
    "AWS": "images/dropdowns/yes.png",
    "Consent": "images/dropdowns/yes.png",
    "Require": "images/dropdowns/no.png",
    "Remote": "images/dropdowns/yes.png",
    "Java": "images/dropdowns/yes.png",
    "Python": "images/dropdowns/yes.png",
    "C++": "images/dropdowns/yes.png",
    "C#": "images/dropdowns/yes.png",
    "JavaScript": "images/dropdowns/yes.png",
    "HTML": "images/dropdowns/yes.png",
    "React": "images/dropdowns/yes.png",
    "CSS": "images/dropdowns/yes.png",
    "SQL": "images/dropdowns/yes.png",
    "MongoDB": "images/dropdowns/yes.png",
    "Software": "images/dropdowns/yes.png",
    "Unity": "images/dropdowns/yes.png",
    "Git": "images/dropdowns/yes.png",
    "Linux": "images/dropdowns/yes.png",
    "CI/CD": "images/dropdowns/yes.png",
    "Azure": "images/dropdowns/yes.png",
    "AGILE": "images/dropdowns/yes.png",
    "Report": "images/dropdowns/yes.png",
    "Microsoft": "images/dropdowns/yes.png",
    "Citizen": "images/dropdowns/yes.png",
    "Age range": "images/dropdowns/ageRange.png",
    "Ethnicity": "images/dropdowns/white.png",
    "pronouns": "images/dropdowns/sheher.png",
    "gender": "images/dropdown/female.png",
    "App Store": "images/dropdowns/no.png",
    "Relocate": "images/dropdowns/yes.png",
}


# gets the text above a blank box centered at the coordinates provided
# this also works for the select an option box
def get_text_image_above(center_of_box):
    # get the coordinates of the center of the box
    (x, y) = center_of_box

    # get the text above the box
    text_above_box = pyautogui.screenshot(region=(x - 483, y - 80, 970, 57))

    return text_above_box


# process the image into text
def get_text(im):
    extracted_text = pytesseract.image_to_string(im)
    return extracted_text


# blank box response text
def blank_box_response_text(text):
    # if any part of text is a key in the blank box response dictionary, return the value, else return "0"
    for key in BLANK_BOX_KEYWORD_DICT:
        if key.lower() in text.lower():
            return BLANK_BOX_KEYWORD_DICT[key]
    return "0"


# select option response text
def select_option_response_text(text):
    # if any part of text is a key in the select option response dictionary, return the value, else return None
    for key in SELECT_OPTION_KEYWORD_DICT:
        if key.lower() in text.lower():
            return SELECT_OPTION_KEYWORD_DICT[key]
    return None