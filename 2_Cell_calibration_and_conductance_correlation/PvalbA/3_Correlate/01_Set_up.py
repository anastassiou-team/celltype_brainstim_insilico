model = "hof_param_569998790_"
file_name = 'CellJ.json'

import os, shutil, sys
import pandas as pd

valus = pd.read_csv('./required_files/Values.csv')

#Create threads
os.mkdir('R:/Temp/Threads10/')
for hof in range(0,40):
    #Set up Json files
    inFile = "./required_files/neuronal_model/" + model + str(hof) +".json"
    outFile = "./required_files/neuronal_model/" + file_name.replace(".json","_fixed.json")

    #Read Cm, Epas and Ra values
    fin = open(inFile, "rt")
    cms = []
    eps = []
    ras = []
    lines = []
    linecount = 0
    for line in fin:
        if "section" in line:
            sec = line.split(":")[1].split(",")[0].split('"')[1]
        if "name" in line:
            name = line.split(":")[1].split(",")[0].split('"')[1]
        if "value" in line:
            val = line.split(":")[1].split(",")[0].split('"')[1]
            if "cm" in name:
                cms.append(sec + " " + val)
                for i in range(linecount-3,linecount+3):
                    lines.append(i)
            elif "e_pas" in name:
                eps.append(sec + " " + val)
                for i in range(linecount-3,linecount+3):
                    lines.append(i)
            elif "Ra" in name:
                ras.append(sec + " " + val)
                for i in range(linecount-3,linecount+3):
                    lines.append(i)
        linecount += 1
    fin.close()

    #Verify Epas same for all sections
    ep=0
    for i in eps:
        if float(i.split(" ")[1]) != float(eps[0].split(" ")[1]):
            raise ValueError('Not all e_pas same!!')
        else:
            ep = eps[0].split(" ")[1]

    #Verify Ra same for all sections
    ra=0
    for i in ras:
        if float(i.split(" ")[1]) != float(ras[0].split(" ")[1]):
            raise ValueError('Not all ra same!!')
        else:
            ra = ras[0].split(" ")[1]

    #Recreate file
    fin = open(inFile, "rt")
    fout = open(outFile, "wt")
    fout.write('{\n')
    fout.write('    "passive":[\n')
    fout.write('        {\n')
    fout.write('            "ra": '+str(ra) + ',\n')
    fout.write('            "cm": [\n')
    for i in cms:
        fout.write('                {\n')
        fout.write('                    "section": "' + i.split(" ")[0] + '",\n')
        fout.write('                    "cm": ' + i.split(" ")[1] + '\n')
        if i != cms[-1]:
            fout.write('                },\n')
        else:
            fout.write('                }\n')
    fout.write('            ],\n')
    fout.write('            "e_pas": ' + str(ep) + '\n')
    fout.write('        }\n')
    fout.write('    ],\n')
    linecount = 0
    passive_section_flag = 1
    stall = 0
    for line in fin:
        if passive_section_flag:
            if "]," in line:
                passive_section_flag = 0
        elif linecount not in lines:
            if stall == 0:
                if "value" in line:
                    nline = line.replace('"', '')
                    nline = nline.replace('value', '"value"')
                    fout.write(nline)
                elif "}," in line:
                    stall = line
                else:
                    fout.write(line)
            else:
                if "{" in line:
                    fout.write(stall)
                    fout.write(line)
                    stall = 0
                else:
                    fout.write(stall.replace(',',''))
                    stall = 0
                    if "value" in line:
                        nline = line.replace('"', '')
                        nline = nline.replace('value', '"value"')
                        fout.write(nline)
                    elif "}," in line:
                        stall = line
                    else:
                        fout.write(line)
        linecount += 1
    fin.close()
    fout.close()
    
    base_name = 'R:/Temp/Threads10/Thread'+str(hof)+'/'
    os.mkdir(base_name)
    os.mkdir(base_name+'neuronal_model/')
    shutil.copyfile('./required_files/neuronal_model/'+file_name.replace("J.json", "_rotated.swc"), base_name+'neuronal_model/Cell_rotated.swc')
    shutil.copyfile('./required_files/neuronal_model/'+file_name.replace(".json","_fixed.json"), base_name+'neuronal_model/CellJ_fixed.json')
    shutil.copyfile('./required_files/Simulation_(Main).py', base_name+'Simulation_(Main).py')
    shutil.copyfile('./required_files/ais_functions.py', base_name+'ais_functions.py')
    shutil.copyfile('./required_files/cell_functions.py', base_name+'cell_functions.py')
    shutil.copytree('./required_files/neuronal_model/modfiles',base_name+'neuronal_model/modfiles')
    shutil.copyfile('./required_files/neuronal_model/nrnmech.dll', base_name+'neuronal_model/nrnmech.dll')
    lines = []
    fin = open(base_name+'Simulation_(Main).py', "rt")
    cnt = 0
    for line in fin:
        if cnt == 0:
            lines.append('BaseDir = "R:/Temp/Threads10/Thread'+str(hof)+'"\n')
        elif cnt == 1:
            lines.append('InnCurr = '+str(valus.iloc[hof,0])+'\n')
        elif cnt == 2:
            lines.append('MeanCurr = '+str(valus.iloc[hof,1])+'\n')
        else:
            lines.append(line)
        cnt += 1
    fin.close()
    fout = open(base_name+'Simulation_(Main).py', "wt")
    for line in lines:
        fout.write(line)
    fout.close()

lines = []
fin = open('./02_Gather_Data.py', "rt")
cnt = 0
for line in fin:
    if cnt == 0:
        nl = 'clmns = ["'
        for i in range(0,40):
            if i == 39:
                nl = nl + str(i) + '"]\n'
            else:
                nl = nl + str(i) + '", "'
        lines.append(nl)
    else:
        lines.append(line)
    cnt += 1
fin.close()
fout = open('./02_Gather_Data.py', "wt")
for line in lines:
    fout.write(line)
fout.close()