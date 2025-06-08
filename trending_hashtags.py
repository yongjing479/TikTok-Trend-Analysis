import streamlit as st
import pandas as pd
import ast
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

def show_trending_hashtags():
    st.markdown('<div style=" padding: 18px 24px; border-radius: 12px; margin-bottom: 1.5em; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: inline-block;">\
        <h2 style="margin: 0; color: #232526; font-weight: 700; letter-spacing: 0.5px;">Trending Hashtags</h2>\
    </div>', unsafe_allow_html=True)
    try:
        trending_hashtags_df = pd.read_csv('back up tiktok/trending_hashtags.csv')
        # --- Industry summary calculation ---
        industry_summary = defaultdict(lambda: {
            'hashtag_count': 0,
            'total_video_views': 0,
            'total_publish_cnt': 0,
            'avg_rank': 0,
            'hashtags': [],
            'trend_slopes': []
        })
        def calc_trend_slope(trend):
            values = [point['value'] for point in trend]
            if len(values) > 1:
                return (values[-1] - values[0]) / (len(values) - 1)
            return 0
        trending_hashtags_df['industry_info'] = trending_hashtags_df['industry_info'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        trending_hashtags_df['trend'] = trending_hashtags_df['trend'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        for _, row in trending_hashtags_df.iterrows():
            industry = row['industry_info']['value']
            industry_summary[industry]['hashtag_count'] += 1
            industry_summary[industry]['total_video_views'] += row['video_views']
            industry_summary[industry]['total_publish_cnt'] += row['publish_cnt']
            industry_summary[industry]['avg_rank'] += row['rank']
            industry_summary[industry]['hashtags'].append(row['hashtag_name'])
            slope = calc_trend_slope(row['trend'])
            industry_summary[industry]['trend_slopes'].append(slope)
        for summary in industry_summary.values():
            summary['avg_rank'] /= summary['hashtag_count']
            if summary['trend_slopes']:
                summary['avg_trend_growth'] = sum(summary['trend_slopes']) / len(summary['trend_slopes'])
            del summary['trend_slopes']
        industry_df = pd.DataFrame.from_dict(industry_summary, orient='index').reset_index()
        industry_df.rename(columns={'index': 'industry'}, inplace=True)
        # --- Existing hashtag tables ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('**Top 10 Hashtags by Rank**')
            top_rank = trending_hashtags_df[['hashtag_name', 'rank']].sort_values(by='rank').head(10)
            top_rank = top_rank.reset_index(drop=True)
            top_rank.index = top_rank.index + 1
            top_rank.index.name = "No."
            st.dataframe(top_rank)
        with col2:
            st.markdown('**Top 10 Hashtags by Video Views**')
            top_views = trending_hashtags_df[['hashtag_name', 'video_views']].sort_values(by='video_views', ascending=False).head(10)
            top_views = top_views.reset_index(drop=True)
            top_views.index = top_views.index + 1
            top_views.index.name = "No."
            st.dataframe(top_views)
        with col3:
            st.markdown('**Top 10 Hashtags by Most Posts**')
            top_posts = trending_hashtags_df[['hashtag_name', 'publish_cnt']].sort_values(by='publish_cnt', ascending=False).head(10)
            top_posts = top_posts.reset_index(drop=True)
            top_posts.index = top_posts.index + 1
            top_posts.index.name = "No."
            st.dataframe(top_posts)
        # --- Top 10 Hashtag Trend Scores Over Time ---
        st.markdown('**Top 10 Hashtag Trend Scores Over Time**')
        # Flatten trend data
        trend_data = []
        for _, row in trending_hashtags_df.iterrows():
            for t in row['trend']:
                trend_data.append({
                    'hashtag_name': row['hashtag_name'],
                    'date': pd.to_datetime(t['date'], unit='s'),
                    'value': t['value']
                })
        trend_df = pd.DataFrame(trend_data)
        # Get top 10 hashtags by average trend value
        top_hashtags = (
            trend_df.groupby('hashtag_name')['value']
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .index
        )
        filtered_trend_df = trend_df[trend_df['hashtag_name'].isin(top_hashtags)]
        import plotly.graph_objects as go
        fig_trend = go.Figure()
        for name in filtered_trend_df['hashtag_name'].unique():
            subset = filtered_trend_df[filtered_trend_df['hashtag_name'] == name]
            fig_trend.add_trace(go.Scatter(
                x=subset['date'],
                y=subset['value'],
                mode='lines+markers',
                name=name
            ))
        fig_trend.update_layout(
            title='Top 10 Hashtag Trend Scores Over Time',
            xaxis_title='Date',
            yaxis_title='Trend Value',
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
        st.plotly_chart(fig_trend, use_container_width=True)
        # --- Remove industries with missing or empty names ---
        industry_df_clean = industry_df[industry_df['industry'].astype(str).str.strip() != '']
    except Exception as e:
        st.error(f'Could not read or plot trending_hashtags.csv: {e}')