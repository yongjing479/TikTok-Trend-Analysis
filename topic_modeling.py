import streamlit as st
import pandas as pd
from gensim import corpora, models

def show_topic_modeling():
    st.markdown('<h2 style="margin-bottom: 0.5em;">Emerging Topics (NLP)</h2>', unsafe_allow_html=True)
    try:
        # Load LDA model and dictionary
        lda_model = models.LdaModel.load("back up tiktok/lda_model.gensim")
        dictionary = corpora.Dictionary.load("back up tiktok/lda_dictionary.dict")
        # Show topics
        topics = lda_model.print_topics(num_words=5)
        # Show topics as a table for better readability
        topic_words = []
        for topic_num, topic_words_str in topics:
            # Parse the topic_words_str to extract words only
            words = [w.split('*')[1].replace('"','').strip() for w in topic_words_str.split('+')]
            topic_words.append([topic_num + 1] + words)  
        # Create DataFrame for table
        max_words = max(len(row)-1 for row in topic_words)
        columns = ['Topic'] + [f'Word {i+1}' for i in range(max_words)]
        topic_df = pd.DataFrame(topic_words, columns=columns)
        topic_df.index = topic_df.index + 1
        st.markdown('### Topics Table (Top Words per Topic)')
        st.dataframe(topic_df, use_container_width=True)

    except Exception as e:
        st.error(f'Could not load or display topic modeling results: {e}')
    
    st.markdown('---')
    st.markdown('### Sentiment Analysis of Video Descriptions')
    try:
        df = pd.read_csv("back up tiktok/full_df_with_sentiment_topics.csv")
        if 'sentiment_category' in df.columns:
            sentiment_counts = df['sentiment_category'].value_counts().reindex(['Negative', 'Neutral', 'Positive']).fillna(0)
            st.markdown('#### Sentiment Distribution')
            st.bar_chart(sentiment_counts)
            if 'views' in df.columns:
                import plotly.express as px
                st.markdown('#### Sentiment vs. Views')
                fig = px.scatter(df, x='sentiment', y='views', color='sentiment_category',
                                labels={'sentiment': 'Sentiment Score', 'views': 'Views'},
                                title='Sentiment vs. Views',
                                color_discrete_map={'Negative':'#EF553B','Neutral':'#636EFA','Positive':'#00CC96'})
                fig.update_layout(plot_bgcolor='#222', paper_bgcolor='#222', font_color='white')
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f'Could not load or display sentiment analysis results: {e}')
    
    st.markdown('---')
    st.markdown('### Named Entity Recognition (NER)')
    try:
        df_entities = pd.read_csv("back up tiktok/full_df_with_entities.csv")
        from collections import defaultdict
        import spacy
        nlp = spacy.load('en_core_web_sm')
        entity_counter = defaultdict(int)
        entity_types = defaultdict(int)
        entity_examples = defaultdict(list)
        for text in df_entities['title'].fillna(''):
            doc = nlp(str(text))
            for ent in doc.ents:
                entity_counter[ent.text.lower()] += 1
                entity_types[ent.label_] += 1
                if ent.text not in entity_examples[ent.label_]:
                    entity_examples[ent.label_].append(ent.text)
        # Display top 10 entities
        top_entities = sorted(entity_counter.items(), key=lambda x: x[1], reverse=True)[:10]
        entity_df = pd.DataFrame(top_entities, columns=['Entity', 'Count'])
      
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('#### Most Frequent Entities (Top 10)')
            st.dataframe(entity_df, use_container_width=True, height=400)  # Set height to match the chart
        with col2:
            st.markdown('#### Entity Type Distribution')
            # Display entity type distribution
            type_counts = pd.Series(entity_types).sort_values(ascending=False)
            st.bar_chart(type_counts, height=400)  
        # Display entity examples 
        example_data = []
        for etype, examples in entity_examples.items():
            example_data.append([etype] + examples[:5])
        max_examples = max(len(row) for row in example_data)
        columns = ["Entity Type"] + [f"Example {i}" for i in range(1, max_examples)]
        example_df = pd.DataFrame(example_data, columns=columns)
        example_df.index = example_df.index + 1 
        st.markdown('#### Entity Examples')
        st.dataframe(example_df, use_container_width=True)
    except Exception as e:
        st.warning(f'Could not load or display NER results: {e}')
