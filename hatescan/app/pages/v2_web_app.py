import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go



def show_new_layout():

    # Define custom CSS styles
    custom_css = """
    <style>
    .spacing {
        margin-top: 200px;
    }
    .st-ds{
        height: 20px;
    }
    .css-1vzeuhh {
        height: 1.5rem;
        width: 1.5rem;
    }
    .css-16idsys p {
        font-size: 20px;
    </style>
    """

    # Hate Scan Title
    # Load the logo image from a local file or URL
    logo_image = 'images/hatescan-high-resolution-logo-color-on-transparent-background.png'
    # Display the logo image in Streamlit
    st.image(logo_image, width=300)  # Adjust the width as needed
    st.markdown('#### Welcome to our Hate Speech recognition app')


    # Section 1 - Tweet Box

    st.markdown('### Enter tweet to analyze:')
    tweet = st.text_area("Tweet Box", max_chars=200)
    st.markdown("Scan:")
    st.write(tweet)
    scanner = st.button('Scan tweet')

    def format_hate_scale(value):
        if value == 0:
            return "Normal"
        elif value == 1:
            return "Offensive"
        elif value == 2:
            return "Hate"
        else:
            return str(value)


    # Section 2  - The Hate Scale
    st.markdown("## Hate Scale")
    hate_scale = st.select_slider("##### Hate label prediction:",
                                    options=[0, 1, 2],
                                    value=0,
                                    format_func=format_hate_scale)

    st.write("Your hate scale is :", format_hate_scale(hate_scale))


    # Apply custom CSS styles
    st.markdown(custom_css, unsafe_allow_html=True)

    st.markdown('<div class="spacing"></div>', unsafe_allow_html=True)

    # Section 3 - Topic's that the Account References

    st.markdown("### Account Scan:" )

    # Assuming you have variables `num_tweets` and `hate_percentage` with the corresponding values
    num_tweets = 20
    hate_percentage = 90

    # Create two columns
    col1, col2 = st.columns(2)

    # Apply CSS style
    st.markdown(custom_css, unsafe_allow_html=True)

    # Display the metrics in each column
    with col1:
        st.metric("Number of Tweets Analyzed", num_tweets)
    with col2:
        st.metric("Average Hate Level of Tweets", f"{hate_percentage}%")

    # Create the DataFrame
    # Create the DataFrame
    # Create the DataFrame
    data = pd.DataFrame({
        'Category': ['Religion', 'Gender', 'Race', 'Politics', 'Sport'],
        'Number of Tweets': [10, 20, 15, 25, 18]
    })

    # Define shades of red colors
    color_palette = ['#FFD4D4', '#FFB2B2', '#FF9191', '#FF7070', '#FF4E4E']

    # Create the bar chart using Plotly
    fig = go.Figure(data=[go.Bar(x=data['Category'], y=data['Number of Tweets'], marker_color=color_palette)])

    # Add category labels
    # Add category labels
    fig.update_layout(
        annotations=[
            go.layout.Annotation(
                x=x,
                y=y,
                text=str(y),
                showarrow=False,
                font=dict(color='grey', size=16),
                xanchor='center',
                yanchor='bottom'
            ) for x, y in zip(data.index, data['Number of Tweets'])
        ],
        title="Number of Tweets by Category",
        title_font=dict(size=20, color="grey"),  # Specify non-bold font style using family parameter
        xaxis=dict(
            title="Category",
            title_font=dict(size=18),
            tickfont=dict(size=16)
        ),
        yaxis=dict(
            title="Number of Tweets",
            title_font=dict(size=18),
            tickfont=dict(size=16)
        )
    )

    # Display the chart using Streamlit
    st.plotly_chart(fig)
