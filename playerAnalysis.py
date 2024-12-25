import streamlit as st
import plotly.graph_objects as go
from scrollToTop import create_scroll_to_top_button
from datasetPreprocessing import new_deliveriesDF



def app():
    st.markdown('''<h1 style='text-align:center; color: #4fb9fc;'><strong>🏏 PLAYER ANALYSIS 🏏</strong></h1>
    <hr style="border-top: 3px solid #4fb9fc;">
    ''', unsafe_allow_html=True)

    Batsman = new_deliveriesDF['batter'].unique().toList()
    Bowler = new_deliveriesDF['bowler'].unique().toList()

    Batsman.extend(Bowler)
    players = list(set(Batsman))

    player = st.selectbox("Select A Player", Players)
    Analyze = st.button('Analyze')

    if Analyze:
        selected_player_bat_df = new_deliveriesDF[new_deliveriesDF['batter']==player]
        if len(selected_player_bat_df) != 0:
            player_runs_against_teams =selected_player_bat_df.groupby('bowling_team')['total_runs'].sun().reset_index().sort_values(
                by = 'total_runs',ascending = False
            )

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=player_runs_against_teams['bowling_team'],
                y=player_runs_against_teams['total_runs'],
                marker=dict(color=player_runs_against_teams['total_runs'],
                            colorscale='Viridis'),
                text=player_runs_against_teams['total_runs'],
                textposition='auto',
                hoverinfo='y+x',
            ))