@ECHO OFF

for /l %%h in (0, 1, 0) do (
    for /l %%d in (50, 48, 1000) do (
        python  "01_Set_up.py" %%d %%h
        (
            start python  "R:/Temp/Threads6/Thread0/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread1/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread2/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread3/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread4/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread5/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread6/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread7/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread8/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread9/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread10/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread11/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread12/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread13/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread14/Simulation_(Main).py" 0
            start python  "R:/Temp/Threads6/Thread15/Simulation_(Main).py" 0
        ) | PAUSE
        python  "02_Gather_Data.py" "Entrain" %%d %%h
        python  "03_Erase_files.py"
        
        python  "01_Set_up.py" %%d %%h
        (
            start python  "R:/Temp/Threads6/Thread0/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread1/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread2/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread3/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread4/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread5/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread6/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread7/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread8/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread9/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread10/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread11/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread12/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread13/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread14/Simulation_(Main).py" 1
            start python  "R:/Temp/Threads6/Thread15/Simulation_(Main).py" 1
        ) | PAUSE
        python  "02_Gather_Data.py" "Control" %%d %%h
        python  "03_Erase_files.py"
    )
)
