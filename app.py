import streamlit as st
import streamlit.components.v1 as components
from components.soil_selector import soil_selector
from components.season_selector import season_selector
from components.crop_recommendations import show_recommendations
from components.three_js_viewer import ThreeJsViewer
from components.information_display import show_info_panel
from assets.app_data import intro_text, about_text, footer_text
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_extras.add_vertical_space import add_vertical_space
import requests
import time


st.set_page_config(
    page_title="Smart Agriculture - Viksit Bharat 2047",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# custom CSS 
st.markdown("""
<style>
    /* Base Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    /* Main app styling */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 60px;
        max-width: 1200px;
    }
    
    /* Global theme */
    :root {
        --primary: #1DB954;
        --primary-light: #1ed760;
        --primary-dark: #18a64b;
        --secondary: #121212;
        --secondary-light: #212121;
        --secondary-dark: #0c0c0c;
        --text-light: #ffffff;
        --text-muted: #999999;
        --accent: #f3a953;
        --accent-secondary: #4361ee;
        --card-bg: rgba(33, 33, 33, 0.7);
        --card-border: rgba(29, 185, 84, 0.3);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-dark);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        color: var(--text-light);
        margin-bottom: 1rem;
    }
    
    p, li, span, label, button {
        font-size: 1rem;
        color: var(--text-light);
        line-height: 1.6;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes scaleUp {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(29, 185, 84, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(29, 185, 84, 0); }
        100% { box-shadow: 0 0 0 0 rgba(29, 185, 84, 0); }
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Apply animations to elements */
    .title-area {
        animation: fadeIn 1.2s ease;
    }
    
    .nav-menu {
        animation: slideInUp 0.8s ease;
    }
    
    .main-content {
        animation: fadeIn 1s ease;
    }
    
    .side-content {
        animation: slideInRight 1s ease;
    }
    
    .fade-in {
        animation: fadeIn 1.5s ease;
    }
    
    .pulse-effect {
        animation: pulse 2s infinite;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, var(--secondary), var(--secondary-dark));
        padding: 1.5rem;
        border-radius: 0 0 15px 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
        border-bottom: 1px solid var(--primary-dark);
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-dark), var(--primary), var(--primary-light));
        z-index: 5;
    }
    
    .app-header-content {
        position: relative;
        z-index: 2;
    }
    
    .app-logo {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, var(--primary), #36e47c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        letter-spacing: -0.5px;
        margin-bottom: 0.25rem;
        text-shadow: 0 2px 10px rgba(29, 185, 84, 0.3);
    }
    
    .app-tagline {
        font-size: 1.1rem;
        color: var(--text-muted);
        font-weight: 400;
        margin-bottom: 0.25rem;
    }
    
    /* Navigation menu styling */
    .nav-container {
        background: rgba(18, 18, 18, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        overflow: hidden;
    }
    
    /* Custom styling for option-menu */
    .option-menu-container {
        padding: 0.5rem;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        background: var(--primary);
        color: #fff;
        border: none;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(29, 185, 84, 0.3);
        background: var(--primary-light);
    }
    
    .stButton button:active {
        transform: translateY(1px);
    }
    
    /* Secondary button */
    .secondary-button button {
        background: transparent;
        border: 2px solid var(--primary);
        color: var(--primary);
    }
    
    .secondary-button button:hover {
        background: rgba(29, 185, 84, 0.1);
    }
    
    /* Action buttons */
    .action-button button {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        box-shadow: 0 4px 10px rgba(29, 185, 84, 0.3);
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .action-button button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(29, 185, 84, 0.4);
    }
    
    /* Card styling */
    .custom-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid var(--card-border);
        backdrop-filter: blur(5px);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        overflow: hidden;
        position: relative;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
    }
    
    .custom-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #fff;
    }
    
    .card-content {
        color: var(--text-muted);
    }
    
    /* Feature card */
    .feature-card {
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: var(--primary);
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    /* Call to action section */
    .cta-section {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.1), rgba(54, 228, 124, 0.05));
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        border: 1px solid rgba(29, 185, 84, 0.2);
    }
    
    .cta-heading {
        font-size: 1.75rem;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #ffffff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(90deg, var(--secondary-dark), var(--secondary));
        color: var(--text-muted);
        text-align: center;
        padding: 12px;
        font-size: 0.9rem;
        z-index: 9999;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Custom data display element */
    .data-display {
        background: rgba(33, 33, 33, 0.5);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        border-left: 3px solid var(--primary);
    }
    
    .data-label {
        font-size: 0.9rem;
        color: var(--text-muted);
        margin-bottom: 0.25rem;
    }
    
    .data-value {
        font-size: 1.1rem;
        font-weight: 500;
        color: white;
    }
    
    /* Statistics card */
    .stat-card {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.05), rgba(18, 18, 18, 0.8));
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(29, 185, 84, 0.1);
        text-align: center;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-muted);
    }
    
    /* Custom alert boxes */
    .custom-alert {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .custom-alert::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
    }
    
    .info-alert {
        background: rgba(67, 97, 238, 0.1);
        border: 1px solid rgba(67, 97, 238, 0.3);
    }
    
    .info-alert::before {
        background: var(--accent-secondary);
    }
    
    .warning-alert {
        background: rgba(243, 169, 83, 0.1);
        border: 1px solid rgba(243, 169, 83, 0.3);
    }
    
    .warning-alert::before {
        background: var(--accent);
    }
    
    .success-alert {
        background: rgba(29, 185, 84, 0.1);
        border: 1px solid rgba(29, 185, 84, 0.3);
    }
    
    .success-alert::before {
        background: var(--primary);
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-primary {
        background: var(--primary);
        color: white;
    }
    
    .badge-secondary {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text-muted);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .badge-accent {
        background: var(--accent);
        color: white;
    }
    
    /* Glassmorphism effect */
    .glass-card {
        background: rgba(33, 33, 33, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress section */
    .progress-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
    }
    
    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 20%;
        position: relative;
    }
    
    .progress-step::after {
        content: '';
        position: absolute;
        height: 3px;
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        top: 1.5rem;
        left: 50%;
        z-index: 1;
    }
    
    .progress-step:last-child::after {
        display: none;
    }
    
    .step-circle {
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        background: var(--secondary-light);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-bottom: 0.75rem;
        z-index: 2;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .active-step .step-circle {
        background: var(--primary);
        border-color: var(--primary-light);
        box-shadow: 0 0 0 5px rgba(29, 185, 84, 0.2);
    }
    
    .completed-step .step-circle {
        background: var(--primary-dark);
        border-color: var(--primary);
    }
    
    .step-label {
        font-size: 0.85rem;
        color: var(--text-muted);
        text-align: center;
    }
    
    .active-step .step-label {
        color: white;
        font-weight: 500;
    }
    
    /* Tabs styling */
    div.stTabs {
        background: rgba(18, 18, 18, 0.5);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    div.stTabs button {
        border-radius: 8px;
        font-weight: 500;
        color: var(--text-muted);
        padding: 0.5rem 1rem;
    }
    
    div.stTabs button[aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
        font-weight: 600;
    }
    
    /* Option menu styling overrides */
    .nav-link {
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to load Lottie animations
def load_lottie_url(url):
    """Load a Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Animation URLs
LOTTIE_FARM = "https://assets3.lottiefiles.com/packages/lf20_qsvdh1dd.json"
LOTTIE_PLANT = "https://assets9.lottiefiles.com/packages/lf20_kfzgxkvq.json"
LOTTIE_INFO = "https://assets2.lottiefiles.com/packages/lf20_hfnakrwm.json"

# Initialize session state variables if not already present
if 'selected_soil' not in st.session_state:
    st.session_state.selected_soil = None
if 'selected_season' not in st.session_state:
    st.session_state.selected_season = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Home"

# Modern header with logo animation
st.markdown("""
<div class="app-header fade-in">
    <div class="app-header-content">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="app-logo">Smart Agriculture</div>
                <div class="app-tagline">Empowering Farmers with Data-Driven Insights</div>
                <div style="font-size: 0.9rem; color: var(--text-muted); margin-top: 0.5rem;">
                    <span style="background: linear-gradient(90deg, #f5f5f5, #e0e0e0); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 600;">
                        Viksit Bharat 2047 Initiative
                    </span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="margin-bottom: 0.5rem; color: var(--text-muted); font-size: 0.9rem;">
                    Advanced 3D Crop Recommendation System
                </div>
                <div>
                    <span class="badge badge-primary">AI-Powered</span>
                    <span class="badge badge-secondary">Precision Farming</span>
                    <span class="badge badge-accent">Sustainable</span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Progress tracker
if st.session_state.selected_soil and st.session_state.selected_season and st.session_state.show_results:
    progress_status = 3
elif st.session_state.selected_soil and st.session_state.selected_season:
    progress_status = 2
elif st.session_state.selected_soil:
    progress_status = 1
else:
    progress_status = 0

if progress_status > 0:
    st.markdown("""
    <div class="glass-card" style="padding: 1rem; margin-bottom: 1.5rem;">
        <div class="progress-container">
            <div class="progress-step {0}">
                <div class="step-circle">1</div>
                <div class="step-label">Soil Selection</div>
            </div>
            <div class="progress-step {1}">
                <div class="step-circle">2</div>
                <div class="step-label">Season Selection</div>
            </div>
            <div class="progress-step {2}">
                <div class="step-circle">3</div>
                <div class="step-label">Recommendations</div>
            </div>
        </div>
    </div>
    """.format(
        "completed-step" if progress_status >= 1 else "",
        "completed-step" if progress_status >= 2 else ("active-step" if progress_status == 1 else ""),
        "completed-step" if progress_status >= 3 else ("active-step" if progress_status == 2 else "")
    ), unsafe_allow_html=True)

# Horizontal navigation menu with improved styling
with st.container():
    st.markdown('<div class="nav-container nav-menu">', unsafe_allow_html=True)
    
    # Get the current page from session state or default to Home
    current_page = st.session_state.get("selected_page", "Home")
    
    # Determine the index based on the current page
    page_options = ["Home", "Soil Selection", "Season Selection", "Crop Recommendations", "Knowledge Hub"]
    default_index = page_options.index(current_page) if current_page in page_options else 0
    
    selected_page = option_menu(
        menu_title=None,
        options=page_options,
        icons=["house-fill", "moisture", "cloud-sun", "flower3", "book-half"],
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "var(--primary)", "font-size": "1.1rem", "margin-right": "0.5rem"},
            "nav-link": {"font-size": "1rem", "text-align": "center", "padding": "0.8rem 1rem", 
                        "border-radius": "8px", "margin": "0.2rem"},
            "nav-link-selected": {"background-color": "var(--primary)", "color": "white", 
                                "font-weight": "600", "box-shadow": "0 2px 10px rgba(29, 185, 84, 0.3)"},
        }
    )
    
    # Update the session state with the selected page
    st.session_state.selected_page = selected_page
    
    st.markdown('</div>', unsafe_allow_html=True)

# Content container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Display the appropriate content based on the selected page
if selected_page == "Home":
    # Two column layout for header section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="custom-card" style="animation-delay: 0.2s;">
            <div class="card-title">
                Precision Agriculture for Sustainable Farming
            </div>
            <div class="card-content">
                <p style="font-size: 1.1rem; margin-bottom: 1rem; color: #e0e0e0;">
                    Our advanced 3D recommendation system helps Indian farmers select optimal crops 
                    based on soil type and growing season, enhancing productivity and sustainability.
                </p>
                <p style="color: var(--text-muted);">
                    Using data-driven insights and machine learning, we provide personalized recommendations 
                    that consider local environmental conditions, helping you make better farming decisions.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Load and display the farm animation
        farm_animation = load_lottie_url(LOTTIE_FARM)
        if farm_animation:
            st_lottie(farm_animation, height=220, key="farm_animation")
    
    # Statistics section
    st.markdown("""
    <div style="margin: 1.5rem 0;">
        <div style="font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; color: white;">
            Improving Agricultural Outcomes
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">30%</div>
            <div class="stat-label">Average Yield Increase</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">25%</div>
            <div class="stat-label">Water Conservation</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">40%</div>
            <div class="stat-label">Reduced Input Waste</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">60%</div>
            <div class="stat-label">Better Decision Making</div>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works section
    st.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <div style="font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; color: white;">
            How It Works
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="custom-card feature-card">
            <div style="font-size: 2rem; color: var(--primary); margin-bottom: 1rem;">
                🌱
            </div>
            <div class="feature-title">Soil Analysis</div>
            <p style="color: var(--text-muted);">
                Select your soil type to get specific insights about its properties, composition,
                and suitability for different crops.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card feature-card">
            <div style="font-size: 2rem; color: var(--primary); margin-bottom: 1rem;">
                ☀️
            </div>
            <div class="feature-title">Season Optimization</div>
            <p style="color: var(--text-muted);">
                Choose the growing season to understand seasonal patterns, rainfall distribution,
                and temperature effects on crop growth.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="custom-card feature-card">
            <div style="font-size: 2rem; color: var(--primary); margin-bottom: 1rem;">
                🌾
            </div>
            <div class="feature-title">Crop Recommendations</div>
            <p style="color: var(--text-muted);">
                Receive personalized crop recommendations with detailed information on planting,
                care, and expected yields.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action section
    st.markdown("""
    <div class="cta-section pulse-effect" style="margin-top: 2rem;">
        <div class="cta-heading">Ready to Optimize Your Farm?</div>
        <p style="color: #e0e0e0; margin-bottom: 1.5rem;">
            Get personalized crop recommendations based on your specific conditions. Start by selecting your soil type.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="action-button">', unsafe_allow_html=True)
        if st.button("Start Now", use_container_width=True):
            st.session_state.selected_page = "Soil Selection"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif selected_page == "Soil Selection":
    # Call the soil selector component
    soil_selector()
    
    # Navigation buttons
    if st.session_state.selected_soil:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; margin-top: 1.5rem;">
            <div style="width: 48%;">
                <div class="secondary-button">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col2:
            st.markdown('<div class="action-button">', unsafe_allow_html=True)
            if st.button("Next: Select Season →", use_container_width=True):
                st.session_state.selected_page = "Season Selection"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif selected_page == "Season Selection":
    # Check if soil has been selected
    if not st.session_state.selected_soil:
        st.markdown("""
        <div class="warning-alert" style="margin: 2rem 0;">
            <div style="font-weight: 600; margin-bottom: 0.5rem; color: var(--accent);">
                Soil Type Required
            </div>
            <p style="color: var(--text-muted);">
                Please select a soil type first to get accurate seasonal recommendations for your region.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Go to Soil Selection", use_container_width=True):
                st.session_state.selected_page = "Soil Selection"
                st.rerun()
    else:
        # Display the current soil selection
        st.markdown(f"""
        <div class="custom-card" style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                        Selected Soil
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: white;">
                        {st.session_state.selected_soil}
                    </div>
                </div>
                <div class="secondary-button">
        """, unsafe_allow_html=True)
        
        col_right1, col_right2 = st.columns([3, 1])
        with col_right2:
            if st.button("Change", use_container_width=True, key="change_soil_btn"):
                st.session_state.selected_page = "Soil Selection"
                st.rerun()
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Call the season selector component
        season_selector()
        
        # Display navigation buttons if a season has been selected
        if st.session_state.selected_season:
            col1, col2 = st.columns(2)
            with col2:
                st.markdown('<div class="action-button">', unsafe_allow_html=True)
                if st.button("View Recommendations →", use_container_width=True):
                    st.session_state.show_results = True
                    st.session_state.selected_page = "Crop Recommendations"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

elif selected_page == "Crop Recommendations":
    # Check if soil and season have been selected
    if not st.session_state.selected_soil or not st.session_state.selected_season:
        st.markdown("""
        <div class="warning-alert" style="margin: 2rem 0;">
            <div style="font-weight: 600; margin-bottom: 0.5rem; color: var(--accent);">
                Selection Required
            </div>
            <p style="color: var(--text-muted);">
                Please select both soil type and season to get personalized crop recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Start from Soil Selection", use_container_width=True):
                st.session_state.selected_page = "Soil Selection"
                st.rerun()
    else:
        # Display the current selections
        st.markdown(f"""
        <div class="custom-card" style="margin-bottom: 1.5rem;">
            <div style="display: flex; flex-wrap: wrap; gap: 1.5rem;">
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                        Selected Soil
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: white;">
                        {st.session_state.selected_soil}
                    </div>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                        Selected Season
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: white;">
                        {st.session_state.selected_season}
                    </div>
                </div>
                <div style="display: flex; align-items: flex-end; gap: 0.5rem;">
        """, unsafe_allow_html=True)
        
        col_right1, col_right2 = st.columns(2)
        with col_right1:
            if st.button("Change Soil", use_container_width=True, key="change_soil_btn2"):
                st.session_state.selected_soil = None
                st.session_state.selected_page = "Soil Selection"
                st.rerun()
        
        with col_right2:
            if st.button("Change Season", use_container_width=True, key="change_season_btn"):
                st.session_state.selected_season = None
                st.session_state.selected_page = "Season Selection"
                st.rerun()
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show recommendations
        show_recommendations(st.session_state.selected_soil, st.session_state.selected_season)

elif selected_page == "Knowledge Hub":
    # Header for Knowledge Hub
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; color: white;">
            Agricultural Knowledge Hub
        </div>
        <div style="color: var(--text-muted); margin-bottom: 1rem;">
            Access detailed information on soil types, farming practices, and sustainable agriculture
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the soil information panel
    if st.session_state.selected_soil and st.session_state.selected_season:
        # Display current selections
        st.markdown(f"""
        <div class="custom-card" style="margin-bottom: 1.5rem;">
            <div style="display: flex; flex-wrap: wrap; gap: 1.5rem;">
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                        Selected Soil
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: white;">
                        {st.session_state.selected_soil}
                    </div>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                        Selected Season
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: white;">
                        {st.session_state.selected_season}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        show_info_panel(st.session_state.selected_soil, st.session_state.selected_season)
    elif st.session_state.selected_soil:
        # Display current soil selection
        st.markdown(f"""
        <div class="custom-card" style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                        Selected Soil
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: white;">
                        {st.session_state.selected_soil}
                    </div>
                </div>
                <div>
                    <span class="badge badge-primary">Viewing Soil Information</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        show_info_panel(st.session_state.selected_soil)
    else:
        # If no selections have been made, show a message
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="custom-card">
                <div class="card-title">Agricultural Knowledge Hub</div>
                <div class="card-content">
                    <p style="margin-bottom: 1rem; color: #e0e0e0;">
                        Please select a soil type to view detailed information about soil characteristics, 
                        farming practices, and sustainability recommendations.
                    </p>
                    <p style="color: var(--text-muted);">
                        Our knowledge hub provides comprehensive guidance on:
                    </p>
                    <ul style="color: var(--text-muted); margin-top: 0.5rem;">
                        <li>Soil properties and composition</li>
                        <li>Optimal cultivation practices</li>
                        <li>Water and nutrient management</li>
                        <li>Sustainable farming techniques</li>
                        <li>Season-specific recommendations</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Load the info animation
            info_animation = load_lottie_url(LOTTIE_INFO)
            if info_animation:
                st_lottie(info_animation, height=200, key="info_animation")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown('<div class="action-button">', unsafe_allow_html=True)
            if st.button("Select Soil Type", use_container_width=True):
                st.session_state.selected_page = "Soil Selection"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main-content div

# Add the custom footer
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;">
        <div style="font-size: 0.85rem;">
            Smart Agriculture Platform • Version 2.0
        </div>
        <div>
            Smart Agriculture - Viksit Bharat 2047 | Empowering farmers through technology
        </div>
        <div style="font-size: 0.85rem;">
            © 2025 Viksit Bharat Initiative
        </div>
    </div>
</div>
""", unsafe_allow_html=True)