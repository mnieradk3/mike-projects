galvanic_cycle_analyzer.py
written in cpython 3.6

(A) Required python modules:

	(1) tkinter
	(2) os
	(3) re
	(4) math
	(5) matplotlib

(B) Overview:

	--> GUI that calculates and plots performance parameters of galvanic cycles for half-cell or battery systems
		(1) Start, End and Total Charge and Discharge times, seconds
		(2) Total Coulombic Efficiency, % (based on ratio of total discharge and charge times)
		(3) Charge and Discharge Plateau Potentials, V (based on midpoints of total charge and discharge times)
		(4) Internal Resistance based on Charge-Discharge Plateau Separation (ohm cm^2)
		(5) Internal Resistance based on Charge-Discharge IR transition (ohm cm^2)
		(6) Total Charge and Discharge Capacities per unit area, mA*h/cm^2
		(7) Total Discharge time and discharge percent above or below specified potential threshold 
	--> use to rapidly obtain and visualize performance data of galvanic cycles based on cycle set input file (E vs. time)
	--> capacity and resistance calculations are based on PLANAR electrodes (i.e. these values are scaled to squared cm)

(C) GUI structure:

    (1) Input window 
	- where user chooses input file, output directory, analysis options, etc. and inputs cycle parameters
    (2) Output table window
	- composed of a grid of entry widgets, vertically scrollable, containing cycle analysis results (if analysis successful)
    (3) Output graph window(s) (if user selected at least one graphical analysis option) 
	- each graph window has a matplotlib graph of one cycle analysis result parameter for the cycle set (eg. resistance)


(D) How to perform analysis run on a cycle set:

	(1) Enter or select input file with cycle set data into source field
		- cycle set data must be plain text (.txt) with columnar data of E (potential,V) vs. time (seconds)
		- lines inside input file that are blank or contain non-numerical info are ignored
		- see sample input files provided for examples

	(2) Enter or select directory into destination field for output files (if desired)
		- otherwise output files will be deposited into the same directory as the input file

	(3) Select cell style option 1 or 2 on the side
		- style 1: charge to discharge IR transition < 0 V, discharge to charge IR transition > 0 V
		- style 2: charge to discharge IR transition > 0 V, discharge to charge IR transition < 0 V
		- if the selected cell style is the opposite of the actual style of your cycles the analysis will fail !
		- see sample cell style files provided for examples

	(4) Enter charge/discharge current of cycle set in uA (microamps) > 0

	(5) Enter approximate value of instantaneous charge to discharge IR transition
		- corresponds to instantaneous potential change from end of charging in a cycle
		  to the start of discharging of the SAME cycle
		- sign of this value MUST be based on the cell style option that was selected
		- the absolute value of this approximation MUST be valid for ALL cycles in the set from the input file
			--> i.e. it MUST be sufficiently larger than the charge-discharge IR transition of ALL your cycles
			--> otherwise the cycle analysis will fail
		- this IR transition approximation is determined externally by YOU BEFORE trying to run the analysis

	(6) Enter approximate value of instantaneous discharge to charge IR transition
		- corresponds to instantaneous potential change from end of discharging of current cycle
		  to start of charging for NEXT cycle
		- sign of this value must be based on the cell style option that was selected
		- i.e. it will be the opposite sign of the approximation given for charge-discharge transition (#5)
		- the absolute value of this approximation MUST be valid for ALL cycles in the set from the input file
			--> i.e. it MUST be sufficiently larger than the discharge-charge IR transition of ALL your cycles
			--> otherwise the cycle analysis will fail
		- this IR transition approximation is determined externally by YOU BEFORE trying to run the analysis

	(7) Enter charge/discharge time per cycle in seconds > 0
		- this is the designated charge/discharge time you put into your electrochem software during your cycling experiment
		- eg. 1000 seconds
		- NOT the actual charge/discharge times of each cycle, those values will be computed by my program

	(8) Enter the number of cycles in the set > 0

	(9) Enter the planar anode-cathode contact area in squared cm > 0
		- in a half-cell this would be the cross-sectional area of a single electrode exposed to electrolyte
		- in a battery this would be the cross-sectional area of electrodes exposed to electrolyte,
		  which is likely to be the same value for both electrodes (eg. 1.54 cm^2 for anode and cathode each in my experiments)

	(10) Enter discharge potential threshold if desired (default = +2V)
		- in cell style option 1 this value will be used to determine percent of discharge ABOVE the threshold
		- in cell style option 2 this value will be used to determine percent of discharge BELOW the threshold
		- specified value MUST be within the potential range of the discharge portion of your cycles
		- otherwise a value of zero will be computed for the discharge percent above/below threshold

	(11) Select any graphical analysis options if desired
		- each option selected will open up a separate graph when the analysis is run

	(12) Select one of the output options
		- if option 2 or 3 selected the output files will go into the destination directory (if specified)

	(13) Click 'Analyze' button
		- if analysis method is successful a message box will pop up and output windows will appear
		
(E) Other Important Notes:

    - If the input cycle set has very unstable charge/discharge potential responses with potential jump magnitudes
      similar to the given IR transition approximations the analysis will fail or give wrong values !
    - cycle parameters described in steps 3 to 9 above for the input window MUST be ALL determined externally
      by YOU before trying to run this analysis program
    - cycle set input file must begin within the charging portion of a cycle and end within the discharging portion of a cycle
    - when opening output text file (output options 2/3 selected) in excel increase column width to size 20 to clearly see header fields !


(F) Possible additional features and things to add/change/fix:

    (1) Refactor most/all graphing methods to reduce code space
    (2) Allow different units of time (minutes, hours, etc.) for charge/discharge time input
    (3) Fix discharge percent above/below threshold calculation so values outside the discharge potential range are possible
    (4) Make output table horizontally scrollable to fit in all analysis results values
    (5) Allow options for gravimetric (per unit mass) and volumetric (per unit volume) calculations for resistance and capacities
    (6) Use 'pandas' module to also output statistics (mean, STD, min, max, etc.) of cycle analysis results (as a DataFrame)
    (6) Program could be customized based on input files that contain additional experimental info
	- therefore requiring less user input and approximations into the input window
        - the only useful info in MY cycle input files was E vs. time columnar data so that is how I structured the program


