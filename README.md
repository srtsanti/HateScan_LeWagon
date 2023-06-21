# HateScan

This project was built by Elina Emsems, Joaquin Ortega and Santiago Rodriguez as the final deliverable in Le Wagons #1237 Data Science Batch.

With HateScan, you can analyze language usage from real Twitter accounts. Such as from friends, celebrities and public figures. Compare tweets, accounts and glocal scores to to gain a deeper understanding of speech patterns and explore prevalent topics.
#
### Model 1: Hate Label Prediction
Our first Recurrent Neural Network model classifies whether a tweet contains Normal, Offensive or Hateful language

### Model 2: Hate Topic Prediction
Our second developed RNN model classifies what the topic is about: Religion, Gender, Race, Politics & Sport.
#
### Functionality 1: Tweet Scan
Obtain the Hate Label and Topic prediction of real tweets with our trained models.

### Functionality 2: Account Scan
Analyze twitter accounts of your choice. Select the number of tweets and Twitter API is used to calculate with our model the overall Hate level of the account and the prevalance of the topics that the Account tweets about. Understand the impact of a hateful account by visualizing the account dashboard with number of followers as an impact KPI.

### Functionality 3: Global Scan
Discover all the accounts that have been scanned in the App, which are automatically stored in a database upon scan. We take the data from the DB and represent the hate level of public figures with respect to eachother on a 3D Plotly graph.

HateScan web: https://hatescan.streamlit.app/
