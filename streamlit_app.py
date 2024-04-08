#Import python packages
import streamlit as st
import time
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

# Data frame as ingredients from fruit name column in fruit options
#session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


# USER INPUT: add name, choose fruit, submit order

Name_on_order = st.text_input('Name on smoothie:')
#st.write('The name on your smoothie will be', Name_on_order)

ingredients_list = st.multiselect(
    'Choose your favorites:'
    , my_dataframe
    , max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + Name_on_order + """')"""
    
    #st.write(my_insert_stmt)
    #st.stop
    
    time_to_insert = st.button ('Submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Thanks ' + Name_on_order + ', your smoothie is ordered!', icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width='TRUE')
