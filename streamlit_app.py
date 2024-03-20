import streamlit as st
import snowflake.connector
import pandas as pd

st.title("Zena's Amazing Athleisure Catalog")

# Connect to Snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Run a Snowflake query
my_cur.execute("SELECT color_or_style FROM catalog_for_website")
my_catalog = my_cur.fetchall()

# Put the data into a DataFrame
df = pd.DataFrame(my_catalog, columns=['color_or_style'])

# Put the first column into a list
color_list = df['color_or_style'].tolist()

# Let's put a pick list here so they can pick the color
option = st.selectbox('Pick a sweatsuit color or style:', color_list)

# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Use the option selected to go back and get all the info from the database
query = """
SELECT direct_url, price, size_list, upsell_product_desc 
FROM catalog_for_website 
WHERE color_or_style = '{}';
""".format(option)
my_cur.execute(query)
df2 = my_cur.fetchone()

if df2:
    st.image(df2[0], width=400, caption=product_caption)
    st.write('Price: ', df2[1])
    st.write('Sizes Available: ', df2[2])
    st.write(df2[3])
else:
    st.write("No details found for the selected option.")



