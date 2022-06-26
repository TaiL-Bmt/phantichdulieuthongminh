import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def convert_dtype(x):
    if not x:
        return ''
    try:
        return str(x)   
    except:        
        return ''
# Read dataset *.csv file
df = pd.read_csv('./dataset/players_16.csv', dtype={104: str})
print(df.dtypes)
print(df.columns)
print(df)

## Do some clean data
#df['income'] = df['income'].replace({',':'.'}, regex=True).astype(float)
#df['outcome'] = df['outcome'].replace({',':'.'}, regex=True).astype(float)
#df['food_expenditure'] = df['food_expenditure'].replace({',':'.'}, regex=True).astype(float)
#print(df.columns)
#
## Graph scatter income/outcome
#if 0:
#    fig,ax = plt.subplots(1, 1)
#    ax.scatter(df['income'], df['outcome'], color='b', edgecolor='grey')
#    ax.set_xlabel('income')
#    ax.set_ylabel('outcome')
#    ax.set_title('income/outcome scatter figure')
#    plt.show()
#
## Histogram graphs of income rural/urban
#if 0:
#    fig,ax = plt.subplots(1, 2)
#    bins_number = 25
#    # Rural
#    df_rural= df.loc[df['area'] == 'rural']
#    ax[0].hist(df_rural['income'], bins=bins_number, color='b', edgecolor='grey')
#    ax[0].set_title('histogram of rural income')
#    # Urban
#    df_urban= df.loc[df['area'] == 'urban']
#    ax[1].hist(df_urban['income'], bins=bins_number, color='green', edgecolor='grey')
#    ax[1].set_title('histogram of urban income')
#
#    plt.show()
#
## Contour graph of income/outcome
#if 0:
#    fig,ax = plt.subplots(1, 1)
#    x = df['income']
#    y = df['outcome']
#    ax.set_title('seaborn graph')
#    sns.kdeplot(df['income'], df['outcome'], ax=ax)
#    #sns.rugplot(df['income'], color='g', ax=ax)
#    #sns.rugplot(df['outcome'], vertical=True, ax=ax, color='k')
#    plt.show()
#
## Stacked histogram
#if 1:
#    fix,ax = plt.subplots(1, 1)
#    bins_number = 25
#    # Rural
#    df_rural= df.loc[df['area'] == 'rural']
#    # Urban
#    df_urban= df.loc[df['area'] == 'urban']
#    ax.hist([df_rural['income'], df_urban['income']], bins=bins_number, color=['b', 'g'], edgecolor='grey', stacked=True)
#    ax.set_title('Stacked histogram urban/rural income')
#
#    plt.show()

