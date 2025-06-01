"""
Search page for IP Address Tracker
Handles IP address and hostname search functionality
"""

import streamlit as st
import pandas as pd
import ipaddress
from sqlalchemy import or_, and_
from models.database import get_db_session, Site, IPAddress, Subnet

def render_search_page():
    """Render the search and browse page"""
    st.header("🔍 Search & Browse")
    
    # Get search parameters from session state
    selected_site = st.session_state.get('selected_site', 'ALL')
    search_query = st.session_state.get('search_query', '')
    
    # Advanced search options
    with st.expander("🔧 Advanced Search Options"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Status Filter",
                ['All', 'active', 'inactive', 'reserved'],
                key="status_filter"
            )
        
        with col2:
            role_filter = st.text_input(
                "Role Filter",
                placeholder="e.g., Server, Workstation",
                key="role_filter"
            )
        
        with col3:
            owner_filter = st.text_input(
                "Owner Filter",
                placeholder="e.g., IT Team, John Doe",
                key="owner_filter"
            )
    
    # Perform search
    search_results = perform_search(
        search_query=search_query,
        site_filter=selected_site,
        status_filter=status_filter,
        role_filter=role_filter,
        owner_filter=owner_filter
    )
    
    # Display results
    if search_results is not None:
        display_search_results(search_results, search_query)
    
    # Browse all data section
    st.markdown("---")
    render_browse_section(selected_site)

def perform_search(search_query, site_filter, status_filter, role_filter, owner_filter):
    """Perform search based on provided criteria"""
    session = get_db_session()
    
    try:
        # Base query
        query = session.query(
            IPAddress.id,
            IPAddress.ip_cidr,
            IPAddress.hostname,
            IPAddress.gateway,
            IPAddress.role,
            IPAddress.system_owner,
            IPAddress.description,
            IPAddress.status,
            IPAddress.created_at,
            IPAddress.updated_at,
            Site.name.label('site_name')
        ).join(Site)
        
        # Apply filters
        filters = []
        
        # Site filter
        if site_filter and site_filter != 'ALL':
            filters.append(Site.name == site_filter)
        
        # Status filter
        if status_filter and status_filter != 'All':
            filters.append(IPAddress.status == status_filter)
        
        # Role filter
        if role_filter:
            filters.append(IPAddress.role.ilike(f'%{role_filter}%'))
        
        # Owner filter
        if owner_filter:
            filters.append(IPAddress.system_owner.ilike(f'%{owner_filter}%'))
        
        # Search query filter
        if search_query:
            search_filters = []
            
            # Try to parse as IP address
            try:
                # Handle both single IP and CIDR notation
                if '/' not in search_query:
                    search_ip = f"{search_query}/32"
                else:
                    search_ip = search_query
                
                # Validate IP
                ipaddress.ip_network(search_ip, strict=False)
                search_filters.append(IPAddress.ip_cidr.op('>>=')(search_ip))
                search_filters.append(IPAddress.ip_cidr.op('<<=')(search_ip))
                search_filters.append(IPAddress.ip_cidr == search_ip)
            except ValueError:
                pass
            
            # Search in hostname
            search_filters.append(IPAddress.hostname.ilike(f'%{search_query}%'))
            
            # Search in description
            search_filters.append(IPAddress.description.ilike(f'%{search_query}%'))
            
            # Search in role
            search_filters.append(IPAddress.role.ilike(f'%{search_query}%'))
            
            # Search in system owner
            search_filters.append(IPAddress.system_owner.ilike(f'%{search_query}%'))
            
            if search_filters:
                filters.append(or_(*search_filters))
        
        # Apply all filters
        if filters:
            query = query.filter(and_(*filters))
        
        # Execute query
        results = query.order_by(IPAddress.ip_cidr).all()
        
        # Convert to DataFrame
        data = []
        for result in results:
            data.append({
                'ID': result.id,
                'Site': result.site_name,
                'IP Address': str(result.ip_cidr),
                'Hostname': result.hostname or 'N/A',
                'Gateway': str(result.gateway) if result.gateway else 'N/A',
                'Role': result.role or 'N/A',
                'System Owner': result.system_owner or 'N/A',
                'Description': result.description or 'N/A',
                'Status': result.status,
                'Created': result.created_at.strftime('%Y-%m-%d %H:%M') if result.created_at else 'N/A',
                'Updated': result.updated_at.strftime('%Y-%m-%d %H:%M') if result.updated_at else 'N/A'
            })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return None
    finally:
        session.close()

