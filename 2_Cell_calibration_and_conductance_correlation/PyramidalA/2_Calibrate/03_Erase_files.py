import shutil

print ("Erasing...")

shutil.rmtree("R:/Temp/Threads2/")
shutil.copyfile('./required_files/Values.csv', './Calibrated.csv')