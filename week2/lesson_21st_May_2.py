import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read dataset *.csv file
df1 = pd.read_csv('./data/24_HCM_XULN_sheet1.csv')
df2 = pd.read_csv('./data/24_HCM_XULN_sheet2.csv')
df = pd.concat([df1, df2])
#print('df shape is', df.shape)

# Do some clean data
# Clean redundant spaces
df['DIEM_THI'].replace(r'(\:\s*)', ':', regex=True, inplace=True)
# Extract Maths score to another column
df['Maths'] = df['DIEM_THI'].str.extract(r'(Maths\:\S*)', expand=True)
df['Maths'] = df['Maths'].str.extract(r'(\d\S*)', expand=True).astype(float)
df_maths = df['Maths'].dropna()
print("df_maths shape: ", df_maths.shape)

# calculate the number of pupils attend maths test and not
df_maths_number = pd.DataFrame([[df['Maths'].isna().sum(), df['Maths'].count()]], columns=['not join', 'join'])

if 1:
    fig,ax = plt.subplots(1, 2)

    # Histogram graph for Maths scores
    ax[0].hist(df_maths, bins=20, edgecolor='grey')
    ax[0].set_title('income/outcome scatter figure')

    # Bar chart; join and not join
    ax[1].bar(df_maths_number.columns, df_maths_number.loc[0].to_numpy(), edgecolor='grey')
    ax[1].set_title('The number of pupils joined and not-joined Maths test')
    ax[1].yaxis.grid(color='blue', linewidth=0.25)

    plt.show()

