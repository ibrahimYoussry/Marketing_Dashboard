import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Marketing",
                page_icon=None,
                layout="wide",
                initial_sidebar_state="expanded")

df = pd.read_csv('Marketing_Cleaned.csv')

#Sidbar
st.sidebar.header('Marketing Dashboard' , text_alignment="center")
st.sidebar.subheader("About Dashboard :")
st.sidebar.write("""
Performing EDA on marketing campaign data to analyze campaign performance,
audience segments, and spending patterns. Creating KPIs and visualizations
to uncover key marketing insights.
""")
st.sidebar.divider()
st.sidebar.subheader('Dashboard Filters : ')

cat1_fil = st.sidebar.selectbox('ChanneL : ' , [None,'TikTok Ads','Instagram Ads' , 'Facebook Ads' , 'Google Ads' ,'Email'])
cat2_fil = st.sidebar.selectbox('Campaign_Type : ' , [None ,'Conversion','Traffic','Retargeting' ,'Lead Generation','Awareness'])
cat3_fil = st.sidebar.selectbox('Region : ' , [None ,'Mansoura','Cairo','Assiut','Giza','Alexandria'])
cat4_fil = st.sidebar.selectbox('Audience : ' , [None ,'Interest-Based','Lookalike','Remarketing','Existing Customers','Broad Audience' ,'Unknown'])
df = df[
    ((df['Channel'] == cat1_fil) | (cat1_fil is None)) &
    ((df['Campaign_Type'] == cat2_fil) | (cat2_fil is None)) &
    ((df['Region'] == cat3_fil) | (cat3_fil is None)) &
    ((df['Audience'] == cat4_fil) | (cat4_fil is None))
]

st.sidebar.markdown("Created by : Ibrahim Youssry")


#body
st.header('Marketing Campaign performance')
st.text('Marketing Analytics • Data-Driven Insights')
st.markdown("""
<hr style="
    width: 600px;
    margin-top: -10px;
    margin-left: 0;
    border: 2px solid #36415A;
    border-radius: 5px;
">
""", unsafe_allow_html=True)
cl1 ,cl2 , cl3, cl4 , cl5 = st.columns(5)
cl1.metric('TotaL Spend' , f"{df['Spend_EGP'].sum():,.0f} EGP")
cl2.metric('TotaL Revenue' , f"{df['Revenue_EGP'].sum():,.0f} EGP")
cl3.metric('Average CTR ' , f"{df['CTR'].mean():.2f}%")
cl4.metric('Average CVR' , f"{df['CVR'].mean():.2f}%")
cl5.metric('Overall ROAS' , f"{df['ROAS'].mean():.2f}X")
st.divider()
channel_roas = df.groupby('Channel').agg(
    Total_Revenue=('Revenue_EGP', 'sum'),
    Total_Spend=('Spend_EGP', 'sum')
).reset_index()
channel_roas['ROAS'] = (
    channel_roas['Total_Revenue'] /
    channel_roas['Total_Spend']
)
st.subheader('Channel performance')
c1 , c2 = st.columns(2)
fig = px.bar(data_frame= df, 
                x= 'Channel',
                y = 'Spend_EGP' ,
                color= "Channel",
                title='Spend by Channel')
fig.update_layout(
    legend=dict(
        title='Channel',
        orientation='v',
        x=1.02,
        y=0.5
    )
)
c1.plotly_chart(fig , use_container_width=True)

fig2 = px.bar(data_frame= channel_roas, 
                x= 'Channel',
                y = 'ROAS' ,
                color= 'Channel',
                title= "ROAS by Channel")
fig2.update_layout(
    legend=dict(
        title='Channel',
        orientation='v',
        x=1.02,
        y=0.5
    )
)
c2.plotly_chart(fig2 , use_container_width=True)


st.markdown("""**Summary Insight** : Facebook Ads recorded the highest marketing spend, while Email generated the highest ROAS, indicating better returns relative to its spending\n
**Recommendation** : Reallocate the marketing budget strategically across channels to maximize overall returns while maintaining a strong presence across all social media platforms, rather than relying heavily on a single channel.......  **⬆** """)


st.divider()
st.subheader('Audience Targeting Efficiency')
audience_cpa = df.groupby('Audience', as_index=False).agg(
    Total_Spend=('Spend_EGP', 'sum'),
    Total_Conversions=('Conversions', 'sum')
)

