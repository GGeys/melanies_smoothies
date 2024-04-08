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

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'),
st.stop()

Name_on_order = st.text_input('Name on smoothie:')

ingredients_list = st.multiselect(
    'Choose your favorites:'
    , my_dataframe
    , max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition information')
        
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + Name_on_order + """')"""

    time_to_insert = st.button ('Submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Thanks ' + Name_on_order + ', your smoothie is ordered!', icon="✅")



