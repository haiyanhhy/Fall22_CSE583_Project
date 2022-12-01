import streamlit as st

# st.write("""
# #My first app
# Hello *world!*
# """)

# title
st.title('Seattle housing price analysis'.center(33, '-'))
 
# sidebar
st.sidebar.expander('')     # expander必须接受一个 label参数，我这里留了一个空白
st.sidebar.subheader('Selection')       # subtitle
# st.selectbox
cluster_class = st.sidebar.selectbox('1.House Type:', ['Single family house','Apartment'])    
minmaxscaler = st.sidebar.radio('2.City:', ['Seattle', 'Bellevue']) 