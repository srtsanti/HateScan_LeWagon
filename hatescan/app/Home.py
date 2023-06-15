import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from PIL import Image

st.title('Hi, welcome to Hatescan :wave:')

logo = Image.open("hatescan/app/images/logo.svg")
st.image(logo, width=200)
























# import streamlit as st
# import time
# import requests
# from google.oauth2 import service_account
# import pandas as pd
# from google.cloud import bigquery
# from sklearn.decomposition import PCA
# import plotly.express as px

# ### Funcions and BQ ###

# scale_mapping = {
#         0: ("Normal", "🙂"),
#         1: ("Offensive", "😡"),
#         2: ("Hate", "🤬")
#     }
# def format_hate_scale(value):
#     if value == 0:
#         return "🙂"
#     elif value == 1:
#         return "😡"
#     elif value == 2:
#         return "🤬"
#     else:
#         return str(value)

# def transform_hate_label(scale):
#     if 0 <= scale < 0.85:
#         return 0
#     elif 0.85 <= scale < 1.5:
#         return 1
#     elif scale >= 1.5:
#         return 2

# # GET data from BigQuery
# # Create API client.
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"]
# )
# client = bigquery.Client(credentials=credentials)
# def run_query(query):
#     query_job = client.query(query)
#     rows_raw = query_job.result()
#     # Convert to list of dicts. Required for st.cache_data to hash the return value.
#     rows = [dict(row) for row in rows_raw]
#     df = pd.DataFrame(rows)
#     return df

# def transform_hate_label(scale):
#             if 0 <= scale < 0.85:
#                 return 0
#             elif 0.85 <= scale < 1.5:
#                 return 1
#             elif scale >= 1.5:
#                 return 2

# ### WEB STARTS HERE ###

# st.title('Welcome to the Hater Scan App')

# #### THIS IS PAGE 1
# url = st.secrets['key_ap']
# st.title("Tweet Box")
# tweet = st.text_area("Enter your tweet:", max_chars=300)
# params = {'tweet' : tweet}
# st.write("Your tweet:")
# st.write(tweet)
# scanner = st.button('Scan tweet')

# # This is the code for printing the Hate scale
# if scanner:
#     response = requests.get(url, params=params)
#     #Connection to model_scale through our API
#     scale = response.json()['hate_scale']['HateLabel']
#     scale = transform_hate_label(scale)
#     #Connection to model_topic through our API
#     topics = response.json()['hate_class']
#     if scale in scale_mapping:
#         label, emoji = scale_mapping[scale]
#         st.write("Hate Label Scale:", f"{label} {emoji}")
#         st.title("Hate Level:")
#         st.select_slider("Your tweet is:",
#                                   options=[0, 1, 2],
#                                   value=scale,
#                                   format_func=format_hate_scale)
#     else:
#         st.write("Hate Label Scale:", scale)

#     st.markdown("---")

# # This is the code for printing the Hate topics
#     st.title('Hate topics:')
#     for key, value in topics.items():
#         class_name = ""
#         if key == '0':
#             class_name = "Religion"
#         elif key == '1':
#             class_name = "Gender"
#         elif key == '2':
#             class_name = "Race"
#         elif key == '3':
#             class_name = "Politics"
#         elif key == '4':
#             class_name = "Sports"
#         st.write(f"{class_name}:  {value} %")

# st.markdown("---")

# #### THIS IS PAGE 2
# url_2 = st.secrets['key_ap_user']

# st.title("Twitter User profile")
# user = st.text_area("Enter your user:", max_chars=50)
# n_tweets = st.slider("Select a number between 5 and 50", 5, 50, 15)

# params_2 = {'user' : user,
#             'n_tweets': n_tweets }

# scanner_user = st.button('Scan user')

# # Query to check if username is in BQ
# query_user_bq = f"""
# WITH temp_table as (
# SELECT *, LOWER(user_name) as name_lower FROM {st.secrets["GCP_PROJECT"]}.{st.secrets["BQ_DATASET"]}.{st.secrets["BQ_TABLE"]})
# SELECT * from temp_table
# WHERE name_lower = LOWER('{user}')
# """
# query_result = run_query(query_user_bq)

# # Logic to scann user, if it is in BQ bring data from BQ; if not get prediction from our API

