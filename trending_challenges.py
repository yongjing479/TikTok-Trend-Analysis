import streamlit as st
import pandas as pd
import ast

def show_trending_challenges():
    st.markdown('<h2 style="margin-bottom: 0.5em;">Trending Challenges</h2>', unsafe_allow_html=True)
    try:
        df = pd.read_csv('back up tiktok/trending_challenges.csv')
         # --- Word Cloud for Common Words in Challenge Descriptions ---
        if 'desc' in df.columns and not df['desc'].dropna().empty:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            text = " ".join(df["desc"].dropna())
            wordcloud = WordCloud(width=600, height=200, background_color='white', colormap='coolwarm').generate(text)
            st.markdown('**Common Words in Challenge Descriptions**')
            fig_wc, ax = plt.subplots(figsize=(3,1))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig_wc)
        # --- User Count vs View Count Scatterplot (Plotly) ---
        if 'userCount' in df.columns and 'viewCount' in df.columns:
            import plotly.express as px
            fig_scatter = px.scatter(
                df,
                x="userCount",
                y="viewCount",
                color="viewCount",
                color_continuous_scale="RdBu",
                labels={"userCount": "User Count", "viewCount": "View Count"},
                title="User Count vs View Count"
            )
            fig_scatter.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='#232526')
            st.plotly_chart(fig_scatter, use_container_width=True)
        # --- Top 10 Trending Challenges by User Count and Views Side by Side ---
        col1, col2 = st.columns(2)
        if 'userCount' in df.columns:
            with col1:
                st.markdown('**Top 10 Challenges by User Count**')
                import plotly.express as px
                top10_user = df.sort_values("userCount", ascending=False).head(10)
                fig_user = px.bar(
                    top10_user,
                    x="userCount",
                    y="challenge_name" if 'challenge_name' in df.columns else 'name',
                    orientation='h',
                    color="userCount",
                    color_continuous_scale="Blues",
                    labels={"userCount": "User Count", "challenge_name": "Challenge", "name": "Challenge"},
                    title="Top 10 Trending Challenges by User Count"
                )
                fig_user.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', paper_bgcolor='white', font_color='#232526')
                st.plotly_chart(fig_user, use_container_width=True)
        if 'viewCount' in df.columns:
            with col2:
                st.markdown('**Top 10 Challenges by Views**')
                import plotly.express as px
                top10_views = df.sort_values("viewCount", ascending=False).head(10)
                fig_views = px.bar(
                    top10_views,
                    x="viewCount",
                    y="name",
                    orientation='h',
                    color="viewCount",
                    color_continuous_scale="RdBu",
                    labels={"viewCount": "Views", "name": "Challenge"},
                    title="Top 10 TikTok Challenges by Views"
                )
                fig_views.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', paper_bgcolor='white', font_color='#232526')
                st.plotly_chart(fig_views, use_container_width=True)
    except Exception as e:
        st.error(f'Could not read or plot trending_challenges.csv: {e}')
