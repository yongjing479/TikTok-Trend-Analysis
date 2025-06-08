import streamlit as st
import plotly.express as px
import pandas as pd
import ast

def show_industry_analytics(trending_hashtags_df=None, industry_df=None):
    st.markdown('<h2 style="margin-bottom: 0.5em;">Industry Analysis</h2>', unsafe_allow_html=True)
    if trending_hashtags_df is None or industry_df is None:
        try:
            trending_hashtags_df = pd.read_csv('back up tiktok/trending_hashtags.csv')
            trending_hashtags_df['industry_info'] = trending_hashtags_df['industry_info'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            trending_hashtags_df['trend'] = trending_hashtags_df['trend'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            # --- Industry summary calculation ---
            from collections import defaultdict
            def calc_trend_slope(trend):
                values = [point['value'] for point in trend]
                if len(values) > 1:
                    return (values[-1] - values[0]) / (len(values) - 1)
                return 0
            industry_summary = defaultdict(lambda: {
                'hashtag_count': 0,
                'total_video_views': 0,
                'total_publish_cnt': 0,
                'avg_rank': 0,
                'hashtags': [],
                'trend_slopes': []
            })
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
        except Exception as e:
            st.error(f'Could not read or process trending_hashtags.csv: {e}')
            return
    # --- Remove industries with missing or empty names ---
    industry_df_clean = industry_df[industry_df['industry'].astype(str).str.strip() != '']
    # --- Total Video Views by Industry ---
    st.markdown('**Total Video Views by Industry**')
    fig = px.bar(
        industry_df_clean.sort_values('total_video_views', ascending=False),
        x='industry',
        y='total_video_views',
        color='total_video_views',
        color_continuous_scale='RdBu',
        labels={'industry': 'Industry', 'total_video_views': 'Total Video Views'},
        title='Total Video Views by Industry'
    )
    fig.update_layout(
        xaxis_title='Industry',
        yaxis_title='Total Video Views',
        font_color='#232526',
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font=dict(size=20, color='#232526', family='Arial'),
        margin=dict(l=60, r=30, t=60, b=40),
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    # --- Average Trend Growth by Industry ---
    st.markdown('**Average Trend Growth by Industry**')
    fig2 = px.bar(
        industry_df_clean.sort_values('avg_trend_growth', ascending=False),
        x='industry',
        y='avg_trend_growth',
        color='avg_trend_growth',
        color_continuous_scale='RdBu',
        labels={'industry': 'Industry', 'avg_trend_growth': 'Average Trend Growth'},
        title='Average Trend Growth by Industry'
    )
    fig2.update_layout(
        xaxis_title='Industry',
        yaxis_title='Average Trend Growth',
        font_color='#232526',
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font=dict(size=20, color='#232526', family='Arial'),
        margin=dict(l=60, r=30, t=60, b=40),
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)
