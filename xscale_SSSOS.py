#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Created on Mon Aug  4 17:17:39 2014
Copyright (c) 2014, Nicolas Foos
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/
or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE."""

import os
import sys
import re
import time

def StartingOpen():   
    """ Function open the initial XSCALE.INP file,
        The easyest way to work is to use standard XSACLE.INP correctly setup 
        with the default parameters you want (output, input). On way is to use
        xscale2.py from Pierre Legrand
        This function return xdsinp which is list containing all the XSCALE.INP 
        lines.     
    """
# arg is global, because it's re-used during code execution as parameters to
# find the relativ-path.           
    global arg2
    for arg in sys.argv[1:]:
        arg2 = os.path.abspath(arg)
        try:
            if os.path.isfile(arg2):
                with open(arg2) as input_file :
                    global xdsinp                    
                    xdsinp = input_file.readlines()
                    for lines in xdsinp :
                        if re.search(r"XSCALE", lines):
                            create = True
                    if create == True:
                        print "XSCALE.INP is take in count"
                        return create
                        return xdsinp
                        return arg2
                    
        except:
            print ("it's not XSCALE.INP or it's corrupted")
            exit(0)       

def makeResultFile(create):
    """ Function create folder to write the file generate by other function
        Default name is given to avoid conflict or error.    
    """    
    if create :        
        resultFile = raw_input ('give name for result file, default is : result.' \
+str(time.time())+ ' :')
        if resultFile == '' :
             resultFile = "result."+ str(time.time())
        else :
            resultFile = resultFile
        try:
            os.makedirs(resultFile, 0777)
            return resultFile
        except OSError:
            print 'WARNING : Problem to create Directory for results'
            
def symlink_creation(srcFile, dest):
    os.symlink(srcFile, dest)   

def writing_list_in_file(path, file2write):
    """ Function to write string contain in a list 
    """    
    outputfile = open(os.path.join(path, "XSCALE.INP"), 'a')
    for line in file2write:    
        outputfile.write(line)
        
#function to edit the file path    
def editFilePath(xdsinp):
    """ Function to modify the path write in original XSCALE.INP, 
        the new path write in the new XSCALE.INP create, will be set according 
        the right path to read the symlink create by the symlink creation 
        function. The old path is change in 0,1,2... .HKL corrsponding to 
        the symlink 
    """
    numberOfFile = []
    for lines in xdsinp:
        if re.findall(r"INPUT_FILE=", lines):
            numberOfFile.append(lines)
            xdsinp.__setitem__(xdsinp.index(lines), "   INPUT_FILE= ../"+str(numberOfFile.index(lines))+".HKL\n")

def changeFriedelsettings(xdsinp, settings):
    if "-ano" in settings:
        for lines in xdsinp:
            if re.findall(r"FRIEDEL'S_LAW=", lines):
                xdsinp.__setitem__(xdsinp.index(lines), "      FRIEDEL'S_LAW= FALSE\n")
    else :
        for lines in xdsinp:
            if re.findall(r"FRIEDEL'S_LAW=", lines):
                xdsinp.__setitem__(xdsinp.index(lines), "      FRIEDEL'S_LAW= TRUE\n")

def settings_XDS_strictAbsCorr(xdsinp, settings):
    if "-sa" in settings:
        for lines in xdsinp:
            if re.findall(r"STRICT_ABSORPTION_CORRECTION=", lines):
                xdsinp.__setitem__(xdsinp.index(lines), "STRICT_ABSORPTION_CORRECTION= TRUE \n" )
    else :
        for lines in xdsinp:
            if re.findall(r"STRICT_ABSORPTION_CORRECTION=", lines):
                xdsinp.__setitem__(xdsinp.index(lines), "STRICT_ABSORPTION_CORRECTION= FALSE \n" )
        pass

def zerodDose(xdsinp, settings):
    if "-zd" in settings:
        for lines in xdsinp:
            if re.findall(r"INPUT_FILE=", lines):        
                 xdsinp.insert(xdsinp.index(lines)+1, "      CRYSTAL_NAME=something\n")
    else :
        pass

def merge(xdsinp, settings):
    if "-merge" in settings:
        for lines in xdsinp:
            if re.findall(r"OUTPUT_FILE=", lines):
                xdsinp.insert(xdsinp.index(lines)+1, "    MERGE=TRUE\n")
    else :
        pass

def correction(xdsinp, settings):
    if "-corr" in settings:
        for lines in xdsinp:
            if re.findall(r"INPUT_FILE=", lines):        
                xdsinp.insert(xdsinp.index(lines)+1, "      CORRECTIONS= DECAY MODULATION ABSORBTION\n")
    elif "-corr-none" in settings:
        for lines in xdsinp:
            if re.findall(r"INPUT_FILE=", lines):        
                xdsinp.insert(xdsinp.index(lines)+1, "      CORRECTIONS=!\n")      
    elif "-decay" in settings : 
         for lines in xdsinp:           
            if re.findall(r"INPUT_FILE=", lines):        
                xdsinp.insert(xdsinp.index(lines)+1, "      CORRECTIONS= DECAY\n")
    elif "-mod" in settings :
         for lines in xdsinp:
            if re.findall(r"INPUT_FILE=", lines):        
                xdsinp.insert(xdsinp.index(lines)+1, "      CORRECTIONS= MODULATION\n")       
    elif  "-abs" in settings :
         for lines in xdsinp:
            if re.findall(r"INPUT_FILE=", lines):        
                 xdsinp.insert(xdsinp.index(lines)+1, "      CORRECTIONS= ABSORBTION\n") 
    elif  "-dec_mod" in settings :
         for lines in xdsinp:
            if re.findall(r"INPUT_FILE=", lines):        
                 xdsinp.insert(xdsinp.index(lines)+1, "      CORRECTIONS= DECAY MODULATION\n")                 
    elif  "-dec_abs" in settings :
         for lines in xdsinp:
            if re.findall(r"INPUT_FILE=", lines):        
                 xdsinp.insert(xdsinp.index(lines)+1, "      CORRECTIONS= DECAY ABSORBTION\n")                 
    elif  "-mod_abs" in settings :
         for lines in xdsinp:
            if re.findall(r"INPUT_FILE=", lines):        
                 xdsinp.insert(xdsinp.index(lines)+1, "      CORRECTIONS= MODULATION ABSORBTION\n")                 
                 

def resolutionMax(xdsinp):
    global resMax   
    try :
        resMax = float(raw_input('set the resolution maxi, default is : the one used originaly in your input files : '))
        for lines in xdsinp:
            if re.findall(r"INCLUDE_RESOLUTION_RANGE=", lines):               
                xdsinp.__setitem__(xdsinp.index(lines), "INCLUDE_RESOLUTION_RANGE= 50.000    "+str(resMax)+"\n")    
    except : 
        #except is using to take in count the case where the user doesn't 
        # want to modify the resolutuion parameter
        for lines in xdsinp:
            if re.findall(r"INCLUDE_RESOLUTION_RANGE=", lines):
                resMax = float(lines[-10:])  


def resolutionShells(xdsinp):
    shellsToUse = []
    listOFres = [20, 15, 10, 6, 4, 3, 2.5, 2.2, 2, 1.8, 1.7, 1.6]
    for nb in listOFres:
        if nb >= resMax:
            shellsToUse.append(nb)
            for lines in xdsinp:
                if re.findall(r"RESOLUTION_SHELLS=", lines):
                    xdsinp.__setitem__(xdsinp.index(lines), "RESOLUTION_SHELLS="+str(shellsToUse))
            for lines in xdsinp:
                if re.findall(r"RESOLUTION_SHELLS=", lines):            
                    newline = lines            
                    newline = newline.replace("[", " ")
                    newline = newline.replace("]", "\n")
                    newline = newline.replace(",", "")
                    xdsinp.__setitem__(xdsinp.index(lines), newline)

def givenUserOption():
    option1 = raw_input ('Please chose if you want to use the parameter \
    ZERO_DOSE [N/y] : ')
    if option1 == '' :
        option1 = 'N'
    else:
        option1 = option1
    
    option2 = raw_input ('Please choose if you want to modify the corrections parameters\
 concern CORRECTION options : "m" for MODULATION, "d" for DECAY, "a" for\
 ABSORP, "n" for NONE default is ALL (example : md):')
    if option2 =='':
        option2 = 'all'
    else:
        option2 = option2
    listofOptions = [option1, option2] 
    return listofOptions
    

# this defined schemes for automatic usage of this script in order to 
# test different strategy of scaling with XSCALE

scheme0 = [ "-corr", "-sa0"]
scheme1 = [ "-corr", "-sa1"] 
scheme2 = [ "-corr", "-sa2"]

scheme0_1 = [ "-decay", "-sa0"]
scheme0_2 = [ "-modul", "-sa0"]
scheme0_3 = [ "-abs", "-sa0"]
scheme0_4 = [ "-dec_mod", "-sa0"]
scheme0_5 = [ "-dec_abs", "-sa0"]
scheme0_6 = [ "-mod_abs", "-sa0"]
scheme0_7 = [ "-corr_none", "-sa0"]

scheme1_1 = [ "-decay", "-sa1"]
scheme1_2 = [ "-modul", "-sa1"]
scheme1_3 = [ "-abs", "-sa1"]
scheme1_4 = [ "-dec_mod", "-sa1"]
scheme1_5 = [ "-dec_abs", "-sa1"]
scheme1_6 = [ "-mod_abs", "-sa1"]
scheme1_7 = [ "-corr_none", "-sa1"]

scheme2_1 = [ "-decay", "-sa2"]
scheme2_2 = [ "-modul", "-sa2"]
scheme2_3 = [ "-abs", "-sa2"]
scheme2_4 = [ "-dec_mod", "-sa2"]
scheme2_5 = [ "-dec_abs", "-sa2"]
scheme2_6 = [ "-mod_abs", "-sa2"]
scheme2_7 = [ "-corr_none", "-sa2"] 
 
scheme0_a = [ "-zd", "-corr", "-sa0"]
scheme1_a = [ "-zd", "-corr", "-sa1"] 
scheme2_a = [ "-zd", "-corr", "-sa2"] 
 
 
scheme0_1_a = [ "-zd", "-zd1", "-decay", "-sa0"]
scheme0_2_a = [ "-zd", "-zd1", "-modul", "-sa0"]
scheme0_3_a = [ "-zd", "-zd1", "-abs", "-sa0"]
scheme0_4_a = [ "-zd", "-zd1", "-dec_mod", "-sa0"]
scheme0_5_a = [ "-zd", "-zd1", "-dec_abs", "-sa0"]
scheme0_6_a = [ "-zd", "-zd1", "-mod_abs", "-sa0"]
scheme0_7_a = [ "-zd", "-zd1", "-corr_none", "-sa0"]

scheme1_1_a = [ "-zd", "-zd1", "-decay", "-sa1"]
scheme1_2_a = [ "-zd", "-zd1", "-modul", "-sa1"]
scheme1_3_a = [ "-zd", "-zd1", "-abs", "-sa1"]
scheme1_4_a = [ "-zd", "-zd1", "-dec_mod", "-sa1"]
scheme1_5_a = [ "-zd", "-zd1", "-dec_abs", "-sa1"]
scheme1_6_a = [ "-zd", "-zd1", "-mod_abs", "-sa1"]
scheme1_7_a = [ "-zd", "-zd1", "-corr_none", "-sa1"]

scheme2_1_a = [ "-zd", "-zd1", "-decay", "-sa2"]
scheme2_2_a = [ "-zd", "-zd1", "-modul", "-sa2"]
scheme2_3_a = [ "-zd", "-zd1", "-abs", "-sa2"]
scheme2_4_a = [ "-zd", "-zd1", "-dec_mod", "-sa2"]
scheme2_5_a = [ "-zd", "-zd1", "-dec_abs", "-sa2"]
scheme2_6_a = [ "-zd", "-zd1", "-mod_abs", "-sa2"]
scheme2_7_a = [ "-zd", "-zd1", "-corr_none", "-sa2"]
 
listOfexperiment1 = [scheme0, scheme1, scheme2]
listOfexperiment2 = [scheme0_7, scheme1_7, scheme2_7]
listOfexperiment3 = [scheme0_2, scheme1_2, scheme2_2]
listOfexperiment4 = [scheme0_1, scheme1_1, scheme2_1]
listOfexperiment5 = [scheme0_3, scheme1_3, scheme2_3]
listOfexperiment6 = [scheme0_5, scheme1_5, scheme2_5]
listOfexperiment7 = [scheme0_4, scheme1_4, scheme2_4]
listOfexperiment8 = [scheme0_6, scheme1_6, scheme2_6]

listOfexperiment1_a = [scheme0_a, scheme1_a, scheme2_a]
listOfexperiment2_a = [scheme0_7_a, scheme1_7_a, scheme2_7_a]
listOfexperiment3_a = [scheme0_2_a, scheme1_2_a, scheme2_2_a]
listOfexperiment4_a = [scheme0_1_a, scheme1_1_a, scheme2_1_a]
listOfexperiment5_a = [scheme0_3_a, scheme1_3_a, scheme2_3_a]
listOfexperiment6_a = [scheme0_5_a, scheme1_5_a, scheme2_5_a]
listOfexperiment7_a = [scheme0_4_a, scheme1_4_a, scheme2_4_a]
listOfexperiment8_a = [scheme0_6_a, scheme1_6_a, scheme2_6_a]

listofOptions = givenUserOption()
if listofOptions[0] == 'y':
    zd = 'zd1'
else :
    zd = 'zd0'
if listofOptions[1] == 'm':
   corr = 'modulation'
elif listofOptions[1] == 'd':
   corr = 'decay'
elif listofOptions[1] == 'a':
   corr = 'absorp'
elif listofOptions[1] == 'n':
   corr = 'none'     
elif listofOptions[1] == 'all':
   corr = 'all'
elif listofOptions[1] == 'da' or 'ad':
   corr = 'abs_dec'
elif listofOptions[1] == 'dm' or 'md':
   corr = 'mod_dec'
else :
   corr = 'abs_mod'

if zd == 'zd0' and corr == 'all':
    listOfexperiment = listOfexperiment1
elif zd == 'zd0' and corr == 'none':
    listOfexperiment = listOfexperiment2
elif zd == 'zd0' and corr == 'modulation':
    listOfexperiment = listOfexperiment3
elif zd == 'zd0' and corr == 'decay':
    listOfexperiment = listOfexperiment4
elif zd == 'zd0' and corr == 'absorp':
    listOfexperiment = listOfexperiment5
elif zd == 'zd0' and corr == 'abs_dec':
    listOfexperiment = listOfexperiment6    
elif zd == 'zd0' and corr == 'mod_dec':
    listOfexperiment = listOfexperiment7
elif zd == 'zd0' and corr == 'abs_mod':
    listOfexperiment = listOfexperiment8   
    
elif zd == 'zd1' and corr == 'all':
    listOfexperiment = listOfexperiment1_a
elif zd == 'zd1' and corr == 'none':
    listOfexperiment = listOfexperiment2_a
elif zd == 'zd1' and corr == 'modulation':
    listOfexperiment = listOfexperiment3_a
elif zd == 'zd1' and corr == 'decay':
    listOfexperiment = listOfexperiment4_a
elif zd == 'zd1' and corr == 'absorp':
    listOfexperiment = listOfexperiment5_a
elif zd == 'zd1' and corr == 'abs_dec':
    listOfexperiment = listOfexperiment6_a    
elif zd == 'zd1' and corr == 'mod_dec':
    listOfexperiment = listOfexperiment7_a
elif zd == 'zd1' and corr == 'abs_mod':
    listOfexperiment = listOfexperiment8_a 

listOfFile = []             
#open file and create output directory
create = StartingOpen()
resultFile = makeResultFile(create)
resolutionMax(xdsinp)
# create link which point to the original XDS_ASCII.HKL files
for lines in xdsinp:
    if re.findall(r"INPUT_FILE=", lines):
        listOfFile.append(lines)
for i in listOfFile:
    #this line correspond to the need of only one parts of the original path
    # initially typed by the user. It's concatenation of the strating parts of
    # the original path typed and the current path to the symlink newly created
    # just before.
    link = symlink_creation(arg2[:-10]+i[15:-1], "./"+str(resultFile)+"/"+str(listOfFile.index(i))+".HKL")
listofFolder = []
for scheme in listOfexperiment:
    # create differents folders for each scheme used
    listofFolder.append(resultFile+"/"+"scheme"+ str(listOfexperiment.index(scheme)))
for path in listofFolder:
    os.mkdir(path)   

file2write = []
for scheme in listOfexperiment:
    settings = scheme
    editFilePath(xdsinp)    
    resolutionShells(xdsinp)
    changeFriedelsettings(xdsinp, settings)
    merge(xdsinp, settings)
# the line just after remove the CORRECTION, CRYSTAL_NAME, STRICT_ABSORBTION
# already write by the precedent round of the loop    
    for line in xdsinp:    
        if re.findall(r"CORRECTIONS=", line):        
            xdsinp.pop(xdsinp.index(line))
    correction(xdsinp, settings)
    for line in xdsinp:    
        if re.findall(r"CRYSTAL_NAME=", line):        
            xdsinp.pop(xdsinp.index(line))   
    zerodDose(xdsinp, settings)
    for line in xdsinp:    
        if re.findall(r"STRICT_ABSORPTION=", line):        
            xdsinp.pop(xdsinp.index(line))     
    settings_XDS_strictAbsCorr(xdsinp, settings)
    i = listOfexperiment.index(scheme)
# writing XSCALE.INP at each round of the loop, because xdsinp is modify 
# iterativelly and that caused the loose of your parameters
    pathXscaleInp = str(listofFolder[i])+"/"
    writing_list_in_file(pathXscaleInp, xdsinp)



