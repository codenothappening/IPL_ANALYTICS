import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.offline as pyo
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from datasetProcessing import new_matchesDF, new_deliveriesDF

def app():
    st.markdown('''
    <h1 style='text-align:center; color: #ffffff;'><strong> 🏏 TEAM ANALYSIS 🤾‍♂️ </strong></h1>
    <hr style="border-top: 3px solid #4ef037;">
    ''', unsafe_allow_html=True)
    
    Teams = new_matchesDF.team1.drop_duplicates().tolist()

    team = st.selectbox('Select a Team', Teams)

    Analyze = st.button('Analyze')

    if Analyze:
        st.markdown(f"<h4 style='text-align: center; color: #ffffff;'> {team} </h4>", unsafe_allow_html=True)

        selected_team_df = new_deliveriesDF[new_deliveriesDF['batting_team'].str.strip() == team]

        innings_data = selected_team_df.groupby(['match_id','inning','bowling_team'])['total_runs'].sum().reset_index()

        innings_data_scores = innings_data.groupby('bowling_team')['total_runs'].mean().round().astype(int).reset_index().sort_values(by = 'total_runs',ascending= False,)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=innings_data_scores['bowling_team'],
            y=innings_data_scores['total_runs'],
            mode='lines+markers+text',
            text=innings_data_scores['total_runs'],
            textposition='top center',
            marker=dict(color='lime', size=10),
            line=dict(color='lime', width=2),
        ))

        for i in range(len(innings_data_scores)):
            fig.add_trace(go.Scatter(
                x = [innings_data_scores['bowling_team'][i],
                    innings_data_scores['bowling_team'][i]],
                y=[0, innings_data_scores['total_runs'][i]],
                mode='lines',
                line=dict(color='orange', width=1, dash='dot'),
                showlegend=False
            ))
        
        fig.update_layout(
            title=f'Average Runs Scored By {team.strip()} Against Different Teams',
            title_font=dict(color='white'),
            xaxis_title="Bowling Teams",
            xaxis_title_font=dict(color='white'),
            yaxis_title="Total Runs",
            yaxis_title_font=dict(color='white'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                tickmode='linear',
                fixedrange=True
            ),
            height=600,
        )

        st.plotly_chart(fig,use_container_width=True)

        st.image("Images/divider.png")
        team_over_data = (selected_team_df.groupby('over')['total_runs'].mean()*6).round().astype(int).reset_index()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x = team_over_data['over'],
            y = team_over_data['total_runs'],

            mode = 'lines+markers+text',
            text=team_over_data['total_runs'],
            textposition='top center',
            marker=dict(color= 'lime',size= 8),
            line=dict(color = 'lime',width = 2),
        ))

        for i in range(len(team_over_data)):
            fig.add_trace(go.Scatter(
                x=[team_over_data['over'][i], team_over_data['over'][i]],
                y=[0, team_over_data['total_runs'][i]],
                mode='lines',
                line=dict(color='lime', width=1, dash='dot'),
                showlegend=False
            ))

        fig.update_layout(
            title=f'Average Runs Scored By {team} in Different Overs',
            title_font=dict(color='white'),
            xaxis_title="Overs",
            xaxis_title_font=dict(color='white'),
            yaxis_title="Total Runs",
            yaxis_title_font=dict(color='white'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=1,
                range=[0, 20],
                fixedrange=True
            ),
            height=600,
        )

        st.plotly_chart(fig,
                        use_container_width=True)

        st.image("Images/divider.png")

        team_toss_decision = new_matchesDF[new_matchesDF['toss_winner']==team]['toss_decision']
        team_toss_decision_counts = team_toss_decision.value_counts().reset_index()
        team_toss_decision_counts.columns = ['toss_decision','count']

        fig = px.bar(
            team_toss_decision_counts,
            x='toss_decision',
            y='count',
            text='count',
            labels={'toss_decision': 'Toss Decision', 'count': 'Count'},
            color_discrete_sequence=['lime'],
        )

        fig.update_layout(
            title=f'{team} Toss Decision',
            title_font=dict(color='white'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                fixedrange=True
            ),
            yaxis=dict(
                fixedrange=True
            ),
            height=400,
        )

        st.plotly_chart(fig, use_container_width=True)

        st.image("Images/divider.png")

        st. markdown(f"<h5 style='text-align: center; color: white;'> {team} Match Wins Based On Venue </h5>", unsafe_allow_html=True)

        venue_win = new_matchesDF[new_matchesDF['winner'] == team]['venue'].value_counts()[
            :10]

        fig = plt.figure(figsize=(20, 5))
        ax = sns.barplot(x=venue_win.index, y=venue_win.values)
        ax.bar_label(ax.containers[0],color='white')
        plt.xlabel('Venues', color='white')
        plt.ylabel('Wins', color='white')
        plt.xticks(fontsize=12, rotation='vertical', color='white')
        plt.yticks(color='white')
        plt.title(f'{team} Match Wins By Venue', color='white')
        st.pyplot(fig, transparent=True)

        st.image("Images/divider.png")

        st. markdown(f"<h5 style='text-align: center; color: #ffffff;'> {team} 200+ Runs </h5>", unsafe_allow_html=True)

        fig = plt.figure(figsize=(12, 10))
        team_runs_over_200_df = selected_team_df.groupby(['match_id', 'bowling_team', 'inning'])[
            'total_runs'].sum().reset_index().sort_values(by='total_runs', ascending=False)
        team_runs_over_200 = team_runs_over_200_df[team_runs_over_200_df['total_runs'] > 200]

        # Assign match_id + bowling_team to a new column `data` (used for the figure)
        team_runs_over_200['data'] = team_runs_over_200['match_id'].astype(str) + "_" + team_runs_over_200['bowling_team']

        # Format the labels to only display the `bowling_team` part
        formatted_labels = team_runs_over_200['bowling_team']

        ax = sns.barplot(data=team_runs_over_200, y='data', x='total_runs', ci=None)
        ax.set_yticklabels(formatted_labels)  # Set the y-axis labels to only display bowling_team
        ax.bar_label(ax.containers[0], color='white')
        plt.title(f'{team} 200+ Runs : Total({len(team_runs_over_200)})', color='white')
        plt.xlabel('Runs', color='white')
        plt.ylabel('Opponents', color='white')
        plt.xticks(fontsize=12, rotation='vertical', color='white')
        plt.yticks(color='white')
        st.pyplot(fig, transparent=True)



        st.image("Images/divider.png")
        st.markdown(f"<h5 style='text-align: center; color: #ffffff;'> {team} Top 10 Lowest Runs </h5>", unsafe_allow_html=True)

        fig = plt.figure(figsize=(12, 10))
        team_runs_over_df = selected_team_df.groupby(['match_id', 'bowling_team', 'inning'])['total_runs'].sum().reset_index().sort_values(by='total_runs', ascending=False)
        team_runs_over_df = team_runs_over_df[team_runs_over_df['inning'] < 3]
        team_runs_over_df = team_runs_over_df[:10]

        team_runs_over_df['data'] = team_runs_over_df['bowling_team']

        # Set ci=None to remove horizontal lines
        ax = sns.barplot(data=team_runs_over_df, y='data', x='total_runs', ci=None)
        ax.bar_label(ax.containers[0], color='white')  # Set color for bar labels
        plt.title(f'{team} Top 10 Lowest Runs', color='white')
        plt.xlabel('Runs', color='white')
        plt.ylabel('Opponents', color='white')
        plt.xticks(fontsize=12, rotation='vertical', color='white')
        plt.yticks(color='white')
        st.pyplot(fig, transparent=True)

        

        st.image("Images/divider.png")
