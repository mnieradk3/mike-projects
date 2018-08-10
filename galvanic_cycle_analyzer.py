import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import re
import math

import matplotlib
# set matplotlib backend
matplotlib.use('TkAgg')
# special canvas widget for embedding (ie. drawing) of matplotlib graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class InputWindow(tk.Frame):
    """
    Input GUI window 
    Takes user input: cycle files, cycle parameters and analysis options
    """
    def __init__(self, master):
        """
        Input Window frame widget constructor
        """
        # call Frame superclass constructor with Tk widget as master
        tk.Frame.__init__(self, master)
        # assign Tk widget as instance attribute
        self.master = master
        # set geometry of input window frame
        self.master.geometry('700x770')
        # prevent resizing of the window 'frame'
        self.master.resizable(width=False, height=False)
        # call input window construction method below
        self.init_window()
    

    def init_window(self):
        """
        Method that implements the remaining widgets of the input GUI
        """
        # set the title of our master (Tk widget)      
        self.master.title("Basic Galvanic Cycle Data Analyzer - Input Window")

        # pack the window frame widget (self) into the full space of the Tk widget
        self.pack(fill = tk.BOTH, expand = True)

        # entry field widget for exported cycle set source file path 
        self.sourceField = tk.Entry(self, width = 40, font = 18)
        self.sourceField.place(x = 75, y = 50)
        sourceLabel = tk.Label(self, font = 24,
                               text = 'Source path for input cycle set file (.txt) :')
        sourceLabel.place(x = 25, y = 25)

        # button widget to 'browse' windows
        # to manually select exported cycle set file, handled by load_file method
        sourceButton = tk.Button(self, font = 12, width = 6, text = 'Browse',
                                 background = 'white',
                                 command = lambda: self.load_file())
        sourceButton.place(x = 450, y = 45)

        # entry field widget for destination folder path (optional)
        # for generated spreadsheet and plot files 
        self.destField = tk.Entry(self, width = 40, font = 18)
        self.destField.place(x = 75, y = 105)
        destLabel = tk.Label(self, font = 24,
                             text = 'Destination path for output files (optional) :')
        destLabel.place(x = 25, y = 80)

        # button widget to 'browse' windows
        # to manually select destination folder, handled by output_dir method
        destButton = tk.Button(self, font = 12, width = 6, text = 'Browse',
                                 background = 'white',
                                 command = lambda: self.output_dir())
        destButton.place(x = 450, y = 100)

        # entry field widget for charge/discharge current (in uA) of the cycle set
        self.currentField = tk.Entry(self, width = 10, font = 18)
        self.currentField.place(x = 75, y = 155)
        currentLabel = tk.Label(self, font = 24,
                                text = 'Charge/Discharge current of cycle set (uA > 0) :')
        currentLabel.place(x = 25, y = 130)

        # entry field widget for typical charge-discharge IR transition of the cycle set
        self.transOneField = tk.Entry(self, width = 10, font = 18)
        self.transOneField.place(x = 75, y = 205)
        transOneLabel = tk.Label(self, font = 24,
                                 text = 'Approximate charge to discharge IR transition value (V) :')
        transOneLabel.place(x = 25, y = 180)

        # entry field widget for typical discharge-charge IR transition of the cycle set
        self.transTwoField = tk.Entry(self, width = 10, font = 18)
        self.transTwoField.place(x = 75, y = 255)
        transTwoLabel = tk.Label(self, font = 24,
                                 text = 'Approximate discharge to charge IR transition value (V) :')
        transTwoLabel.place(x = 25, y = 230)

        # entry field widget for the charge/discharge time in sec per cycle for the set
        self.timeField = tk.Entry(self, width = 10, font = 18)
        self.timeField.place(x = 75, y = 305)
        timeLabel = tk.Label(self, font = 24,
                             text = 'Time for charge/discharge portions of cycles (sec > 0)  :')
        timeLabel.place(x = 25, y = 280)

        # entry field widget for number of cycles in this set 
        self.numField = tk.Entry(self, width = 10, font = 18)
        self.numField.place(x = 75, y = 355)
        numLabel = tk.Label(self, font = 24, text = 'Number of cycles in this set (integer > 0)  :')
        numLabel.place(x = 25, y = 330)

        # entry field widget for anode-cathode contact area (in cm^2)
        self.areaField = tk.Entry(self, width = 10, font = 18)
        self.areaField.place(x = 75, y = 405)
        areaLabel = tk.Label(self, font = 24, text = 'Anode-Cathode contact area (cm\u00b2 > 0) :')
        areaLabel.place(x = 25, y = 380)

        # entry field widget for discharge potential threshold (optional)
        self.disField = tk.Entry(self, width = 10, font = 18)
        self.disField.place(x = 75, y = 455)
        disLabel = tk.Label(self, font = 24, text = 'Discharge threshold (V, default = 2) :')
        disLabel.place(x = 25, y = 430)

        # radiobutton widget with 2 input options for 'cell style'
        # (1) Charge to Discharge IR transition < 0
        #     Discharge to Charge IR transition > 0
        #     ie. charge plateau potentials > discharge plateau potentials
        # (2) Charge to Discharge IR transition < 0
        #     Discharge to Charge IR transition > 0
        #     ie. charge plateau potentials < discharge plateau potentials
        cellLabel = tk.Label(self, font = 'Helvetica 18 bold', text = 'Cell style')
        cellLabel.place(x = 480, y = 320)

        # the two cell options share this single IntVar variable
        self.cellVar = tk.IntVar()
        cellfirst = tk.Radiobutton(self, font = 14, height = 2, width = 35,
                                  variable = self.cellVar, value = 1,
                                  text = '(1) Charge-discharge IR transition < 0')
        cellfirst.place(x = 350, y = 350)
        firstlabel = tk.Label(self, font = 20, text = 'Discharge-charge IR transition > 0')
        firstlabel.place(x = 420, y = 385)
        cellsecond = tk.Radiobutton(self, font = 14, height = 2, width = 35,
                                   variable = self.cellVar, value = 2,
                                   text = '(2) Charge-discharge IR transition > 0')
        cellsecond.place(x = 350, y = 410)
        secondlabel = tk.Label(self, font = 20, text = 'Discharge-charge IR transition < 0')
        secondlabel.place(x = 420, y = 445)
        # set default input window initialization to select first style (value = 1)
        self.cellVar.set(1)
        
        # nine checkbox widgets for graphical analysis options versus cycle number
        # (1) Total Coulombic Efficiency
        # (2) Resistance based on IR drop calculation
        # (3) Resistance based on charge-discharge plateau separation calculation
        # (4) Total Charge Capacity
        # (5) Charge Plateau Potential
        # (6) Total Discharge Capacity
        # (7) Discharge Plateau Potential
        # (8) Charge-Discharge Plateau Separation
        # (9) Discharge Percent above specified threshold 
        optionsLabel = tk.Label(self, font = 'Helvetica 16 bold',
                                text = 'Graphical Analysis Options')
        optionsLabel.place(x = 25, y = 490)
        
        # separate IntVar variables for each checkbox to inspect their on/off state
        self.ceVar = tk.IntVar(name = 'CE')
        ceCheck = tk.Checkbutton(text = 'Coulombic Efficiency',
                                 variable = self.ceVar)
        ceCheck.place(x = 25, y = 520)
        self.res1Var = tk.IntVar(name = 'RES1')
        res1Check = tk.Checkbutton(text = 'Resistance (from IR drop)',
                                   variable = self.res1Var)
        res1Check.place(x = 25, y = 545)
        self.res2Var = tk.IntVar(name = 'RES2')
        res2Check = tk.Checkbutton(text = 'Resistance (from ch-dis plat. sep.)',
                                   variable = self.res2Var)
        res2Check.place(x = 25, y = 570)
        self.chVar = tk.IntVar(name = 'CH')
        chCheck = tk.Checkbutton(text = 'Charge Capacity',
                                 variable = self.chVar)
        chCheck.place(x = 25, y = 595)
        self.chpVar = tk.IntVar(name = 'CHP')
        chpCheck = tk.Checkbutton(text = 'Charge Plateau Potential',
                                  variable = self.chpVar)
        chpCheck.place(x = 25, y = 620)
        self.disVar = tk.IntVar(name = 'DIS')
        disCheck = tk.Checkbutton(text = 'Discharge Capacity',
                                  variable = self.disVar)
        disCheck.place(x = 25, y = 645)
        self.dispVar = tk.IntVar(name = 'DISP')
        dispCheck = tk.Checkbutton(text = 'Discharge Plateau Potential',
                                   variable = self.dispVar)
        dispCheck.place(x = 25, y = 670)
        self.psVar = tk.IntVar(name = 'PLATSEP')
        psCheck = tk.Checkbutton(text = 'Charge-Discharge Plateau Separation',
                                 variable = self.psVar)
        psCheck.place(x = 25, y = 695)
        self.percentVar = tk.IntVar(name = 'DISPERCENT')
        percentCheck = tk.Checkbutton(text = 'Discharge Percent Above/Below Threshold',
                                      variable = self.percentVar)
        percentCheck.place(x = 25, y = 720)
        
        # radiobutton widget with 3 output choices:
        # (1) output text + graph windows only, (2) + saved text file, (3) + saved graph files
        outputLabel = tk.Label(self, font = 'Helvetica 18 bold', text = 'Output Options')
        outputLabel.place(x = 335, y = 490)
        # the three output options share this single IntVar variable
        self.outputVar = tk.IntVar()
        output1 = tk.Radiobutton(self, font = 14, height = 2, width = 15,
                                  variable = self.outputVar, value = 1,
                                  text = '(1) Window only')
        output1.place(x = 320, y = 525)
        output2 = tk.Radiobutton(self, font = 14, height = 2, width = 20,
                                  variable = self.outputVar, value = 2,
                                  text = '(2) Window + text file')
        output2.place(x = 315, y = 560)
        output3 = tk.Radiobutton(self, font = 14, height = 2, width = 25,
                                  variable = self.outputVar, value = 3,
                                  text = '(3) Window + text file + graph files')
        output3.place(x = 335, y = 595)
        # set default input window initialization to select the first output option (value = 1)
        self.outputVar.set(1)

        # button widget 'Analyze'
        # when user is finished inputing and ready to begin analysis
        # command handled by 'router' method
        gobutton = tk.Button(self, font = 'Helvetica 18 bold', height = 2, width = 7,
                          text = 'Analyze', background = 'white',
                             command = self.router)
        gobutton.place(x = 350, y = 640)


    # input window event methods begin here
    
    def load_file(self):
        """
        Method to handle 'browse' button event for source field
        Opens file dialog for user to select exported cycle set (.txt) files
        If user does not select .txt file an error messagebox appears
        Otherwise the .txt file path is inserted into source field
        """
        self.filename = filedialog.askopenfilename(initialdir = "/",
                                                   title = "Select source file",
                                                   filetypes = [("text files","*.txt")])
        if self.filename:
            if self.filename.endswith('.txt'):    
                self.sourceField.delete(0,tk.END)
                self.sourceField.insert(tk.INSERT, self.filename)
            else:
                messagebox.showerror('Invalid input','Source file must be .txt')

    def output_dir(self):
        """
        Method to handle 'browse' button event for destination field
        Opens file dialog for user to select destination directory (folder)
        Selected folder path is inserted into destination field
        """
        self.outputDir = filedialog.askdirectory(initialdir = "/",
                                                title = "Select destination folder")
        if self.outputDir:
            self.destField.delete(0,tk.END)
            self.destField.insert(tk.INSERT, self.outputDir)

            
    def router(self):
        """
        Method to handle 'Analyze' button event
        Begins textAnalysis method
        Afterwards also begins graph analysis methods (if user selected any)
        """
        results = self.textAnalysis()
        # if data analysis is successful inspect graphical analysis checkbuttons
        # selected buttons go to corresponding plotting methods
        if results:
            if self.ceVar.get() == 1:
                self.plotCE(results)
            if self.res1Var.get() == 1:    
                self.plotResIR(results)
            if self.res2Var.get() == 1:    
                self.plotResPS(results)
            if self.chVar.get() == 1:
                self.plotChCap(results)
            if self.chpVar.get() == 1:
                self.plotChPlat(results)
            if self.disVar.get() == 1:
                self.plotDisCap(results)
            if self.dispVar.get() == 1:
                self.plotDisPlat(results)
            if self.psVar.get() == 1:
                self.plotPlatSep(results)
            if self.percentVar.get() == 1:
                self.plotDisPercent(results)
         
    
    def textAnalysis(self):
        """
        Method to handle analysis of the cycle set data, called by router method
        Attempts to compute all relevant results from the cycle set
            based on given cycle input parameters
        Stores the relevant results as a tuple of lists
        Passes these results to output table window and output graph windows
        Also prints out these results to a .txt file if radiobutton options 2/3 selected
        Raises various ValueError if any required cycle parameters are missing or invalid
        Raises FileNotFoundError if source file path does not exist
        """
        try:
            # check if any required fields are missing or have invalid input
            sourceStr = self.sourceField.get()
            if not sourceStr:
                raise ValueError('missing source file path')
            currStr = self.currentField.get()
            if not currStr:
                raise ValueError('missing current value')
            if float(currStr) < 0:
                raise ValueError('current value must be greater than zero')
            transOneStr = self.transOneField.get()
            if not transOneStr:
                raise ValueError('missing charge-discharge IR transition value')
            transTwoStr = self.transTwoField.get()
            if not transTwoStr:
                raise ValueError('missing discharge-charge IR transition value')
            # check given transition values based on cell style selected
            if self.cellVar.get() == 1:
                if float(transOneStr) > 0 or float (transTwoStr) < 0:
                    raise ValueError('Cell style 1: ch-dis transition < 0, dis-ch transition > 0')
            elif self.cellVar.get() == 2:
                if float(transOneStr) < 0 or float (transTwoStr) > 0:
                    raise ValueError('Cell style 2: ch-dis transition > 0, dis-ch transition < 0')
            timeStr = self.timeField.get()
            if not timeStr:
                raise ValueError('missing value for time in seconds per cycle')
            if float(timeStr) < 0:
                raise ValueError('time in seconds per cycle value must be greater than zero')
            numStr = self.numField.get()
            if not numStr:
                raise ValueError('missing value for number of cycles in set')
            if float(numStr) < 0:
                raise ValueError('number of cycles must be positive value')
            areaStr = self.areaField.get()
            if not areaStr:
                raise ValueError('missing value for electrode contact area')
            if float(areaStr) < 0:
                raise ValueError('electrode contact area must be positive value')
            disStr = self.disField.get()
            if not disStr:
                # if no discharge threshold specified then use default of +2 V
                disStr = '2'
            if self.cellVar.get() == 1:
                compare = ' > '
            elif self.cellVar.get() == 2:
                compare = ' < '
            
            # if no exceptions raised try to create input file object
            input_file = open(sourceStr,'r')
            
        except (FileNotFoundError, ValueError) as err:
            # print exception information to a messagebox that appears
            messagebox.showerror('Invalid input', err)
            # then leave analysis method immediately 
            return None
        
        else:
            # if user wants output text file (radiobutton options 2 or 3)
            # determine output file path first and make a writeable file object there
            outPath = ''
            if self.outputVar.get() == 2 or self.outputVar.get() == 3:
                if self.destField.get():
                    # assume destination path is valid, use as output directory
                    output_dir = self.destField.get()
                    # make output txt file string based on this path and the source string
                    base = os.path.basename(sourceStr)
                    outPath = output_dir + '\\' + base[:base.index('.')] + '-out' + '.txt'
                else:
                    # create output txt filename string based on source file path given 
                    output_dir = os.path.dirname(sourceStr)
                    outPath = sourceStr[:sourceStr.index('.')]+'-out'+'.txt'
                output_file = open(outPath,'a')
                # write header and unit rows to the output txt file (very long string, scroll right!)
                print('Cycle #\tTop\tBot\tResistance (IR Drop)\tCharge start\tCharge finish\tTotal Charge\tCharge Plateau\tCharge Capacity\tDischarge start\tDischarge finish\tTotal Discharge\tDischarge Plateau\tDischarge Capacity\tPlateau Separation\tResistance (Plat. Sep.)\tCoulombic Efficiency\tTot. Dis.' + compare + disStr + ' V ' + '\tDischarge Percent' + compare + disStr + ' V ',file = output_file) 
                print('\t(V)\t(V)\t(ohm cm\u00b2)\t(sec)\t(sec)\t(sec)\t(V)\t(mA*h/cm\u00b2)\t(sec)\t(sec)\t(sec)\t(V)\t(mA*h/cm\u00b2)\t(V)\t(ohm cm\u00b2)\t(%)\t(sec)\t(%)',file = output_file)

            # determine cycle parameter values from given field strings
            current = float(currStr)/(10**6)
            area = float(areaStr)
            disT = float(disStr)
            current_density = current/area
            transOne = float(transOneStr)
            transTwo = float(transTwoStr)

            # lists to hold cell potential (y) and time (x) values
            #    from parsed input data
            # ie. a pair of values from the two lists at the same list index
            #    represents a SINGLE E vs. time data point in the input cycle set
            # column 0 = time, column 1 = cell potential
            times = []
            potentials = []

            # ignore lines of input file containing non-numerical data or blank lines
            reg1 = re.compile(r'[a-zA-Z]')
            reg2 = re.compile(r'\d')
            for line in input_file:
                if not reg1.search(line) and reg2.search(line) :
                    times.append(float(line.split()[0]))
                    potentials.append(float(line.split()[1]))

            # start at cycle number 1
            cycle = 1
            # charging start time of first cycle
            ch_start_ind = 0
            ch_start = times[ch_start_ind]
            dis_tot_T = 0

            # lists to hold cycle numbers and respective calculated results
            cycNums, tops, bots, chPlats, disPlats, platSeps = [],[],[],[],[],[]
            CEs, resIRs, resPSs, disCaps, chCaps, disPercents = [],[],[],[],[],[]

            # start actually analyzing the potential vs. time input data
            for i in range(0,len(potentials)):
                
                # determine charge-discharge transition from given IR transition value # 1
                # this transition corresponds to the end of the charge portion of the cycle
                if (i>10 and ((self.cellVar.get() == 1 and potentials[i]-potentials[i-1]<transOne)
                    or (self.cellVar.get() == 2 and potentials[i]-potentials[i-1]>transOne))):
                    # cell potentials before/after charge-discharge transition
                    top = potentials[i-1]
                    tops.append(top)
                    bot = potentials[i]
                    bots.append(bot)
                    # internal resistance based on charge-discharge transition
                    resIR = abs(round(((top-bot)/2)/current_density,2))
                    resIRs.append(resIR)
                    # end and total charge times based on charge-discharge transition
                    ch_end = abs(times[i-1])
                    ch_tot = ch_end - ch_start
                    # total charge capacity based on total charge time
                    ch_cap = round((ch_tot/3600)*current_density*1000,6)
                    chCaps.append(ch_cap)
                    # charge plateau potential, based on midpoint time of charging
                    chPlat = potentials[ch_start_ind + round((i - ch_start_ind)/2)]
                    chPlats.append(chPlat)
                    # charge end time = discharge begin time
                    dis_start_ind = i
                    dis_start = abs(times[dis_start_ind])
                    
                # determine total dis. time above or below specified potential threshold (disT)
                if i>10:
                    # cell style 1: total discharge above potential threshold
                    if self.cellVar.get() == 1:
                        if ((round(potentials[i],2) < disT) and ((round(potentials[i-1],2) > disT
                            or round(potentials[i-1],2) == disT))):
                            dis_end_T = abs(times[i])
                            dis_tot_T = dis_end_T - dis_start
                    # cell style 2: total discharge below potential threshold
                    elif self.cellVar.get() == 2:
                        if ((round(potentials[i],2) > disT) and ((round(potentials[i-1],2) < disT
                            or round(potentials[i-1],2) == disT))):
                            dis_end_T = abs(times[i])
                            dis_tot_T = dis_end_T - dis_start
                    
                # determine discharge-charge transition from given IR transition value # 2
                # this transition corresponds to the end of the discharge portion of the cycle
                # for the last cycle this will correspond to the final potential data point
                if (i>10 and ((self.cellVar.get() == 1 and potentials[i]-potentials[i-1]>transTwo)
                    or (self.cellVar.get() == 2 and potentials[i]-potentials[i-1]<transTwo)
                    or i == len(potentials)-1)):
                    # end and total discharge times based on discharge-charge transition
                    dis_end = abs(times[i])
                    dis_tot = dis_end - dis_start
                    # total discharge capacity based on total discharge time
                    dis_cap = round((dis_tot/3600)*current_density*1000,6)
                    disCaps.append(dis_cap)
                    # percent of total discharge capacity above potential threshold
                    dis_percent_T = round((dis_tot_T/dis_tot)*100,1)
                    disPercents.append(dis_percent_T)
                    # total coulombic efficiency based on total charge/discharge times
                    CE = round(((dis_end-dis_start)/(ch_end-ch_start))*100,1)
                    CEs.append(CE)
                    # discharge plateau potential, based on midpoint time of discharging
                    disPlat = potentials[dis_start_ind + round((i - dis_start_ind)/2)]
                    disPlats.append(disPlat)
                    # charge-discharge plateau separation
                    platSep = abs(round(disPlat - chPlat,3))
                    platSeps.append(platSep)
                    # internal resistance based on plateau separation
                    resPS = round((platSep/2)/current_density,2)
                    resPSs.append(resPS)
                    
                    # write results for the current cycle to output txt file
                    #    if user selected radiobutton output options 2 or 3
                    if self.outputVar.get() == 2 or self.outputVar.get() == 3:
                        print(cycle,'\t',top,'\t',bot,'\t',resIR,'\t',ch_start,'\t',
                              ch_end,'\t',ch_tot,'\t',chPlat,'\t',ch_cap,'\t',dis_start,
                              '\t',dis_end,'\t',dis_tot,'\t',disPlat,'\t',dis_cap,'\t',
                              platSep,'\t',resPS,'\t',CE,'\t',dis_tot_T,'\t',dis_percent_T,
                              file = output_file)

                    if not i == len(potentials)-1:
                        # end of current discharge time = start of next charge time
                        ch_start_ind = i
                        ch_start = dis_end      
                        cycNums.append(cycle)
                        # end of current discharge, go to next cycle
                        cycle += 1
                    else:
                        cycNums.append(cycle)
                    
            # show message box for textual analysis completion
            messagebox.showinfo('Analysis complete', 'Analysis complete')
            # close input file
            input_file.close()
            # if user selected radiobutton output options 2 or 3
            # then close output txt file too
            if self.outputVar.get() == 2 or self.outputVar.get() == 3:
                output_file.close()
                
            # results from textual analysis will be sent to output windows for text and graphs
            # create lists of header and unit fields that will be included with the results
            headers = [r'Cycle #','Coulombic Efficiency','Resistance (IR drop)',
                       'Resistance (Plat. Sep.)','Charge Capacity','Charge Plateau',
                       'Discharge Capacity','Discharge Plateau','Plateau Separation',
                       r'Discharge %' + compare + str(disT) + ' V ']
            units = ['','(%)','(ohms cm\u00b2)','(ohms cm\u00b2)','(mA*h/cm\u00b2)','(V)',
                     '(mA*h/cm\u00b2)','(V)','(V)','(%)']
            results = (headers,units,cycNums,CEs,resIRs,resPSs,chCaps,chPlats,disCaps,
                       disPlats,platSeps,disPercents)
                
            # make output text table window with results
            OutputTable(tk.Tk(),results)
            # make output graphs based on graphical analysis checkbutton selections
            for var in (self.ceVar,self.res1Var,self.res2Var,self.chVar,self.chpVar,
                        self.disVar,self.dispVar,self.psVar,self.percentVar):
                if var.get() == 1:
                    # if output graph files radiobutton selected (option 3)
                    # --> saveOutput arg = True
                    if self.outputVar.get() == 3:
                        OutputGraph(tk.Tk(),results,var._name,True,currStr,
                                    timeStr,numStr,disStr,self.cellVar.get(),outPath)
                    # otherwise output options 1 or 2 selected
                    # --> saveOutput arg = False
                    else:
                        OutputGraph(tk.Tk(),results,var._name,False,currStr,
                                    timeStr,numStr,disStr,self.cellVar.get(),outPath)
            

