#!/usr/bin/env python
# coding: utf-8

# ### Listing the required libraries

# In[1]:


import sys
get_ipython().system('pip install pandas')
get_ipython().system('pip install numpy')
get_ipython().system('pip install datapane')
get_ipython().system('pip install plotly')


# In[2]:


import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datapane as dp


# ### Connection to the database

# In[3]:


#put the name of your database here:
db = 'Project3.sqlite'


def run_query(q):   #
    with sqlite3.connect(db) as conn:
        return pd.read_sql(q,conn)
    
def run_command(c):
    with sqlite3.connect(db) as conn:
        conn.isolation_level = None
        conn.execute(c) 


# ### Testing the connection by printing the name and number of records for all the tables available in the database

# In[4]:


def show_tables():
    q = '''
        SELECT
            name
        FROM sqlite_master
        WHERE type IN ("table","view");
        '''
    return run_query(q)

def get_table_row_count(tablename):
    q = '''
        SELECT
            COUNT(1)
        FROM %s;
        ''' % tablename
    return run_query(q)["COUNT(1)"][0]

tables = show_tables()
tables["row_count"] = [get_table_row_count(t) for t in tables["name"]]

tables


# ### Sample code that shows how to print the columns in each table

# In[5]:


conn = sqlite3.connect(db)
cursor = conn.cursor()


print("Columns of Table Detailrental")
data=cursor.execute('''SELECT * FROM Detailrental''')
for column in data.description:
    print(column[0])
print("-------------------------------")
    
    
print("Columns of Table Membership")
data=cursor.execute('''SELECT * FROM Membership''')
for column in data.description:
    print(column[0])
print("-------------------------------")


print("Columns of Table Movie")
data=cursor.execute('''SELECT * FROM Movie''')
for column in data.description:
    print(column[0])       
print("-------------------------------")


# ### Copy your Datapane token (from the website) to create the online dashboard

# In[6]:


# copy your datapane token below
get_ipython().system('datapane login --token=672a4996b5c846b448cd4b82f027f535a83f90b4')


# ### How to run a query

# In[7]:


# based on quuestion 14 in HW3

movie_noc_query = '''
    SELECT MOVIE_GENRE, COUNT(MOVIE_NUM) as MovCounts
    FROM Movie 
    GROUP BY Movie_Genre
    Having COUNT(MOVIE_NUM) > 0
    ORDER BY MovCounts DESC;
'''
movie_noc = run_query(movie_noc_query)
movie_noc


# In[8]:


#### Show in a bar chart
movie_genre_breakdown = go.Figure(data=[go.Pie(
    labels = movie_noc["MOVIE_GENRE"], 
    values=movie_noc["MovCounts"], 
    hole=.3)
                                 ])

movie_genre_breakdown.update_layout(title_text="Number of movie genre")

movie_genre_breakdown.show()


# In[9]:


#After you develop your query in the sqlite developer (oracle developer), you can copy it here and 
#give it a name (such as top_10_tracks_query) 

moviesdetails_query = '''
    SELECT Movie_Title,Price_Description, movie_cost 
    FROM Movie INNER JOIN Price  

    ORDER BY movie_title, price_description, movie_cost DESC 
   
    '''

# use run_query to run the it and see the results
moviesdetails_df = run_query(moviesdetails_query)

moviesdetails_df

# dp.Report(
#     dp.DataTable(top_10_df)
# ).upload(name="Music Sales")


# In[10]:



sales_by_country = '''
Select Mem_FName,Mem_LName, Rent_Date,Detail_Fee,Detail_DueDate
from Membership
inner join Rental on Membership.Mem_Num = Rental.Mem_Num
inner join detailrental on Rental.rent_Num = detailrental.Rent_Num;


'''

sales_track = run_query(sales_by_country)
sales_track


# #### Print a bar chart based on the data

# In[11]:


clv = px.bar(
    sales_track,
    x = 'MEM_LNAME',
    y = 'DETAIL_DUEDATE',
    
    
    title = " Due Date For Returning Rented Movie"
)

clv.update_layout(showlegend=False)


clv.show()


# ### calcuating the summary values on the top of the dashboard

# In[12]:


membership = run_query('''Select Count(*) as count From Membership''')["count"][0]
detailrental = run_query('''Select Count(*) as count From detailrental''')["count"][0]
movie = run_query('''Select Count(*) as count From movie''')["count"][0]


# ## Defining the layout of the final dashboard

# In[13]:


r = dp.Report( 
    dp.Group(
        dp.BigNumber(heading="Total membership", value = membership),
        dp.BigNumber(heading="Total detailrental", value = detailrental),
        dp.BigNumber(heading="Total movie", value = movie),
        columns = 3,
        name="Little_group"
    ),
    dp.Plot(clv, name = "membership-movie-rent"),
    dp.Plot(movie_genre_breakdown, name = "mimbership-video"),
    dp.DataTable(moviesdetails_df, name = "video-rental"),
).upload(name="Interactive Dashboard using SQL")


# In[ ]:




