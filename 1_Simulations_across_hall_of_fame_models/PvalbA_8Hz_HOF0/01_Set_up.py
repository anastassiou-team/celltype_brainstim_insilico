file_name = 'CellJ.json'
rotationXY = 0 #degrees XY
rotationYZ = 0 #degrees YZ
rotationXZ = 0 #degrees XZ

import math as mth
import neurom as nm
from neurom import viewer
from matplotlib.backends.backend_pdf import PdfPages
from subprocess import call
import os, shutil, sys

#Rotate morphologies
pp = PdfPages('./Results/Cells.pdf')
inFile = "./required_files/neuronal_model/" + file_name.replace("J.json", ".swc")
outFile = inFile.replace(".swc", "_rotated.swc")
rotationXY = (mth.pi/180)*rotationXY
rotationYZ = (mth.pi/180)*rotationYZ 
rotationXZ = (mth.pi/180)*rotationXZ

m = nm.load_morphology(inFile)
fig, ax = viewer.draw(m)
ax.set_title("Before")
fig.show()

fin = open(inFile, "rt")
fout = open(outFile, "wt")
xo=0
yo=0
zo=0
for line in fin:
        if line[0] == "#":
            fout.write(line)
        else:
            d,t,x,y,z,r,p = line.split(" ")
            if float(t)==1:
                line = d+" "+t+" {0:.4f}".format(0)+" {0:.4f}".format(0)+" {0:.4f}".format(0)+" "+r+" "+p
                fout.write(line)
                xo=float(x)
                yo=float(y)
                zo=float(z)
            else:
                x=float(x)-xo
                y=float(y)-yo
                z=float(z)-zo
                xn = x*mth.cos(rotationXY)-y*mth.sin(rotationXY)
                y = x*mth.sin(rotationXY)+y*mth.cos(rotationXY)
                x = xn
                yn = y*mth.cos(rotationYZ)-z*mth.sin(rotationYZ)
                z = y*mth.sin(rotationYZ)+z*mth.cos(rotationYZ)
                y = yn
                xn = x*mth.cos(rotationXZ)-z*mth.sin(rotationXZ)
                z = x*mth.sin(rotationXZ)+z*mth.cos(rotationXZ)
                x = xn
                line = d+" "+t+" {0:.4f}".format(x)+" {0:.4f}".format(y)+" {0:.4f}".format(z)+" "+r+" "+p
                #if int(t)!=2:
                fout.write(line)

fin.close()
fout.close()

m = nm.load_morphology(outFile)
fig, ax = nm.viewer.draw(m)
ax.set_title(file_name.replace("J.json", ''))
pp.savefig(fig)
pp.close()

#Set up Json files
inFile = "./required_files/neuronal_model/hof_param_569998790_" + sys.argv[2]+".json"
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
    
#Compile mechanisms
status=call("nrnivmodl modfiles",cwd='./required_files/neuronal_model',shell=True)
if status:
    raise ValueError('NEURON ERROR')
else:
    print ("Mechanisms compiled.")

#Create threads
os.mkdir('R:/Temp/Threads2/')
for i in range(0,16):
    base_name = 'R:/Temp/Threads2/Thread'+str(i)+'/'
    os.mkdir(base_name)
    os.mkdir(base_name+'neuronal_model/')
    shutil.copyfile('./required_files/neuronal_model/'+file_name.replace("J.json", "_rotated.swc"), base_name+'neuronal_model/Cell_rotated.swc')
    shutil.copyfile('./required_files/neuronal_model/'+file_name.replace(".json","_fixed.json"), base_name+'neuronal_model/CellJ_fixed.json')
    shutil.copyfile('./required_files/Simulation_(Main).py', base_name+'Simulation_(Main).py')
    shutil.copytree('./required_files/neuronal_model/modfiles',base_name+'neuronal_model/modfiles')
    shutil.copyfile('./required_files/neuronal_model/nrnmech.dll', base_name+'neuronal_model/nrnmech.dll')
    lines = []
    fin = open(base_name+'Simulation_(Main).py', "rt")
    cnt = 0
    for line in fin:
        if cnt == 0:
            lines.append('BaseDir = "R:/Temp/Threads2/Thread'+str(i)+'"\n')
        elif cnt == 1:
            lines.append('InnCurr = '+str(int(sys.argv[1])+i*3)+'\n')
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
        for i in range(0,16):
            if i == 15:
                nl = nl + str(int(sys.argv[1])+i*3) + '"]\n'
            else:
                nl = nl + str(int(sys.argv[1])+i*3) + '", "'
        lines.append(nl)
    else:
        lines.append(line)
    cnt += 1
fin.close()
fout = open('./02_Gather_Data.py', "wt")
for line in lines:
    fout.write(line)
fout.close()