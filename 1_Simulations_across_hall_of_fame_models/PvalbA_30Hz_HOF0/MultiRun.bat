@ECHO OFF

for /l %%d in (200, 48, 1200) do (
	python  "01_Set_up.py" %%d 0
	(
		start python  "R:/Temp/Threads3/Thread0/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread1/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread2/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread3/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread4/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread5/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread6/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread7/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread8/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread9/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread10/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread11/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread12/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread13/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread14/Simulation_(Main).py" 0
		start python  "R:/Temp/Threads3/Thread15/Simulation_(Main).py" 0
	) | PAUSE
	python  "02_Gather_Data.py" "Entrain" %%d 0
	python  "03_Erase_files.py"
	
	python  "01_Set_up.py" %%d 0
	(
		start python  "R:/Temp/Threads3/Thread0/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread1/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread2/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread3/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread4/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread5/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread6/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread7/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread8/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread9/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread10/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread11/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread12/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread13/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread14/Simulation_(Main).py" 1
		start python  "R:/Temp/Threads3/Thread15/Simulation_(Main).py" 1
	) | PAUSE
	python  "02_Gather_Data.py" "Control" %%d 0
	python  "03_Erase_files.py"
)
