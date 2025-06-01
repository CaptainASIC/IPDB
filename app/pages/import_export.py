"""
Import/Export page for IP Address Tracker
Handles CSV import and export functionality
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.import_export import import_export_manager
from models.database import get_db_session, Site

def render_import_export_page():
    """Render the import/export page"""
    st.header("📥 Import/Export")
    
    # Create tabs for import and export
    tab1, tab2, tab3 = st.tabs(["📥 Import Data", "📤 Export Data", "📋 Templates"])
    
    with tab1:
        render_import_section()
    
    with tab2:
        render_export_section()
    
    with tab3:
        render_templates_section()

def render_import_section():
    """Render data import interface"""
    st.subheader("📥 Import Data from CSV")
    
    st.markdown("""
    ### 📋 Import Guidelines
    
    - **IP Addresses**: Must be in RFC-1918 private ranges
    - **CIDR Notation**: Single IPs will automatically get /32 suffix
    - **Required Fields**: Vary by data type (see templates)
    - **File Format**: CSV files only
    - **Encoding**: UTF-8 recommended
    """)
    
    # Data type selection
    data_type = st.selectbox(
        "Select Data Type to Import",
        ["ip_addresses", "sites", "subnets"],
        format_func=lambda x: {
            "ip_addresses": "🌐 IP Addresses",
            "sites": "🏢 Sites",
            "subnets": "🔗 Subnets"
        }[x]
    )
    
    # File upload
    uploaded_file = st.file_uploader(
        f"Choose CSV file for {data_type.replace('_', ' ').title()}",
        type=['csv'],
        help="Upload a CSV file with the appropriate format"
    )
    
    if uploaded_file is not None:
        # Preview file content
        try:
            df_preview = pd.read_csv(uploaded_file)
            
            st.markdown("### 👀 File Preview")
            st.dataframe(df_preview.head(10), use_container_width=True)
            
            st.markdown(f"**File Info**: {len(df_preview)} rows, {len(df_preview.columns)} columns")
            
            # Validation section
            st.markdown("### ✅ Validation")
            
            # Reset file pointer for validation
            uploaded_file.seek(0)
            file_content = uploaded_file.read()
            
            is_valid, errors = import_export_manager.validate_import_data(df_preview, data_type)
            
            if is_valid:
                st.success("✅ File validation passed!")
                
                # Import confirmation
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if st.button("🚀 Import Data", type="primary"):
                        with st.spinner("Importing data..."):
                            success, message, count = import_export_manager.import_csv_data(file_content, data_type)
                            
                            if success:
                                st.success(f"✅ {message}")
                                st.balloons()
                                
                                # Show import summary
                                st.markdown("### 📊 Import Summary")
                                st.metric("Records Imported", count)
                                
                                # Refresh page data
                                st.rerun()
                            else:
                                st.error(f"❌ Import failed: {message}")
                
                with col2:
                    st.info("💡 Click 'Import Data' to proceed with the import")
            
            else:
                st.error("❌ File validation failed!")
                
                with st.expander("🔍 View Validation Errors"):
                    for error in errors:
                        st.error(f"• {error}")
                
                st.markdown("### 💡 How to Fix")
                st.markdown("""
                1. Download the appropriate template from the Templates tab
                2. Ensure all required columns are present
                3. Verify data formats (IP addresses, hostnames, etc.)
                4. Check for duplicate entries
                5. Ensure IP addresses are in RFC-1918 private ranges
                """)
        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.markdown("### 💡 Troubleshooting")
            st.markdown("""
            - Ensure the file is in CSV format
            - Check that the file is not corrupted
            - Verify the file encoding is UTF-8
            - Make sure the file has proper column headers
            """)

def render_export_section():
    """Render data export interface"""
    st.subheader("📤 Export Data to CSV")
    
    st.markdown("""
    ### 📋 Export Options
    
    Export your data for backup, analysis, or migration purposes.
    All exports include timestamps and are formatted for easy re-import.
    """)
    
    # Export type selection
    export_type = st.selectbox(
        "Select Data Type to Export",
        ["ip_addresses", "sites", "subnets"],
        format_func=lambda x: {
            "ip_addresses": "🌐 IP Addresses",
            "sites": "🏢 Sites", 
            "subnets": "🔗 Subnets"
        }[x]
    )
    
    # Site filter for IP addresses and subnets
    site_filter = None
    if export_type in ["ip_addresses", "subnets"]:
        sites = get_sites_for_filter()
        site_filter = st.selectbox(
            "Filter by Site",
            ["ALL"] + sites,
            help="Select a specific site or ALL for complete export"
        )
    
    # Export preview
    if st.button("👀 Preview Export Data"):
        with st.spinner("Generating preview..."):
            try:
                preview_data = get_export_preview(export_type, site_filter)
                
                if preview_data is not None and not preview_data.empty:
                    st.markdown("### 👀 Export Preview")
                    st.dataframe(preview_data.head(10), use_container_width=True)
                    st.markdown(f"**Total Records**: {len(preview_data)}")
                else:
                    st.info("No data available for export with current filters")
            
            except Exception as e:
                st.error(f"Error generating preview: {str(e)}")
    
    # Export button
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("📥 Export Data", type="primary"):
            with st.spinner("Generating export file..."):
                try:
                    csv_data = import_export_manager.export_data_to_csv(export_type, site_filter)
                    
                    if csv_data:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{export_type}_{timestamp}.csv"
                        
                        st.download_button(
                            label="💾 Download CSV File",
                            data=csv_data,
                            file_name=filename,
                            mime="text/csv",
                            type="primary"
                        )
                        
                        st.success(f"✅ Export ready! Click 'Download CSV File' to save.")
                    else:
                        st.error("No data available for export")
                
                except Exception as e:
                    st.error(f"Export failed: {str(e)}")
    
    with col2:
        st.info("💡 Click 'Export Data' to generate the download file")

def render_templates_section():
    """Render CSV templates section"""
    st.subheader("📋 CSV Templates")
    
    st.markdown("""
    ### 📥 Download Import Templates
    
    Use these templates to ensure your CSV files have the correct format for importing.
    Each template includes sample data and proper column headers.
    """)
    
    # Template download buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🌐 IP Addresses Template")
        st.markdown("""
        **Required Columns:**
        - site_name
        - ip_address
        - hostname
        - gateway
        - role
        - system_owner
        
        **Optional Columns:**
        - description
        - status
        """)
        
        if st.button("📥 Download IP Template"):
            template_data = import_export_manager.generate_import_template("ip_addresses")
            st.download_button(
                label="💾 Save IP Template",
                data=template_data,
                file_name="ip_addresses_template.csv",
                mime="text/csv"
            )
    
    with col2:
        st.markdown("#### 🏢 Sites Template")
        st.markdown("""
        **Required Columns:**
        - name
        - description
        - location
        """)
        
        if st.button("📥 Download Sites Template"):
            template_data = import_export_manager.generate_import_template("sites")
            st.download_button(
                label="💾 Save Sites Template",
                data=template_data,
                file_name="sites_template.csv",
                mime="text/csv"
            )
    
    with col3:
        st.markdown("#### 🔗 Subnets Template")
        st.markdown("""
        **Required Columns:**
        - site_name
        - subnet_cidr
        - name
        - description
        
        **Optional Columns:**
        - vlan_id
        """)
        
        if st.button("📥 Download Subnets Template"):
            template_data = import_export_manager.generate_import_template("subnets")
            st.download_button(
                label="💾 Save Subnets Template",
                data=template_data,
                file_name="subnets_template.csv",
                mime="text/csv"
            )
    
    # Import guidelines
    st.markdown("---")
    st.markdown("### 📋 Import Guidelines")
    
    with st.expander("🌐 IP Addresses Import Guidelines"):
        st.markdown("""
        - **IP Address Format**: Can be single IP (192.168.1.10) or CIDR (192.168.1.10/32)
        - **RFC-1918 Compliance**: Only private IP ranges allowed (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
        - **Site Names**: Must match existing sites or will be auto-created
        - **Hostnames**: Optional, but recommended for identification
        - **Gateway**: Must be valid IP address format
        - **Status**: Must be 'active', 'inactive', or 'reserved'
        """)
    
    with st.expander("🏢 Sites Import Guidelines"):
        st.markdown("""
        - **Name**: Must be unique across all sites
        - **Description**: Brief description of the site purpose
        - **Location**: Physical location or address
        - **Duplicates**: Existing sites with same name will be skipped
        """)
    
    with st.expander("🔗 Subnets Import Guidelines"):
        st.markdown("""
        - **Subnet CIDR**: Must be valid CIDR notation (e.g., 192.168.1.0/24)
        - **Site Names**: Must match existing sites
        - **Name**: Descriptive name for the subnet
        - **VLAN ID**: Optional, must be between 1-4094 if specified
        - **Duplicates**: Same subnet CIDR per site will be skipped
        """)

def get_sites_for_filter():
    """Get list of site names for filtering"""
    session = get_db_session()
    
    try:
        sites = session.query(Site.name).order_by(Site.name).all()
        return [site.name for site in sites]
    except Exception as e:
        st.error(f"Error loading sites: {str(e)}")
        return []
    finally:
        session.close()

def get_export_preview(export_type, site_filter):
    """Get preview of export data"""
    try:
        # Generate export data
        csv_data = import_export_manager.export_data_to_csv(export_type, site_filter)
        
        if csv_data:
            # Convert to DataFrame for preview
            from io import StringIO
            df = pd.read_csv(StringIO(csv_data.decode('utf-8')))
            return df
        else:
            return pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error generating preview: {str(e)}")
        return pd.DataFrame()

