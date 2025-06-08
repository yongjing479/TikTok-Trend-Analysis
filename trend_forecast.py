import streamlit as st
import pandas as pd
import pickle
import os
import plotly.graph_objects as go

# Trend Forecast Section

def show_trend_forecast():
    st.markdown('<h2 style="margin-bottom: 0.5em;">Trend Forecast</h2>', unsafe_allow_html=True)
    
    # --- Prophet Time Series Forecast (if model and data available) ---
    prophet_path = 'back up tiktok/prophet_model.pkl'
    data_path = 'back up tiktok/enhanced_trend_predictions.csv'
    
    if os.path.exists(prophet_path) and os.path.exists(data_path):
        try:
            with open(prophet_path, 'rb') as f:
                prophet_model = pickle.load(f)
            
            df = pd.read_csv(data_path)
            df['create_time'] = pd.to_datetime(df['create_time'])
            ts_data = df.groupby(df['create_time'].dt.date)['is_trending'].sum().reset_index()
            ts_data.columns = ['ds', 'y']
            
            # Forecast next 30 days
            future = prophet_model.make_future_dataframe(periods=30)
            forecast = prophet_model.predict(future)
            
            # Create the figure with white background
            fig = go.Figure()
            
            # Add the actual data points
            fig.add_trace(go.Scatter(
                x=ts_data['ds'],
                y=ts_data['y'],
                mode='markers',
                name='Actual Data',
                marker=dict(
                    color='#2ca02c',
                    size=8,
                    line=dict(
                        color='#1a661a',
                        width=1
                    )
                )
            ))
            
            # Add the forecast line
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat'],
                mode='lines',
                name='Forecast',
                line=dict(
                    color='#1f77b4',
                    width=2,
                    dash='solid'
                )
            ))
            
            # Update layout
            fig.update_layout(
                title={
                    'text': 'Trending Content Forecast for Next 30 Days',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': dict(size=20)
                },
                xaxis_title='Date',
                yaxis_title='Trending Count',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(
                    family="Arial, sans-serif",
                    size=14,
                    color="black"
                ),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor='rgba(255, 255, 255, 0.9)',
                    bordercolor='#DDDDDD',
                    borderwidth=1
                ),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#EEEEEE',
                    tickfont=dict(size=12),
                    tickangle=45
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#EEEEEE',
                    tickfont=dict(size=12)
                ),
                margin=dict(l=60, r=30, t=80, b=80),
                height=500,
                hovermode='x unified'
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.warning(f'Could not load Prophet forecast: {e}')
    
    option = st.selectbox(
        'Select time range:',
        ('Next 24 Hours', 'Next 7 Days'),
        key='trend_time_range'
    )
    if option == 'Next 24 Hours':
        hashtag_csv = 'back up tiktok/top10_hashtags_24h.csv'
        video_csv = 'back up tiktok/predicted_viral_videos_next_24h.csv'
        subtitle_hashtag = 'Top 10 Hashtags'
        subtitle_video = 'Top 10 Viral Videos'
    else:
        hashtag_csv = 'back up tiktok/top10_hashtags_7d.csv'
        video_csv = 'back up tiktok/predicted_viral_videos_next_7d.csv'
        subtitle_hashtag = 'Top 10 Hashtags'
        subtitle_video = 'Top 10 Viral Videos'
    col1, col2 = st.columns(2)
    with col1:
        try:
            df_hashtag = pd.read_csv(hashtag_csv)
            df_hashtag.index = df_hashtag.index + 1
            st.subheader(subtitle_hashtag)
            st.dataframe(df_hashtag)
        except Exception as e:
            st.error(f'Could not read {hashtag_csv}: {e}')
    with col2:
        try:
            df_video = pd.read_csv(video_csv)
            df_video.index = df_video.index + 1
            columns_to_show = {}
            if 'id' in df_video.columns:
                columns_to_show['id'] = 'Video ID'
            if 'desc' in df_video.columns:
                columns_to_show['desc'] = 'Description'
            if 'author_user_id' in df_video.columns:
                columns_to_show['author_user_id'] = 'Author ID'
            if 'music_author' in df_video.columns:
                columns_to_show['music_author'] = 'Music Author'
            if 'music_id' in df_video.columns:
                columns_to_show['music_id'] = 'Music ID'
            if columns_to_show:
                st.subheader(subtitle_video)
                st.dataframe(df_video[list(columns_to_show.keys())].rename(columns=columns_to_show).head(10))
            else:
                st.subheader(subtitle_video)
                st.dataframe(df_video.head(10))
        except Exception as e:
            st.error(f'Could not read {video_csv}: {e}')