# if scanner_user:
#     if not query_result.empty:
#         hate_columns = ['hate_label','Religion_class', 'Gender_class', 'Race_class', 'Politics_class', 'Sports_class']
#         hate_data = query_result[hate_columns]
#         scale = hate_data['hate_label'].item()
#         scale = transform_hate_label(scale)
#         if scale in scale_mapping:
#             label, emoji = scale_mapping[scale]
#             st.write("Hate Label Scale:", f"{label} {emoji}")
#             st.title("Hate Level:")
#             st.select_slider("Your tweet is:",
#                                     options=[0, 1, 2],
#                                     value=scale,
#                                     format_func=format_hate_scale)
#         # This is the code for printing the Hate topics
#         st.title('Hate topics:')
#         class_columns = ['Religion_class', 'Gender_class', 'Race_class', 'Politics_class', 'Sports_class']
#         class_data = query_result[class_columns]
#         top_values = class_data.select_dtypes(include='float').transpose().nlargest(5, columns=0)
#         top_values.index = top_values.index.str.replace('_class', '')
#         formatted_values = top_values.applymap(lambda x: f'{x:.1%}')
#         for index, value in formatted_values.iterrows():
#             st.write(f'{index}: {value[0]}')
#     else:
#         # This is the code for printing the Hate scale
#         response = requests.get(url_2, params=params_2)
#         #Connection to model_scale through our API
#         scale = response.json()['hate_scale']['HateLabel']
#         scale = transform_hate_label(scale)
#         #Connection to model_topic through our API
#         topics = response.json()['hate_class']
#         if scale in scale_mapping:
#             label, emoji = scale_mapping[scale]
#             st.write("Hate Label Scale:", f"{label} {emoji}")
#             st.title("Hate Level:")
#             st.select_slider("Your tweet is:",
#                                     options=[0, 1, 2],
#                                     value=scale,
#                                     format_func=format_hate_scale)
#         else:
#             st.write("Hate Label Scale:", scale)

#         st.markdown("---")
#         # This is the code for printing the Hate topics
#         st.title('Hate topics:')
#         for key, value in topics.items():
#             class_name = ""
#             if key == '0':
#                 class_name = "Religion"
#             elif key == '1':
#                 class_name = "Gender"
#             elif key == '2':
#                 class_name = "Race"
#             elif key == '3':
#                 class_name = "Politics"
#             elif key == '4':
#                 class_name = "Sports"
#             st.write(f"{class_name}:  {value} %")


# ##Query to get data from BQ to graph as you want
# # Query will need to be modified depending on the graph that needed to be ploted
# st.markdown("---")


# query = f"""
#     SELECT *
#     FROM {st.secrets["GCP_PROJECT"]}.{st.secrets["BQ_DATASET"]}.{st.secrets["BQ_TABLE"]}
#     LIMIT 200
# """
# df_queried = run_query(query)

# pca = PCA(n_components=3)
# pca_df = pca.fit_transform(df_queried[['Religion_class', 'Gender_class', 'Race_class', 'Politics_class', 'Sports_class']])
# pca_df = pd.DataFrame(pca_df, columns=['pca_1', 'pca_2', 'pca_3'])
# df_combined = pd.concat([df_queried, pca_df], axis=1)
# # Calculate the normalized sizes based on 'nr_followers'
# max_followers = df_combined['nr_followers'].max()
# min_followers = df_combined['nr_followers'].min()
# df_combined['normalized_size'] = ((df_combined['nr_followers'] - min_followers) / (max_followers - min_followers)) * 100
# # Apply the transformation to the 'hate_label' column
# df_combined['hate_label'] = df_combined['hate_label'].apply(transform_hate_label)
# df_combined['hate_label_name'] = df_combined['hate_label']
# df_combined['hate_label_name'] = df_combined['hate_label_name'].replace(0, "Normal")
# df_combined['hate_label_name'] = df_combined['hate_label_name'].replace(1, "Offensive")
# df_combined['hate_label_name'] = df_combined['hate_label_name'].replace(2, "Hate")
# fig = px.scatter_3d(df_combined, x='pca_1', y='pca_2', z='pca_3', color='hate_label',
#                     size='normalized_size', hover_name='name_lastname', color_continuous_scale='temps',
#                     range_color=[0, 2], size_max=50, custom_data=['hate_label', 'name_lastname', 'nr_followers', 'hate_label_name'])
# fig.update_layout(
#     scene=dict(
#         xaxis_title='PCA 1',
#         yaxis_title='PCA 2',
#         zaxis_title='PCA 3',
#         camera=dict(
#             eye=dict(x=1, y=-1.5, z=1)
#         )
#     ),
#     margin=dict(l=0, r=0, b=0, t=0)
# )
# fig.update_traces(opacity=1, marker=dict(symbol='circle'), hovertemplate='<b>%{hovertext}</b><br>Hate Label: %{customdata[3]}<br>Followers: %{customdata[2]:,.0f}')
# fig.update_layout(coloraxis_colorbar=dict(title='Hate Label'), coloraxis_colorbar_len=1, coloraxis_colorbar_thickness=15)
# st.title("Twitter User profile")
# st.plotly_chart(fig)

# #Space for graph
