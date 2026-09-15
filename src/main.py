import streamlit as st
from fetcher.pti_fetcher import fetch_live_pti

st.set_page_config(page_title="PTI Live News", layout="wide")

def main():
    st.title("📰 PTI Live News Fetcher")
    st.write("Fetch and view live news from the PTI API.")
    
    st.header("Live News Aggregator")
    
    col1, col2 = st.columns(2)
    with col1:
        date_input = st.date_input("Select Date")
    with col2:
        source_input = st.selectbox("Select News Source", ["All", "PTI", "Times of India", "Hindustan Times", "NDTV", "The Hindu"])
    
    # Initialize session state for pagination
    if 'news_data' not in st.session_state:
        st.session_state.news_data = None
    if 'page_num' not in st.session_state:
        st.session_state.page_num = 1
        
    if st.button("Fetch News"):
        with st.spinner(f"Fetching live news from {source_input}..."):
            date_str = date_input.strftime('%d-%m-%Y')
            news_data = fetch_live_pti(date_str, source_input)
            
            st.session_state.news_data = news_data
            st.session_state.page_num = 1 # Reset to page 1 on new fetch
            
    # Display logic using session state
    if st.session_state.news_data is not None:
        news_data = st.session_state.news_data
        
        if isinstance(news_data, dict) and "error" in news_data:
            st.error(f"Error fetching news: {news_data['error']}")
        elif not news_data:
            st.info("No news found for this date.")
        else:
            if isinstance(news_data, list):
                st.success(f"News fetched successfully! Total articles: {len(news_data)}")
                
                # Pagination calculations
                ITEMS_PER_PAGE = 10
                total_articles = len(news_data)
                import math
                total_pages = math.ceil(total_articles / ITEMS_PER_PAGE)
                
                # Make sure page_num is within bounds
                if st.session_state.page_num > total_pages:
                    st.session_state.page_num = total_pages
                if st.session_state.page_num < 1:
                    st.session_state.page_num = 1
                    
                current_page = st.session_state.page_num
                
                start_idx = (current_page - 1) * ITEMS_PER_PAGE
                end_idx = start_idx + ITEMS_PER_PAGE
                
                page_data = news_data[start_idx:end_idx]
                
                st.markdown(f"**Page {current_page} of {total_pages}**")
                
                for article in page_data:
                    with st.container(border=True):
                        title = article.get('title', 'No Title Provided')
                        link = article.get('link', '#')
                        published = article.get('published', 'Unknown Date')
                        source = article.get('source', 'PTI API (Original)')
                        st.markdown(f"#### [{title}]({link})")
                        st.caption(f"📰 **Source:** {source} &nbsp; | &nbsp; 🕒 **Published:** {published}")
                        
                # Pagination Controls
                if total_pages > 1:
                    st.write("---")
                    col_prev, col_spacer, col_next = st.columns([1, 2, 1])
                    
                    with col_prev:
                        if st.button("⬅️ Previous", disabled=(current_page == 1)):
                            st.session_state.page_num -= 1
                            st.rerun()
                            
                    with col_next:
                        if st.button("Next ➡️", disabled=(current_page == total_pages)):
                            st.session_state.page_num += 1
                            st.rerun()
            else:
                st.json(news_data)

if __name__ == "__main__":
    main()

# Trigger reload
