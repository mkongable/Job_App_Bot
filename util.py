import pyautogui
import time
from playsound import playsound
from screenshot import *
from additional_page import *
from text_recognition import *

JOB_REGION = (170, 239, 700, 800)
APPLICATION_REGION = (850, 200, 1000, 800)
FILL_OUT_REGION = (442, 123, 1050, 900)
FILE_SYSTEM_REGION = (0, 0, 1195, 717)
BOTTOM_RIGHT_REGION = (910, 649, 600, 400)
HEADER_REGION = (421, 120, 500, 500)
JOB_NAME_REGION = (877, 255, 717, 100)

def move_to_and_click(loc, duration=0.2):
    """
    Moves the mouse to loc in the given duration and clicks.
    The moving happens immediately after function call.
    """
    pyautogui.moveTo(loc, duration=duration, tween=pyautogui.easeOutQuad)
    pyautogui.click(loc)


# this function processes an application, assuming its easy apply button is on the right half of the screen
def process_application():
    try:
        while True:
            # check if there is any page to fill out, then fill it out. Otherwise, submit the application or error out
            additional = pyautogui.locateCenterOnScreen('images/additional.png', confidence=0.95, region=HEADER_REGION)
            additionalQuestions = pyautogui.locateCenterOnScreen('images/additionalQ.png', confidence=0.95, region=HEADER_REGION)
            contactPage = pyautogui.locateCenterOnScreen('images/contactPage.png', confidence=0.95, region=HEADER_REGION)
            resumePage = pyautogui.locateCenterOnScreen('images/resumePage.png', confidence=0.95, region=HEADER_REGION)
            diversityPage = pyautogui.locateCenterOnScreen('images/diversity.png', confidence=0.95, region=HEADER_REGION)
            screeningPage = pyautogui.locateCenterOnScreen('images/screeningPage.png', confidence=0.95, region=HEADER_REGION)
            homePage = pyautogui.locateCenterOnScreen('images/homePage.png', confidence=0.95, region=HEADER_REGION)
            reviewPage = pyautogui.locateCenterOnScreen('images/reviewPage.png', confidence=0.95, region=HEADER_REGION)
            workAuthPage = pyautogui.locateCenterOnScreen('images/workAuth.png', confidence=0.95, region=HEADER_REGION)
            workExperiencePage = pyautogui.locateCenterOnScreen('images/workExperience.png', confidence=0.95, region=HEADER_REGION)
            educationPage = pyautogui.locateCenterOnScreen('images/education.png', confidence=0.95, region=HEADER_REGION)
            privacyPage = pyautogui.locateCenterOnScreen('images/privacyPolicy.png', confidence=0.95, region=HEADER_REGION)

            if contactPage:
                print("Processing contact page")
                result = process_contact_page()  # sometimes the contact page is the submit page
                if result == "Submitted":
                    pyautogui.moveTo(497, 595, duration=0.2) # move to the job section
                    return "Submitted"
                elif result == "Error":
                    print("Unknown contents in contact page")
                    bail_with_save()
                    return "Error"
            elif homePage:
                print("Processing home page")
                result = process_home_page()
                if result == "Blocked":
                    print("Home page blocked, save and bail")
                    bail_with_save()
            elif resumePage:
                print("Processing resume page")
                process_resume_page()
            elif diversityPage:
                print("Processing diversity page")
                process_diversity_page()
            elif workAuthPage:
                print("Processing work auth page")
                process_work_auth_page()
            elif screeningPage:
                print("Processing screening page")
                process_screening_page()
            elif additional:
                print("Processing additional page")
                result = process_additional_page()
                if result == "Blocked":
                    print("Additional page blocked, save and bail")
                    bail_with_save()  # cannot proceed, so save and bail
                    return "Error"
            elif additionalQuestions:
                print("Processing additional questions page")
                result = process_additional_page()
                if result == "Blocked":
                    print("Additional page blocked, save and bail")
                    bail_with_save()  # cannot proceed, so save and bail
                    return "Error"
            elif workExperiencePage:
                print("Processing work experience page")
                result = process_work_experience_page()
                if result == "Blocked":
                    print("Work experience page blocked, save and bail")
                    bail_with_save()
                    return
            elif educationPage:
                print("Processing education page")
                result = process_education_page()
                if result == "Blocked":
                    print("Education page blocked, save and bail")
                    bail_with_save()
                    return
            elif privacyPage:
                print("Processing privacy page")
                process_privacy_page()
            elif reviewPage:
                print("Processing review page")
                result = process_review_page()  # sometimes the contact page is the submit page
                if result == "Submitted":
                    pyautogui.moveTo(497, 595, duration=0.2) # move to the job section
                    return "Submitted"
                else:
                    return "Error" # this should never happen
            else:
                # this should never happen
                print("Error: did not detect any known page to fill out")
                bail_with_save()
                return "Error"

            # wait 1 second after processing a page
            pyautogui.sleep(1)
    except Exception as e:
        # take a screenshot of the screen and save it
        log_error_screenshot(FILL_OUT_REGION)
        playsound('audio/errorAudio.mp3')
        raise e

    
