"""
Dashboard page for IP Address Tracker
Provides overview and summary information
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import func
from models.database import get_db_session, Site, IPAddress, Subnet

def render_dashboard():
    """Render the main dashboard page"""
    st.header("🏠 Dashboard")
    
    # Get dashboard data
    dashboard_data = get_dashboard_data()
    
    if not dashboard_data:
        st.error("Unable to load dashboard data")
        return
    
    # Render overview metrics
    render_overview_metrics(dashboard_data)
    
    # Render charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_site_distribution_chart(dashboard_data)
        render_ip_status_chart(dashboard_data)
    
    with col2:
        render_recent_activity(dashboard_data)
        render_subnet_utilization(dashboard_data)

def get_dashboard_data():
    """Get all data needed for dashboard"""
    session = get_db_session()
    
    try:
        data = {}
        
        # Basic counts
        data['total_ips'] = session.query(IPAddress).count()
        data['total_sites'] = session.query(Site).count()
        data['total_subnets'] = session.query(Subnet).count()
        data['active_ips'] = session.query(IPAddress).filter_by(status='active').count()
        data['inactive_ips'] = session.query(IPAddress).filter_by(status='inactive').count()
        data['reserved_ips'] = session.query(IPAddress).filter_by(status='reserved').count()
        
        # Site distribution
        site_counts = session.query(
            Site.name,
            func.count(IPAddress.id).label('ip_count')
        ).outerjoin(IPAddress).group_by(Site.name).all()
        
        data['site_distribution'] = [
            {'site': site, 'count': count} for site, count in site_counts
        ]
        
        # Recent activity (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_ips = session.query(IPAddress).filter(
            IPAddress.created_at >= week_ago
        ).order_by(IPAddress.created_at.desc()).limit(10).all()
        
        data['recent_activity'] = []
        for ip in recent_ips:
            site_name = session.query(Site.name).filter_by(id=ip.site_id).scalar()
            data['recent_activity'].append({
                'ip': str(ip.ip_cidr),
                'hostname': ip.hostname or 'N/A',
                'site': site_name,
                'created': ip.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        # Subnet utilization
        subnets = session.query(Subnet).all()
        data['subnet_utilization'] = []
        
        for subnet in subnets:
            site_name = session.query(Site.name).filter_by(id=subnet.site_id).scalar()
            ip_count = session.query(IPAddress).filter(
                IPAddress.site_id == subnet.site_id,
                IPAddress.ip_cidr.op('<<')(subnet.subnet_cidr)
            ).count()
            
            # Calculate subnet capacity (simplified)
            import ipaddress
            network = ipaddress.ip_network(str(subnet.subnet_cidr))
            capacity = network.num_addresses - 2  # Exclude network and broadcast
            utilization = (ip_count / capacity * 100) if capacity > 0 else 0
            
            data['subnet_utilization'].append({
                'subnet': str(subnet.subnet_cidr),
                'name': subnet.name,
                'site': site_name,
                'used': ip_count,
                'capacity': capacity,
                'utilization': round(utilization, 1)
            })
        
        return data
        
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")
        return None
    finally:
        session.close()

def render_overview_metrics(data):
    """Render overview metrics cards"""
    st.subheader("📊 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #FF6B35; margin: 0;">🌐 Total IPs</h3>
            <h2 style="margin: 0.5rem 0;">{}</h2>
            <p style="color: #cccccc; margin: 0;">IP Addresses</p>
        </div>
        """.format(data['total_ips']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #FF6B35; margin: 0;">✅ Active IPs</h3>
            <h2 style="margin: 0.5rem 0;">{}</h2>
            <p style="color: #cccccc; margin: 0;">Currently Active</p>
        </div>
        """.format(data['active_ips']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #FF6B35; margin: 0;">🏢 Sites</h3>
            <h2 style="margin: 0.5rem 0;">{}</h2>
            <p style="color: #cccccc; margin: 0;">Network Sites</p>
        </div>
        """.format(data['total_sites']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #FF6B35; margin: 0;">🔗 Subnets</h3>
            <h2 style="margin: 0.5rem 0;">{}</h2>
            <p style="color: #cccccc; margin: 0;">Network Subnets</p>
        </div>
        """.format(data['total_subnets']), unsafe_allow_html=True)

def render_site_distribution_chart(data):
    """Render site distribution pie chart"""
    st.subheader("🏢 IP Distribution by Site")
    
    if not data['site_distribution']:
        st.info("No data available for site distribution")
        return
    
    df = pd.DataFrame(data['site_distribution'])
    
    fig = px.pie(
        df,
        values='count',
        names='site',
        title="IP Addresses per Site",
        color_discrete_sequence=['#FF6B35', '#FF8C42', '#FFA500', '#FFB84D', '#FFC966']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_ip_status_chart(data):
    """Render IP status distribution chart"""
    st.subheader("📊 IP Status Distribution")
    
    status_data = [
        {'status': 'Active', 'count': data['active_ips']},
        {'status': 'Inactive', 'count': data['inactive_ips']},
        {'status': 'Reserved', 'count': data['reserved_ips']}
    ]
    
    df = pd.DataFrame(status_data)
    
    fig = px.bar(
        df,
        x='status',
        y='count',
        title="IP Addresses by Status",
        color='status',
        color_discrete_map={
            'Active': '#00ff00',
            'Inactive': '#ff0000',
            'Reserved': '#FFA500'
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_recent_activity(data):
    """Render recent activity table"""
    st.subheader("🕒 Recent Activity")
    
    if not data['recent_activity']:
        st.info("No recent activity to display")
        return
    
    df = pd.DataFrame(data['recent_activity'])
    
    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ip": "IP Address",
            "hostname": "Hostname",
            "site": "Site",
            "created": "Created"
        }
    )

def render_subnet_utilization(data):
    """Render subnet utilization chart"""
    st.subheader("📈 Subnet Utilization")
    
    if not data['subnet_utilization']:
        st.info("No subnet data available")
        return
    
    df = pd.DataFrame(data['subnet_utilization'])
    
    # Create horizontal bar chart
    fig = px.bar(
        df,
        x='utilization',
        y='name',
        orientation='h',
        title="Subnet Utilization (%)",
        color='utilization',
        color_continuous_scale=['#00ff00', '#FFA500', '#ff0000'],
        range_color=[0, 100]
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed table
    with st.expander("📋 Detailed Subnet Information"):
        st.dataframe(
            df[['subnet', 'site', 'used', 'capacity', 'utilization']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "subnet": "Subnet CIDR",
                "site": "Site",
                "used": "Used IPs",
                "capacity": "Total Capacity",
                "utilization": st.column_config.ProgressColumn(
                    "Utilization %",
                    help="Percentage of subnet capacity used",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                )
            }
        )

