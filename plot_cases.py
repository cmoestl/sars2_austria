#!/usr/bin/env python
# coding: utf-8

# ## SARS-2 Austria 
# 
# C. Möstl, Graz, https://twitter.com/chrisoutofspace
# 
# data source for Austria
# https://orf.at/corona/stories/3157533/
# 
# data source for South Korea
# https://www.worldometers.info/coronavirus/country/south-korea/
# 
# for converting to script on the command line:
# jupyter nbconvert --to script plot_cases.ipynb

# In[1]:


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from sunpy.time import parse_time
import datetime
from set_input_here import t_start_string, t_end_string, cases_list, filename, country, south_korea_offset

def expon(x, a, k, b):
    return a*np.exp(k*x) + b


sns.set_style('darkgrid')
sns.set_context('paper')   

print(country)
print(t_start_string)
print(t_end_string)
print(cases_list)
print(south_korea_offset)


# 
# ### Austria

# In[2]:


t_start=parse_time(t_start_string).datetime
t_end=parse_time(t_end_string).datetime

dates=parse_time([t_start + datetime.timedelta(days=1*n) for n in range((t_end - t_start).days+1)]).datetime
cases=np.array(cases_list)

print(parse_time(dates).iso)
print(cases)

dates1=parse_time(dates).plot_date
dates1=dates1-dates1[0] 

#for morning numbers
#param = scipy.optimize.curve_fit(expon, dates1[0:-2], cases[0:-2] )
#afternoon numbers
param = scipy.optimize.curve_fit(expon, dates1[0:-1], cases[0:-1] )

p1=param[0][0]
p2=param[0][1]
p3=param[0][2]

t_end2=parse_time('2020-04-10 23:00').datetime

dates_fut=parse_time([t_start + datetime.timedelta(days=n) for n in range((t_end2 - t_start).days)]).plot_date
dates_fut1=dates_fut-dates_fut[0]

fit=expon(dates_fut1,p1,p2,p3)
now=datetime.datetime.utcnow().strftime("%Y-%b-%d %H:%M")
#now=dates[-1].strftime("%Y-%b-%d %H:%M")


# ### South Korea

# In[3]:


t_start_sk=parse_time('2020-02-15 20:00').datetime
t_end_sk=parse_time('2020-03-18 20:00').datetime

t_start_sk=t_start_sk+datetime.timedelta(days=south_korea_offset)
t_end_sk=t_end_sk+datetime.timedelta(days=south_korea_offset)

dates_sk=parse_time([t_start_sk + datetime.timedelta(days=1*n) for n in range((t_end_sk - t_start_sk).days)]).datetime

print(parse_time(dates_sk).iso)
cases_sk=np.array([28, 29, 30, 31, 58, 111, 209, 436,602, 833, 977, 1261, 1766, 2337,                   3150,3736, 4335,5186,5621,6284,6593,7041,7313,7478,7513,7755,7869,                   7979,8086,8162,8236,8320])
print(cases_sk)
print(len(cases_sk),len(dates_sk))


# In[5]:


plt.figure(1,figsize=(10,6),dpi=150)
ax1 = plt.subplot(211) 

ax1.plot(dates,cases,marker='o',color='tomato',label=country+' verified cases',markersize=6)
ax1.plot(dates_fut,fit,linestyle='-',color='tomato',label='exponential fit')
ax1.plot(dates_sk,cases_sk,linestyle='--',color='steelblue',label='South Korea verified cases +'+str(south_korea_offset)+' days')


ax1.xaxis.set_major_formatter( matplotlib.dates.DateFormatter('%b-%d') )
ax1.set_xlim([dates_fut[0],dates_fut[-1]])
plt.xticks(rotation=60)
plt.ylabel('Total cases')
plt.ylim(-200,10000)
plt.title(country+' SARS-2  '+now+ ' UTC')
plt.legend()
ax1.set_xticks(dates_fut)


ax2 = plt.subplot(212) 

ax2.bar(dates,np.gradient(cases),color='tomato',label=country+' daily new cases')
ax2.plot(dates_fut,np.gradient(fit),color='tomato',label='exponential fit')
ax2.plot(dates_sk,np.gradient(cases_sk),marker='o',color='steelblue',label='South Korea daily new cases +'+str(south_korea_offset)+' days')



ax2.xaxis.set_major_formatter( matplotlib.dates.DateFormatter('%b-%d') )

plt.xticks(rotation=60)
plt.ylabel('New cases')
ax2.set_xlim([dates_fut[0],dates_fut[-1]])
plt.title(country+' SARS-2  '+now + ' UTC')
ax2.set_xticks(dates_fut)
plt.ylim(0,np.max(np.gradient(cases_sk)))

plt.legend()

plt.tight_layout()
print('current total cases '+country,cases[-1])

plt.savefig(filename)


# In[ ]:




