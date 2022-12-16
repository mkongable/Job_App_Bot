from util import *

# failsafe to stop the bot
pyautogui.FAILSAFE = True

playsound('audio/start.mp3') # play start sound
APPLICATIONS_SUBMITTED = 0 # number of applications submitted
APPLICATIONS_SAVED = 0 # number of applications saved

# wait for 4 seconds so I can get my linkedin to the right page
pyautogui.sleep(4)

# ENSURE 110% ZOOM ON THE LINKEDIN JOBS SCROLL PAGE

while True:
    # process current screen iteration
    # find all jobs marked by LinkedIn easy apply
    easy_applies_on_screen = list(pyautogui.locateAllOnScreen('images/small_easy.png', region=JOB_REGION, confidence=0.85))

    # for each easy apply, process its application
    if easy_applies_on_screen == 0:
        # play error sound and raise exception
        playsound('audio/error.mp3')
        raise Exception("No easy apply jobs found on screen.")
        
    for easy_apply in easy_applies_on_screen:
        move_to_and_click(easy_apply)

        # wait for 1.3 seconds to load the application
        pyautogui.sleep(1.3)

        # use text recognition to check if the job is suitable for the bot to apply to
        job_name_screenshot = pyautogui.screenshot('screenshots/job.png', region=JOB_NAME_REGION)

        suitable, keyword = is_job_suitable(job_name_screenshot)
        if suitable:
            print(f'Job is suitable.')
        else:
            print('Job is not suitable. Skipping application.')
            continue

        # if program makes it here, job is suitable
        # look for the large easy apply button
        large_easy_apply = pyautogui.locateOnScreen('images/buttons/large_easy.png', confidence=0.95, region=APPLICATION_REGION)
        if large_easy_apply is None:
            # already applied
            print('Already applied to this job. Skipping application.')
            continue
        else:
            # click the easy apply button
            move_to_and_click(large_easy_apply)

        # wait for 0.5 seconds to load the application
        pyautogui.sleep(0.5)

        print(f"Filling out application for {keyword} job.")
        result = process_application()  # attempt to fill the application out
        if result == "Submitted":
            APPLICATIONS_SUBMITTED += 1
            print(f"Submitted application for {keyword} job.")
            print(f"Total applications submitted: {APPLICATIONS_SUBMITTED}")
        else:
            APPLICATIONS_SAVED += 1
            print(f"Total applications saved: {APPLICATIONS_SAVED}")

        # wait for 1 second to transition to the next application
        pyautogui.sleep(1)

    # after each easy apply is done check if we reached the end of the page

    current_page_indicator = pyautogui.locateOnScreen('images/currentPageIndic.png', confidence=0.9, region=JOB_REGION)

    # if we do not see the end of the page, scroll down and repeat
    if current_page_indicator is None:
        pyautogui.scroll(-700)
        # wait for 2 seconds to transition to the next scroll scene
        pyautogui.sleep(2)
    else:
        # if we do see the end of the page, advance to a new page
        # get coordinates of the current page indicator
        (x, y) = pyautogui.center(current_page_indicator)
        next_page_coords = (x + 60, y)
        
        # move the mouse 60 pixels to the right and click to get the next page
        move_to_and_click(next_page_coords)

        # wait 2 seconds to transition to the next page
        pyautogui.sleep(2)