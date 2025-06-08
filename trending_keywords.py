import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def show_trending_keywords():
    st.markdown('<h2 style="margin-bottom: 0.5em;">Trending Keywords</h2>', unsafe_allow_html=True)
    try:
        trending_keywords_df = pd.read_csv('back up tiktok/trending_keywords.csv')
        # Word Cloud for keyword prominence
        st.markdown('**Keyword Prominence (Word Cloud)**')
        text = " ".join(trending_keywords_df['keyword'].astype(str).tolist())
        wordcloud = WordCloud(background_color='white', width=600, height=200, colormap='Purples').generate(text)
        fig_wc, ax_wc = plt.subplots(figsize=(3, 1))
        ax_wc.imshow(wordcloud, interpolation='bilinear')
        ax_wc.axis("off")
        st.pyplot(fig_wc)
        # Top 10 by CTR
        top_ctr = trending_keywords_df.sort_values(by='ctr', ascending=False).head(10)
        # Synthetic engagement score
        trending_keywords_df['engagement'] = trending_keywords_df['like'] + trending_keywords_df['comment'] + trending_keywords_df['share']
        top_engagement = trending_keywords_df.sort_values('engagement', ascending=False).head(10)
        # Display CTR and Engagement charts side by side
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig = px.bar(
                top_ctr,
                x='ctr',
                y='keyword',
                orientation='h',
                color='ctr',
                color_continuous_scale='Blues',
                labels={'ctr': 'Click-Through Rate (CTR)', 'keyword': 'Keyword'},
                title='Top 10 Keywords by CTR'
            )
            fig.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_color='#232526',
                xaxis_title='CTR',
                yaxis_title='Keyword',
                title_font=dict(size=20, color='#232526', family='Arial'),
                margin=dict(l=60, r=30, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
        with chart_col2:
            fig_eng = px.bar(
                top_engagement,
                x='engagement',
                y='keyword',
                orientation='h',
                color='engagement',
                color_continuous_scale='Magma',
                labels={'engagement': 'Engagement Score', 'keyword': 'Keyword'},
                title='Top 10 Keywords by Engagement Score'
            )
            fig_eng.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_color='#232526',
                xaxis_title='Engagement Score',
                yaxis_title='Keyword',
                title_font=dict(size=20, color='#232526', family='Arial'),
                margin=dict(l=60, r=30, t=60, b=40)
            )
            st.plotly_chart(fig_eng, use_container_width=True)
        # Top 10 by CVR, Play Six Rate, and Post-Change Impact (side by side)
        top_cvr = trending_keywords_df.sort_values(by='cvr', ascending=False).head(10)
        top_play_six = trending_keywords_df.sort_values(by='play_six_rate', ascending=False).head(10)
        post_impact = None
        if 'post_change' in trending_keywords_df.columns:
            post_impact = trending_keywords_df.sort_values('post_change', ascending=False)[['keyword', 'post_change']].head(10).reset_index(drop=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('**Top 10 by CVR**')
            st.dataframe(top_cvr[['keyword', 'cvr']].reset_index(drop=True))
        with col2:
            st.markdown('**Top 10 by Play Six Rate**')
            st.dataframe(top_play_six[['keyword', 'play_six_rate']].reset_index(drop=True))
        with col3:
            if post_impact is not None:
                st.markdown('**Top 10 by Post-Change Impact**')
                st.dataframe(post_impact)
        # Cost vs Performance Bubble Chart
        if 'cost' in trending_keywords_df.columns:
            st.markdown('**Cost vs CTR by Keyword (Bubble Chart)**')
            fig_bubble = px.scatter(
                trending_keywords_df,
                x='cost',
                y='ctr',
                size='engagement',
                color='ctr',
                text='keyword',
                color_continuous_scale='Blues',
                labels={'cost': 'Cost', 'ctr': 'Click-Through Rate (CTR)', 'engagement': 'Engagement'},
                title='Cost vs CTR by Keyword (Bubble size = Engagement)'
            )
            fig_bubble.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')), textposition='top center')
            fig_bubble.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_color='#232526',
                xaxis_title='Cost',
                yaxis_title='CTR',
                title_font=dict(size=20, color='#232526', family='Arial'),
                margin=dict(l=60, r=30, t=60, b=40),
                legend_title_text='CTR'
            )
            st.plotly_chart(fig_bubble, use_container_width=True)
    except Exception as e:
        st.error(f'Could not read or plot trending_keywords.csv: {e}')
