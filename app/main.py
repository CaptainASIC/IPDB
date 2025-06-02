"""
IP Database - Main Streamlit Application
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
    page_title="IP DB",
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
        #return ['ALL'] + sorted(site_names)
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
    
    ### RFC-1918 Compliance
    
    This application follows RFC-1918 standards:
    - All IP addresses are stored in CIDR notation
    - Single IP addresses are automatically converted to /32
    - Only private IP address ranges are supported
    
    ### Import/Export
    
    - **CSV Import**: Upload CSV files with IP address data
    - **CSV Export**: Download your data for backup or analysis
    - **Templates**: Download CSV templates for proper formatting
    
    ### Support
    
    For technical support or feature requests, please contact your system administrator.
    """)

if __name__ == "__main__":
    main()

