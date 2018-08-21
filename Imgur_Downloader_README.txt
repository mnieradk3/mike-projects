Imgur_Downloader.py
written in cpython 3.6

(A) Required python modules:

	(1) os
	(2) sys
	(3) time
	(4) threading
	(5) datetime
	(6) requests
	(7) selenium (and geckodriver.exe for mozilla firefox)

(B) Overview:

	- downloads all images from all galleries from imgur.com 
          based on specified search term, output folder directory, etc.
	- performed through selenium module webdriver (geckodriver) controlling Firefox browser
 		--> this allows automated up/down scrolling of the webpage by the script
    		--> and to allow clicking of 'load more' button to load more galleries
    		--> required to unlock ALL gallery elements from a single search term
		--> this starting browser MUST be left maximized during this process but you can
		    switch focus to work in other windows
        with no mouse+keyboard input !
	- gallery elements are then fed to 1-3 output browser windows
	  through multithreading, each output browser window = one thread
    		--> each browser window visits a group of galleries sequentially
	        --> image elements are obtained by selenium from the gallery
    		--> requests module is then used to obtain the HTML string
        	    (image file) from the image URL
	        --> image is then downloaded, repeat for all image elements in gallery
		--> these output browsers are minimized, you can continue work elsewhere while
	            they are visiting galleries and downloading
	- designated time delays throughout script are based on testing with my broadband cable internet
		--> if your connection is very slow (due to hardware or lag or other reasons)
	            the time delays will have to be set higher throughout the script
	- if running with 3 output windows it is recommended to set a high timeout
	  value in seconds (>10), and to NOT also run any other internet-related applications

(C) How to use:

	(1) Place the full path of your selenium firefox geckodriver into the script
		--> located in string immediately below import statements

	(2) Run Script
	
	(3) Enter search term or 'exit' to exit program
	
	(4) Enter full valid path of folder where you want to save subfolder of downloaded images
		--> if folder does not exist it will be created

	(5) Enter number (1-4) of output browser windows you want to use to visit galleries
		--> if none given defaults to 1 window

	(6) Enter number in seconds for timeout value for output browser windows
		--> maximum loading time allowed for an output browser window before it is stopped
		--> if none given defaults to 10 seconds

	(7) Starting browser will load into imgur URL according to search term
		--> this window will keep automatically scrolling down until ALL galleries are unlocked
		--> this window MUST be left maximized AND in focus with no mouse+keyboard input !

	(8) Designated number of output (downloading) browsers will then load and minimize
		--> each will visit a group of galleries from the total number, and download their images
		--> the progress of each thread will be printed to the standard output stream (console)
		--> you can continue work elsewhere in other programs/windows during these download processes

	
(D) Possible additional features and things to add/change/fix:

	(1) Allow customizable amount of end clicks to unlock groups of gallery results
		--> currently, unless the 'clicks' variable is modified in the 'getNumClicks' variable
		    of the script,the program will keep scrolling until ALL galleries are unlocked
	(2) Allow more than 3 output browser windows
		--> for better internet connections that can handle it
		--> requires better exception handling for connectivity issues that begin to appear 

		