class OutputTable(tk.Frame):
    """
    Output GUI window
    Displays results from textAnalysis method in a table
    Vertical scrollbar attached
    """
    def __init__(self, master, results):
        """
        Output GUI window constructor
        Takes 'results' from textAnalysis method as tuple of lists
        """
        # call superclass constructor with Tk widget as master
        tk.Frame.__init__(self, master)
        # make canvas widget inside tk widget
        self.canvas = tk.Canvas(master, borderwidth=0, background="#ffffff")
        # make another frame widget within the canvas
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        # make vertical scroll bar widget
        self.vsb = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        # attach scroll bar to side of canvas
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        
        # reference to master widget, which is the Tk widget
        self.master = master
        self.results = results
        # set geometry and title of output window 
        self.master.geometry('800x800')
        self.master.title("Basic Cycle Data Analyzer - Output Text Window")
        # make and populate the table
        self.init_table()

        
    def init_table(self):
        """
        Constructs a table made of entry widgets
        These are positioned on a grid relative to parent frame widget (self.frame)
        Populates the table with results from textAnalysis method
        """        
        width = 10
        height = len(self.results[2])
        # construct headers of table
        for x in range(width):
            cell = tk.Entry(self.frame)
            cell.insert(tk.INSERT,self.results[0][x])
            cell.grid(row = 0, column = x)
        # construct unit fields for headers
        for i in range(width):
            cell2 = tk.Entry(self.frame)
            cell2.insert(tk.INSERT,self.results[1][i])
            cell2.grid(row = 1, column = i)
        # construct remainder of table with entries for results values
        for j in range(height):
            for k in range(2,width+2):
                cell3 = tk.Entry(self.frame)
                cell3.insert(tk.INSERT,self.results[k][j])
                cell3.grid(row = j+2, column = k-2)

                
    def onFrameConfigure(self, event):
        """
        Method to reset the scroll region of vertical scrollbar
           to encompass the whole canvas
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            
class OutputGraph(tk.Frame):
    """
    Output GUI window
    Plots results from textAnalysis method into one type of graph
       using matplotlib and then outputs this graph to a window
    Also possibly saves these graphs to separate PNG files if
       user selected radiobutton option 3 at input window
    One window constructed per unique graph type per analysis run
    """
    def __init__(self, master, results, outputType, saveOutput, current,
                 time, num, threshold, cellStyle, outPath):
        """
        Output GUI window constructor that takes these extra arguments:
        (1) 'results': from textAnalysis method, as tuple of lists
        (2) 'outputType': indicating type of graph output, as acronym string
        (3) 'saveOutput': whether to save graphs to file, as True/False
        (4) 'current': current density of cycle set (mA/cm^2), as string
        (5) 'time': time per charge/discharge portion (sec), as string
        (6) 'num': number of cycles in set, as string
        (7) 'threshold': specified discharge potential threshold (V), as string
        (8) 'cellStyle': cell style 1 or 2 specified from input window, as int
        (9) 'outPath': output root path for graph files, as string
        """
        # call superclass constructor with Tk widget as master
        tk.Frame.__init__(self, master)
        # reference to master widget, which is the Tk widget
        self.master = master
        # set geometry of output window frame
        self.master.geometry('750x600')
        self.pack(fill = tk.BOTH, expand = True)
        
        # store constructor args as instance attributes
        # to share with plotting methods
        self.results = results
        self.saveOutput = saveOutput
        self.current = current
        self.time = time
        self.num = num
        self.threshold = threshold
        if cellStyle == 1:
            self.compare = '>'
        elif cellStyle == 2:
            self.compare = '<'
        self.outPath = outPath
            
        # get figure object from plotting methods
        # based on outputType string passed into constructor
        if outputType == 'CE': fig = self.plotCE(self.results)
        elif outputType == 'RES1': fig = self.plotResIR(self.results)
        elif outputType == 'RES2': fig = self.plotResPS(self.results)
        elif outputType == 'CH': fig = self.plotChCap(self.results)
        elif outputType == 'CHP': fig = self.plotChPlat(self.results)
        elif outputType == 'DIS': fig = self.plotDisCap(self.results)
        elif outputType == 'DISP': fig = self.plotDisPlat(self.results)
        elif outputType == 'PLATSEP': fig = self.plotPlatSep(self.results)
        elif outputType == 'DISPERCENT': fig = self.plotDisPercent(self.results)
        
        # send this figure object to be drawn on a FigureCanvasTkAgg widget
        self.master.title(fig.get_axes()[0].get_ylabel())
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().pack()
        canvas.draw()
        # after drawing this figure...
        # --> close and delete its figure object from memory for next analysis run
        plt.close()


    # methods to plot different data sets from the 'results' tuple of lists
    
    def plotCE(self,results):
        """
        Total coulombic efficiency vs. cycle number
        """
        xCE = results[2]
        yCE = results[3]
        fCE = plt.figure(1)
        axCE = fCE.add_subplot(111)
        axCE.set(title = 'Total Coulombic Efficiency vs. Cycle Number',
                 xlabel = 'Cycle Number',ylabel = r'Coulombic Efficiency (%)')
        axCE.set_xlim(0,xCE[-1])
        axCE.set_ylim(0,100)
        labelCE = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axCE.plot(xCE,yCE,color='black',marker='o',markersize=4,
                  linestyle='solid',label = labelCE)
        axCE.legend(loc='lower right')
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fCE.savefig(self.outPath[:self.outPath.index('.')]
                        +'-out-' + 'CE' + '.png')
        # return figure to be drawn in canvas
        return fCE


    def plotResIR(self,results):
        """
        Internal resistance (based on IR charge-discharge transition) vs. cycle number
        """
        xRESIR = results[2]
        yRESIR = results[4]
        fRESIR = plt.figure(2)
        axRESIR = fRESIR.add_subplot(111)
        axRESIR.set(title = 'Internal Resistance from IR transition vs. Cycle Number',
                  xlabel = 'Cycle Number',ylabel = 'Resistance from IR transition (ohm cm\u00b2)')
        axRESIR.set_xlim(0,xRESIR[-1])
        # find appropriate upper y-axis limit for evenly spaced ticks
        s = str(int(max(yRESIR)))
        lim = int(math.ceil(max(yRESIR)/(10**(len(s)-1))))*(10**(len(s)-1))
        axRESIR.set_ylim(0,lim)
             
        labelRESIR = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axRESIR.plot(xRESIR,yRESIR,color='black',marker='o',markersize=4,
                   linestyle='solid',label = labelRESIR)
        axRESIR.legend()
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fRESIR.savefig(self.outPath[:self.outPath.index('.')]
                         +'-out-' + 'resIR' + '.png')
        # return figure to be drawn in canvas
        return fRESIR

    def plotResPS(self,results):
        """
        Internal resistance (based on charge-discharge plateau separation) vs. cycle number
        """
        xRESPS = results[2]
        yRESPS = results[5]
        fRESPS = plt.figure(3)
        axRESPS = fRESPS.add_subplot(111)
        axRESPS.set(title = 'Internal Resistance from Charge-Discharge Plat. Sep. vs. Cycle Number',
                  xlabel = 'Cycle Number',ylabel = 'Resistance from Chg-Dis Plat. Sep. (ohm cm\u00b2)')
        axRESPS.set_xlim(0,xRESPS[-1])
        # find appropriate upper y-axis limit for evenly spaced ticks
        s = str(int(max(yRESPS)))
        lim = int(math.ceil(max(yRESPS)/(10**(len(s)-1))))*(10**(len(s)-1))
        axRESPS.set_ylim(0,lim)
        
        labelRESPS = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axRESPS.plot(xRESPS,yRESPS,color='black',marker='o',markersize=4,
                   linestyle='solid',label = labelRESPS)
        axRESPS.legend()
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fRESPS.savefig(self.outPath[:self.outPath.index('.')]
                         +'-out-' + 'resPS' + '.png')
        # return figure to be drawn in canvas
        return fRESPS


    def plotChCap(self,results):
        """
        Total charge capacity vs. cycle number
        """
        xCH = results[2]
        yCH = results[6]
        fCH = plt.figure(4)
        axCH = fCH.add_subplot(111)
        axCH.set(title = 'Charge Capacity vs. Cycle Number',
                 xlabel = 'Cycle Number',ylabel = 'Charge Capacity (mA*h/cm\u00b2)')
        axCH.set_xlim(0,xCH[-1])
        # find appropriate upper y-axis limit for evenly spaced ticks
        if max(yCH) < 1:
            s = str(max(yCH)).split('.')[1]
            reg = re.compile(r'[1-9]')
            ind = reg.search(s).span()[0]
            lim = math.ceil(max(yCH)*(10**(ind+1)))/(10**(ind+1))
            axCH.set_ylim(0,lim)
        elif max(yCH) >= 1:
            s = str(int(max(yCH)))
            lim = int(math.ceil(max(yCH)/(10**(len(s)-1))))*(10**(len(s)-1))
            axCH.set_ylim(0,lim)
                                           
        labelCH = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axCH.plot(xCH,yCH,color='black',marker='o',markersize=4,linestyle='solid',label = labelCH)
        axCH.legend(loc='lower right')
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fCH.savefig(self.outPath[:self.outPath.index('.')]
                        +'-out-' + 'ChCap' + '.png')
        # return figure to be used in canvas
        return fCH

    def plotChPlat(self,results):
        """
        Charge Plateau Potential vs. cycle number
        """
        xCHP = results[2]
        yCHP = results[7]
        fCHP = plt.figure(5)
        axCHP = fCHP.add_subplot(111)
        axCHP.set(title = 'Charge Plateau Potential vs. Cycle Number',
                 xlabel = 'Cycle Number',ylabel = 'Charge Plateau Potential (V)')
        axCHP.set_xlim(0,xCHP[-1])
        # find appropriate upper y-axis limit for evenly spaced ticks
        if max(yCHP) >= 0 and min(yCHP) >= 0:
            upperLim = math.ceil(max(yCHP)*1)/1
            lowerLim = 0
        elif max(yCHP) >= 0 and min(yCHP) < 0:
            lowerLim = -math.ceil(-min(yCHP)*1)/1
            upperLim = math.ceil(max(yCHP)*1)/1
        elif max(yCHP) < 0 and min(yCHP) < 0:
            lowerLim = -math.ceil(-min(yCHP)*1)/1
            upperLim = 0
        axCHP.set_ylim(lowerLim,upperLim)
        
        labelCHP = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axCHP.plot(xCHP,yCHP,color='black',marker='o',markersize=4,linestyle='solid',label = labelCHP)
        axCHP.legend(loc='lower right')
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fCHP.savefig(self.outPath[:self.outPath.index('.')]
                        +'-out-' + 'ChPlat' + '.png')
        # return figure to be used in canvas
        return fCHP


    def plotDisCap(self,results):
        """
        Total discharge capacity vs. cycle number
        """
        xDIS = results[2]
        yDIS = results[8]
        fDIS = plt.figure(6)
        axDIS = fDIS.add_subplot(111)
        axDIS.set(title = 'Discharge Capacity vs. Cycle Number',
                  xlabel = 'Cycle Number',ylabel = 'Discharge Capacity (mA*h/cm\u00b2)')
        axDIS.set_xlim(0,xDIS[-1])
        # find appropriate upper y-axis limit for evenly spaced ticks
        if max(yDIS) < 1:
            s = str(max(yDIS)).split('.')[1]
            reg = re.compile(r'[1-9]')
            ind = reg.search(s).span()[0]
            lim = math.ceil(max(yDIS)*(10**(ind+1)))/(10**(ind+1))
            axDIS.set_ylim(0,lim)
        elif max(yDIS) >= 1:
            s = str(int(max(yDIS)))
            lim = int(math.ceil(max(yDIS)/(10**(len(s)-1))))*(10**(len(s)-1))
            axDIS.set_ylim(0,lim)
            
        labelDIS = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axDIS.plot(xDIS,yDIS,color='black',marker='o',markersize=4,
                   linestyle='solid',label = labelDIS)
        axDIS.legend(loc='lower right')
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fDIS.savefig(self.outPath[:self.outPath.index('.')]
                         +'-out-' + 'DisCap' + '.png')
        # return figure to be used in canvas
        return fDIS

    def plotDisPlat(self,results):
        """
        Discharge Plateau Potential vs. cycle number
        """
        xDISP = results[2]
        yDISP = results[9]
        fDISP = plt.figure(7)
        axDISP = fDISP.add_subplot(111)
        axDISP.set(title = 'Discharge Plateau Potential vs. Cycle Number',
                 xlabel = 'Cycle Number',ylabel = 'Discharge Plateau Potential (V)')
        axDISP.set_xlim(0,xDISP[-1])
        # find appropriate upper y-axis limit for evenly spaced ticks
        if max(yDISP) >= 0 and min(yDISP) >= 0:
            upperLim = math.ceil(max(yDISP)*1)/1
            lowerLim = 0
        elif max(yDISP) >= 0 and min(yDISP) < 0:
            lowerLim = -math.ceil(-min(yDISP)*1)/1
            upperLim = math.ceil(max(yDISP)*1)/1
        elif max(yDISP) < 0 and min(yDISP) < 0:
            lowerLim = -math.ceil(-min(yDISP)*1)/1
            upperLim = 0
        axDISP.set_ylim(lowerLim,upperLim)
            
        labelDISP = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axDISP.plot(xDISP,yDISP,color='black',marker='o',markersize=4,linestyle='solid',label = labelDISP)
        axDISP.legend(loc='lower right')
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fDISP.savefig(self.outPath[:self.outPath.index('.')]
                        +'-out-' + 'DIsPlat' + '.png')
        # return figure to be used in canvas
        return fDISP

    def plotPlatSep(self,results):
        """
        Charge-Discharge Plateau Separation vs. cycle number
        """
        xPS = results[2]
        yPS = results[10]
        fPS = plt.figure(8)
        axPS = fPS.add_subplot(111)
        axPS.set(title = 'Charge-Discharge Plateau Separation vs. Cycle Number',
                 xlabel = 'Cycle Number',ylabel = 'Charge-Discharge Plat. Sep. (V)')
        axPS.set_xlim(0,xPS[-1])
        if round(max(yPS))<max(yPS):
            axPS.set_ylim(0,round(max(yPS)+1))
        else:
            axPS.set_ylim(0,round(max(yPS)))
     
        labelPS = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axPS.plot(xPS,yPS,color='black',marker='o',markersize=4,linestyle='solid',label = labelPS)
        axPS.legend(loc='lower right')
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fPS.savefig(self.outPath[:self.outPath.index('.')]
                        +'-out-' + 'PlatSep' + '.png')
        # return figure to be used in canvas
        return fPS
    

    def plotDisPercent(self,results):
        """
        Total Discharge Percent above or below specified discharge potential threshold
        """        
        xDIST = results[2]
        yDIST = results[11]
        fDIST = plt.figure(9)
        axDIST = fDIST.add_subplot(111)
        axDIST.set(title = 'Discharge Percent %s %s V vs. Cycle Number' %
                   (self.compare,self.threshold),xlabel = 'Cycle Number',
                    ylabel = 'Discharge Percent %s %s V' %
                   (self.compare,self.threshold))
        axDIST.set_xlim(0,xDIST[-1])
        axDIST.set_ylim(0,100)
        labelDIST = '%s uA x %s seconds x %s' % (self.current,self.time,self.num)
        axDIST.plot(xDIST,yDIST,color='black',marker='o',markersize=4,
                     linestyle='solid',label = labelDIST)
        axDIST.legend(loc='lower right')
        # save plot results as figure if user selected radiobutton output option 3
        if self.saveOutput == True:
            fDIST.savefig(self.outPath[:self.outPath.index('.')]
                           +'-out-' + 'DisPercent' + '.png')
        # return figure to be used in canvas
        return fDIST

if __name__ == '__main__':

    root = tk.Tk()
    app = InputWindow(root)
    app.mainloop()



   
        
        



               
               
