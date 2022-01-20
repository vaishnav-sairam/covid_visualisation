import pandas as pd
import plotly.express as px
# Reading covid database to a dataframe
url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df = pd.read_csv(url)

# Exploratory analysis of the database
df.info
df.describe()
df.shape
df.head()
df.tail()

# Some further digging
df_confirmed = df[df['Confirmed']>0]
df_india = df[df.Country == 'India']
df_india.tail()
# Plotting confirmed case distribution over countries of the world
fig=px.choropleth(df, locations='Country', locationmode='country names', color='Confirmed',
                  animation_frame='Date')
fig.update_layout(title_text='Covid cases across the world')
fig.show()

# Plotting global deaths due to covid
fig=px.choropleth(df, locations='Country', locationmode='country names', color='Deaths',
                  animation_frame='Date')
fig.update_layout(title_text='Covid deaths across the world')
fig.show()

# Plotting number of cases and infection rate of covid in india for a period till date
df_india_subset=df_india[['Date', 'Confirmed']]
df_india_subset['Infection rate'] = df_india_subset['Confirmed'].diff()
df_india_subset.shape

fig2=px.line(df_india_subset, x='Date', y=['Confirmed', 'Infection rate'])
fig2.show()
df_india_subset['Infection rate'].max()

# Getting insights for all countries ( max infection rates )
countries = list(df['Country'].unique())
max_ir=[]
for c in countries :
    mir = df[df.Country == c].Confirmed.diff().max()
    max_ir.append(mir)

df_countries= pd.DataFrame()
df_countries['Country']=countries
df_countries['Maximum infection rate']=max_ir

# Plot the max infection rate for the different countries
fig3=px.bar(df_countries, y = 'Country', x = 'Maximum infection rate', color='Country',
            title='Maximum infection rate for each country during covid', log_x=True)
fig3.show()

# Infection rate before and after lockdown for india
india_lock = '2020-03-24'
india_end = '2020-12-31'
fig4 = px.line(df_india_subset,x='Date',y='Infection rate',title='Covid infection rate in India')
fig4.add_shape(dict( type='line',x0=india_lock,y0=0,x1=india_lock,y1=df_india_subset['Infection rate'].max(),line=dict(color='green',width=0.5)))
fig4.add_annotation(dict(x=india_lock,y=df_india_subset['Infection rate'].max(),text='Start of lockdown'))
fig4.add_shape(dict( type='line',x0=india_end,y0=0,x1=india_end,y1=df_india_subset['Infection rate'].max(),line=dict(color='red',width=0.5)))
fig4.add_annotation(dict(x=india_end,y=df_india_subset['Infection rate'].max(),text='End of year'))
fig4.show()

# Comparing death rates to the infection rates for india with lockdown window till year end
df_india['Infection rate']=df_india['Confirmed'].diff()
df_india['Death rate']=df_india['Deaths'].diff()
df_india['Infection rate']=df_india['Infection rate']/df_india['Infection rate'].max()  # normalising the infection and death rates between 0 and 1 for better readability
df_india['Death rate']=df_india['Death rate']/df_india['Death rate'].max()
fig5=px.line(df_india,x='Date', y=['Infection rate','Death rate'])
fig5.add_shape(dict( type='line',x0=india_lock,y0=0,x1=india_lock,y1=df_india['Infection rate'].max(),line=dict(color='green',width=0.5)))
fig5.add_annotation(dict(x=india_lock,y=df_india['Infection rate'].max(),text='Start of lockdown'))
fig5.add_shape(dict( type='line',x0=india_end,y0=0,x1=india_end,y1=df_india['Infection rate'].max(),line=dict(color='red',width=0.5)))
fig5.add_annotation(dict(x=india_end,y=df_india['Infection rate'].max(),text='End of year'))
fig5.show()
