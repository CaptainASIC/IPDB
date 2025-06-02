"""
IP Address Tracker - Main Streamlit Application
A comprehensive tool for tracking and managing IP addresses across multiple sites
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from typing import List, Dict, Any

# Import custom modules
from models.database import init_database, get_db_session, Site, IPAddress, Subnet
from utils.import_export import import_export_manager
from pages import dashboard, search, settings, import_export
from components.enhanced_styles import get_enhanced_css

# Page configuration
st.set_page_config(
    page_title="IP Address Tracker",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def initialize_app():
    """Initialize the application and database"""
    try:
        init_database()
        return True
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        return False

def load_custom_css():
    """Load enhanced custom CSS for dark mode and orange theme"""
    st.markdown(get_enhanced_css(), unsafe_allow_html=True)

def get_site_list() -> List[str]:
    """Get list of all sites for dropdown"""
    session = get_db_session()
    try:
        sites = session.query(Site).all()
        site_names = [site.name for site in sites]
        return ['ALL'] + sorted(site_names)
    except Exception as e:
        st.error(f"Error loading sites: {str(e)}")
        return ['ALL']
    finally:
        session.close()

def render_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🌐 IP Address Tracker</h1>
        <p>Comprehensive IP address and network management system</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_navigation():
    """Render sidebar navigation menu with logo"""
    # Display logo at the top of sidebar
    try:
        st.sidebar.image("assets/logo.png", width=200)
    except:
        # Fallback if logo not found
        st.sidebar.markdown("## 🌐 IPDB")
    
    st.sidebar.markdown("## 📋 Navigation")
    
    pages = {
        "🏠 Dashboard": "dashboard",
        "🔍 Search & Browse": "search",
        "📊 Analytics": "analytics",
        "⚙️ Settings": "settings",
        "📥 Import/Export": "import_export",
        "📚 Help": "help"
    }
    
    selected_page = st.sidebar.radio(
        "Select Page",
        list(pages.keys()),
        key="page_selector"
    )
    
    return pages[selected_page]

def render_sidebar_stats():
    """Render sidebar statistics"""
    st.sidebar.markdown("## 📊 Quick Stats")
    
    session = get_db_session()
    try:
        # Get statistics
        total_ips = session.query(IPAddress).count()
        total_sites = session.query(Site).count()
        total_subnets = session.query(Subnet).count()
        active_ips = session.query(IPAddress).filter_by(status='active').count()
        
        # Display metrics
        st.sidebar.metric("Total IP Addresses", total_ips)
        st.sidebar.metric("Active IP Addresses", active_ips)
        st.sidebar.metric("Total Sites", total_sites)
        st.sidebar.metric("Total Subnets", total_subnets)
        
    except Exception as e:
        st.sidebar.error(f"Error loading statistics: {str(e)}")
    finally:
        session.close()

def render_sidebar_about():
    """Render sidebar about section with credits and links"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("## ℹ️ About")
    
    st.sidebar.markdown("""
    
    ---
    
    © 2024 Captain ASIC  
    Licensed under MIT License
    """)
    
    # GitHub link button
    if st.sidebar.button("🐙 View on GitHub", help="Open the IPDB repository on GitHub"):
        st.sidebar.markdown("""
        <script>
        window.open('https://github.com/CaptainASIC/IPDB', '_blank');
        </script>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize application
    if not initialize_app():
        st.stop()
    
    # Load custom CSS
    load_custom_css()
    
    # Render header
    render_header()
    
    # Render sidebar
    selected_page = render_sidebar_navigation()
    render_sidebar_stats()
    render_sidebar_about()
    
    # Render main content based on selected page
    if selected_page == "dashboard":
        dashboard.render_dashboard()
    elif selected_page == "search":
        search.render_search_page()
    elif selected_page == "analytics":
        render_analytics_page()
    elif selected_page == "settings":
        settings.render_settings_page()
    elif selected_page == "import_export":
        import_export.render_import_export_page()
    elif selected_page == "help":
        render_help_page()

def render_analytics_page():
    """Render analytics page placeholder"""
    st.header("📊 Analytics")
    st.info("Analytics page coming soon! This will include network utilization charts, IP allocation graphs, and site comparison metrics.")

def render_help_page():
    """Render help page"""
    st.header("📚 Help & Documentation")
    
    st.markdown("""
    ## Welcome to IP Address Tracker
    
    This application helps you manage and track IP addresses across multiple network sites.
    
    ### Key Features
    
    - **🏠 Dashboard**: Overview of your network infrastructure
    - **🔍 Search & Browse**: Find IP addresses and hostnames quickly
    - **⚙️ Settings**: Manage sites, subnets, and IP assignments
    - **📥 Import/Export**: Bulk operations with CSV files
    
    ### Getting Started
    
    1. **Add Sites**: Use the Settings page to add your network sites
    2. **Define Subnets**: Configure your network subnets for each site
    3. **Add IP Addresses**: Manually add IPs or import from CSV
    4. **Search & Filter**: Use the search functionality to find specific IPs
    
    ### Universal IP Address Support
    
    This application supports all IP address ranges:
    - All IP addresses are stored in CIDR notation
    - Single IP addresses are automatically converted to /32
    - Supports private, public, multicast, and all valid IPv4/IPv6 ranges
    - No restrictions on address space (RFC-1918, public IPs, etc.)
    
    ### Import/Export
    
    - **CSV Import**: Upload CSV files with IP address data
    - **CSV Export**: Download your data for backup or analysis
    - **Templates**: Download CSV templates for proper formatting
    
    ### Support
    
    For technical support, feature requests, or bug reports:
    
    - **GitHub Issues**: [Report an issue or request a feature](https://github.com/CaptainASIC/IPDB/issues)
    - **Documentation**: Refer to this help page and the project README
    - **Community**: Check existing issues for solutions to common problems
    
    **Before reporting an issue:**
    1. Check if the issue already exists in GitHub Issues
    2. Include your browser information and steps to reproduce
    3. Provide relevant error messages or screenshots
    4. Describe the expected vs actual behavior
    
    **Feature Requests:**
    - Use GitHub Issues with the "enhancement" label
    - Describe the use case and expected functionality
    - Include any relevant examples or mockups
    """)

if __name__ == "__main__":
    main()

