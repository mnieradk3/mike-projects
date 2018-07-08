'''
python 3
sciCalc.py
Calculator that mimics most buttons/functions of windows calculator
    --> basic math, memory recall/store, clear, trigonometry, roots, logarithms, etc.
Can toggle GUI between standard (default) and scientific mode using menu or through keyboard shortcuts
GUI structure: (1) Tk widget (top-level GUI application), (2) window frame widget (class) packed into Tk widget
               (3) buttons, menu and four entry field widgets placed into window frame widget
'''

import tkinter as tk
from tkinter import messagebox
import math
import fractions

# for copying/pasting to/from windows clipboard
import pyperclip


# variable to hold current memory value from input entry field
# initialized to None
mem = None

# variable to hold current amount of unclosed left brackets
# initialized to 0
num_brackets = 0

# variable to hold truth value of recent computation performed
# computations are roots, powers, =, factorial, trig, etc.
# if recent computation status is True:
#   --> decimal or number insertion into input field will
#       first clear the input field contents
# if recent computation status is False:
#   --> decimal or number insertion into input field will
#       place values after existing input field contents
# initialized to False
eq = False


class Window(tk.Frame):
    """
    GUI window frame widget as subclass of Frame class from tkinter module
    """
    def __init__(self, master):
        """
        Window frame widget constructor
        """
        # call Frame superclass constructor with Tk widget as master
        tk.Frame.__init__(self, master)
        # assign Tk widget as instance attribute
        self.master = master
        self.init_window()
    
    def init_window(self):
        """
        Method that implements the remaining widgets of the calculator GUI
        """
        # set the title of our master (Tk widget)      
        self.master.title("Calculator")

        # pack the window frame widget (self) into the full space of the Tk widget
        self.pack(fill = tk.BOTH, expand = True)

        # instance of Menu class as the 'main' menu widget, with Tk widget as its master
        mainMenu = tk.Menu(self.master)
        # bind this main menu instance as the menu for the master Tk widget
        self.master.config(menu = mainMenu)

        # input (lower) field where input numbers will appear, disabled state
        self.inputField = tk.Entry(self, width = 25, state = 'disabled',
                                   font = ('Calibri',12), disabledbackground = 'white')                 
        self.inputField.place(x = 25, y = 32)

        # operation (upper) field where operations with input will appear, disabled state
        # scrolls right when input exceeds width of field
        self.opField = tk.Entry(self, width = 25, state = 'disabled',
                                font = ('Calibri', 12), disabledbackground = 'white')
        self.opField.place(x = 25, y = 2)

        # memory field where current memory value (if present) will appear, disabled state
        self.memField = tk.Entry(self, width = 2, state = 'disabled',
                                font = ('Calibri', 12), disabledbackground = 'white')
        self.memField.place(x = 0, y = 15)

        # 'view' menu option as instance of Menu class
        view = tk.Menu(mainMenu)

        # add two commands to the 'view' menu option
        # standard (Alt + 1), scientific (Alt + 2)
        # switches calculator layout between modes
        # command handled by modeSwitch method
        view.add_command(label = 'Standard', command = lambda: self.modeSwitch('ST'),
                         accelerator = 'Alt+1')
        view.add_command(label = 'Scientific', command = lambda: self.modeSwitch('SC'),
                         accelerator = 'Alt+2')
        # add keyboard shortcuts for both commands
        self.bind_all('<Alt-Key-1>',lambda event: self.modeSwitch('ST'))
        self.bind_all('<Alt-Key-2>',lambda event: self.modeSwitch('SC'))
        
        # add a third command to the 'view' menu option, with text 'exit'
        # command handled by client_exit event method
        view.add_command(label="Exit", command=self.client_exit, accelerator = 'Ctrl+Q')
        # add CTRL+Q keyboard shortcut for exit command
        self.bind_all('<Control-Key-q>',lambda event: self.client_exit())

        # add the 'view' menu option to the 'main' menu widget, cascade style
        mainMenu.add_cascade(label="View", menu=view)

        # 'edit' menu option as instance of Menu class
        edit = tk.Menu(mainMenu)

        # add two commands to the 'edit' menu option: copy and paste
        # commands handled by copy and paste event methods
        edit.add_command(label = 'Copy', command = self.copy, accelerator = "Ctrl+C")
        edit.add_command(label = 'Paste', command = self.paste, accelerator = "Ctrl+V")
        # add keyboard shortcuts for copy (CTRL+C) and paste (CTRL+V)
        self.bind_all('<Control-Key-c>',lambda event: self.copy())
        self.bind_all('<Control-Key-v>',lambda event: self.paste())

        # add the 'edit' menu option to the 'main' menu widget, cascade style
        mainMenu.add_cascade(label="Edit", menu=edit)

        # add standard clear (C) button, handled by clear event method
        clearButton = tk.Button(self, font = 16, height = 2,
                                width = 5, background = 'white',
                                text = 'C', command = self.clear)
        clearButton.place(x = 180, y = 60)

        # add ESCAPE keyboard shortcut for clear command
        self.bind_all('<Key-Escape>', lambda event: self.clear())

        # add delete button (<--)
        # deletes single characters from input field
        # command handled by delete event method
        delButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '←', background = 'white', command = self.delete)
        delButton.place(x = 120, y = 60)

        # add BACKSPACE keyboard shortcut for delete command
        self.bind_all('<BackSpace>', lambda event: self.delete())

        # add standard number buttons 0-9 and decimal button, handled by insert event methods
        decButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '.', background = 'white', command = self.decInsert)
        decButton.place(x = 120, y = 300)
        zeroButton = tk.Button(self, font = 16, height = 2, width = 12,
                               text = '0', background = 'white', command = self.zeroInsert)
        zeroButton.place(x = 0, y = 300)
        oneButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '1', background = 'white', command = lambda: self.oneToNineInsert(1))
        oneButton.place(x = 0, y = 240)
        twoButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '2', background = 'white', command = lambda: self.oneToNineInsert(2))
        twoButton.place(x = 60, y = 240)
        threeButton = tk.Button(self, font = 16, height = 2, width = 5,
                                text = '3', background = 'white', command = lambda: self.oneToNineInsert(3))
        threeButton.place(x = 120, y = 240)
        fourButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '4', background = 'white', command = lambda: self.oneToNineInsert(4))
        fourButton.place(x = 0, y = 180)
        fiveButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '5', background = 'white', command = lambda: self.oneToNineInsert(5))
        fiveButton.place(x = 60, y = 180)
        sixButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '6', background = 'white', command = lambda: self.oneToNineInsert(6))
        sixButton.place(x = 120, y = 180)
        sevenButton = tk.Button(self, font = 16, height = 2, width = 5,
                                text = '7', background = 'white', command = lambda: self.oneToNineInsert(7))
        sevenButton.place(x = 0, y = 120)
        eightButton = tk.Button(self, font = 16, height = 2, width = 5,
                                text = '8', background = 'white', command = lambda: self.oneToNineInsert(8))
        eightButton.place(x = 60, y = 120)
        nineButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '9', background = 'white', command = lambda: self.oneToNineInsert(9))
        nineButton.place(x = 120, y = 120)

        # add keyboard shortcuts for decimal and number presses
        self.bind_all('<Key-.>', lambda event: self.decInsert())
        self.bind_all('<Key-0>', lambda event: self.zeroInsert())
        self.bind_all('<Key-1>', lambda event: self.oneToNineInsert(1))
        self.bind_all('<Key-2>', lambda event: self.oneToNineInsert(2))
        self.bind_all('<Key-3>', lambda event: self.oneToNineInsert(3))
        self.bind_all('<Key-4>', lambda event: self.oneToNineInsert(4))
        self.bind_all('<Key-5>', lambda event: self.oneToNineInsert(5))
        self.bind_all('<Key-6>', lambda event: self.oneToNineInsert(6))
        self.bind_all('<Key-7>', lambda event: self.oneToNineInsert(7))
        self.bind_all('<Key-8>', lambda event: self.oneToNineInsert(8))
        self.bind_all('<Key-9>', lambda event: self.oneToNineInsert(9))
               
        # add standard sign, +, -, *, /, =, reciprocal, sqrt operation buttons
        # commands handled by sign, math, compute, recip, sqrt event methods
        signButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '±', background = 'white',
                               command = self.sign)
        signButton.place(x = 180, y = 120)
        addButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '+', background = 'white',
                              command = lambda: self.math(' + '))
        addButton.place(x = 180, y = 180)
        subButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '-', background = 'white',
                              command = lambda: self.math(' - '))
        subButton.place(x = 180, y = 240)
        mulButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '*', background = 'white',
                              command = lambda: self.math(' * '))
        mulButton.place(x = 180, y = 300)
        divButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '/', background = 'white',
                              command = lambda: self.math(' / '))
        divButton.place(x = 180, y = 360)
        eqButton = tk.Button(self, font = 16, height = 2, width = 5,
                             text = '=', background = 'white',
                             command = self.compute)
        eqButton.place(x = 120, y = 360)
        recButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = '1/x', background = 'white',
                              command = self.recip)
        recButton.place(x = 60, y = 360)
        sqrtButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '√', background = 'white',
                               command = self.sqrt)
        sqrtButton.place(x = 0, y = 360)
        
        # add keyboard shortcuts for +,-, *, /, = operation presses
        self.bind_all('<Key-plus>', lambda event: self.math(' + '))
        self.bind_all('<Key-minus>', lambda event: self.math(' - '))
        self.bind_all('<Key-asterisk>', lambda event: self.math(' * '))
        self.bind_all('<Key-slash>', lambda event: self.math(' / '))
        self.bind_all('<Key-equal>', lambda event: self.compute())
        self.bind_all('<Key-Return>', lambda event: self.compute())

        # add standard MS (memory store) and MR (memory recall) buttons
        # commands handled by memRecall and memStore event methods
        mrButton = tk.Button(self, font = 16, height = 2, width = 5,
                             text = 'MR', background = 'white', command = self.memRecall)
        mrButton.place(x = 0, y = 60)
        msButton = tk.Button(self, font = 16, height = 2, width = 5,
                             text = 'MS', background = 'white', command = self.memStore)
        msButton.place(x = 60, y = 60)

        # add entry field near parantheses buttons
        # current number of unclosed left brackets will be displayed here
        self.paraField = tk.Entry(self, width = 5, state = 'disabled',
                                   font = ('Calibri',14), disabledbackground = 'white')
        self.paraField.place(x = 360, y = 75)
        
        # add scientific mode buttons: parantheses, exponentials, logarithms, etc.
        # commands handled by para, math, xpow, log, etc. event methods
        paraButtonL = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '(', background = 'white',
                               command = lambda: self.paraInsert('left'))
        paraButtonL.place(x = 240, y = 60)                        
        paraButtonR = tk.Button(self, font = 16, height = 2, width = 5,
                               text = ')', background = 'white',
                               command = lambda: self.paraInsert('right'))
        paraButtonR.place(x = 300, y = 60)
        # x^2
        xsqButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = 'x\u00b2', background = 'white',
                              command = lambda: self.xpow(2))
        xsqButton.place(x = 240, y = 120)
        # x^3
        xcubeButton = tk.Button(self, font = 16, height = 2, width = 5,
                                text = 'x\u00b3', background = 'white',
                                command = lambda: self.xpow(3))
        xcubeButton.place(x = 240, y = 180)
        # x^y
        xtoyButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = 'x\u02b8', background = 'white',
                               command = lambda: self.math(' ^ '))
        xtoyButton.place(x = 240, y = 240)
        # log base 10
        logButton = tk.Button(self, font = 16, height = 2, width = 5,
                              text = 'log', background = 'white',
                              command = lambda: self.log(10))
        logButton.place(x = 240, y = 300)
        # log base e
        lnButton = tk.Button(self, font = 16, height = 2, width = 5,
                             text = 'ln', background = 'white',
                             command = lambda: self.log(math.e))
        lnButton.place(x = 240, y = 360)
        # n!
        factoButton = tk.Button(self, font = 16, height = 2, width = 5,
                             text = 'n!', background = 'white',
                             command = self.facto)
        factoButton.place(x = 300, y = 120)
        # x^(1/3)
        cubeRootButton = tk.Button(self, font = ('calibri',12), height = 2, width = 6,
                               text = '\u221b', background = 'white',
                               command = self.cubeRoot)
        cubeRootButton.place(x = 300, y = 180)
        # x root y
        nthRootButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '\u02b8√', background = 'white',
                               command = lambda: self.math(' root '))
        nthRootButton.place(x = 300, y = 240)
        # 10^x
        tentoxButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '10\N{MODIFIER LETTER SMALL X}',
                               background = 'white', command = lambda: self.baseToX(10))
        tentoxButton.place(x = 300, y = 300)
        # e^x
        etoxButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = 'e\N{MODIFIER LETTER SMALL X}',
                               background = 'white', command = lambda: self.baseToX(math.e))
        etoxButton.place(x = 300, y = 360)
        sinButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = 'sin', background = 'white',
                              command = lambda: self.trig('sin'))
        sinButton.place(x = 360, y = 120)
        cosButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = 'cos', background = 'white',
                              command = lambda: self.trig('cos'))
        cosButton.place(x = 360, y = 180)
        tanButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = 'tan', background = 'white',
                              command = lambda: self.trig('tan'))
        tanButton.place(x = 360, y = 240)
        # exponential (scientific notation) conversion
        expButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = 'exp', background = 'white',
                               command = self.exp)
        expButton.place(x = 360, y = 300)
        piButton = tk.Button(self, font = 16, height = 2, width = 5,
                               text = '\u03C0', background = 'white',
                               command = self.pi)
        piButton.place(x = 360, y = 360)

        # add keyboard shortcuts for '(' and ')' button presses
        self.bind_all('<(>', lambda event: self.paraInsert('left'))
        self.bind_all('<)>', lambda event: self.paraInsert('right'))

     
    # Standard mode button and keyboard event methods begin here

    def copy(self):
        """
        Method to handle 'copy' menu event
        Copies current contents of input field to windows clipboard
        """
        copyString = pyperclip.copy(self.inputField.get())
        
    
    def paste(self):
        """
        Method to handle 'paste' menu event
        Gets current content of windows clipboard as string
        Inspects this string see if it ONLY contains numbers and leading sign
           ie. if it can be converted to float
        Raises ValueError if string contains non-e letters or operations (trailing signs)
        If successful then paste this string into input field
        """
        pasteString = pyperclip.paste()
        if pasteString:
            try:
                float_paste = float(pasteString)
            except ValueError:
                messagebox.showerror('Invalid input',
                                    'Cannot paste string with letters or operations')
            else:                                     
                self.inputField.config(state = 'normal')
                if self.inputField.get():
                    # delete input field contents first if present
                    self.inputField.delete(0,tk.END)
                # insert the clipboard string into input field
                self.inputField.insert(tk.INSERT,pasteString)
                self.inputField.config(state = 'disabled')


    def modeSwitch(self, mode):
        """
        Method to handle calculator mode switch event
           either through keyboard shortcut or menu option
        Switching to scientific mode expands GUI Window
        This reveals scientific mode buttons, clears all fields
           and also expands the width of both entry fields
        """
        if mode == 'ST':
            self.clear()
            self.master.geometry('235x450')
            self.inputField.config(width = 25)
            self.opField.config(width = 25)
        elif mode == 'SC':
            self.clear()
            self.master.geometry('430x450')
            self.inputField.config(width = 48)
            self.opField.config(width = 48)
    
    
    def client_exit(self):
        """
        Method to handle menu option event 'file' --> 'exit'
        Exits the GUI application
        """
        exit()

    
    def clear(self):
        """
        Method to handle clear (C) button event
           or when handling invalid input/output exceptions
        Clears input, operation and parantheses fields
           and resets number of unclocked parantheses to zero
        """
        self.inputField.config(state = 'normal')
        self.opField.config(state = 'normal')
        self.paraField.config(state = 'normal')
        self.inputField.delete(0,tk.END)
        self.opField.delete(0,tk.END)
        self.paraField.delete(0,tk.END)
        self.inputField.config(state = 'disabled')
        self.opField.config(state = 'disabled')
        self.paraField.config(state = 'disabled')
        global num_brackets
        num_brackets = 0


    def delete(self):
        """
        Method to handle delete (<--) button event
        Deletes character from input field
        """
        s_in = self.inputField.get()
        if s_in:
            self.inputField.config(state = 'normal')
            # check if current input field contents are NOT from a recent computation result
            if not eq:
                if 'e' in s_in:
                    # if exponent of power of e is double digit or larger delete last digit
                    if len(s_in[s_in.index('e')+2:]) >= 2:
                        self.inputField.delete(len(s_in)-1)
                    # elif exponent of power of e is single non-zero digit change it to zero
                    elif (len(s_in[s_in.index('e')+2:]) == 1
                          and s_in[s_in.index('e')+2] != '0'):
                          self.inputField.delete(0,tk.END)
                          self.inputField.insert(tk.INSERT,s_in[:s_in.index('e')+2] + '0')
                    # elif exponent of power of e is zero then delete entire exponential portion
                    else:
                        self.inputField.delete(0,tk.END)
                        self.inputField.insert(tk.INSERT,s_in[:s_in.index('e')])
                else:
                    self.inputField.delete(len(s_in)-1)
            self.inputField.config(state = 'disabled')

    
    def decInsert(self):
        """
        Method to handle '.' button event
        Inserts decimal into input field
        """
        s_in = self.inputField.get()
        # only allow decimal to be placed under one of two conditions
        # (1) the recent computation status is True
        # (2) or there is no decimal present inside input field AND the input field
        #     is NOT in exponential form
        global eq
        if eq or ('.' not in s_in and 'e' not in s_in):
            self.inputField.config(state = 'normal')
            # if recent computation then clear input field before inserting decimal
            if eq:
                self.inputField.delete(0,tk.END)
                self.inputField.insert(tk.INSERT,'0.')    
            elif s_in == '': self.inputField.insert(tk.INSERT,'0.')
            else: self.inputField.insert(tk.INSERT,'.')
            self.inputField.config(state = 'disabled')
            # change recent computation status to False
            eq = False
        
  
    def zeroInsert(self):
        """
        Method to handle '0' button event
        Inserts zero into input field
        """
        self.inputField.config(state = 'normal')
        s_in = self.inputField.get()
        global eq
        if eq:
            # if recent computation then clear input field before inserting 0
            self.inputField.delete(0,tk.END)
            self.inputField.insert(tk.INSERT,'0')
            eq = False
        else:
            # allow zero insertion into power of e if leading zero NOT present
            if 'e' in s_in and s_in[s_in.index('e')+2] != '0':
                self.inputField.insert(tk.INSERT,'0')
            elif 'e' not in s_in:
                # otherwise allow zero to be placed under one of these conditions:
                # (1) if a decimal is present inside input field
                # (2) or the input field is empty
                # (3) or the input field contains a leading non-zero
                if '.' in s_in or s_in == '' or (s_in!= '' and s_in[0] != '0'):
                    self.inputField.insert(tk.INSERT,'0')
        self.inputField.config(state = 'disabled')

        
    def oneToNineInsert(self, num):
        """
        Method to handle '1-9' button events
        Inserts designated number into input field
        """
        self.inputField.config(state = 'normal')
        s_in = self.inputField.get()
        global eq
        if eq:
            # if recent computation then clear input field before inserting number
            self.inputField.delete(0,tk.END)
            eq = False
        # if exponential form with leading zero in power of e, replace zero with number
        if 'e' in s_in and s_in[s_in.index('e')+2] == '0':
            s_new = s_in[:s_in.index('e')+2] + str(num)
            self.inputField.delete(0,tk.END)
            self.inputField.insert(tk.INSERT,s_new)
        # otherwise place number at end
        else:
            self.inputField.insert(tk.INSERT,str(num))
        #self.inputField.config(state = 'disabled')
        
    
    def math(self, op):
        """
        Method to handle +, -, *, /, ^ button events
        Transfers the current input field contents and specified
           math operation (op) into the operation field
        This method does NOT handle the actual result computation
        Computation is instead handled by 'compute' method
        """
        s_in = self.inputField.get()
        s_op = self.opField.get()
        self.inputField.config(state = 'normal')
        self.opField.config(state = 'normal')
        global eq
        # Allow for operator sign insertion under one of these conditions:
        # (1) Input field non-empty and operations field NOT ending with ')'
        # (2) Input field empty and operations field ending with ')'
        if s_in and not s_op.endswith(') '):
            # check for trailing decimal on current input field
            if s_in.endswith('.'):
                self.opField.insert(tk.INSERT,s_in[:-1] + op)
            else:
                self.opField.insert(tk.INSERT,s_in + op)
            self.inputField.delete(0,tk.END)
            # change recent computation status to False
            eq = False
        elif not s_in and s_op.endswith(') '):
            self.opField.insert(tk.INSERT,op)
            # change recent computation status to False
            eq = False
        self.inputField.config(state = 'disabled')
        self.opField.config(state = 'disabled') 
        

    def sign(self):
        """
        Method to handle '±' button event
        Changes the sign of current input field contents
        """
        s_in = self.inputField.get()
        if s_in:
            # change sign of power of e
            if 'e' in s_in:
                sign_index = s_in.index('e')+1
                if s_in[sign_index] == '-':
                    s_new = (s_in[:sign_index] + '+' +
                             s_in[sign_index + 1:])
                else:
                    s_new = (s_in[:sign_index] + '-' +
                             s_in[sign_index + 1:])
            # change sign of coefficient in front of power of e
            elif '-' in s_in:
                s_new = s_in[1:]
            else:
                s_new = '-' + s_in
            self.inputField.config(state = 'normal')
            self.inputField.delete(0,tk.END)
            self.inputField.insert(tk.INSERT,s_new)
            self.inputField.config(state = 'disabled')
            

    def list_rfind(self, L, item):
        """
        Custom method to reverse index a list for specific item
        Used for finding indices of brackets in compute method below
        """
        for i in range(len(L)-1,-1,-1):
            if L[i] == item:
                return i
        else:
            return None

            
    def compute(self):
        """
        Method to handle '=' button event
        Gathers values and operations from operations field
             as well as any remaining value from input field
        Parses all values as Fraction objects to maintain precision
        Computes the result according to BEDMAS
        Raises ZeroDivisionError if a step involves dividing by zero
            or ValueError if even root of negative value,
            or OverflowError if computed result is too large to show    
        Successful result is sent to input field and para + operation
            fields are cleared
        """
        s_in = self.inputField.get()
        s_op = self.opField.get()
        # check for trailing operation strings or left bracket
        # remove them from operation field if the input field is empty
        # else add input field contents to operation field
        if (s_op.endswith(('+ ','- ','* ','/ ','^ ','root ','( '))
            and not s_in):
            s_op = s_op[:-3]
        elif s_in:
            s_op += s_in

        # Add leading left bracket to op string (for computing by BEDMAS)
        s_op = ' ( ' + s_op
        
        # Add right brackets until they match the number of left brackets
        while s_op.count('(') > s_op.count(')'):
            s_op += ' ) '
           
        L_op = s_op.split()
        # determine amount of operations in resulting list (excluding brackets)
        num_ops = sum([i.endswith(('+','-','*','/','^','root')) for i in L_op])
        # try to parse the values of list
        # neg/pos int and float strings are converted to Fraction objects
        #   --> will raise OverflowError if resulting numerator is too large
        # operation and bracket strings are unchanged
        try: 
            for i in range(len(L_op)):
                if ('.' in L_op[i] or L_op[i].isdigit()
                    or (len(L_op[i]) >= 2 and L_op[i] != 'root')):
                    L_op[i] = fractions.Fraction.from_float(float(L_op[i]))
        except OverflowError:
            messagebox.showerror('Overflow',
                                 'Infinite numerator in conversion to fraction')
        else:
            # determine amount of values in resulting list
            num_vals = sum([type(i) == type(fractions.Fraction(1)) for i in L_op])
            
            # Only try to compute result if there are at least 2 values
            #     and 1 operation in L_op
            if num_vals >= 2 and num_ops >= 1:
                try:
                    # try computing according to BEDMAS
                    
                    while '(' in L_op and (L_op.count('(') + L_op.count(')') < len(L_op)):
                        # get last left bracket and its corresponding right bracket indices
                        lb_ind = self.list_rfind(L_op,'(')
                        rb_ind = L_op.index(')',lb_ind+1)
                        # get sub-list M_op of values and operands within these brackets
                        M_op = L_op[lb_ind+1:rb_ind]
                        
                        while 'root' in M_op:
                            # convert root operations to equivalent powers (^)
                            root_ind = M_op.index('root')
                            M_op[root_ind] = '^'
                            M_op[root_ind+1] = 1/M_op[root_ind+1]
                            
                        while '^' in M_op:
                            # shorten M list by evaluating power portions
                            pow_ind = M_op.index('^')
                            # check for even roots of negative values, raise exception
                            if M_op[pow_ind-1] < 0 and M_op[pow_ind+1].denominator % 2 == 0:
                                raise ValueError
                            
                            # check for odd roots of negative values, handle negative parsing
                            elif M_op[pow_ind-1] < 0 and M_op[pow_ind+1].denominator != 1: 
                                M_op = (M_op[:pow_ind-1] + [-(-M_op[pow_ind-1])**M_op[pow_ind+1]]
                                        + M_op[pow_ind+2:])
                            # any other arrangement evaluate directly using ** expression
                            else:
                                M_op = (M_op[:pow_ind-1] + [M_op[pow_ind-1]**M_op[pow_ind+1]]
                                        + M_op[pow_ind+2:])                                
                        while '*' in M_op or '/' in M_op:
                            # shorten M list by evaluating mul or div portions as they appear
                            for j in range(1,len(M_op)-1,2):
                                if j+1 < len(M_op):
                                    if M_op[j] == '*':
                                        M_op = M_op[:j-1] + [M_op[j-1]*M_op[j+1]] + M_op[j+2:]
                                    elif M_op[j] == '/':
                                        M_op = M_op[:j-1] + [M_op[j-1]/M_op[j+1]] + M_op[j+2:]
                                    
                        # take first item of resulting M list as current sub-answer of M
                        sub_answer = M_op[0]
                        # go through remaining items in the M list
                        # add or subtract items from the current sub-answer, and update
                        for k in range(1,len(M_op)-1,2):
                            if k+1 < len(M_op):
                                if M_op[k] == '+':
                                    sub_answer += M_op[k+1]
                                elif M_op[k] == '-':
                                    sub_answer -= M_op[k+1]
                        # shorten L_op list by removing M_op list values and their surrounding brackets
                        # in their place insert the sub-answer from computation of M_op list
                        L_op = L_op[:lb_ind] + [sub_answer] + L_op[rb_ind+1:]
                    
                    # finally convert all sub-answers in L_op list to float before summation
                    L_op = list(map(float,L_op))
                    # determine final answer
                    final_answer = sum(L_op)

                except OverflowError:
                    messagebox.showerror('Overflow', 'Result is too large to display')
                    self.clear()
                except ZeroDivisionError:
                    messagebox.showerror('Invalid input', 'Cannot divide by zero')
                    self.clear()
                except ValueError:
                    messagebox.showerror('Invalid input',
                                         'Cannot take even root of negative number')
                    self.clear()                
                else:
                    # clear BOTH fields when performing '='
                    self.clear()
                    # send successful computation result to input field
                    self.inputField.config(state = 'normal')
                    self.inputField.insert(tk.INSERT, str(final_answer))
                    self.inputField.config(state = 'disabled')
                    # change recent computation status to True
                    global eq
                    eq = True

           
    def recip(self):
        """
        Method to handle '1/x' button event
        Calculates the reciprocal of x
        Raises ZeroDivisionError if x is zero
        Successful result is sent to input field
        """
        s_in = self.inputField.get()
        if s_in:
            try:
                result = 1/float(s_in)
            except ZeroDivisionError:
                messagebox.showerror('Invalid input',
                                     'Cannot divide by zero')
                self.clear()
            else:
                self.inputField.config(state = 'normal')
                self.inputField.delete(0,tk.END)
                self.inputField.insert(tk.INSERT,str(result))
                self.inputField.config(state = 'disabled')
                # change recent computation status to True
                global eq
                eq = True       

    
    def sqrt(self):
        """
        Method to handle square root button event
        Calculates the square root of x with math.sqrt(x)
        Raises ValueError if x is negative
        Successful result is sent to input field
        """
        s_in = self.inputField.get()
        if s_in:
            try:
                result = math.sqrt(float(s_in))
            except ValueError:
                messagebox.showerror('Invalid input',
                                     'Cannot calculate square root of negative value')
                self.clear()
            else:
                self.inputField.config(state = 'normal')
                self.inputField.delete(0,tk.END)
                self.inputField.insert(tk.INSERT,str(result))
                self.inputField.config(state = 'disabled')
                # change recent computation status to True
                global eq
                eq = True

            
    def memStore(self):
        """
        Method to handle 'MS' button event
        Takes current input field contents (if present)
        and stores it in global mem variable
        Writes 'M' to memField
        """
        global mem
        if self.inputField.get():
            mem = self.inputField.get()
            self.memField.config(state = 'normal')
            self.memField.insert(tk.INSERT,'M')
            self.memField.config(state = 'disabled')
            

    def memRecall(self):
        """
        Method to handle 'MR' button event
        Takes current value from globel mem variable
        and inserts it into input field
        """
        if mem:
            self.inputField.config(state = 'normal')
            self.inputField.delete(0,tk.END)
            self.inputField.insert(tk.INSERT,mem)
            self.inputField.config(state = 'disabled')


    # Scientific mode button and keyboard event methods begin here

    def paraInsert(self, side):
        """
        Method to handle '(' and ')' button events
        Inspects input and operation field contents
        If valid then will insert specified left/right
            bracket side into operation field
        Increments/Decrements global number of unclosed left brackets
            each time that a left/right bracket is added
        If resulting number is > 0, displays this number in paraField
        """
        s_in = self.inputField.get()
        s_op = self.opField.get()
        num_left = s_op.count('(')
        num_right = s_op.count(')')
        self.paraField.config(state = 'normal')
        global num_brackets
        
        if side == 'left':
            # Allow left bracket insertion under one of these conditions:
            # (1) both fields are empty
            # (2) or opfield ends with left bracket and infield is empty
            # (2) or opfield ends with op string
            if ((not s_in and not s_op) or (s_op.endswith('( ') and not s_in)
                or s_op.endswith(('+ ','- ','* ','/ ','^ ','root '))):
                self.opField.config(state = 'normal')
                self.opField.insert(tk.INSERT,' ( ')
                self.opField.config(state = 'disabled')
                num_brackets += 1
                
        elif side == 'right':
            # Allow right bracket insertion under one of these conditions:
            # (1) num_left > num_right
            #     and opfield ends with op string
            #     and infield is non-empty
            # (2) num_left > num_right
            #     and op field ends with right bracket
            if ((num_left > num_right and
                s_op.endswith(('+ ','- ','* ','/ ','^ ','root ',')'))
                and s_in) or (num_left > num_right and s_op.endswith(') '))):
                self.opField.config(state = 'normal')
                self.inputField.config(state = 'normal')
                self.opField.insert(tk.INSERT,self.inputField.get())
                self.opField.insert(tk.INSERT,' ) ')
                self.inputField.delete(0,tk.END)
                self.opField.config(state = 'disabled')
                self.inputField.config(state = 'disabled')
                num_brackets -= 1

        if num_brackets > 0:
            self.paraField.delete(0,tk.END)
            self.paraField.insert(tk.INSERT,' ( = ' + str(num_brackets))            
        else:
            self.paraField.delete(0,tk.END)
            
        self.paraField.config(state = 'disabled')
            
            
    def xpow(self, num):
        """
        Method to handle x^2 and x^3 button events
        Calculates the square or cube power of x
        Raises OverflowError if result is too large to show
        Successful result sent to input field
        """
        s_in = self.inputField.get()
        if s_in:
            try:
                result = float(s_in) ** num
            except OverflowError:
                messagebox.showerror('Overflow',
                                     'Result is too large to display')
                self.clear()
            else:
                self.inputField.config(state = 'normal')
                self.inputField.delete(0,tk.END)
                self.inputField.insert(tk.INSERT,str(result))
                self.inputField.config(state = 'disabled')
                # change recent computation status to True
                global eq
                eq = True
    
    
    def log(self, base):
        """
        Method to handle 'log' (base 10) and 'ln' (base e) button events
        Calculates the logarithm of x with math.log(x, base)
        Raises ValueError if x is negative
        Successful result is sent to input field
        """
        s_in = self.inputField.get()
        if s_in:
            try:
                result = math.log(float(s_in),base)
            except ValueError:
                messagebox.showerror('Invalid input',
                                     'Cannot calculate logarithm of negative value')
                self.clear()
            else:
                self.inputField.config(state = 'normal')
                self.inputField.delete(0,tk.END)
                self.inputField.insert(tk.INSERT,str(result))
                self.inputField.config(state = 'disabled')
                # change recent computation status to True
                global eq
                eq = True
                

    def facto(self):
        """
        Method to handle 'n!' button event
        Calculates the factorial of n with math.factorial(n)
        Raises ValueError if (n is negative or int(n) != n)
            or OverflowError if result is too large to display
        Successful result is sent to input field
        """
        s_in = self.inputField.get()
        if s_in:
            try:
                if '.' in s_in:
                    # check if all decimal places are zeros
                    # ie. it is equivalent to its int form
                    if float(s) == math.trunc(float(s_in)):
                        result = math.factorial(math.trunc(float(s_in)))
                    # otherwise raise ValueError because you can't factorial float
                    else:
                        raise ValueError
                else:
                    # will raise ValueError is negative
                    result = math.factorial(int(s_in))
            except ValueError:
                messagebox.showerror('Invalid input',
                                     'Cannot calculate factorial of negative or float values')
                self.clear()
            except OverflowError:
                messagebox.showerror('Overflow',
                                     'Result is too large to display')
                self.clear()
            else:
                self.inputField.config(state = 'normal')
                self.inputField.delete(0,tk.END)
                self.inputField.insert(tk.INSERT,str(result))
                self.inputField.config(state = 'disabled')
                # change recent computation status to True
                global eq
                eq = True
            

    def cubeRoot(self):
        """
        Method to handle cube root button event
        Calculates the cube root of x with x ** (1/3)
        Result is sent to input field
        """
        s_in = self.inputField.get()
        if s_in:
            if '.' in s_in:
                # if x is negative perform cube root first THEN apply sign
                if '-' in s_in:
                    result = -(abs(float(s_in))**(1/3))
                else:
                    result = float(s_in)**(1/3)
            else:
                # if x is negative perform cube root first THEN apply sign
                if '-' in s_in:
                    result = -(abs(int(s_in))**(1/3))
                else:
                    result = int(s_in)**(1/3)
            self.inputField.config(state = 'normal')
            self.inputField.delete(0,tk.END)
            self.inputField.insert(tk.INSERT,str(result))
            self.inputField.config(state = 'disabled')
            # change recent computation status to True
            global eq
            eq = True


    def baseToX(self, base):
        """
        Method to handle '10^x' and 'e^x' button events
        Calculates the corresponding powers
        Raises OverflowError if result is too large to show
        Sends result to input field
        """
        s_in = self.inputField.get()
        if s_in:
            try:
                result = base ** float(s_in)
            except OverflowError:
                messagebox.showerror('Overflow',
                                     'Result is too large to display')
                self.clear()
            else:
                self.inputField.config(state = 'normal')
                self.inputField.delete(0,tk.END)
                self.inputField.insert(tk.INSERT,str(result))
                self.inputField.config(state = 'disabled')
                # change recent computation status to True
                global eq
                eq = True
        
    def trig(self, func):
        """
        Method to handle 'sin','cos','tan' button events
        Takes input field contents as degrees and converts to radians
        Then calculates the specified function result using math.func
        Raises OverflowError for discontinuities of tan function
        Successful result is sent to input field
        """
        s_in = self.inputField.get()
        if s_in:
            try:
                # s_in assumed to be string repr. of degrees
                result = getattr(math,func)(math.radians(float(s_in)))
            except OverflowError:
                messagebox.showerror('Overflow',
                                     'Result is too large to display')
                self.clear()
            else:
                self.inputField.config(state = 'normal')
                self.inputField.delete(0,tk.END)
                self.inputField.insert(tk.INSERT,str(result))
                self.inputField.config(state = 'disabled')
            # change recent computation status to True
            global eq
            eq = True

                
    def exp(self):
        """
        Method to handle 'exp' button event
        Takes input field content as coefficient x and converts
           to exponential scientific notation (x * e+0)
        Further numerical input or sign change will then alter
           the power of e   
        """
        s_in = self.inputField.get()
        # Allow conversion to exponential form if:
        # (1) input field non-empty
        # (2) input field NOT already in exponential form
        # (3) input field NOT equivalent to zero
        # (4) input field does NOT have a trailing decimal
        # (5) input field NOT from a recent computation
        if (s_in and 'e' not in s_in and float(s_in) != 0
            and not s_in.endswith('.') and not eq):
            s_in += 'e+0'
            self.inputField.config(state = 'normal')
            self.inputField.delete(0,tk.END)
            self.inputField.insert(tk.INSERT,s_in)
            self.inputField.config(state = 'disabled')
            
        
    def pi(self):
        """
        Method to handle pi button event
        Takes pi value from math.pi
        Clears input field, then inserts this value
        """
        self.inputField.config(state = 'normal')
        s_in = self.inputField.get()
        if s_in:
            self.inputField.delete(0,tk.END)
        self.inputField.insert(tk.INSERT,str(math.pi))
        self.inputField.config(state = 'disabled')
         # treat pi insertion as computation event
         # change status to True
        global eq
        eq = True
        
        
if __name__ == '__main__':
    
    # make instance of Tk class as master widget
    root = tk.Tk()

    # set the calculator initially to default standard mode dimensions
    root.geometry('235x450')

    # prevent resizing of the window 'frame'
    root.resizable(width=False, height=False)

    # make instance of Window class with master
    app = Window(root)

    # start mainloop of window to show all GUI components
    app.mainloop()
