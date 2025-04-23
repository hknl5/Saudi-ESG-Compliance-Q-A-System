import streamlit as st
import time
import pandas as pd

# Page configuration - using "centered" layout instead of "wide"
st.set_page_config(
    page_title="Smart ESG Compliance Assistant",
    page_icon="ESG",
    layout="centered"  # Changed from "wide" to "centered"
)

# Custom CSS for styling the UI components
st.markdown("""
<style>
    /* Main container styling */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        background: linear-gradient(to bottom, #ffffff, #f8f9fa);
        padding: 20px;
        border-radius: 10px;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #1e293b;
    }
    
    .header-icon {
        color: #15803d;
        margin-right: 10px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Card styling */
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-left: 4px solid #15803d;
    }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1e293b;
        display: flex;
        align-items: center;
    }
    
    .card-icon {
        color: #15803d;
        margin-right: 8px;
    }
    
    .confidence-badge {
        background-color: rgba(21, 128, 61, 0.1);
        color: #15803d;
        padding: 4px 8px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        float: right;
    }
    
    /* Source styling */
    .source-card {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        background-color: white;
    }
    
    .source-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
        background-color: #f8fafc;
        padding: 10px;
        margin: -16px;
        margin-bottom: 16px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .source-title {
        font-weight: 600;
        display: flex;
        align-items: center;
        color: #1e293b;
    }
    
    .source-title-icon {
        color: #15803d;
        margin-right: 8px;
    }
    
    .source-meta {
        font-size: 0.875rem;
        color: #64748b;
    }
    
    .source-relevance {
        text-align: right;
        font-size: 0.875rem;
    }
    
    .source-relevance-value {
        font-weight: 700;
        color: #15803d;
    }
    
    .source-excerpt {
        font-size: 0.875rem;
        border-left: 3px solid rgba(21, 128, 61, 0.3);
        padding-left: 16px;
        margin-top: 12px;
        font-style: italic;
        color: #334155;
    }
    
    /* Info box styling */
    .info-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
    }
    
    .info-title {
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        color: #1e293b;
    }
    
    .info-icon {
        color: #15803d;
        margin-right: 8px;
    }
    
    .info-text {
        font-size: 0.875rem;
        color: #64748b;
        margin-bottom: 12px;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
    }
    
    .info-item {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px;
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }
    
    .info-item-icon-container {
        background-color: rgba(21, 128, 61, 0.1);
        padding: 6px;
        border-radius: 6px;
        margin-top: 2px;
    }
    
    .info-item-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    .info-item-text {
        font-size: 0.75rem;
        color: #64748b;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #15803d;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-weight: 500;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #166534;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
        padding: 8px 16px;
        background-color: #f1f5f9;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        border-bottom: 2px solid #15803d !important;
    }
    
    /* Hide Streamlit elements we don't want */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Center the content */
    .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state to track if a search has been performed
if 'has_searched' not in st.session_state:
    st.session_state.has_searched = False

# Header section
st.markdown('<div class="main-header"><span class="header-icon">ESG</span>Smart ESG Compliance Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask any question about ESG regulations, standards, or best practices. Our AI will retrieve relevant information from trusted sources and provide accurate answers.</div>', unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("Search Settings")
    top_results = st.slider("Number of top results", min_value=1, max_value=10, value=3)
    enable_reranking = st.toggle("Enable GPT reranking", value=True)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This assistant uses RAG (Retrieval Augmented Generation) to provide accurate answers to your ESG compliance questions.")
    
    # Add some additional information about the system
    st.markdown("### How it works")
    st.markdown("""
    1. **Retrieval**: Finds relevant documents from the knowledge base
    2. **Reranking**: Sorts results by relevance (optional)
    3. **Generation**: Creates a comprehensive answer based on retrieved information
    """)

# Main content - Search card
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title"><span class="card-icon">Q</span>Ask a question</div>', unsafe_allow_html=True)
st.markdown('Enter your ESG-related question to get an accurate, sourced answer', unsafe_allow_html=True)

# Input field for the question
query = st.text_input("", value="How do commercial banks incorporate ESG factors into their credit analysis?", label_visibility="collapsed", placeholder="e.g., How do commercial banks incorporate ESG factors into their credit analysis?")

# Search button
search_button = st.button("Search")

st.markdown('</div>', unsafe_allow_html=True)

# Handle search - only trigger when the search button is clicked
if search_button:
    st.session_state.has_searched = True
    
    # Show loading spinner
    with st.spinner("Searching for relevant information..."):
        # Simulate API call delay
        time.sleep(2)

# Display results if search has been performed
if st.session_state.has_searched:
    # Create tabs for Answer and Sources
    tab1, tab2 = st.tabs(["Answer", "Sources (3)"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="card-icon">A</span>ESG Factors in Credit Analysis<span class="confidence-badge">High Confidence</span></div>', unsafe_allow_html=True)
        
        answer = "Commercial banks incorporate ESG factors into their credit analysis through a systematic and explicit inclusion of material ESG factors into traditional fundamental financial analysis. This is done by considering qualitative risks and opportunities, quantitative metrics, and incorporating ESG variables into models. These aspects collectively inform the bank's decision-making processes involved in proprietary investing and lending. This approach thus influences the way they assess the creditworthiness of borrowers."
        st.markdown(f'<p>{answer}</p>', unsafe_allow_html=True)
        
        st.markdown('<hr style="margin: 20px 0; border-color: #e2e8f0;">', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; justify-content: space-between; align-items: center;">', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; align-items: center; gap: 8px; color: #64748b; font-size: 0.875rem;"><span>i</span> Answer generated from 3 sources</div>', unsafe_allow_html=True)
        st.markdown('<a href="#" style="color: #15803d; text-decoration: none; font-size: 0.875rem; display: flex; align-items: center; gap: 4px;">Learn More</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        # Source data - in a real application, this would come from a database or API
        sources = [
            {
                "title": "commercial-banks-standard_en-gb.pdf",
                "page": 12,
                "excerpt": "The entity shall describe its approach to the incorporation of environmental, social and governance (ESG) factors in its credit analysis....",
                "relevance": 0.8859
            },
            {
                "title": "investment-banking-and-brokerage-standard_en-gb.pdf",
                "page": 24,
                "excerpt": "Integration of ESG factors is defined as the systematic and explicit inclusion of material ESG factors into traditional fundamental financial analysis...",
                "relevance": 0.8833
            },
            {
                "title": "commercial-banks-standard_en-gb.pdf",
                "page": 31,
                "excerpt": "5.1.4 Approach to incorporating ESG factors into assessing creditworthiness of borrowers...",
                "relevance": 0.8809
            }
        ]
        
        # Display each source as a card
        for source in sources:
            st.markdown(f'''
            <div class="source-card">
                <div class="source-header">
                    <div>
                        <div class="source-title"><span class="source-title-icon">DOC</span>{source['title']}</div>
                        <div class="source-meta">Page {source['page']}</div>
                    </div>
                    <div class="source-relevance">
                        <div>Relevance: <span class="source-relevance-value">{source['relevance']*100:.1f}%</span></div>
                        <div class="progress-container" style="width: 100px; height: 6px; background-color: #e2e8f0; border-radius: 3px; margin-top: 4px;">
                            <div style="width: {source['relevance']*100}%; height: 100%; background-color: #15803d; border-radius: 3px;"></div>
                        </div>
                    </div>
                </div>
                <div class="source-excerpt">{source['excerpt']}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Additional information box
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown('<div class="info-title"><span class="info-icon">i</span>About ESG in Banking</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Environmental, Social, and Governance (ESG) factors are increasingly important in the banking sector as financial institutions assess risks and opportunities in their lending and investment practices.</div>', unsafe_allow_html=True)
    
    # Create a 3-column layout for the info items
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div class="info-item">
            <div class="info-item-icon-container">S</div>
            <div>
                <div class="info-item-title">Systematic Integration</div>
                <div class="info-item-text">ESG factors are systematically included in financial analysis</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown('''
        <div class="info-item">
            <div class="info-item-icon-container">R</div>
            <div>
                <div class="info-item-title">Risk Assessment</div>
                <div class="info-item-text">Qualitative and quantitative ESG metrics inform risk models</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown('''
        <div class="info-item">
            <div class="info-item-icon-container">C</div>
            <div>
                <div class="info-item-title">Creditworthiness</div>
                <div class="info-item-text">ESG factors directly impact borrower creditworthiness evaluation</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Reset button
    if st.button("Reset Search"):
        st.session_state.has_searched = False
        st.experimental_rerun()

# If no search has been performed yet, show a placeholder
elif not st.session_state.has_searched:
    st.markdown('''
    <div style="text-align: center; padding: 40px 20px; color: #64748b;">
        <div style="font-size: 3rem; margin-bottom: 20px;">?</div>
        <h3 style="margin-bottom: 10px; color: #1e293b;">Enter your ESG question above</h3>
        <p>Get accurate answers with citations from trusted sources</p>
    </div>
    ''', unsafe_allow_html=True)