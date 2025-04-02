import streamlit as st
from duckduckgo_search import DDGS
import datetime
import os

# Define regions dictionary with region codes for DuckDuckGo
REGIONS = {
    "India": "in-en",
    "United States": "us-en",
    "United Kingdom": "uk-en",
    "Canada": "ca-en",
    "Australia": "au-en",
    "Germany": "de-de",
    "France": "fr-fr",
    "Japan": "jp-jp",
    "Brazil": "br-pt",
    "Global": "wt-wt"
}

def get_news(topic, keywords="", region="wt-wt", time_filter="d", max_results=10):
    """Fetch news articles related to the given topic using DuckDuckGo search."""
    try:
        with DDGS() as ddgs:
            # Format the search query to focus on news from the selected topic with optional keywords
            query = f"{topic} news"
            if keywords.strip():
                query = f"{query} {keywords.strip()}"
            
            # Search for news articles
            results = list(ddgs.news(
                query, 
                region=region, 
                safesearch="off", 
                timelimit=time_filter,
                max_results=max_results
            ))
            
            return results
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

def main():
    # Set page config with custom theme
    st.set_page_config(
        page_title="Think why? News Agent", 
        page_icon="🧠", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for better UI
    st.markdown("""
    <style>
    .main {
        padding: 1rem;
        background-color: #f8f9fa;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        width: 100%;
    }
    .news-item {
       
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 0.7rem;
        border-left: 3px solid #4CAF50;
        transition: transform 0.2s ease;
    }
    .news-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.12);
    }
    /* Container styling to reduce gaps */
    .stContainer {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Reduce padding in expandable sections */
    .streamlit-expanderContent {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    h1 {
        color: #2E7D32;
        font-size: 2.2rem;
    }
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem;
        }
        .stSelectbox, .stTextInput, .stSlider {
            margin-bottom: 1rem;
        }
    }
    /* Header styling */
    .header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .header-emoji {
        font-size: 2.5rem;
        margin-right: 0.5rem;
    }
    .header-text h1 {
        margin: 0;
        padding: 0;
    }
    .header-text p {
        margin: 0;
        padding: 0;
        color: #555;
    }
    /* Navigation styling */
    .nav-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    .nav-button {
        flex: 1;
        text-align: center;
        padding: 10px;
        background-color: #E8F5E9;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .nav-button:hover {
        background-color: #C8E6C9;
        transform: translateY(-2px);
    }
    .nav-button.active {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # App title and description using custom header
    st.markdown("""
    <div class="header">
        <div class="header-emoji">🧠</div>
        <div class="header-text">
            <h1>Think why? News Agent</h1>
            <p>Smart news search from around the world</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create responsive columns for the search filters
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # List of news categories/areas
        news_areas = [
            "World News",
            "Technology",
            "Business",
            "Politics",
            "Sports",
            "Entertainment",
            "Science",
            "Health",
            "Environment",
            "Education"
        ]
        
        # Dropdown for selecting news area
        selected_area = st.selectbox("📋 Select News Category", news_areas)
        
        # Keywords input
        keywords = st.text_input("🔍 Add Specific Keywords (optional)", 
                                placeholder="e.g., AI, climate change, etc.")
    
    with col2:
        # Region selection
        selected_region = st.selectbox("🌎 Select Region", 
                                       list(REGIONS.keys()), 
                                       index=list(REGIONS.keys()).index("Global"))
        
        # Time filter
        time_options = {
            "Last 24 hours": "d",
            "Last week": "w",
            "Last month": "m"
        }
        time_filter = st.selectbox("⏱️ Time Period", 
                                   list(time_options.keys()),
                                   index=0)
    
    # Number of results slider
    max_results = st.slider("📊 Maximum Number of Results", 5, 30, 10)
    
    # Search button - take full width
    search_button = st.button("🔎 Search News")
    
    # Search results section
    if search_button:
        # Convert user selections to API parameters
        region_code = REGIONS[selected_region]
        time_code = time_options[time_filter]
        
        with st.spinner("🔄 Searching for latest news..."):
            # Get news results
            news_results = get_news(
                selected_area, 
                keywords=keywords, 
                region=region_code, 
                time_filter=time_code, 
                max_results=max_results
            )
            
            if news_results:
                st.success(f"Found {len(news_results)} news articles for '{selected_area}'{' with keywords: ' + keywords if keywords else ''}")
                
                # Display filtering message
                st.markdown(f"*Showing results for {selected_area} from {selected_region}, {time_filter.lower()}*")
                
                # Display results
                for i, article in enumerate(news_results, 1):
                    with st.container():
                        st.markdown(f'<div class="news-item">', unsafe_allow_html=True)
                        
                        # Create responsive layout for article display
                        # For mobile: stack image and content vertically on small screens
                        # For desktop: keep side-by-side layout
                        img_col, content_col = st.columns([1, 3])
                        
                        with img_col:
                            st.markdown(f"**#{i}**")
                            if "image" in article and article["image"]:
                                st.image(article["image"], width=150)
                            else:
                                # Placeholder image if none available
                                st.markdown("📄")
                        
                        with content_col:
                            title = article.get("title", "No title")
                            url = article.get("url", "#")
                            source = article.get("source", "Unknown source")
                            date = article.get("date", "Unknown date")
                            body = article.get("body", "No description available")
                            
                            # Format the date if it's in ISO format
                            formatted_date = date
                            try:
                                if date != "Unknown date":
                                    # Parse the ISO 8601 timestamp
                                    dt = datetime.datetime.fromisoformat(date.replace('Z', '+00:00'))
                                    # Format it as a readable string
                                    formatted_date = dt.strftime("%b %d, %Y • %I:%M %p")
                            except:
                                # If parsing fails, use the original date string
                                formatted_date = date
                            
                            st.markdown(f"### [{title}]({url})")
                            st.markdown(f"**Source:** {source} | **Published:** {formatted_date}")
                            
                            # Show snippet of the article body with "Read more" option
                            if len(body) > 150:  # Reduced preview length for mobile
                                with st.expander("Article Preview"):
                                    st.markdown(body)
                            else:
                                st.markdown(body)
                            
                            # Replace simple link with a styled button
                            st.markdown(f"""
                            <a href="{url}" target="_blank" style="
                                display: inline-block;
                                background-color: #4CAF50;
                                color: white;
                                text-align: center;
                                padding: 8px 16px;
                                text-decoration: none;
                                font-weight: bold;
                                border-radius: 4px;
                                margin-top: 8px;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                transition: all 0.2s ease;
                            ">Read Full Article</a>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning(f"No news found for '{selected_area}'{' with keywords: ' + keywords if keywords else ''}. Try another topic or check your connection.")
    
    # Footer with tips
    st.markdown("---")
    with st.expander("💡 Tips for better searching"):
        st.markdown("""
        - Try using specific keywords to narrow down your search
        - Change the region to get localized news
        - Adjust the time period to find historical news
        """)

if __name__ == "__main__":
    main() 