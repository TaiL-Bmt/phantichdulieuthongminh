import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Read dataset *.csv file
df = pd.read_csv('./data/data-vn.csv')

# Do some clean data
df['income'] = df['income'].replace({',':'.'}, regex=True).astype(float)
df['outcome'] = df['outcome'].replace({',':'.'}, regex=True).astype(float)
df['food_expenditure'] = df['food_expenditure'].replace({',':'.'}, regex=True).astype(float)
df['area_norm'] = np.where(df['area'] != 'rural', 1, 0)
#df['area_norm'] = np.where(df['area'] != 'abc', 1, 0)
print(df.columns)
print(df)

outcome = df['outcome'].tolist()
income = df['income'].tolist()
people = df['people'].tolist()

#result = smf.ols('outcome ~ income + people', data=df).fit()
result = smf.ols('outcome ~ area_norm + income', data=df).fit()
print(result.summary())




# Graph scatter income/outcome
if 0:
    fig,ax = plt.subplots(1, 1)
    ax.scatter(df['income'], df['outcome'], color='b', edgecolor='grey')
    ax.set_xlabel('income')
    ax.set_ylabel('outcome')
    ax.set_title('income/outcome scatter figure')
    plt.show()

# Histogram graphs of income rural/urban
if 0:
    fig,ax = plt.subplots(1, 2)
    bins_number = 25
    # Rural
    df_rural= df.loc[df['area'] == 'rural']
    ax[0].hist(df_rural['income'], bins=bins_number, color='b', edgecolor='grey')
    ax[0].set_title('histogram of rural income')
    # Urban
    df_urban= df.loc[df['area'] == 'urban']
    ax[1].hist(df_urban['income'], bins=bins_number, color='green', edgecolor='grey')
    ax[1].set_title('histogram of urban income')

    plt.show()

# Contour graph of income/outcome
if 0:
    fig,ax = plt.subplots(1, 1)
    x = df['income']
    y = df['outcome']
    ax.set_title('seaborn graph')
    sns.kdeplot(df['income'], df['outcome'], ax=ax)
    #sns.rugplot(df['income'], color='g', ax=ax)
    #sns.rugplot(df['outcome'], vertical=True, ax=ax, color='k')
    plt.show()

# Stacked histogram
if 0:
    fix,ax = plt.subplots(1, 1)
    bins_number = 25
    # Rural
    df_rural= df.loc[df['area'] == 'rural']
    # Urban
    df_urban= df.loc[df['area'] == 'urban']
    ax.hist([df_rural['income'], df_urban['income']], bins=bins_number, color=['b', 'g'], edgecolor='grey', stacked=True)
    ax.set_title('Stacked histogram urban/rural income')

    plt.show()

