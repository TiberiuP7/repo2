import streamlit as st
from data_processor import CAENDataProcessor
from translations import TRANSLATIONS
import sys
import os

st.header("Tool gratuit de conversiune a codurilor CAEN Rev. 2 la Nomenclatorul CAEN Rev.3")
st.text("Actualizarea codurilor CAEN Rev. 2 la Nomenclatorul CAEN Rev. 3.  Convertor Coduri CAEN Instrumentul oficial pentru conversia codurilor CAEN Rev.2 la Rev.3. Actualizat pentru anul 2024 conform reglementărilor în vigoare.")
st.text("Actualizeaza-ti codurile CAEN ale firmei tale la nomenclatorul CAEN Rev. 3, Tool oficial gratuit 2025")
st.text("Convertor oficial și gratuit pentru codurile CAEN Rev.2 la Rev.3. Instrument actualizat 2024 pentru companii și PFA. Conversie instantă și export rezultate.")

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def get_translation(key):
    return TRANSLATIONS[st.session_state.language][key]

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'ro'
if 'advanced_search_results' not in st.session_state:
    st.session_state.advanced_search_results = []
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'keyword' not in st.session_state:
    st.session_state.keyword = ''

def initialize_data():
    if 'data_processor' not in st.session_state:
        processor = CAENDataProcessor()
        processor.extract_correspondence_data('attached_assets/Corespondenta-CAEN-Rev.2-CAEN-Rev.3.pdf')
        processor.extract_rev3_details('attached_assets/CAEN-Rev.3_structura-completa.pdf')
        st.session_state.data_processor = processor

def display_results(results):
    """Display search results in a consistent format"""
    for result in results:
        st.markdown(f"""
            <div class="result-card">
                <div class="result-header">
                    <div class="code-box">
                        <span class="label">{get_translation('old_code')}</span>
                        <span class="value">{result['rev2_code']}</span>
                    </div>
                    <div class="arrow">✨➜✨</div>
                    <div class="code-box">
                        <span class="label">{get_translation('new_code')}</span>
                        <span class="value">{result['rev3_code']}</span>
                    </div>
                </div>
                <div class="activity-name">
                    <h4>📝 {get_translation('activity_name')}</h4>
                    <p>{result['description']}</p>
                    <p><em>{result.get('category', '')}</em></p>
                </div>
            </div>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Coduri CAEN Rev 3",
        page_icon="🔍",
        layout="wide"
    )

    # Load custom CSS
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Navigation menu
    st.markdown("""
        <div class="nav-container">
            <div class="nav-menu">
                <a href="/" target="_self">🔄 Conversie Coduri CAEN</a>
                <a href="/coduri_caen_rev3" class="active" target="_self">📋 Coduri CAEN Rev 3</a>
                <a href="/file_converter" target="_self">📄 Convertor Fișiere</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    initialize_data()

    # Page title and subtitle
    st.markdown("## Coduri CAEN Rev 3")
    st.markdown("### Lista completă și actualizată a Codurilor CAEN Rev 3 2025")

    # Keyword search
    keyword = st.text_input(
        get_translation('keyword_search'),
        key='keyword_input',
        placeholder=get_translation('keyword_placeholder'),
        value=st.session_state.keyword
    )

    # Category filter
    categories = [''] + st.session_state.data_processor.get_categories()
    category = st.selectbox(
        get_translation('category_filter'),
        categories,
        index=0,
        format_func=lambda x: get_translation('select_category') if x == '' else x,
        key='category_select',
        help="Select a section to filter activities"
    )

    if category:
        st.markdown(f"""
            <div class="category-info">
                <p><strong>{category.split(' - ')[0]}</strong></p>
                <p>{category.split(' - ')[1]}</p>
            </div>
        """, unsafe_allow_html=True)

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        search_clicked = st.button(
            get_translation('apply_filters'),
            key='apply_advanced_search'
        )
    with col2:
        reset_clicked = st.button(
            get_translation('reset_filters'),
            key='reset_advanced_search'
        )

    # Handle reset
    if reset_clicked:
        st.session_state.keyword = ''
        st.session_state.selected_category = None
        st.session_state.advanced_search_results = []
        st.rerun()

    # Handle search
    if search_clicked:
        # Perform search
        results = st.session_state.data_processor.search_activities(
            keyword=keyword if keyword else None,
            category=category if category else None
        )

        # Display results
        if results:
            st.markdown(f"### {get_translation('advanced_search_results')}")
            display_results(results)
            from main import display_export_buttons
            display_export_buttons(results, 'advanced_search')
        else:
            st.warning(get_translation('no_matches'))

        # Update session state
        st.session_state.keyword = keyword
        st.session_state.selected_category = category
        st.session_state.advanced_search_results = results

if __name__ == "__main__":
    main()
