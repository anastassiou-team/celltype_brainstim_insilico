import subprocess

result = subprocess.run(["python", "00_Initialize.py"], capture_output=True, text=True, check=True)
print('output: ', result.stdout)
print('error: ', result.stderr)

for stp in range(1000):
    print ("-----------------------------------------------Runnning STEP: "+str(stp))
    result = subprocess.run(["python", "01_Set_up.py"], capture_output=True, text=True, check=True)
    print('output: ', result.stdout)
    print('error: ', result.stderr)

    processes = []
    for j in range(40):
        comnd = ["python", "R:/Temp/Threads2/Thread"+str(j)+"/Simulation_(Main).py"]
        p = subprocess.Popen(comnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(p)           
    for p in processes:
        p.wait()
        output, error = p.communicate()
        print(f'Output of {p.args}: {output.decode()}')
        print(f'Error of {p.args}: {error.decode()}')
            
    result = subprocess.run(["python", "02_Generate.py"], capture_output=True, text=True, check=True)
    print('output: ', result.stdout)
    print('error: ', result.stderr)
    
    result = subprocess.run(["python", "03_Erase_files.py"], capture_output=True, text=True, check=True)
    print('output: ', result.stdout)
    print('error: ', result.stderr)