# process the contacts page
def process_contact_page():
    # sometimes the submit button is on the contacts page
    # scroll down a little bit

    pyautogui.scroll(-800)

    # wait 0.5 seconds
    pyautogui.sleep(0.5)

    submit = pyautogui.locateCenterOnScreen('images/buttons/submit.png', confidence=0.95, region=BOTTOM_RIGHT_REGION)
    next = pyautogui.locateCenterOnScreen('images/buttons/next.png', confidence=0.95, region=BOTTOM_RIGHT_REGION)
    
    if submit:
        process_submit()
        return "Submitted"
    elif next:
        move_to_and_click(next)
        return "Proceed"
    else:
        return "Error"
        

def process_resume_page():

    while True:
        uploadCoverLetter = pyautogui.locateCenterOnScreen('images/buttons/uploadCL.png', confidence=0.95, region=FILL_OUT_REGION)
        review = pyautogui.locateCenterOnScreen('images/buttons/review.png', confidence=0.95, region=FILL_OUT_REGION)
        next = pyautogui.locateCenterOnScreen('images/buttons/next.png', confidence=0.95, region=FILL_OUT_REGION)

        if uploadCoverLetter:
            print("Detected cover letter")
            # click upload cover letter
            move_to_and_click(uploadCoverLetter)

            # wait 1 second
            pyautogui.sleep(1)

            # click the file system
            CL = pyautogui.locateCenterOnScreen('images/CL_WORD.png', confidence=0.95, region=FILE_SYSTEM_REGION)
            move_to_and_click(CL)

            # wait 0.25 seconds
            pyautogui.sleep(0.25)

            # click open
            open = pyautogui.locateCenterOnScreen('images/fOpen.png', confidence=0.95, region=FILE_SYSTEM_REGION)
            move_to_and_click(open)

            # wait 2 second
            pyautogui.sleep(2)
            continue
        elif review:
            print("Detected review")
            move_to_and_click(review)
            return
        elif next:
            print("Detected next")
            move_to_and_click(next)
            return
        else:
            # raise exception
            raise Exception("Did not detect upload cover letter, review, or next button on resume page")


def process_diversity_page():
    start_time = time.perf_counter()

    while True:
        
        # the diversity page must be filled within 30 seconds or the bot bails
        time_elapsed = time.perf_counter() - start_time
        if time_elapsed > 30:
            print("Diversity taking too long")
            raise Exception("Diversity taking too long")

        gender = pyautogui.locateCenterOnScreen('images/gender.png', confidence=0.95, region=FILL_OUT_REGION)
        race = pyautogui.locateCenterOnScreen('images/race.png', confidence=0.95, region=FILL_OUT_REGION)
        veteran = pyautogui.locateCenterOnScreen('images/vetStatus.png', confidence=0.95, region=FILL_OUT_REGION)
        disability = pyautogui.locateCenterOnScreen('images/disability.png', confidence=0.95, region=FILL_OUT_REGION)
        next = pyautogui.locateCenterOnScreen('images/buttons/next.png', confidence=0.95, region=BOTTOM_RIGHT_REGION)

        if gender:
            print("Detected gender")
            # click on the gender drop down and select female
            move_to_and_click(gender)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)

            female = pyautogui.locateCenterOnScreen('images/female.png', confidence=0.95, region=FILL_OUT_REGION)
            move_to_and_click(female)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)
            continue
        elif race:
            print("Detected race")
            # click on the gender drop down and select female
            move_to_and_click(race)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)

            white = pyautogui.locateCenterOnScreen('images/white.png', confidence=0.95, region=FILL_OUT_REGION)
            move_to_and_click(white)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)
            continue
        elif veteran:
            print("Detected veteran")
            # click on the gender drop down and select female
            move_to_and_click(veteran)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)

            not_protected = pyautogui.locateCenterOnScreen('images/not_protected.png', confidence=0.95, region=FILL_OUT_REGION)
            move_to_and_click(not_protected)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)
            continue
        elif disability:
            print("Detected disability")
            # click on the gender drop down and select female
            move_to_and_click(disability)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)

            no_dis = pyautogui.locateCenterOnScreen('images/noDisab.png', confidence=0.95, region=FILL_OUT_REGION)
            move_to_and_click(no_dis)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)
            continue
        elif next:
            print("Detected next button")
            # click next
            move_to_and_click(next)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)
            return  # next page
        else:
            print("Did not detect anything useful on screen")
            print("scrolling")
            # scroll down a little bit
            pyautogui.scroll(-800)

            # wait 0.5 seconds
            pyautogui.sleep(0.5)


