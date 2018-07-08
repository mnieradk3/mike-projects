sciCalc.py
written in python 3.6
Calculator GUI that mimics most buttons/functions of windows 7 calculator
    --> basic math, memory recall/store, clear, trigonometry, roots, logarithms, etc.
    --> single step functions (eg. x^2, sin x) work in traditional 'backwards' calculator mode
    --> ie. the value to be sent to the function is input by the user BEFORE the function button is selected
    --> single step functions when executed produce the result (if valid) immediately inside input field
    --> multi step functions (eg. x ^ y, x root y) are handled in general through 'compute' function by BEDMAS
    --> invalid input/output within exception handlers triggers error-type messageboxes

GUI structure:
    --> toggle between standard (default) and scientific mode using menu or through keyboard shortcuts (alt+1,alt+2)
    --> Tk widget (top-level GUI application) 
    --> Window frame widget (subclass of Frame) packed into Tk widget
    --> buttons, menu and four entry field widgets (input, operations, parantheses, memory) 
        placed into window frame widget


Additional features and things to add/change:
    --> limit number of text characters to input and operations fields to not exceed maximum set width
    --> add more memory options: MC, M+, M-
    --> add hyperbolic trigonometry buttons and functions
    --> add radio button with degrees/radians/gradians options for computation with trig functions
    --> improve design and look of the GUI, eg. button images instead of plain text
    --> overall test the program more comprehensively 
            --> advanced input expressions containing many different functions !
            --> outlier cases such as extremely small values, large values, infinities