def display_search_results(df, search_query):
    """Display search results in a formatted table"""
    if df.empty:
        if search_query:
            st.info(f"No results found for '{search_query}'")
        else:
            st.info("No IP addresses match the current filters")
        return
    
    st.subheader(f"📋 Search Results ({len(df)} found)")
    
    # Add action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📥 Export Results", key="export_search"):
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"ip_search_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("🔄 Refresh", key="refresh_search"):
            st.rerun()
    
    # Display results table
    display_df = df.drop('ID', axis=1)  # Hide ID column
    
    # Configure column display
    column_config = {
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Current status of the IP address",
            options=["active", "inactive", "reserved"],
        ),
        "IP Address": st.column_config.TextColumn(
            "IP Address",
            help="IP address in CIDR notation",
            width="medium"
        )
    }
    
    # Display with custom styling
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        height=400
    )
    
    # Show detailed view for selected row
    if not df.empty:
        with st.expander("🔍 View Details"):
            selected_ip = st.selectbox(
                "Select IP for details:",
                options=df['IP Address'].tolist(),
                key="detail_selector"
            )
            
            if selected_ip:
                ip_details = df[df['IP Address'] == selected_ip].iloc[0]
                render_ip_details(ip_details)

def render_ip_details(ip_data):
    """Render detailed view of selected IP address"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Basic Information")
        st.text(f"IP Address: {ip_data['IP Address']}")
        st.text(f"Hostname: {ip_data['Hostname']}")
        st.text(f"Site: {ip_data['Site']}")
        st.text(f"Status: {ip_data['Status']}")
        
    with col2:
        st.markdown("### 🔧 Configuration")
        st.text(f"Gateway: {ip_data['Gateway']}")
        st.text(f"Role: {ip_data['Role']}")
        st.text(f"System Owner: {ip_data['System Owner']}")
        
    st.markdown("### 📝 Description")
    st.text(ip_data['Description'])
    
    st.markdown("### 🕒 Timestamps")
    col1, col2 = st.columns(2)
    with col1:
        st.text(f"Created: {ip_data['Created']}")
    with col2:
        st.text(f"Updated: {ip_data['Updated']}")

def render_browse_section(selected_site):
    """Render browse all data section"""
    st.subheader("📚 Browse All Data")
    
    tab1, tab2, tab3 = st.tabs(["🌐 IP Addresses", "🏢 Sites", "🔗 Subnets"])
    
    with tab1:
        render_all_ips_table(selected_site)
    
    with tab2:
        render_all_sites_table()
    
    with tab3:
        render_all_subnets_table(selected_site)

def render_all_ips_table(site_filter):
    """Render table of all IP addresses"""
    session = get_db_session()
    
    try:
        query = session.query(
            IPAddress.ip_cidr,
            IPAddress.hostname,
            IPAddress.status,
            IPAddress.role,
            Site.name.label('site_name')
        ).join(Site)
        
        if site_filter and site_filter != 'ALL':
            query = query.filter(Site.name == site_filter)
        
        results = query.order_by(IPAddress.ip_cidr).all()
        
        if results:
            data = []
            for result in results:
                data.append({
                    'Site': result.site_name,
                    'IP Address': str(result.ip_cidr),
                    'Hostname': result.hostname or 'N/A',
                    'Role': result.role or 'N/A',
                    'Status': result.status
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No IP addresses found")
            
    except Exception as e:
        st.error(f"Error loading IP addresses: {str(e)}")
    finally:
        session.close()

def render_all_sites_table():
    """Render table of all sites"""
    session = get_db_session()
    
    try:
        sites = session.query(Site).order_by(Site.name).all()
        
        if sites:
            data = []
            for site in sites:
                ip_count = session.query(IPAddress).filter_by(site_id=site.id).count()
                subnet_count = session.query(Subnet).filter_by(site_id=site.id).count()
                
                data.append({
                    'Site Name': site.name,
                    'Description': site.description or 'N/A',
                    'Location': site.location or 'N/A',
                    'IP Count': ip_count,
                    'Subnet Count': subnet_count
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No sites found")
            
    except Exception as e:
        st.error(f"Error loading sites: {str(e)}")
    finally:
        session.close()

def render_all_subnets_table(site_filter):
    """Render table of all subnets"""
    session = get_db_session()
    
    try:
        query = session.query(
            Subnet.subnet_cidr,
            Subnet.name,
            Subnet.description,
            Subnet.vlan_id,
            Site.name.label('site_name')
        ).join(Site)
        
        if site_filter and site_filter != 'ALL':
            query = query.filter(Site.name == site_filter)
        
        results = query.order_by(Subnet.subnet_cidr).all()
        
        if results:
            data = []
            for result in results:
                data.append({
                    'Site': result.site_name,
                    'Subnet CIDR': str(result.subnet_cidr),
                    'Name': result.name,
                    'Description': result.description or 'N/A',
                    'VLAN ID': result.vlan_id or 'N/A'
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No subnets found")
            
    except Exception as e:
        st.error(f"Error loading subnets: {str(e)}")
    finally:
        session.close()

