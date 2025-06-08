import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast
from scipy.stats import linregress

def show_trending_songs():
    st.markdown('<h2 style="margin-bottom: 0.5em;">Trending Songs</h2>', unsafe_allow_html=True)
    song_col1, song_col2 = st.columns(2)
    try:
        trending_songs_df = pd.read_csv('back up tiktok/trending_songs.csv')
        trending_songs_df['trend'] = trending_songs_df['trend'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        # Expand trend list into new DataFrame
        trend_rows = []
        for idx, row in trending_songs_df.iterrows():
            for trend_point in row['trend']:
                trend_rows.append({
                    'title': row['title'],
                    'author': row['author'],
                    'date': pd.to_datetime(trend_point['date'], unit='s'),
                    'value': trend_point['value']
                })
        trend_df = pd.DataFrame(trend_rows)
        # Get top 5 songs by max trend value
        top_titles = trend_df.groupby('title')['value'].max().sort_values(ascending=False).head(5).index
        top_df = trend_df[trend_df['title'].isin(top_titles)]
        with song_col1:
            fig = go.Figure()
            for title in top_titles:
                song_data = top_df[top_df['title'] == title]
                fig.add_trace(go.Scatter(
                    x=song_data['date'],
                    y=song_data['value'],
                    mode='lines+markers',
                    name=title
                ))
            fig.update_layout(
                title='Top 5 Songs: Trend Value Over Time',
                xaxis_title='Date',
                yaxis_title='Trend Score',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_color='#232526',
                legend=dict(
                    x=1.02, y=1, xanchor='left', yanchor='top',
                    bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                ),
                margin=dict(l=60, r=30, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
        # Calculate growth rate (slope) for each song
        growth_data = []
        for title in trending_songs_df['title'].unique():
            subset = trend_df[trend_df['title'] == title].sort_values('date')
            if len(subset) >= 2:
                x = (subset['date'] - subset['date'].min()).dt.total_seconds()
                y = subset['value']
                slope, _, _, _, _ = linregress(x, y)
                growth_data.append({'title': title, 'slope': slope})
        growth_df = pd.DataFrame(growth_data).sort_values('slope', ascending=False)
        with song_col2:
            fig2 = px.bar(
                growth_df.head(5),
                x='slope',
                y='title',
                orientation='h',
                labels={'title': 'Song Title', 'slope': 'Trend Growth Slope'},
                color='slope',
                color_continuous_scale='Blues',
                title='Top 5 Fastest Growing Song Trends (Slope)'
            )
            fig2.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_color='#232526',
                xaxis_title='Trend Growth Slope',
                yaxis_title='Song Title',
                title_font=dict(size=20, color='#232526', family='Arial'),
                margin=dict(l=60, r=30, t=60, b=40)
            )
            st.plotly_chart(fig2, use_container_width=True)
        # Song Duration vs Average Trend Score (no extra h2, just chart below)
        trend_rows_duration = []
        for _, row in trending_songs_df.iterrows():
            if isinstance(row['trend'], list):
                for t in row['trend']:
                    trend_rows_duration.append({
                        'title': row['title'],
                        'duration': row['duration'],
                        'date': pd.to_datetime(t['date'], unit='s'),
                        'value': t['value']
                    })
        trend_df_duration = pd.DataFrame(trend_rows_duration)
        avg_trend = trend_df_duration.groupby(['title', 'duration'])['value'].mean().reset_index()
        fig3 = px.scatter(
            avg_trend,
            x='duration',
            y='value',
            trendline='ols',
            labels={'duration': 'Duration (seconds)', 'value': 'Average Trend Score'},
            title='Song Duration vs Average Trend Score',
            color_discrete_sequence=['#7f7fd5']
        )
        fig3.update_traces(marker=dict(size=10, opacity=0.7))
        fig3.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='#232526',
            xaxis_title='Duration (seconds)',
            yaxis_title='Average Trend Score',
            title_font=dict(size=20, color='#232526', family='Arial'),
            margin=dict(l=60, r=30, t=60, b=40)
        )
        st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.error(f'Could not read or plot trending_songs.csv: {e}')
