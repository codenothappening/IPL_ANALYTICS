import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datasetProcessing import new_matchesDF, new_deliveriesDF

def app():
    st.markdown(''' 
    <h1 style='text-align:center; color: #e8630a;'><strong>📈EXPLORATORY DATA ANALYSIS📈</strong></h1>
    <hr style="border-top: 3px solid #e8630a;">
    ''', unsafe_allow_html=True)

    # Dataset Overview
    with st.expander("Matches Dataset: 2008-2024"):
        st.write(new_matchesDF.head(5))
        
        # Add a download button for Matches dataset
        st.download_button(
            label="Download Matches Dataset (CSV)",
            data=new_matchesDF.to_csv(index=False),
            file_name="matches_2008_2024.csv",
            mime="text/csv"
        )
        
        if st.checkbox(label="Code", key=0):
            st.code(''' 
                new_matchesDF = pd.read_csv('matches_2008-2024.csv')
                new_matchesDF.columns = new_matchesDF.columns.str.strip()
                st.write(new_matchesDF.head(5))
            ''', language='python')

    with st.expander("Delivery Dataset: 2008-2024"):
        st.write(new_deliveriesDF.head(5))
        
        # Add a download button for Deliveries dataset
        st.download_button(
            label="Download Deliveries Dataset (CSV)",
            data=new_deliveriesDF.to_csv(index=False),
            file_name="deliveries_2008_2024.csv",
            mime="text/csv"
        )
        
        if st.checkbox(label="View Code", key=1):
            st.code(''' 
                new_deliveriesDF = pd.read_csv('deliveries_2008-2024.csv')
                new_deliveriesDF.columns = new_deliveriesDF.columns.str.strip()
                st.write(new_deliveriesDF.head(5))
            ''', language='python')

    # Matches per Season
    with st.expander("Matches per Season"):
        # Filter data for seasons 2009 to 2024
        filtered_seasons = new_matchesDF[new_matchesDF['season'] >= 2008]
        matches_per_season = filtered_seasons['season'].value_counts().sort_index()

        # Define colors only for the filtered seasons
        colors = px.colors.qualitative.Safe
        color_list = [colors[i % len(colors)] for i in range(len(matches_per_season))]

        trace = go.Bar(
            x=matches_per_season.index,
            y=matches_per_season.values,
            text=matches_per_season.values,
            marker={'color': color_list}
        )

        layout = go.Layout(
            title="Matches Per Season (2009-2024)",
            xaxis={'title': 'Season'},
            yaxis={'title': 'Number of Matches Played'}
        )

        fig = go.Figure(data=[trace], layout=layout)

        st.plotly_chart(fig, use_container_width=True)

    # Top Players of the Match
    with st.expander("Top Players with Most Player of the Match Awards"):
        num_players = st.slider(
            "Select Number of Players to Display",
            min_value=5, max_value=50, value=30, step=5
        )

        top_POTM = new_matchesDF['player_of_match'].value_counts().head(num_players)

        fig = px.bar(
            x=top_POTM.values,
            y=top_POTM.index,
            orientation='h',
            labels={'x': 'POTM Awards', 'y': 'Player'},
            text=top_POTM.values,
            color=top_POTM.index,
            color_discrete_sequence=px.colors.qualitative.Safe
        )

        fig.update_layout(
            height=700,
            width=900,
            title="Top Players with Most Player of the Match Awards"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Top Venues with Most Matches
    with st.expander("Top Venues with Most Matches"):
        num_venues = st.slider(
            "Select Number of Venues to Display",
            min_value=5, max_value=20, value=10, step=1
        )

        top_venues = new_matchesDF['venue'].value_counts().head(num_venues)

        fig = px.bar(
            x=top_venues.index,
            y=top_venues.values,
            labels={'x': 'Venue', 'y': 'Total Matches Played'},
            text=top_venues.values,
            color=top_venues.index,
            color_discrete_sequence=px.colors.qualitative.Safe
        )

        fig.update_layout(
            title="Top Venues with Most Matches",
            height=700,
            width=900
        )

        st.plotly_chart(fig, use_container_width=True)

    # Team with Most Match Wins
    with st.expander("Team with Most Match Wins"):
        teams_to_include = st.multiselect(
            "Select Teams to Display",
            options=new_matchesDF['winner'].unique(),
            default=new_matchesDF['winner'].dropna().unique()
        )

        team_wins = (
            new_matchesDF[new_matchesDF['winner'].isin(teams_to_include)]
            .groupby('winner').size()
            .sort_values()
        )

        fig = px.bar(
            y=team_wins.index,
            x=team_wins.values,
            orientation='h',
            labels={'x': 'Total Wins', 'y': 'Team'},
            text=team_wins.values,
            color=team_wins.index,
            color_discrete_sequence=px.colors.qualitative.Safe
        )

        fig.update_layout(
            title="Team with Most Match Wins",
            height=700,
            width=900
        )

        st.plotly_chart(fig, use_container_width=True)