# handle screening page
def process_screening_page():
    scroll_and_proceed()


# processes the submit page. This method is called when there is a submit button on the screen
def process_submit():
    submit = pyautogui.locateCenterOnScreen('images/buttons/submit.png', confidence=0.95, region=FILL_OUT_REGION)
    move_to_and_click(submit)

    if not submit:
        raise Exception("Did not detect submit button on submit page")

    # wait 2 second
    pyautogui.sleep(2)

    tries = 1
    while True:
        # check for the done button. 5 tries, each 0.5 seconds apart

        if tries > 5:
            raise Exception("Did not detect done button on submit page")
        
        done = pyautogui.locateCenterOnScreen('images/buttons/done.png', confidence=0.95, region=FILL_OUT_REGION)
        done2 = pyautogui.locateCenterOnScreen('images/buttons/done2.png', confidence=0.95, region=FILL_OUT_REGION)
        dones = [done, done2]

        if not any(dones):
            # wait 0.5 seconds
            print(f"Attempt {tries} to detect done button")
            pyautogui.sleep(0.5)
        else:
            break

        tries += 1

    # move to and click the done button that is found
    move_to_and_click(next(done for done in dones if done is not None))

    # move mouse to the top left corner
    pyautogui.moveTo(5, 5, duration=0.1)

    return


# exits the application
def bail():
    print("Exiting application")

    bail = pyautogui.locateCenterOnScreen('images/bail.png', confidence=0.95, region=FILL_OUT_REGION)
    move_to_and_click(bail)

    # wait 0.2 seconds
    pyautogui.sleep(0.2)

    discard = pyautogui.locateCenterOnScreen('images/buttons/discard.png', confidence=0.95, region=FILL_OUT_REGION)
    move_to_and_click(discard)

    # wait 0.5 seconds
    pyautogui.sleep(0.5)

    pyautogui.moveTo(497, 595, duration=0.2) # move to the job section
    return


# exits the application, but saves it
def bail_with_save():

    # log screenshot of the fill out section for error analysis
    log_error_screenshot(FILL_OUT_REGION)

    print("Saving application...")
    bail = pyautogui.locateCenterOnScreen('images/bail.png', confidence=0.95, region=FILL_OUT_REGION)
    move_to_and_click(bail)

    # wait 0.2 seconds
    pyautogui.sleep(0.2)

    # try 5 times to find the save button
    move_to_and_click_with_retry(['images/buttons/save.png'], region=FILL_OUT_REGION, num_tries=5)

    # wait 1.5 seconds
    pyautogui.sleep(1.5)

    saveSuccess = pyautogui.locateCenterOnScreen('images/saveSuccess.png', confidence=0.95, region=JOB_REGION)
    if saveSuccess:
        move_to_and_click(saveSuccess)

    pyautogui.moveTo(497, 595, duration=0.2) # move to the job section


