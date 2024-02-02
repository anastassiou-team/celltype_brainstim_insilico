import shutil

print ("Erasing...")

shutil.rmtree("R:/Temp/Threads10/")
shutil.copyfile('./required_files/Values.csv', './Calibrated.csv')