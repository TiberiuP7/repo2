import streamlit as st
from data_processor import CAENDataProcessor
from translations import TRANSLATIONS
import sys
import os
import pandas as pd

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def get_translation(key):
    return TRANSLATIONS[st.session_state.language][key]

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'ro'
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'keyword' not in st.session_state:
    st.session_state.keyword = ''

def initialize_data():
    if 'data_processor' not in st.session_state:
        try:
            processor = CAENDataProcessor()
            processor.extract_correspondence_data('attached_assets/Corespondenta-CAEN-Rev.2-CAEN-Rev.3.pdf')
            processor.extract_rev3_details('attached_assets/CAEN-Rev.3_structura-completa.pdf')
            st.session_state.data_processor = processor
        except Exception as e:
            st.error(f"Failed to initialize data: {str(e)}")
            # Fall back to sample data
            processor = CAENDataProcessor()
            st.session_state.data_processor = processor

def main():
    st.set_page_config(
        page_title="Căutare Avansată Coduri CAEN",
        page_icon="🔍",
        layout="wide"
    )

    # Load custom CSS
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Navigation menu with back button
    st.markdown("""
        <div class="nav-container">
            <div class="nav-menu">
                <a href="/" class="back-button" style="font-size: 1.2rem; background: #f0f2f6; padding: 0.8rem 1.5rem; border-radius: 8px; margin-right: 20px;">
                    ← Înapoi la Convertor
                </a>
                <a href="/coduri_caen_rev3" target="_self">📋 Coduri CAEN Rev 3</a>
                <a href="/file_converter" target="_self">📄 Convertor Fișiere</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    initialize_data()

    # Page title and subtitle
    st.markdown(f"## 🔍 {get_translation('advanced_search')}")
    st.markdown("### Căutați și filtrați codurile CAEN Rev 3")

    # Create a container for search filters
    with st.expander("Filtre de căutare", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            keyword = st.text_input(
                "🔍 " + get_translation('keyword_search'),
                key='keyword_input',
                placeholder=get_translation('keyword_placeholder'),
                value=st.session_state.keyword if 'keyword' in st.session_state else ''
            )

        with col2:
            categories = [''] + st.session_state.data_processor.get_categories()
            category = st.selectbox(
                "📑 " + get_translation('category_filter'),
                categories,
                index=0,
                format_func=lambda x: get_translation('select_category') if x == '' else x,
                key='category_select'
            )

        # Action buttons
        col3, col4 = st.columns(2)
        with col3:
            search_clicked = st.button(
                "🔎 " + get_translation('apply_filters'),
                key='apply_advanced_search'
            )
        with col4:
            reset_clicked = st.button(
                "🔄 " + get_translation('reset_filters'),
                key='reset_advanced_search'
            )

        # Handle reset
        if reset_clicked:
            st.session_state.keyword = ''
            st.session_state.selected_category = None
            st.rerun()

    # Display search results or all codes
    st.markdown("---")
    st.markdown(f"## 📚 {get_translation('all_activities')}")

    # Get and display activities based on search or show all
    if search_clicked and (keyword or category):
        results = st.session_state.data_processor.search_activities(
            keyword=keyword if keyword else None,
            category=category if category else None
        )

        if results:
            # Sort results by CAEN code
            results.sort(key=lambda x: x['rev3_code'])

            # Display results in a more organized way
            for result in results:
                with st.container():
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="code-box">
                            <strong>{result['rev3_code']}</strong>
                        </div>
                        <div class="activity-name">
                            {result['description']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning(get_translation('no_matches'))
    else:
        # Display all activities organized by section
        for section in st.session_state.data_processor.get_categories():
            with st.expander(section, expanded=False):
                results = st.session_state.data_processor.search_activities(category=section)
                if results:
                    results.sort(key=lambda x: x['rev3_code'])

                    # Create header
                    st.markdown("""
                        <div class="section-codes-header">
                            <div class="code-column">Cod CAEN</div>
                            <div class="description-column">Denumire Activitate</div>
                        </div>
                    """, unsafe_allow_html=True)

                    # Display activities for this section
                    for activity in results:
                        st.markdown(f"""
                        <div class="section-codes-row">
                            <div class="code-column">{activity['rev3_code']}</div>
                            <div class="description-column">{activity['description']}</div>
                        </div>
                        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()