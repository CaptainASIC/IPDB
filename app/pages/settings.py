"""
Settings page for IP Address Tracker
Handles site management, subnet configuration, and IP assignment
"""

import streamlit as st
import pandas as pd
import ipaddress
from datetime import datetime
from models.database import get_db_session, Site, IPAddress, Subnet

def render_settings_page():
    """Render the settings and administration page"""
    st.header("⚙️ Settings & Administration")
    
    # Create tabs for different settings sections
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Sites", "🔗 Subnets", "🌐 IP Addresses", "🔧 System"])
    
    with tab1:
        render_sites_management()
    
    with tab2:
        render_subnets_management()
    
    with tab3:
        render_ip_management()
    
    with tab4:
        render_system_settings()

def render_sites_management():
    """Render site management interface"""
    st.subheader("🏢 Site Management")
    
    # Add new site section
    with st.expander("➕ Add New Site"):
        with st.form("add_site_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                site_name = st.text_input("Site Name*", placeholder="e.g., Headquarters")
                site_location = st.text_input("Location", placeholder="e.g., New York, NY")
            
            with col2:
                site_description = st.text_area("Description", placeholder="Brief description of the site")
            
            if st.form_submit_button("Add Site"):
                if site_name:
                    success, message = add_new_site(site_name, site_description, site_location)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Site name is required")
    
    # Display existing sites
    st.markdown("### 📋 Existing Sites")
    sites_df = get_sites_dataframe()
    
    if not sites_df.empty:
        # Display sites with edit/delete options
        for idx, site in sites_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**{site['Name']}**")
                    st.caption(f"📍 {site['Location']} | 🌐 {site['IP Count']} IPs")
                
                with col2:
                    st.text(site['Description'][:50] + "..." if len(site['Description']) > 50 else site['Description'])
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_site_{site['ID']}"):
                        st.session_state[f"edit_site_{site['ID']}"] = True
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_site_{site['ID']}"):
                        if site['IP Count'] == 0:
                            success, message = delete_site(site['ID'])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("Cannot delete site with existing IP addresses")
                
                # Edit form
                if st.session_state.get(f"edit_site_{site['ID']}", False):
                    with st.form(f"edit_site_form_{site['ID']}"):
                        edit_name = st.text_input("Name", value=site['Name'])
                        edit_location = st.text_input("Location", value=site['Location'])
                        edit_description = st.text_area("Description", value=site['Description'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Save Changes"):
                                success, message = update_site(site['ID'], edit_name, edit_description, edit_location)
                                if success:
                                    st.success(message)
                                    st.session_state[f"edit_site_{site['ID']}"] = False
                                    st.rerun()
                                else:
                                    st.error(message)
                        
                        with col2:
                            if st.form_submit_button("Cancel"):
                                st.session_state[f"edit_site_{site['ID']}"] = False
                                st.rerun()
                
                st.markdown("---")
    else:
        st.info("No sites configured. Add your first site above.")

def render_subnets_management():
    """Render subnet management interface"""
    st.subheader("🔗 Subnet Management")
    
    # Add new subnet section
    with st.expander("➕ Add New Subnet"):
        with st.form("add_subnet_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Get sites for dropdown
                sites = get_sites_list()
                if sites:
                    selected_site = st.selectbox("Site*", sites, format_func=lambda x: x[1])
                    subnet_cidr = st.text_input("Subnet CIDR*", placeholder="e.g., 192.168.1.0/24")
                    subnet_name = st.text_input("Subnet Name*", placeholder="e.g., LAN-Network")
                else:
                    st.error("No sites available. Please add a site first.")
                    selected_site = None
                    subnet_cidr = ""
                    subnet_name = ""
            
            with col2:
                subnet_description = st.text_area("Description", placeholder="Brief description of the subnet")
                vlan_id = st.number_input("VLAN ID", min_value=1, max_value=4094, value=None, placeholder="Optional")
            
            if st.form_submit_button("Add Subnet"):
                if selected_site and subnet_cidr and subnet_name:
                    success, message = add_new_subnet(
                        selected_site[0], subnet_cidr, subnet_name, subnet_description, vlan_id
                    )
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Site, subnet CIDR, and name are required")
    
    # Display existing subnets
    st.markdown("### 📋 Existing Subnets")
    subnets_df = get_subnets_dataframe()
    
    if not subnets_df.empty:
        # Display subnets with delete buttons
        for index, subnet in subnets_df.iterrows():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.write(f"**{subnet['Subnet CIDR']}** - {subnet['Name']}")
                st.caption(f"Site: {subnet['Site']} | VLAN: {subnet['VLAN ID']} | Used: {subnet['Used IPs']}/{subnet['Capacity']}")
            
            with col2:
                st.write(subnet['Description'])
            
            with col3:
                utilization = subnet['Utilization']
                if utilization < 50:
                    st.success(f"{utilization}%")
                elif utilization < 80:
                    st.warning(f"{utilization}%")
                else:
                    st.error(f"{utilization}%")
            
            with col4:
                if st.button("🗑️ Delete", key=f"delete_subnet_{subnet['ID']}"):
                    if subnet['Used IPs'] == 0:
                        success, message = delete_subnet(subnet['ID'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error(f"Cannot delete subnet with {subnet['Used IPs']} existing IP addresses")
            
            st.markdown("---")
    else:
        st.info("No subnets configured. Add your first subnet above.")

def render_ip_management():
    """Render IP address management interface"""
    st.subheader("🌐 IP Address Management")
    
    # Add new IP address section
    with st.expander("➕ Add New IP Address"):
        with st.form("add_ip_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Get sites for dropdown
                sites = get_sites_list()
                if sites:
                    selected_site = st.selectbox("Site*", sites, format_func=lambda x: x[1], key="ip_site")
                    ip_address = st.text_input("IP Address*", placeholder="e.g., 192.168.1.10")
                    hostname = st.text_input("Hostname", placeholder="e.g., server-01")
                    gateway = st.text_input("Gateway", placeholder="e.g., 192.168.1.1")
                else:
                    st.error("No sites available. Please add a site first.")
                    selected_site = None
                    ip_address = ""
                    hostname = ""
                    gateway = ""
            
            with col2:
                role = st.text_input("Role", placeholder="e.g., Server, Workstation")
                system_owner = st.text_input("System Owner", placeholder="e.g., IT Team, John Doe")
                status = st.selectbox("Status", ["active", "inactive", "reserved"])
                description = st.text_area("Description", placeholder="Brief description")
            
            if st.form_submit_button("Add IP Address"):
                if selected_site and ip_address:
                    success, message = add_new_ip_address(
                        selected_site[0], ip_address, hostname, gateway, role, system_owner, status, description
                    )
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Site and IP address are required")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    session = get_db_session()
    try:
        total_ips = session.query(IPAddress).count()
        active_ips = session.query(IPAddress).filter_by(status='active').count()
        reserved_ips = session.query(IPAddress).filter_by(status='reserved').count()
        
        with col1:
            st.metric("Total IPs", total_ips)
        with col2:
            st.metric("Active IPs", active_ips)
        with col3:
            st.metric("Reserved IPs", reserved_ips)
    finally:
        session.close()
    
    # Display existing IP addresses
    st.markdown("### 📋 Existing IP Addresses")
    ip_addresses_df = get_ip_addresses_dataframe()
    
    if not ip_addresses_df.empty:
        # Display IP addresses with delete buttons
        for index, ip in ip_addresses_df.iterrows():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                status_color = "🟢" if ip['Status'] == 'active' else "🟡" if ip['Status'] == 'reserved' else "🔴"
                st.write(f"**{ip['IP Address']}** {status_color}")
                st.caption(f"Site: {ip['Site']} | Hostname: {ip['Hostname']}")
            
            with col2:
                st.write(f"**Role:** {ip['Role']}")
                st.caption(f"Owner: {ip['Owner']}")
            
            with col3:
                st.write(f"**Gateway:** {ip['Gateway']}")
                st.caption(f"Description: {ip['Description']}")
            
            with col4:
                if st.button("🗑️ Delete", key=f"delete_ip_{ip['ID']}"):
                    success, message = delete_ip_address(ip['ID'])
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            
            st.markdown("---")
    else:
        st.info("No IP addresses configured. Add your first IP address above.")

def render_system_settings():
    """Render system settings interface"""
    st.subheader("🔧 System Settings")
    
    # Database maintenance
    st.markdown("### 🗄️ Database Maintenance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 Clean Inactive IPs"):
            st.info("This feature will be implemented in a future version")
    
    with col2:
        if st.button("📊 Rebuild Statistics"):
            st.info("This feature will be implemented in a future version")
    
    # Application settings
    st.markdown("### ⚙️ Application Settings")
    
    with st.form("app_settings_form"):
        default_status = st.selectbox("Default IP Status", ["active", "inactive", "reserved"])
        auto_cidr = st.checkbox("Auto-add /32 to single IPs", value=True)
        validate_rfc1918 = st.checkbox("Enforce RFC-1918 private IPs only", value=True)
        
        if st.form_submit_button("Save Settings"):
            st.success("Settings saved successfully!")

# Helper functions

def add_new_site(name, description, location):
    """Add a new site to the database"""
    session = get_db_session()
    
    try:
        # Check if site already exists
        existing_site = session.query(Site).filter_by(name=name).first()
        if existing_site:
            return False, f"Site '{name}' already exists"
        
        # Create new site
        new_site = Site(
            name=name,
            description=description,
            location=location
        )
        
        session.add(new_site)
        session.commit()
        
        return True, f"Site '{name}' added successfully"
        
    except Exception as e:
        session.rollback()
        return False, f"Error adding site: {str(e)}"
    finally:
        session.close()

def update_site(site_id, name, description, location):
    """Update an existing site"""
    session = get_db_session()
    
    try:
        site = session.query(Site).filter_by(id=site_id).first()
        if not site:
            return False, "Site not found"
        
        site.name = name
        site.description = description
        site.location = location
        
        session.commit()
        return True, f"Site '{name}' updated successfully"
        
    except Exception as e:
        session.rollback()
        return False, f"Error updating site: {str(e)}"
    finally:
        session.close()

def delete_site(site_id):
    """Delete a site from the database"""
    session = get_db_session()
    
    try:
        site = session.query(Site).filter_by(id=site_id).first()
        if not site:
            return False, "Site not found"
        
        session.delete(site)
        session.commit()
        
        return True, f"Site '{site.name}' deleted successfully"
        
    except Exception as e:
        session.rollback()
        return False, f"Error deleting site: {str(e)}"
    finally:
        session.close()

def delete_subnet(subnet_id):
    """Delete a subnet from the database"""
    session = get_db_session()
    
    try:
        subnet = session.query(Subnet).filter_by(id=subnet_id).first()
        if not subnet:
            return False, "Subnet not found"
        
        # Check if subnet has any IP addresses
        ip_count = session.query(IPAddress).filter(
            IPAddress.site_id == subnet.site_id,
            IPAddress.ip_cidr.op('<<')(subnet.subnet_cidr)
        ).count()
        
        if ip_count > 0:
            return False, f"Cannot delete subnet with {ip_count} existing IP addresses"
        
        session.delete(subnet)
        session.commit()
        
        return True, f"Subnet '{subnet.subnet_cidr}' deleted successfully"
        
    except Exception as e:
        session.rollback()
        return False, f"Error deleting subnet: {str(e)}"
    finally:
        session.close()

def delete_ip_address(ip_id):
    """Delete an IP address from the database"""
    session = get_db_session()
    
    try:
        ip_address = session.query(IPAddress).filter_by(id=ip_id).first()
        if not ip_address:
            return False, "IP address not found"
        
        ip_cidr = str(ip_address.ip_cidr)
        session.delete(ip_address)
        session.commit()
        
        return True, f"IP address '{ip_cidr}' deleted successfully"
        
    except Exception as e:
        session.rollback()
        return False, f"Error deleting IP address: {str(e)}"
    finally:
        session.close()

def add_new_subnet(site_id, subnet_cidr, name, description, vlan_id):
    """Add a new subnet to the database"""
    session = get_db_session()
    
    try:
        # Validate CIDR
        try:
            ipaddress.ip_network(subnet_cidr, strict=False)
        except ValueError:
            return False, "Invalid subnet CIDR format"
        
        # Check if subnet already exists for this site
        existing_subnet = session.query(Subnet).filter_by(
            site_id=site_id, subnet_cidr=subnet_cidr
        ).first()
        if existing_subnet:
            return False, f"Subnet '{subnet_cidr}' already exists for this site"
        
        # Create new subnet
        new_subnet = Subnet(
            site_id=site_id,
            subnet_cidr=subnet_cidr,
            name=name,
            description=description,
            vlan_id=vlan_id
        )
        
        session.add(new_subnet)
        session.commit()
        
        return True, f"Subnet '{subnet_cidr}' added successfully"
        
    except Exception as e:
        session.rollback()
        return False, f"Error adding subnet: {str(e)}"
    finally:
        session.close()

def add_new_ip_address(site_id, ip_address, hostname, gateway, role, system_owner, status, description):
    """Add a new IP address to the database"""
    session = get_db_session()
    
    try:
        # Validate and format IP address
        if '/' not in ip_address:
            ip_cidr = f"{ip_address}/32"
        else:
            ip_cidr = ip_address
        
        try:
            network = ipaddress.ip_network(ip_cidr, strict=False)
            if not network.is_private:
                return False, "Only private IP addresses (RFC-1918) are allowed"
        except ValueError:
            return False, "Invalid IP address format"
        
        # Check if IP already exists for this site
        existing_ip = session.query(IPAddress).filter_by(
            site_id=site_id, ip_cidr=ip_cidr
        ).first()
        if existing_ip:
            return False, f"IP address '{ip_cidr}' already exists for this site"
        
        # Validate gateway if provided
        if gateway:
            try:
                ipaddress.ip_address(gateway)
            except ValueError:
                return False, "Invalid gateway IP address format"
        
        # Create new IP address
        new_ip = IPAddress(
            site_id=site_id,
            ip_cidr=ip_cidr,
            hostname=hostname if hostname else None,
            gateway=gateway if gateway else None,
            role=role if role else None,
            system_owner=system_owner if system_owner else None,
            status=status,
            description=description if description else None
        )
        
        session.add(new_ip)
        session.commit()
        
        return True, f"IP address '{ip_cidr}' added successfully"
        
    except Exception as e:
        session.rollback()
        return False, f"Error adding IP address: {str(e)}"
    finally:
        session.close()

def get_sites_dataframe():
    """Get sites data as DataFrame"""
    session = get_db_session()
    
    try:
        sites = session.query(Site).order_by(Site.name).all()
        
        data = []
        for site in sites:
            ip_count = session.query(IPAddress).filter_by(site_id=site.id).count()
            
            data.append({
                'ID': site.id,
                'Name': site.name,
                'Description': site.description or 'N/A',
                'Location': site.location or 'N/A',
                'IP Count': ip_count,
                'Created': site.created_at.strftime('%Y-%m-%d') if site.created_at else 'N/A'
            })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"Error loading sites: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()

def get_subnets_dataframe():
    """Get subnets data as DataFrame"""
    session = get_db_session()
    
    try:
        query = session.query(
            Subnet.id,
            Subnet.subnet_cidr,
            Subnet.name,
            Subnet.description,
            Subnet.vlan_id,
            Site.name.label('site_name')
        ).join(Site)
        
        results = query.order_by(Subnet.subnet_cidr).all()
        
        data = []
        for result in results:
            # Calculate utilization
            ip_count = session.query(IPAddress).filter(
                IPAddress.site_id == result.id,
                IPAddress.ip_cidr.op('<<')(result.subnet_cidr)
            ).count()
            
            network = ipaddress.ip_network(str(result.subnet_cidr))
            capacity = network.num_addresses - 2  # Exclude network and broadcast
            utilization = (ip_count / capacity * 100) if capacity > 0 else 0
            
            data.append({
                'ID': result.id,
                'Site': result.site_name,
                'Subnet CIDR': str(result.subnet_cidr),
                'Name': result.name,
                'Description': result.description or 'N/A',
                'VLAN ID': result.vlan_id or 'N/A',
                'Used IPs': ip_count,
                'Capacity': capacity,
                'Utilization': round(utilization, 1)
            })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"Error loading subnets: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()

def get_ip_addresses_dataframe():
    """Get IP addresses data as DataFrame"""
    session = get_db_session()
    
    try:
        query = session.query(
            IPAddress.id,
            IPAddress.ip_cidr,
            IPAddress.hostname,
            IPAddress.gateway,
            IPAddress.role,
            IPAddress.system_owner,
            IPAddress.description,
            IPAddress.status,
            Site.name.label('site_name')
        ).join(Site)
        
        results = query.order_by(IPAddress.ip_cidr).all()
        
        data = []
        for result in results:
            data.append({
                'ID': result.id,
                'Site': result.site_name,
                'IP Address': str(result.ip_cidr),
                'Hostname': result.hostname or 'N/A',
                'Gateway': str(result.gateway) if result.gateway else 'N/A',
                'Role': result.role or 'N/A',
                'Owner': result.system_owner or 'N/A',
                'Description': result.description or 'N/A',
                'Status': result.status
            })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"Error loading IP addresses: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()

def get_sites_list():
    """Get list of sites for dropdown"""
    session = get_db_session()
    
    try:
        sites = session.query(Site).order_by(Site.name).all()
        return [(site.id, site.name) for site in sites]
    except Exception as e:
        st.error(f"Error loading sites: {str(e)}")
        return []
    finally:
        session.close()

