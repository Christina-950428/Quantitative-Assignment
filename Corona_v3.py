# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 16:43:07 2021

@author: wuxin
"""
# import libraries
import pandas as pd
from datetime import datetime
import datetime
import matplotlib.pyplot as plt
import numpy as np
import plotly
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import missingno as msno
#pip install cufflinks
#pip install missingno
import cufflinks as cf
cf.go_offline()

# import raw data
GMVi_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/changes-visitors-covid.csv'
test_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/covid-19-testing-policy.csv'
cont_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/covid-contact-tracing.csv'
containHealth_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/covid-containment-and-health-index.csv'
strin_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/covid-stringency-index.csv'
covidnum_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/Excel Covid Data.csv'
face_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/face-covering-policies-covid.csv'
intMove_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/internal-movement-covid.csv'
internalTrav_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/international-travel-covid.csv'
pubCamp_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/public-campaigns-covid.csv'
pubEv_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/public-events-covid.csv'
pubGath_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/public-gathering-rules-covid.csv'
pubTrans_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/public-transport-covid.csv'
scho_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/school-closures-covid.csv'
stayhome_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/stay-at-home-covid.csv'
workpl_sour = 'C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/Data/workplace-closures-covid.csv'

# x variables
GMVi_df = pd.read_csv(GMVi_sour,usecols=[1,2,3,4,5,6,7,8])
test_df = pd.read_csv(test_sour,usecols=[1,2,3])
cont_df = pd.read_csv(cont_sour,usecols=[1,2,3])
containHealth_df = pd.read_csv(containHealth_sour,usecols=[1,2,3])
strin_df = pd.read_csv(strin_sour,usecols=[1,2,3])
face_df = pd.read_csv(face_sour,usecols=[1,2,3])
intMove_df = pd.read_csv(intMove_sour,usecols=[1,2,3])
internalTrav_df = pd.read_csv(internalTrav_sour,usecols=[1,2,3])
pubCamp_df = pd.read_csv(pubCamp_sour,usecols=[1,2,3])
pubEv_df = pd.read_csv(pubEv_sour,usecols=[1,2,3])
pubGath_df = pd.read_csv(pubGath_sour,usecols=[1,2,3])
pubTrans_df = pd.read_csv(pubTrans_sour,usecols=[1,2,3])
scho_df = pd.read_csv(scho_sour,usecols=[1,2,3])
stayhome_df = pd.read_csv(stayhome_sour,usecols=[1,2,3])
workpl_df = pd.read_csv(workpl_sour,usecols=[1,2,3])
# y variables (change column names)
convidnum_df = pd.read_csv(covidnum_sour,usecols=[0,3,4,11,14,10,13,12,15,16])
convidnum_df = convidnum_df.rename(columns={'iso_code': 'Code','date':'Day'})
# all variables
variables = [containHealth_df,strin_df,GMVi_df,test_df,cont_df,face_df,intMove_df,internalTrav_df,pubCamp_df,pubEv_df,pubGath_df,pubTrans_df,scho_df,stayhome_df,workpl_df,convidnum_df]
# Change date format and set index
for i in range(0,16):                        
    variables[i]['Day']=pd.to_datetime(variables[i]['Day'],format= '%Y/%m/%d')
    variables[i].set_index(['Code','Day'], inplace = True)


# A preselection of countries
# 7 European countries: Sweden (SWE), France (FRA), Germany (DEU), Spain (ESP), Italy (ITA), Czechia (CZE),Poland (POL)
EU = ['SWE', 'FRA', 'DEU', 'ESP', 'ITA', 'CZE', 'POL']
# 7 Asia-Pacific countries: Thailand (THA), Japan (JPN), South Korea (KOR), Australia (AUS), New Zealand (NZL), Vietnam (VNM),Singapore (SGP)
AP = ['THA', 'JPN', 'KOR', 'AUS', 'NZL', 'VNM', 'SGP']
Countries = EU + AP
# Filter all variable datasets based on criteria "Countries"
for i in range(0,16):
    variables[i]=variables[i].loc[Countries]


# Merge all dataframes into one
df = pd.concat(variables,axis=1)

# A predetermined time frame: freeze data on 2021-03-15
df_v1 = df.unstack(level=0)
df_v1 = df_v1.drop(df_v1.index[[-1,-2,-3,-4,-5]])
df = df_v1.stack()
df = df.reorder_levels(['Code', 'Day']).sort_index()
## now the dataset consists of 14 selected countries for till 20201-03-15




# data exploration
# check data types 
df.dtypes

# A)check missing values
def summarize_na(df: pd.DataFrame) -> pd.DataFrame:
    nan_count = df.isna().sum()
    return pd.DataFrame({'nan_count': nan_count, 
                         'nan_pct': nan_count / len(df) * 100
                         }
                        )[nan_count > 0]
df_nan_sum = summarize_na(df)
df_nan_sum
df_nan_sum.sort_values('nan_pct')

check_cols = ['total_cases',
              'total_cases_per_million',
              ]
check_cols_isna = df[check_cols].isna()
check_cols_isna
for col in check_cols[1:]:
    if (check_cols_isna[check_cols[0]] != check_cols_isna[col]).any():
        print(False)
        break  # print False and exit as soon as two columns are found to have NaNs in different rows
else:
    print(True)
### seems to be a coincidence after checking the data--> further discussion, plus, now 0 numbers for stringency index and containment index

# B)check values
categorical = ['contact_tracing',
               'restrictions_internal_movements',
               'public_information_campaigns',
               'cancel_public_events',
               'close_public_transport',
               'testing_policy',
               'school_closures',
               'stay_home_requirements',
               'workplace_closures',
               'facial_coverings',
               'international_travel_controls',
               'restriction_gatherings']
numerical = ['containment_index',
             'stringency_index',
             'retail_and_recreation',
             'grocery_and_pharmacy',
             'residential',
             'transit_stations',
             'parks',
             'workplaces',
             'total_cases',
             'total_cases_per_million',
             'new_cases_per_million',
             'new_cases_smoothed_per_million',
             'total_deaths_per_million',
             'new_deaths_per_million',
             'new_deaths_smoothed_per_million',
             'reproduction_rate']
# check unique values for categorical values
for i in range(0,12):    
    print(f"{categorical[i]}: {df[categorical[i]].unique()}")
# check value range for numerical values
for i in range(0,15):
    print(f"{numerical[i]}: [{df[numerical[i]].min()},{df[numerical[i]].max()}]")

# C)Descriptive statistics
# Descriptive statistics for numerical variables
Des_num = df[numerical].describe().transpose()
Des_num
# strange number 1: reproduction rate --> very high max, outlier?
r_filter=df['reproduction_rate']>=3
df[r_filter]
# 2)
temp1 = df[df['stringency_index']==0][categorical[3:12]]
pd.DataFrame(temp1 == 0).all(axis=0)

# Descriptive statistics for categorical variables
def get_frequencies(series: pd.Series, n_categories: int = None, 
                    bins: int = None, dropna: bool = True
                    ) -> pd.DataFrame:
    """Return a DataFrame displaying the series frequencies.
    
    Parameters
    ----------
    series: pd.Series
        The series for which frequencies are to be computed.
    n_categories: int, optional
        Maximum number of categories to return in output.
        Low-frequency categories will be grouped together to
        reach this threshold.
        
    """
    vc = series.value_counts(ascending=False, 
                             bins=bins, 
                             dropna=dropna
                             )
    if n_categories is not None:
        if not isinstance(n_categories, int) or n_categories <= 0:
            raise TypeError('n_categories should be a strictly positive integer')
        if n_categories < len(vc):
            freq_others = vc.iloc[n_categories - 1:].sum()
            vc = vc.iloc[:n_categories - 1]\
                   .append(pd.Series({'others': freq_others}))
    return pd.DataFrame({'absolute': vc, 
                         'relative': vc / len(series) * 100},
                        index = vc.index)

def get_frequencies2(series: pd.Series, n_categories: int = None, 
                    bins: int = None, dropna: bool = True
                    ) -> pd.DataFrame:
    """Return a DataFrame displaying the series frequencies.
    
    Parameters
    ----------
    series: pd.Series
        The series for which frequencies are to be computed.
    n_categories: int, optional
        Maximum number of categories to return in output.
        Low-frequency categories will be grouped together to
        reach this threshold.
        
    """
    vc = series.value_counts(ascending=False, 
                             bins=bins, 
                             dropna=dropna
                             )
    if n_categories is not None:
        if not isinstance(n_categories, int) or n_categories <= 0:
            raise TypeError('n_categories should be a strictly positive integer')
        if n_categories < len(vc):
            freq_others = vc.iloc[n_categories - 1:].sum()
            vc = vc.iloc[:n_categories - 1]\
                   .append(pd.Series({'others': freq_others}))
    return pd.DataFrame({'relative': vc / len(series) * 100},
                        index = vc.index)
F_list = []
for i in range(0,12):
    temp3 = get_frequencies(df[categorical[i]], 6,dropna=False)
    temp3 = temp3.rename(columns={'absolute': f"{df[categorical].columns[i]} ab", 'relative': f"{df[categorical].columns[i]} re"})
    F_list.append(temp3)
    Frequency_df = pd.concat(F_list,axis=1)





# D)Visualization
# preparation for visualization (on jupyter)
variables_y = df[numerical]
variables_x = df[categorical]
print(f"dropped {variables_x.isna().sum().sum()} NA")
variables_x.isna().sum()/len(variables_x)
# for other visualizations please see jupyter



### profile exploration
# per country
a_list = []

for i in range(0,14):
    for j in range(0,12):
        a = get_frequencies2(variables_x.loc[Countries[i]][categorical[j]],6, dropna= False)
        a = a.rename(columns={'relative': f"{categorical[j]} {Countries[i]}"})
        a_list.append(a)



per_country_list = []
for i in range(0,14):
        per_country = a_list[i*12:i*12+12]
        per_country = pd.concat(per_country,axis = 1)
        per_country_list.append(per_country)
# per measure
b_list = []

for j in range(0,12):
    for i in range(0,14):
        b = get_frequencies2(variables_x.loc[Countries[i]][categorical[j]],6, dropna= False)
        b = b.rename(columns={'relative': f"{categorical[j]} {Countries[i]}"})
        b_list.append(b)



per_measure_list = []
for i in range(0,12):
        per_measure = b_list[i*14:i*14+14]
        per_measure = pd.concat(per_measure,axis = 1)
        per_measure_list.append(per_measure)







# Data cleaning
# missing values for x variables
b = variables_x[variables_x.drop('school_closures',axis =1).isnull().any(axis=1)]
# excluding school closures, only THA has a serious NA problem 
temp = variables_x.index[variables_x['school_closures'].isnull()==True].tolist()
temp = pd.DataFrame(temp,columns=['Code','Day'])
d1 = datetime.datetime(2020, 1, 20)
temp[temp['Day']>d1]
# all countries have na for the first 20 days (2020-01-01 to 2020-01-20) except the list above --> exclude THA







# missing values for y: based on previous observation, we only focus on total_cases_per_million and reproduction_rate
variables_y = variables_y[['total_cases_per_million','reproduction_rate','total_cases']]
# as total_cases and total_cases_per_million have na always on the same date
variables_y[variables_y.drop('total_cases',axis =1).isnull().any(axis=1)]
# let's focus on total_cases_per_million as we already get the conclusion that it's the best proxy based on NA
temp = variables_y.index[variables_y['total_cases_per_million'].isnull()==True].tolist()
temp = pd.DataFrame(temp,columns=['Code','Day'])
lastNA_list = []
for i in range(0,14):
     lastNA_list.append(temp.loc[temp['Code'] == Countries[i], 'Day'].iloc[-1])
lastNA_df = pd.DataFrame(
    {'Code': Countries,
     'last NA date': lastNA_list
    })
# reproduction rate
temp1 = variables_y.index[variables_y['reproduction_rate'].isnull()==True].tolist()
temp1 = pd.DataFrame(temp1,columns=['Code','Day'])
lastNA1_list = []
for i in range(0,14):
     lastNA1_list.append(temp1.loc[temp1['Code'] == Countries[i], 'Day'].iloc[-1])
lastNA1_df = pd.DataFrame(
    {'Code': Countries,
     'last NA date': lastNA1_list
    })
# missing values for google mobility residential and workplaces as these two can really measure whether people follow the corresponding policies or not
temp2 = df.index[df['residential'].isnull()==True].tolist()
temp2 = pd.DataFrame(temp2,columns=['Code','Day'])
lastNA2_list = []
for i in range(0,14):
     lastNA2_list.append(temp2.loc[temp2['Code'] == Countries[i], 'Day'].iloc[-1])
lastNA2_df = pd.DataFrame(
    {'Code': Countries,
     'last NA date': lastNA2_list
    })
#all mobility data starts from 2020-02-17 for residential
temp3 =df.index[df['workplaces'].isnull()==True].tolist()
temp3 = pd.DataFrame(temp3,columns=['Code','Day'])
lastNA3_list = []
for i in range(0,14):
     lastNA3_list.append(temp3.loc[temp3['Code'] == Countries[i], 'Day'].iloc[-1])
lastNA3_df = pd.DataFrame(
    {'Code': Countries,
     'last NA date': lastNA3_list
    })
#the same for workplaces


# Data transformation
# google mobility data: I only considered

residential = df.iloc[:,4]
residential = residential.unstack(level=0)
residential = residential.reindex(columns=Countries)
residential= residential.sort_index(axis=0,ascending=True)
for i in range(0,14):
    residential = residential.rename(columns={f"{Countries[i]}": f"{Countries[i]} residential"})

workplace = df.iloc[:,4]
workplace = workplace.unstack(level=0)
workplace = workplace.reindex(columns=Countries)
workplace= workplace.sort_index(axis=0,ascending=True)
for i in range(0,14):
    workplace = workplace.rename(columns={f"{Countries[i]}": f"{Countries[i]} workplace"})




# adjustments to y
# consturct a y1 variable only when the total cases registered are greater than 10
y = variables_y['total_cases_per_million'][variables_y['total_cases'] > 10]
y = y.unstack(level=0)
y = y.reindex(columns=Countries)
y = y.sort_index(axis=0,ascending=True)
yfirst_valid_indices = y.apply(lambda series: series.first_valid_index()) 
#remeber, the first valid date is when (at least) the 10th cases registered
for i in range(0,14):
    y = y.rename(columns={f"{Countries[i]}": f"{Countries[i]} total cases/million"})
# consturct a y2 variable: r is avaialable far behind the date when the 10th case is registered for each country 
y2 = variables_y['reproduction_rate']
y2 = y2.unstack(level=0)
y2 = y2.reindex(columns=Countries)
y2 = y2.sort_index(axis=0,ascending=True)

y2first_valid_indices = y2.apply(lambda series: series.first_valid_index()) 
#remeber, the first valid date is when (at least) the 10th cases registered
for i in range(0,14):
    y2 = y2.rename(columns={f"{Countries[i]}": f"{Countries[i]} reproduction_rate"})


# adjustments to x
variables_x = df[categorical]
for i in range(0,12):    
    print(f"{categorical[i]}: {variables_x.loc[:,categorical[i]].unique()}")
cols = variables_x.columns.tolist()

x_any = variables_x.copy(deep=True)
x_any[x_any.isna()==False]= 1
x_any[x_any - variables_x == 1]=0


x_max = variables_x.copy(deep = True)
for i in range(0,5):
    x_max[f"{categorical[i]}"][x_max[f"{categorical[i]}"].isna()==False] = 0
    x_max[f"{categorical[i]}"][x_max[f"{categorical[i]}"]-variables_x[f"{categorical[i]}"]==-2]=1

for j in range(5,9):
    x_max[f"{categorical[j]}"][x_max[f"{categorical[j]}"].isna()==False] = 0
    x_max[f"{categorical[j]}"][x_max[f"{categorical[j]}"]-variables_x[f"{categorical[j]}"]==-3]=1
    
for k in range(9,12):
    x_max[f"{categorical[k]}"][x_max[f"{categorical[k]}"].isna()==False] = 0
    x_max[f"{categorical[k]}"][x_max[f"{categorical[k]}"]-variables_x[f"{categorical[k]}"]==-4]=1


countAny_list = []
for j in range(0,14):
    for i in range(0,12):
        countAny_country = x_any.unstack(level = 0).iloc[:,i*14+j].value_counts(dropna=True) # for all AUS
        countAny_list.append(countAny_country)

countAny_list2 = []
for i in range(0,14):
    countAny_country2 = pd.concat(countAny_list[i*12:i*12+12],axis=1).stack(level=1)
    countAny_list2.append(countAny_country2)

countAny = pd.concat(countAny_list2, axis=0)
temp = countAny.sort_index(level=0)
countAnyNo = temp[0:14]
countAnyYes = temp[14:28]

# count occurance of max for each country
countMax_list = []
for j in range(0,14):
    for i in range(0,12):
        countMax_country = x_max.unstack(level = 0).iloc[:,i*14+j].value_counts(dropna=True) # for all AUS
        countMax_list.append(countMax_country)

countMax_list2 = []
for i in range(0,14):
    countMax_country2 = pd.concat(countMax_list[i*12:i*12+12],axis=1).stack(level=1)
    countMax_list2.append(countMax_country2)

countMax = pd.concat(countMax_list2, axis=0)
temp = countMax.sort_index(level=0)
countMaxNo = temp[0:14]
countMaxYes = temp[14:28]
#countMaxNo.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/countMaxNo.csv")
#countMaxYes.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/countMaxYes.csv")
#countAnyNo.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/countAnyNo.csv")
#countAnyYes.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/countAnyYes.csv")

# single policies
# except for restriction gathering, all NA either at the beginning or the end (NZL 2020/10/23 and THA for some days in 2021/02), so we can choose to omit NA in such case
# for x
singleX_list = []
for i in range(0,12):
        singleX = variables_x.iloc[:,i].unstack(level=0)
        singleX = singleX.reindex(columns=Countries)        
        singleX_list.append(singleX)

for i in range(0,12):
    for j in range(0,14):
        singleX_list[i] = singleX_list[i].rename(columns={f"{Countries[j]}": f"{Countries[j]} {categorical[i]}"})
        


# for x_any
singleXany_list = []
for i in range(0,12):
        singleXany = x_any.iloc[:,i].unstack(level=0)
        singleXany = singleXany.reindex(columns=Countries)        
        singleXany_list.append(singleXany)

for i in range(0,12):
    for j in range(0,14):
        singleXany_list[i] = singleXany_list[i].rename(columns={f"{Countries[j]}": f"{Countries[j]} {categorical[i]}"})
        
# for x_max
singleXmax_list = []
for i in range(0,12):
        singleXmax = x_max.iloc[:,i].unstack(level=0)
        singleXmax = singleXmax.reindex(columns=Countries)        
        singleXmax_list.append(singleXmax)

for i in range(0,12):
    for j in range(0,14):
        singleXmax_list[i] = singleXmax_list[i].rename(columns={f"{Countries[j]}": f"{Countries[j]} {categorical[i]}"})

# merge x and y and consider time lages ranging between 1 and 14
lag_list = []
for i in range(1,15):
    lag=yfirst_valid_indices- pd.DateOffset(days=i)
    lag_list.append(lag)
lag_df = pd.concat(lag_list,axis =1)

lag2_list = []
for i in range(1,15):
    lag2=y2first_valid_indices- pd.DateOffset(days=i)
    lag2_list.append(lag2)
lag2_df = pd.concat(lag2_list,axis =1)


# for y = total cases per million
listAny = []
listMax = []
listX = []
k = 13 # lag between 0 and 13 incl.
for j in range(0,12): # for each policy
    for i in range(0,14): # for each country
        temp1 = singleXany_list[j].loc[lag_df.iloc[i,k]:,f"{Countries[i]} {categorical[j]}"].reset_index().rename(columns={'Day':  f"Day t {-(k+1)}",f"{Countries[i]} {categorical[j]}": f"{categorical[j]}"})
        temp2 = y.loc[yfirst_valid_indices[i]:,f"{Countries[i]} total cases/million"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} total cases/million":"total cases/million" })  
        temp3 = residential.loc[yfirst_valid_indices[i]:,f"{Countries[i]} residential"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} residential":"residential" })  
        temp4 = workplace.loc[yfirst_valid_indices[i]:,f"{Countries[i]} workplace"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} workplace":"workplace" })  
        regAllany = pd.concat([temp1,temp2,temp3,temp4],axis = 1)
        regAllany =regAllany.assign(Code = [Countries[i]]*len(regAllany),timeIndex = range(1,len(regAllany)+1)) # mark contry and time (starting from day 1)
        regAllany.loc[regAllany['Code'].isin(EU) == True, 'cluster'] = 1
        regAllany.loc[regAllany['Code'].isin(EU) != True, 'cluster'] = 0
        #colAny = regAllany.columns.tolist()
        #colAny =  [colAny[-2]] + colAny[:-2]+ [colAny[-1]]
        #regAllany =regAllany[colAny]
        listAny.append(regAllany) # a list of j * i: start with policy 1 and for all countries, then policy 2 for all countries etc.
        temp5 = singleXmax_list[j].loc[lag_df.iloc[i,k]:,f"{Countries[i]} {categorical[j]}"].reset_index().rename(columns={'Day':  f"Day t {-(k+1)}",f"{Countries[i]} {categorical[j]}": f"{categorical[j]}"})
        temp6 = y.loc[yfirst_valid_indices[i]:,f"{Countries[i]} total cases/million"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} total cases/million":"total cases/million" })  
        temp7 = residential.loc[yfirst_valid_indices[i]:,f"{Countries[i]} residential"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} residential":"residential" })  
        temp8 = workplace.loc[yfirst_valid_indices[i]:,f"{Countries[i]} workplace"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} workplace":"workplace" })  
        regAllmax = pd.concat([temp5,temp6,temp7,temp8],axis = 1)
        regAllmax =regAllmax.assign(Code = [Countries[i]]*len(regAllmax),timeIndex = range(1,len(regAllmax)+1)) # mark contry and time (starting from day 1)
        regAllmax.loc[regAllmax['Code'].isin(EU) == True, 'cluster'] = 1
        regAllmax.loc[regAllmax['Code'].isin(EU) != True, 'cluster'] = 0
        #colMax = regAllmax.columns.tolist()
        #colMax =  [colMax[-2]] + colMax[:-2]+ [colMax[-1]]
        #regAllmax =regAllmax[colMax]
        listMax.append(regAllmax) # a list of j * i: start with policy 1 and for all countries, then policy 2 for all countries etc.
        temp9 = singleX_list[j].loc[lag_df.iloc[i,k]:,f"{Countries[i]} {categorical[j]}"].reset_index().rename(columns={'Day':  f"Day t {-(k+1)}",f"{Countries[i]} {categorical[j]}": f"{categorical[j]}"})
        temp10 = y.loc[yfirst_valid_indices[i]:,f"{Countries[i]} total cases/million"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} total cases/million":"total cases/million" })  
        temp11 = residential.loc[yfirst_valid_indices[i]:,f"{Countries[i]} residential"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} residential":"residential" })  
        temp12 = workplace.loc[yfirst_valid_indices[i]:,f"{Countries[i]} workplace"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} workplace":"workplace" })  
        regAllx = pd.concat([temp9,temp10,temp11,temp12],axis = 1)
        regAllx =regAllx.assign(Code = [Countries[i]]*len(regAllx),timeIndex = range(1,len(regAllx)+1)) # mark contry and time (starting from day 1)
        regAllx.loc[regAllx['Code'].isin(EU) == True, 'cluster'] = 1
        regAllx.loc[regAllx['Code'].isin(EU) != True, 'cluster'] = 0
        #colMax = regAllmax.columns.tolist()
        #colMax =  [colMax[-2]] + colMax[:-2]+ [colMax[-1]]
        #regAllmax =regAllmax[colMax]
        listX.append(regAllx) # a list of j * i: start with policy 1 and for all countries, then policy 2 for all countries etc.


policiesAny = categorical[:]
policiesMax = categorical[:]
policiesX = categorical[:]
for i in range(0,12): # for each policy
    policiesAny[i] = pd.concat(listAny[i*14:i*14+14],axis = 0)
    policiesAny[i].set_index(['Code', f"Day t {-(k+1)}"], inplace = True)
    policiesMax[i] = pd.concat(listMax[i*14:i*14+14],axis = 0)
    policiesMax[i].set_index(['Code', f"Day t {-(k+1)}"], inplace = True)
    policiesX[i] = pd.concat(listX[i*14:i*14+14],axis = 0)
    policiesX[i].set_index(['Code', f"Day t {-(k+1)}"], inplace = True)

allXany = pd.concat(policiesAny,axis = 1)
#allX = allX.dropna(axis=0)
allXany = allXany.loc[:,~allXany.columns.duplicated()]
colAny =allXany.columns.tolist()
colAny = [colAny[0]] +colAny[7:]+ colAny[1:7]   
allXany = allXany[colAny]
allXany.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/regallAny14cases.csv")

allXmax = pd.concat(policiesMax,axis = 1)
#allX = allX.dropna(axis=0)
allXmax = allXmax.loc[:,~allXmax.columns.duplicated()]
colMax =allXmax.columns.tolist()
colMax =  [colMax[0]] + colMax[7:]+ colMax[1:7]  
allXmax = allXmax[colMax]
allXmax.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/regallMax14cases.csv")

allX = pd.concat(policiesX,axis = 1)
#allX = allX.dropna(axis=0)
allX = allX.loc[:,~allX.columns.duplicated()]
colX =allX.columns.tolist()
colX =  [colX[0]] + colX[7:]+ colX[1:7]  
allX = allX[colX]
allX.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/QDC/regall14cases.csv")



# for y = reproduction_rate
listAny = []
listMax = []
listX = []
k = 0 # lag between 0 and 13 incl.
for j in range(0,12): # for each policy
    for i in range(0,14): # for each country
        temp1 = singleXany_list[j].loc[lag2_df.iloc[i,k]:,f"{Countries[i]} {categorical[j]}"].reset_index().rename(columns={'Day':  f"Day t {-(k+1)}",f"{Countries[i]} {categorical[j]}": f"{categorical[j]}"})
        temp2 = y2.loc[y2first_valid_indices[i]:,f"{Countries[i]} reproduction_rate"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} reproduction_rate":"reproduction_rate" })  
        temp3 = residential.loc[y2first_valid_indices[i]:,f"{Countries[i]} residential"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} residential":"residential" })  
        temp4 = workplace.loc[y2first_valid_indices[i]:,f"{Countries[i]} workplace"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} workplace":"workplace" })  
        regAllany = pd.concat([temp1,temp2,temp3,temp4],axis = 1)
        regAllany =regAllany.assign(Code = [Countries[i]]*len(regAllany),timeIndex = range(1,len(regAllany)+1)) # mark contry and time (starting from day 1)
        regAllany.loc[regAllany['Code'].isin(EU) == True, 'cluster'] = 1
        regAllany.loc[regAllany['Code'].isin(EU) != True, 'cluster'] = 0
        #colAny = regAllany.columns.tolist()
        #colAny =  [colAny[-2]] + colAny[:-2]+ [colAny[-1]]
        #regAllany =regAllany[colAny]
        listAny.append(regAllany) # a list of j * i: start with policy 1 and for all countries, then policy 2 for all countries etc.
        temp5 = singleXmax_list[j].loc[lag2_df.iloc[i,k]:,f"{Countries[i]} {categorical[j]}"].reset_index().rename(columns={'Day':  f"Day t {-(k+1)}",f"{Countries[i]} {categorical[j]}": f"{categorical[j]}"})
        temp6 = y2.loc[y2first_valid_indices[i]:,f"{Countries[i]} reproduction_rate"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} reproduction_rate":"reproduction_rate" })  
        temp7 = residential.loc[y2first_valid_indices[i]:,f"{Countries[i]} residential"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} residential":"residential" })  
        temp8 = workplace.loc[y2first_valid_indices[i]:,f"{Countries[i]} workplace"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} workplace":"workplace" })  
        regAllmax = pd.concat([temp5,temp6,temp7,temp8],axis = 1)
        regAllmax =regAllmax.assign(Code = [Countries[i]]*len(regAllmax),timeIndex = range(1,len(regAllmax)+1)) # mark contry and time (starting from day 1)
        regAllmax.loc[regAllmax['Code'].isin(EU) == True, 'cluster'] = 1
        regAllmax.loc[regAllmax['Code'].isin(EU) != True, 'cluster'] = 0
        #colMax = regAllmax.columns.tolist()
        #colMax =  [colMax[-2]] + colMax[:-2]+ [colMax[-1]]
        #regAllmax =regAllmax[colMax]
        listMax.append(regAllmax) # a list of j * i: start with policy 1 and for all countries, then policy 2 for all countries etc.
        temp9 = singleX_list[j].loc[lag2_df.iloc[i,k]:,f"{Countries[i]} {categorical[j]}"].reset_index().rename(columns={'Day':  f"Day t {-(k+1)}",f"{Countries[i]} {categorical[j]}": f"{categorical[j]}"})
        temp10 = y2.loc[y2first_valid_indices[i]:,f"{Countries[i]} reproduction_rate"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} reproduction_rate":"reproduction_rate" })  
        temp11 = residential.loc[y2first_valid_indices[i]:,f"{Countries[i]} residential"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} residential":"residential" })  
        temp12 = workplace.loc[y2first_valid_indices[i]:,f"{Countries[i]} workplace"].reset_index().rename(columns={'Day': 'Day t',f"{Countries[i]} workplace":"workplace" })  
        regAllx = pd.concat([temp9,temp10,temp11,temp12],axis = 1)
        regAllx =regAllx.assign(Code = [Countries[i]]*len(regAllx),timeIndex = range(1,len(regAllx)+1)) # mark contry and time (starting from day 1)
        regAllx.loc[regAllx['Code'].isin(EU) == True, 'cluster'] = 1
        regAllx.loc[regAllx['Code'].isin(EU) != True, 'cluster'] = 0
        #colMax = regAllmax.columns.tolist()
        #colMax =  [colMax[-2]] + colMax[:-2]+ [colMax[-1]]
        #regAllmax =regAllmax[colMax]
        listX.append(regAllx) # a list of j * i: start with policy 1 and for all countries, then policy 2 for all countries etc.


policiesAny = categorical[:]
policiesMax = categorical[:]
policiesX = categorical[:]
for i in range(0,12): # for each policy
    policiesAny[i] = pd.concat(listAny[i*14:i*14+14],axis = 0)
    policiesAny[i].set_index(['Code', f"Day t {-(k+1)}"], inplace = True)
    policiesMax[i] = pd.concat(listMax[i*14:i*14+14],axis = 0)
    policiesMax[i].set_index(['Code', f"Day t {-(k+1)}"], inplace = True)
    policiesX[i] = pd.concat(listX[i*14:i*14+14],axis = 0)
    policiesX[i].set_index(['Code', f"Day t {-(k+1)}"], inplace = True)

allXany = pd.concat(policiesAny,axis = 1)
#allX = allX.dropna(axis=0)
allXany = allXany.loc[:,~allXany.columns.duplicated()]
colAny =allXany.columns.tolist()
colAny = [colAny[0]] +colAny[7:]+ colAny[1:7]   
allXany = allXany[colAny]
allXany.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallAny0r.csv")

allXmax = pd.concat(policiesMax,axis = 1)
#allX = allX.dropna(axis=0)
allXmax = allXmax.loc[:,~allXmax.columns.duplicated()]
colMax =allXmax.columns.tolist()
colMax =  [colMax[0]] + colMax[7:]+ colMax[1:7]  
allXmax = allXmax[colMax]
allXmax.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallMax0r.csv")

allX = pd.concat(policiesX,axis = 1)
#allX = allX.dropna(axis=0)
allX = allX.loc[:,~allX.columns.duplicated()]
colX =allX.columns.tolist()
colX =  [colX[0]] + colX[7:]+ colX[1:7]  
allX = allX[colX]
#allX.to_csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regall13r.csv")