# processes the home page
def process_home_page():
    cityBox = detect_first_match(['images/homepage/cityBox.png', 'images/homepage/cityBox2.png'], region=FILL_OUT_REGION)

    if cityBox:

        move_to_and_click(cityBox)

        # wait 0.2 seconds
        pyautogui.sleep(0.2)

        # type "Center Point"
        pyautogui.typewrite("Center Point", interval=0.1)

        # wait 0.2 seconds
        pyautogui.sleep(0.2)

        move_to_and_click_with_retry(['images/homepage/CPI_US.png', 'images/homepage/CPI_US2.png'], region=FILL_OUT_REGION, num_tries=5)

    move_to_and_click_with_retry(['images/buttons/next.png'], region=FILL_OUT_REGION, num_tries=5)

    # wait 0.2 seconds
    pyautogui.sleep(0.2)

    homePage = pyautogui.locateCenterOnScreen('images/homePage.png', confidence=0.95, region=HEADER_REGION)
    if homePage:
         # stuck on homepage, report back the error
         return "Blocked"

    pyautogui.moveTo((655,278), duration=0.1, tween=pyautogui.easeInOutQuad) # in case the next NEXT button appears right where the mouse is
    return "Done"


# process additional questions page
def process_additional_page():
    start_time = time.perf_counter()

    while True:
        # move mouse away to somewhere that is still scrollable
        pyautogui.moveTo((655,278), duration=0.1, tween=pyautogui.easeInOutQuad)

        # the additional page must be filled within 30 seconds or the bot bails
        time_elapsed = time.perf_counter() - start_time
        if time_elapsed > 30:
            print("Additional taking too long")
            return "Blocked"

        blankBoxes = list(pyautogui.locateAllOnScreen('images/blankBox.png', confidence=0.995, region=FILL_OUT_REGION))  # convert generator to list is easier
        blankBoxes.extend(list(pyautogui.locateAllOnScreen('images/blankBox2.png', confidence=0.995, region=FILL_OUT_REGION))) # add instances of the second version of blankbox
        review = pyautogui.locateCenterOnScreen('images/buttons/review.png', confidence=0.95, region=FILL_OUT_REGION)
        selectOptions = list(pyautogui.locateAllOnScreen('images/selectOption.png', confidence=0.95, region=FILL_OUT_REGION))
        next = pyautogui.locateCenterOnScreen('images/buttons/next.png', confidence=0.95, region=FILL_OUT_REGION)
        blankCheck = pyautogui.locateCenterOnScreen('images/ack.png', confidence=0.95, region=FILL_OUT_REGION)

        blankBoxCount = 0
        selectBoxCount = 0
        
        if blankCheck:
            move_to_and_click(blankCheck)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)
            continue
        elif len(blankBoxes) > 0:
            for blankBox in blankBoxes:
                blankBoxCount += 1

                text_image_above = get_text_image_above(pyautogui.center(blankBox))
                processed_image = process_image(text_image_above)
                # save
                processed_image.save(f"screenshots/text_image_above{blankBoxCount}.png")
                text_from_image = get_text(processed_image)
                suitable_response = blank_box_response_text(text_from_image)

                # click the blank box
                move_to_and_click(blankBox)

                # wait 0.1 seconds
                pyautogui.sleep(0.1)

                # type the response
                pyautogui.typewrite(suitable_response, interval=0.05)
            continue
        elif len(selectOptions) > 0:
            for selectOption in selectOptions:
                selectBoxCount += 1
                text_image_above = get_text_image_above(pyautogui.center(selectOption))
                processed_image = process_image(text_image_above)
                # save
                processed_image.save(f"screenshots/select_option{selectBoxCount}.png")
                text_from_image = get_text(processed_image)
                response_img_url = select_option_response_text(text_from_image)

                if not response_img_url:
                    return "Blocked"

                # click the select option
                move_to_and_click(selectOption)

                # wait 0.1 seconds
                pyautogui.sleep(0.1)

                # see if the appropriate response image is on the screen
                response_img = pyautogui.locateCenterOnScreen(response_img_url, confidence=0.95, region=FILL_OUT_REGION)

                if response_img:
                    move_to_and_click(response_img)  # click the dropdown option
                    # wait 0.1 seconds
                    pyautogui.sleep(0.1)
                else:
                    return "Blocked" # unable to proceed
            continue
        elif review:
            move_to_and_click(review)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)

            additional_page = pyautogui.locateCenterOnScreen('images/additional.png', confidence=0.95, region=HEADER_REGION)
            additionalQuestions = pyautogui.locateCenterOnScreen('images/additionalQ.png', confidence=0.95, region=HEADER_REGION)
            additionals = [additional_page, additionalQuestions]

            if any(additionals):
                return "Blocked" # we are still on the additional page

            return "Done"  # we are on the next page
        elif next:
            move_to_and_click(next)

            # wait 0.2 seconds
            pyautogui.sleep(0.2)

            additional_page = pyautogui.locateCenterOnScreen('images/additional.png', confidence=0.95, region=HEADER_REGION)
            additionalQuestions = pyautogui.locateCenterOnScreen('images/additionalQ.png', confidence=0.95, region=HEADER_REGION)
            additionals = [additional_page, additionalQuestions]

            if any(additionals):
                return "Blocked" # we are still on the additional page

            return "Done"  # we are on the next page
        else:
            print("Did not detect anything useful on screen")
            print("scrolling")
            # scroll down a little bit
            pyautogui.scroll(-800)

            # wait 0.5 seconds
            pyautogui.sleep(0.5)