audience_cpa['CPA'] = (
    audience_cpa['Total_Spend'] /
    audience_cpa['Total_Conversions'].replace(0, float('nan'))
)

audience_cpa = audience_cpa.dropna(subset=['CPA']).sort_values('CPA')

fig3 = go.Figure()

for _, row in audience_cpa.iterrows():
    fig3.add_trace(go.Scatter(
        x=[0, row['CPA']],
        y=[row['Audience'], row['Audience']],
        mode='lines',
        line=dict(color='#7C83FD', width=3),
        showlegend=False
    ))

fig3.add_trace(go.Scatter(
    x=audience_cpa['CPA'],
    y=audience_cpa['Audience'],
    mode='markers+text',
    text=audience_cpa['CPA'].round(2),
    textposition='middle right',
    marker=dict(size=13, color='#A78BFA'),
    showlegend=False
))

fig3.update_layout(
    title='CPA by Audience',
    xaxis_title='CPA (EGP)',
    yaxis_title='Audience',
    template='plotly_dark'
)
#st.plotly_chart(fig3, use_container_width=True)

audience_roas = df.groupby('Audience', as_index=False).agg(
    Total_Revenue=('Revenue_EGP', 'sum'),
    Total_Spend=('Spend_EGP', 'sum')
)

audience_roas['ROAS'] = (
    audience_roas['Total_Revenue'] /
    audience_roas['Total_Spend'].replace(0, float('nan'))
)

audience_roas = audience_roas.dropna(subset=['ROAS']).sort_values('ROAS')

fig5 = go.Figure()

for _, row in audience_roas.iterrows():
    fig5.add_trace(go.Scatter(
        x=[0, row['ROAS']],
        y=[row['Audience'], row['Audience']],
        mode='lines',
        line=dict(color='#F59E0B', width=3),
        showlegend=False
    ))

fig5.add_trace(go.Scatter(
    x=audience_roas['ROAS'],
    y=audience_roas['Audience'],
    mode='markers+text',
    text=audience_roas['ROAS'].round(2),
    textposition='middle right',
    marker=dict(size=13, color='#FBBF24'),
    showlegend=False
))

fig5.update_layout(
    title='ROAS by Audience',
    xaxis_title='ROAS (X)',
    yaxis_title='Audience',
    template='plotly_dark'
)


c1, c2 = st.columns(2)

c1.plotly_chart(
    fig3,
    use_container_width=True,
    key='audience_cpa_chart'
)

c2.plotly_chart(
    fig5,
    use_container_width=True,
    key='region_roas_chart'
)
st.markdown("""**Summary Insight** : Lookalike Audience recorded the highest acquisition cost and the lowest ROAS, indicating inefficient spending and weaker returns. In contrast, Unknown Audience generated the highest ROAS, suggesting better advertising efficiency\n
**Recommendation** : Conduct a deeper audience analysis to identify which audience segments respond best to each marketing channel, particularly Email. Evaluate audience engagement and conversion performance to understand whether known or unidentified audience segments deliver better results, then optimize budget allocation based on these findings.......  **⬆** """)

st.divider()



monthly_roas = df.groupby(
    ['Year', 'Month'], as_index=False
).agg(
    Total_Revenue=('Revenue_EGP', 'sum'),
    Total_Spend=('Spend_EGP', 'sum')
)

monthly_roas['ROAS'] = (
    monthly_roas['Total_Revenue'] /
    monthly_roas['Total_Spend'].replace(0, float('nan'))
)

monthly_roas['Period'] = (
    monthly_roas['Year'].astype(str) + '-' +
    monthly_roas['Month'].astype(str).str.zfill(2)
)

monthly_roas = monthly_roas.sort_values(['Year', 'Month'])

fig6 = px.line(
    monthly_roas,
    x='Period',
    y='ROAS',
    markers=True,
    text=monthly_roas['ROAS'].round(2),
    title='Monthly ROAS Trend'
)

fig6.update_traces(
    textposition='top center',
    mode='lines+markers+text'
)

fig6.update_layout(
    xaxis_title='Month',
    yaxis_title='ROAS (X)',
    template='plotly_dark'
)

st.plotly_chart(
    fig6,
    use_container_width=True,
    key='monthly_roas'
)
st.markdown("""**Summary Insight** : ROAS experienced monthly fluctuations throughout the nine-month period, ending with a sharp decline in September, reaching its lowest point in Q3........  **⬆** """)



#df2 = st.dataframe(df)



