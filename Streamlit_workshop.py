#activate venv:
    #source streamlit/bin/activate
#run app:
    #streamlit run Streamlit.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout = "wide")


# text tools
st.title("My funky streamlit app!")
st.header("This is a header")
st.subheader("This is a subheader")
st.markdown("**Streamlit** is super *cool!*")
st.write("We can use this for plain text")

# show code
my_code = """

for i in range(10):
    print(i)
"""

st.code(my_code, language = "python")

# show image
st.image("prins_joachim_foto_dm.jpg")

# widgets

# present a button
if st.button("Say hi!"):
    st.write("Well, hi there!")

# present a slider
st.slider("How old are you?", 0, 100, 50)

# import data
df = pd.DataFrame(px.data.gapminder())

# make a list of countries
clist = df['country'].unique()

# make a dropdown menu with countries
country = st.selectbox("Select a country", clist)

# prepare a plot
dfc = df[df['country']== country]
fig = px.line(dfc, x = "year", y = "lifeExp", title = country)
st.plotly_chart(fig)

#show df
# present a button
if st.checkbox("Show data!"):
    st.dataframe(data=dfc, width=None, height=None)
else:
    st.write('Do you not want to see my data?')


age = st.sidebar.slider("What is your age my friend?", 0, 100, 50)
st.write("I am {} years old".format(age))

###
# make a list of cont
clist = df['continent'].unique()

# make a dropdown menu with countries
continent = st.selectbox("Select a continent", clist)


dfc2 = df[df['continent']==continent]
fig2 = px.line(dfc2, x = "year", y = "lifeExp", title = continent, color='country')
st.plotly_chart(fig2)


with st.expander("Show data!"):
    st.write(dfc)


#Exercise 2
dfc2 = df[df['continent']==continent]
fig2 = px.scatter(dfc2, x = "year", y = "lifeExp", title = continent, color='country', size='pop', size_max=40, hover_name='country')
st.plotly_chart(fig2)

dfc2 = df[df['continent']==continent]
fig2 = px.box(dfc2, y = "lifeExp", title = continent, color='country')
st.plotly_chart(fig2)


#LET'S TRY SOMETHING SIIIICK
# load built-in gapminder dataset from plotly 
gapminder = px.data.gapminder() 

# hover name 
fig2 = px.scatter(gapminder, x='gdpPercap', y='lifeExp', color='continent', size='pop', size_max=40, 
                hover_name='country', log_x=True, animation_frame='year',
                animation_group='country', range_x=[25, 100000], range_y=[25,90])
st.plotly_chart(fig2)


# hover name 
fig = px.scatter(gapminder, x='gdpPercap', y='lifeExp', color='continent', size='pop', size_max=100, 
                log_x=True, animation_frame='year', hover_name='continent',
                animation_group='continent', range_x=[25, 100000], range_y=[25,90])
st.plotly_chart(fig)


col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig, use_column_width=True)

with col2:
    st.plotly_chart(fig, use_column_width=True)
