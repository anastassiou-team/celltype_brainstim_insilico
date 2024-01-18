import shutil

print ("Erasing...")

shutil.rmtree("R:/Temp/Threads3/")
shutil.copyfile('./required_files/Values.csv', './Calibrated.csv')