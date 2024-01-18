import pandas as pd
import numpy as np

a = np.zeros(40) + 0.6
df = pd.DataFrame(a,columns = ['Mean'])
df['StD'] = 0.1
df['SM'] = 0.1
df['SS'] = 0.1
df['PM'] = 0
df['PS'] = 0

df.to_csv('./required_files/Values.csv', index = False)