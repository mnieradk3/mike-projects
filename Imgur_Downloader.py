"""
- Imgur_Downloader.py
- written in cpython 3.6
- downloads all images from all galleries from imgur.com
    based on specified search term, output folder directory, etc.
- performed through selenium module webdriver controlling Firefox browser
    --> this allows automated up/down scrolling of the webpage by the script
    --> and to allow clicking of 'load more' button to load more galleries
    --> required to unlock ALL gallery elements from a single search term
    --> this starting browser MUST be left maximized during this process but you can
	switch focus to work in other windows
- gallery elements are then fed to 1-3 output browser windows
  through multithreading, each output browser window = one thread
    --> each browser window visits a group of galleries sequentially
    --> image elements are obtained by selenium from the gallery
    --> requests module is then used to obtain the HTML string
        (image file) from the image URL
    --> image is then downloaded, repeat for all image elements in gallery
    --> these output browsers are minimized, you can continue work elsewhere while
        they are visiting galleries and downloading
- designated time delays within script are based on testing with my
  broadband cable internet
    --> if your connection is very slow (due to hardware or lag or other reasons)
        the time delays will have to be set higher throughout the script
- if running with 3 output windows it is recommended to set a high timeout
    value in seconds (>10), and to NOT also run any other internet-related applications
"""

import os
import sys
import time
import threading
import datetime

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from requests.exceptions import ConnectionError as CE
from selenium.webdriver.common.keys import Keys

# PLACE YOUR FIREFOX WEBDRIVER FILEPATH (FOR SELENIUM) HERE !
webdriver_path = 'D:\\geckodriver.exe'

# track gallery URL visits for each search+download run
failures = 0
timeouts = 0
nontimeouts = 0


def getInfo():
    """
    Asks for info from user:
        - search term 
        - directory to save images
        - number of threads (output browser windows) to run
        - timeout value in seconds for maximum loading time of output browser windows
    """
    
    # eg. python
    while True:
        search = input("Type search term or type 'exit' to leave program: ")
        if not search:
            continue
        elif search.lower() == 'exit':
            sys.exit()
        else:
            break
    # eg. D:\pics, assumed to be a valid path (whether it currently exists or not)
    while True:
        directory = input("Type full folder path where imgur folder with images will be saved: ")
        if not directory:
            continue
        else:
            break
    # store images in ./imgur subfolder with YYYY-MM-DD stamp    
    os.makedirs(directory + '\\' + 'imgur\\' + search + '\\'
                + str(datetime.datetime.now())[:10], exist_ok=True)

    # 1 to 3 output browser windows, default 1
    while True:
        numThreads = input('How many output browser windows to run (1-3): ')
        if not numThreads:
            numThreads = 1
        elif numThreads in ['1','2','3']:
            numThreads = int(numThreads)
            break
        else:
            continue

    timeout_value = input('Enter a timeout value in seconds for maximum loading time of output browser windows: ')
    # if no timeout value specified default to 10 seconds
    if not timeout_value:
        timeout_value = 10
    else:
        timeout_value = abs(int(timeout_value))
                        
    # starting browser, used to navigate search and eventually find all gallery elements
    startBrowser = webdriver.Firefox(executable_path = webdriver_path)
    # original URL to begin (first page to show after entering search term)
    print('Loading starting imgur URL with search term')
    startBrowser.get('https://imgur.com/search?q=' + search)     
    # 5 seconds to let first page fully load after search, can be customized
    time.sleep(5)
    

    return directory,search,startBrowser,numThreads,timeout_value


def getNumClicks(startBrowser):
    """
    Determines the number of total gallery results obtained for search term within
       the starting browser window
    This total number is used to determine the number of clicks required to unlock
       ALL gallery results for your search term within the starting browser window
    """
    
    # determine the NUMBER of total gallery results found for this search term
    # this number contained in text portion of span tag with class = sorting-text-align
    results = startBrowser.find_element_by_css_selector('span[class="sorting-text-align"]')
    text = results.text
    num = ''
    for i in text:
        if i.isdigit(): num += i
    num = int(num)
    print('%s total gallery results available' % num)

    # imgur by default displays at most 60 gallery results per group
    # --> click 'end' to unlock next group of 60 results
    # periodically a 'load more' button element will appear at the bottom
    # clicking this element will then load another 60 gallery results on the SAME URL page
    # determine number of TOTAL 'end' key presses required to unlock all number
    #    of gallery results equal to 'num'
    clicks = num // 60
    print("%s clicks of 'END' required to unlock all galleries" % clicks)

    return clicks


def getGalleryElements(clicks,startBrowser):
    """
    Scrolls the starting browser window based on total number of clicks required
      to unlock ALL gallery results
    Clicks 'load more' element when it appears to keep scrolling down
    When all gallery elements are obtained the starting browser window stops loading
    """
    
    # find background body element so you can click 'end' on it repeatedly
    body = startBrowser.find_element_by_css_selector('body[class=""]')
    # click on the body element 'clicks' + 1 number of times
    # wait 7 seconds after each time for next results to load
    for click in range(1,clicks+1):
        body.send_keys(Keys.END)
        time.sleep(5)
        # keep checking for 'load more' button: div element with id=load-more
        # if its found --> click on it, wait 3 sec, keep clicking END 
        try:
            loadElem = startBrowser.find_element_by_css_selector('div[id="load-more"]')
            loadElem.click()
            time.sleep(5)
            continue
        # if this element is NOT found then keep clicking END
        except Exception:
            continue
        
    # this will unlock one main page with ALL the gallery elements (ie. ALL gallery results)
    # get the list of these gallery elements --> 'a' element with class=image-list-link
    galleryElems = startBrowser.find_elements_by_css_selector('a[class="image-list-link"]')
    print('total number of gallery elements for',clicks,'clicks','=',len(galleryElems))
    # stop loading starting browser window now that we have our gallery elements
    print('Stopping starting browser window, launching output browser windows')
    startBrowser.minimize_window()
    startBrowser.execute_script('window.stop();')
    time.sleep(5)
    
    return galleryElems


def getGalleryURL(galleryElems,startGalleryIndex,finalGalleryIndex,directory,search,
                  outBrowser,threadNumber):
    """
    Using output browser window tries to sequentially visit gallery URLs obtained
        from a group of gallery elements (start to final index)
    If the visit fails (cannot get URL, except clause) add one to failure counter
    If the visit succeeds (else clause) see if timeout occurs during page loading
        - timeout set at 'timeout_value' seconds for each output browser (default 10 seconds)
        - if timeout add one to timeouts counter
        - otherwise add one to nontimeouts counter
        - in both cases then call downloadImages to begin downloading from gallery page
    """
    for galleryIndex in range(startGalleryIndex,finalGalleryIndex+1):
        # FULL URL of gallery is found in value of 'href' attribute of the gallery element
        try:
            galleryURL = galleryElems[galleryIndex].get_attribute('href')
        except:
            print('failed to find gallery URL with thread %s' % threadNumber)
            global failures
            failures += 1
            continue
        else:
            try:
                # try to visit the gallery URL with the browser 
                outBrowser.get(galleryURL)
            except (TimeoutException,TimeoutError,CE):
                # timeout after 'timeout_value' seconds (default 10 seconds)
                print('timeout gallery URL %s with thread %s' % (galleryURL,threadNumber))
                global timeouts
                timeouts += 1
                outBrowser.execute_script("window.stop();")
                # start downloading images from gallery
                downloadImages(directory,search,outBrowser,threadNumber)
            else:
                # loaded gallery page in under 'timeout_value' seconds
                print('non-timeout gallery URL %s with thread %s' % (galleryURL,threadNumber))
                global nontimeouts
                nontimeouts += 1
                time.sleep(5)
                # start downloading images from gallery
                downloadImages(directory,search,outBrowser,threadNumber)
                
                
def downloadImages(directory,search,outBrowser,threadNumber):
    """
    Attempts to download all images (based on image elements) from a gallery
       in an output browser window
    """
    # get all image elements on current gallery page
    imgElems = outBrowser.find_elements_by_css_selector('img')

    for imgElem in imgElems:
        # URL of image is found in value of 'src' attribute of the img element
        imgURL = imgElem.get_attribute('src')
    
        # Check if the URL of the image exists using requests module
        res = requests.get(imgURL)
        if res.status_code != 200: 
            # if this image link cannot be found...
            # --> skip this image and go to the next element (back to top of imgElems loop)
            continue
        else:
            # If image URL successfully found...
            # --> Create file object to which you can write (save) this image
            # Announce trying to download the image.
            #print('Downloading image at %s with thread %s' % (imgURL,threadNumber))
            # Create file object to which you can write (save) this image
            # remove any possible extra characters in the filename located AFTER the extension
            imageFile = open(os.path.join(directory + '\\' + 'imgur\\' +search + '\\'
                                          +str(datetime.datetime.now())[:10],
                                          os.path.basename(imgURL[:imgURL.rfind('.')+4])), 'wb')
            # Write (save) the image to the binary file
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            # Then close the binary file
            imageFile.close()


def multiThreader(galleryElems,directory,search,numThreads,timeout_value):
    """
    Sets up output browser windows based on number indicated by user (1-4)
    Each output browser window is a separate thread
    Each output browser window is assigned a group of galleries to visit
    """
    
    # lists to hold download threads, output browsers and thread numbers
    downloadThreads = []
    outBrowsers = []
    threadNumbers = [i for i in range(1,numThreads+1)]
    
    # downloading performed through 1-4 simultaneous browser windows
    for num in range(numThreads):
        outBrowser = webdriver.Firefox(executable_path = webdriver_path)
        # timeout value in seconds for page loading from user (default 10 seconds)
        outBrowser.set_page_load_timeout(timeout_value)
        outBrowser.minimize_window()
        outBrowsers.append(outBrowser)
    # 6 seconds to allow all output browsers to load default window, customizable
    time.sleep(6)
    
    # divide total number of gallery elements by numThreads and discard the remainder
    galleryChunk = len(galleryElems)//numThreads

    # one thread per output browser window, each has a group of galleries to visit
    for i,j,k in zip(range(0,numThreads*galleryChunk,galleryChunk),
                     outBrowsers,threadNumbers):
        print('Starting thread for gallery',i,'to',i+galleryChunk-1)
        downloadThread = threading.Thread(target = getGalleryURL,
                                          args=(galleryElems,i,i + galleryChunk-1,
                                                directory,search,j,k))
        downloadThreads.append(downloadThread)
        downloadThread.start()

    # Wait for all threads to end by calling join with each thread in the list
    for downloadThread in downloadThreads:
        downloadThread.join()
    for browser in outBrowsers:
        browser.quit()

    global failures
    global timeouts
    global nontimeouts
    
    # Only print completion after ALL threads are finished
    print('Downloading images complete')
    print('failed gallery URLs: ',failures)
    print('successful gallery URLs with timeouts: ',timeouts)
    print('successful gallery URLs without timeouts: ',nontimeouts)

    failures,timeouts,nontimeouts = 0,0,0


def main():
    while True:
        info = getInfo()
        clicks = getNumClicks(info[2])
        galleryElems = getGalleryElements(clicks,info[2])
        multiThreader(galleryElems,info[0],info[1],info[3],info[4])
        info[2].quit()


if __name__ == '__main__':
    main()



    
