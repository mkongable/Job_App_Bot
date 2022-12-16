import pyautogui
from util import *
large_easy_apply = pyautogui.locateOnScreen('images/buttons/large_easy.png', confidence=0.95, region=APPLICATION_REGION)
print(large_easy_apply)
# log_error_screenshot(APPLICATION_REGION)