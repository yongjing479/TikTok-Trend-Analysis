import streamlit as st
import pandas as pd
import plotly.express as px

def show_trending_creators():
    st.markdown('<h2 style="margin-bottom: 0.5em;">Trending Creators</h2>', unsafe_allow_html=True)
    try:
        creators_df = pd.read_csv('back up tiktok/trending_creators.csv')
        if 'nick_name' in creators_df.columns and 'follower_cnt' in creators_df.columns and 'liked_cnt' in creators_df.columns:
            # Top 10 by Followers and Likes (side by side)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('**Top 10 Most Followed Creators**')
                top_followed = creators_df.sort_values('follower_cnt', ascending=False).head(10)
                st.dataframe(top_followed[['nick_name', 'follower_cnt']].reset_index(drop=True))
            
            with col2:
                st.markdown('**Top 10 Most Liked Creators**')
                top_liked = creators_df.sort_values('liked_cnt', ascending=False).head(10)
                st.dataframe(top_liked[['nick_name', 'liked_cnt']].reset_index(drop=True))

            # Followers vs Likes scatter plot
            st.markdown('### Followers vs Likes Analysis')
            fig_scatter = px.scatter(
                creators_df,
                x='follower_cnt',
                y='liked_cnt',
                labels={'follower_cnt': 'Followers', 'liked_cnt': 'Likes'},
                title='Followers vs Likes Distribution',
                color='follower_cnt',
                color_continuous_scale='Blues',
                hover_data=['nick_name']
            )
            fig_scatter.update_traces(marker=dict(size=10, opacity=0.7))
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e3e7',
                xaxis_title='Followers',
                yaxis_title='Likes',
                title_font=dict(size=20, family='Arial'), 
                margin=dict(l=60, r=30, t=60, b=40)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            # Show correlation
            corr = creators_df[['follower_cnt', 'liked_cnt']].corr()
            corr_display = corr.copy()
            corr_display.index = ['Followers', 'Likes']
            corr_display.columns = ['Followers', 'Likes']
            st.markdown('**Correlation between Followers and Likes**')
            st.dataframe(corr_display.style.set_properties(**{'width': '120px'}), use_container_width=False)

        else:
            st.warning('Required columns not found in trending_creators.csv. Please ensure columns are named correctly.')
    except Exception as e:
        st.error(f'Could not read or plot trending_creators.csv: {e}')
