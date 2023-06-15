import streamlit as st
import numpy as np
import time
import pandas as pd
import requests

import plotly.graph_objects as go
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import time
import pandas as pd
from sklearn.decomposition import PCA
import plotly.express as px
from hatescan.app.pages.single_scan import run_query, transform_hate_label, format_hate_scale

def global_scan_page():

    spacing = '''
        <style>
            .spacing {
                margin-top: 200px;
            }
        </style>
    '''
    gap = '''
        <style>
            .gap {
                margin-top: 50px;
            }
        </style>
    '''

    # Hate Scan Title
    st.title('GlobalScan :mega:')
    st.write('Analysis of All Twitter Accounts Scanned by HateScan')

    # Gap CSS
    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)


    query = f"""
    SELECT *
    FROM {st.secrets["GCP_PROJECT"]}.{st.secrets["BQ_DATASET"]}.{st.secrets["BQ_TABLE"]}
    LIMIT 1000
    """
    df_queried = run_query(query)

    # Displaey metrics
    col1, col2 = st.columns(2)
    # Display the metrics in each column
    with col1:
        st.metric('Number of Accounts Analyzed', len(df_queried))
    with col2:
        st.metric('Number of Tweets Analyzed', df_queried['tweets_analysed'].sum())

    #Space for graph
    # Gap CSS
    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)


    # Plotly graph
    pca = PCA(n_components=3)
    pca_df = pca.fit_transform(df_queried[['Religion_class', 'Gender_class', 'Race_class', 'Politics_class', 'Sports_class']])
    pca_df = pd.DataFrame(pca_df, columns=['pca_1', 'pca_2', 'pca_3'])
    df_combined = pd.concat([df_queried, pca_df], axis=1)
    # Calculate the normalized sizes based on 'nr_followers'
    max_followers = df_combined['nr_followers'].max()
    min_followers = df_combined['nr_followers'].min()
    df_combined['normalized_size'] = ((df_combined['nr_followers'] - min_followers) / (max_followers - min_followers)) * 100
    # Apply the transformation to the 'hate_label' column
    df_combined['hate_label'] = df_combined['hate_label'].apply(transform_hate_label)
    df_combined['hate_label_name'] = df_combined['hate_label']
    df_combined['hate_label_name'] = df_combined['hate_label_name'].replace(0, "Normal")
    df_combined['hate_label_name'] = df_combined['hate_label_name'].replace(1, "Offensive")
    df_combined['hate_label_name'] = df_combined['hate_label_name'].replace(2, "Hate")
    fig = px.scatter_3d(df_combined, x='pca_1', y='pca_2', z='pca_3', color='hate_label',
                        size='normalized_size', hover_name='name_lastname', color_continuous_scale='temps',
                        range_color=[0, 2],size_max= 70 ,custom_data=['hate_label', 'name_lastname', 'nr_followers', 'hate_label_name'])
    fig.update_layout(
        scene=dict(
            xaxis_title='PCA 1',
            yaxis_title='PCA 2',
            zaxis_title='PCA 3',
            camera=dict(
                eye=dict(x=1, y=-1.5, z=1)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    fig.update_traces(opacity=1, marker=dict(symbol='circle', sizemin=25), hovertemplate='<b>%{hovertext}</b><br>Hate Label: %{customdata[3]}<br>Followers: %{customdata[2]:,.0f}')
    fig.update_layout(coloraxis_colorbar=dict(title='Hate Label'), coloraxis_colorbar_len=1, coloraxis_colorbar_thickness=15)
    st.title("Twitter User profile")
    st.plotly_chart(fig)

    # Gap CSS
    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    # Create two columns
    tab1, tab2 = st.columns(2)

    with tab1:
        st.markdown("#### Hate Label Distribution")
        data = {
            'Hate Label': ['Hate', 'Offensive', 'Normal'],
            'Value': [15, 20, 10]  # Update with the actual values
        }
        df = pd.DataFrame(data)

        # Define the custom color palette
        custom_palette = alt.Scale(
            domain=['Hate', 'Offensive', 'Normal'],
            range=['#D7667A', '#E8E29C', '#179A8E']
        )

        # Sort the DataFrame by the predefined order
        df = df.sort_values('Hate Label', key=lambda x: x.map({'Hate': 0, 'Offensive': 1, 'Normal': 2}))

        # Create the stacked bar chart using Altair
        chart = alt.Chart(df).mark_bar().encode(
            x='Value:Q',
            y=alt.Y('Hate Label:O', sort='-x'),
            color=alt.Color('Hate Label:N', scale=custom_palette)
        ).properties(
            width=400,
            height=200
        )

        # Display the chart using Streamlit
        st.altair_chart(chart, use_container_width=True)

    with tab2:
        st.markdown("#### Topic ID Distribution")

        data = {
            'Topic ID': ['Religion', 'Gender', 'Race', 'Politics', 'Sports'],
            'Value': [15, 20, 10, 12, 18]  # Update with the actual values
        }
        df = pd.DataFrame(data)

        # Define the custom color palette
        custom_palette = alt.Scale(
            domain=['Religion', 'Gender', 'Race', 'Politics', 'Sports'],
            range=['#D7667A', '#E8E29C', '#179A8E', '#7B3F61', '#3A6186']
        )

        # Sort the DataFrame by the predefined order
        df = df.sort_values('Topic ID', key=lambda x: x.map({
            'Religion': 0, 'Gender': 1, 'Race': 2, 'Politics': 3, 'Sports': 4
        }))

        # Create the stacked bar chart using Altair
        chart = alt.Chart(df).mark_bar().encode(
            x='Value:Q',
            y=alt.Y('Topic ID:O', sort='-x'),
            color=alt.Color('Topic ID:N', scale=custom_palette)
        ).properties(
            width=400,
            height=200
        )

        # Display the chart using Streamlit
        st.altair_chart(chart, use_container_width=True)
