import pyautogui
import string
import random


# method to take a screenshot of the region provided, and save the error in the error image directory. The error image name will be random
def log_error_screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    file_name = "error/" + get_random_string(10) + ".png"
    screenshot.save(file_name)


# method to generate a random string of length n
def get_random_string(n):
    # choose from all lowercase letters and uppercase letters
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(n))
    return result_str