# process the review page
def process_review_page():
    # scroll down
    pyautogui.scroll(-4000)

    # wait 0.5 seconds
    pyautogui.sleep(0.5)

    process_submit()

    return "Submitted"


# process work auth page
def process_work_auth_page():
    review = pyautogui.locateCenterOnScreen('images/buttons/review.png', confidence=0.95, region=FILL_OUT_REGION)

    if not review:
        raise Exception("Did not detect review button on work auth page")
    
    move_to_and_click(review)

    # wait 0.2 seconds
    pyautogui.sleep(0.2)
    return


# process work experience page
def process_work_experience_page():
    try:
        scroll_and_proceed()
    except Exception as e:
        return "Blocked"
    return "Done"


# process education page
def process_education_page():
    try:
        scroll_and_proceed()
    except Exception as e:
        return "Blocked"
    return "Done"


# process privacy page
def process_privacy_page():
    blankCheck = pyautogui.locateCenterOnScreen('images/ack.png', confidence=0.95, region=FILL_OUT_REGION)

    if blankCheck:
        move_to_and_click(blankCheck)

    # wait 0.2 seconds
    pyautogui.sleep(0.2)
    
    # find and click the next button
    next = pyautogui.locateCenterOnScreen('images/buttons/next.png', confidence=0.95, region=FILL_OUT_REGION)
    move_to_and_click(next)

    # wait 0.2 seconds
    pyautogui.sleep(0.2)

    # check if bot is on the same page
    privacyPage = pyautogui.locateCenterOnScreen('images/privacyPolicy.png', confidence=0.95, region=HEADER_REGION)

    if privacyPage:
        return "Blocked"
    
    return "Done"



# scroll and proceed to the next page
def scroll_and_proceed():
    # move mouse away to somewhere that is still scrollable
    pyautogui.moveTo((655,278), duration=0.1, tween=pyautogui.easeInOutQuad)

    # scroll down a lot
    pyautogui.scroll(-4000)

    # wait 0.5 seconds
    pyautogui.sleep(0.5)

    review = pyautogui.locateCenterOnScreen('images/buttons/review.png', confidence=0.95, region=FILL_OUT_REGION)
    next = pyautogui.locateCenterOnScreen('images/buttons/next.png', confidence=0.95, region=FILL_OUT_REGION)

    proceed_buttons = [review, next]
    if any(proceed_buttons):
        proceed = next if next else review

        move_to_and_click(proceed)

        # wait 0.2 seconds
        pyautogui.sleep(0.2)
    else:
        raise Exception("Did not detect next or review button on page")


# tries some number of times to detect an image in a specified region and click on it. raises exception if it fails. Delay parameter is the time to wait between tries
def move_to_and_click_with_retry(image_urls, region, num_tries=5, delay=0.5):
    if len(image_urls) == 0:
        raise Exception("No images to detect")
    
    # open the image urls
    images = [Image.open(image_url) for image_url in image_urls]
    for i in range(num_tries):
        instances = [pyautogui.locateCenterOnScreen(image, confidence=0.95, region=region) for image in images]

        if any(instances):
            instance = next(instance for instance in instances if instance)
            move_to_and_click(instance)
            return
        else:
            print(f"Attempt {i}. Failed to detect {image_urls[0]} on screen. Retrying...")
            pyautogui.sleep(delay)
    raise Exception(f"Failed to detect {image_urls[0]} on screen after {num_tries} tries")


# tries to detect all instances of a list of images urls, and returns the first match box it finds
def detect_first_match(image_urls, region):
    images = [Image.open(image_url) for image_url in image_urls]
    for image in images:
        instance = pyautogui.locateCenterOnScreen(image, confidence=0.95, region=region)
        if instance:
            return instance
    return None