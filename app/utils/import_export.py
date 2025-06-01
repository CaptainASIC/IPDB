"""
Import/Export utilities for IP Tracker application
Handles CSV and Excel file operations for bulk data management
"""

import pandas as pd
import streamlit as st
from io import BytesIO, StringIO
import ipaddress
import validators
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from models.database import Site, IPAddress, Subnet, get_db_session

class ImportExportManager:
    """Manages import and export operations for IP tracking data"""
    
    def __init__(self):
        self.required_ip_columns = ['site_name', 'ip_address', 'hostname', 'gateway', 'role', 'system_owner']
        self.optional_ip_columns = ['description', 'status']
        self.required_site_columns = ['name', 'description', 'location']
        self.required_subnet_columns = ['site_name', 'subnet_cidr', 'name', 'description']
        self.optional_subnet_columns = ['vlan_id']
    
    def validate_ip_address(self, ip_str: str) -> Tuple[bool, str]:
        """Validate IP address and ensure CIDR notation"""
        try:
            if '/' not in ip_str:
                # Add /32 for single IP addresses per RFC-1918 requirement
                ip_str = f"{ip_str}/32"
            
            # Validate CIDR notation
            network = ipaddress.ip_network(ip_str, strict=False)
            
            # Check if it's a private IP (RFC-1918)
            if not network.is_private:
                return False, f"IP address {ip_str} is not a private IP address (RFC-1918)"
            
            return True, str(network)
        except ValueError as e:
            return False, f"Invalid IP address format: {str(e)}"
    
    def validate_hostname(self, hostname: str) -> bool:
        """Validate hostname format"""
        if not hostname or pd.isna(hostname):
            return True  # Hostname is optional
        
        # Basic hostname validation
        if len(hostname) > 255:
            return False
        
        # Check for valid characters
        import re
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        return bool(re.match(pattern, hostname))
    
    def validate_import_data(self, df: pd.DataFrame, data_type: str) -> Tuple[bool, List[str]]:
        """Validate imported data format and content"""
        errors = []
        
        if data_type == 'ip_addresses':
            # Check required columns
            missing_cols = [col for col in self.required_ip_columns if col not in df.columns]
            if missing_cols:
                errors.append(f"Missing required columns: {', '.join(missing_cols)}")
            
            # Validate data content
            for idx, row in df.iterrows():
                # Validate IP address
                if 'ip_address' in row:
                    is_valid, msg = self.validate_ip_address(str(row['ip_address']))
                    if not is_valid:
                        errors.append(f"Row {idx + 1}: {msg}")
                
                # Validate hostname
                if 'hostname' in row and not self.validate_hostname(str(row['hostname'])):
                    errors.append(f"Row {idx + 1}: Invalid hostname format")
                
                # Validate gateway
                if 'gateway' in row and not pd.isna(row['gateway']):
                    try:
                        ipaddress.ip_address(str(row['gateway']))
                    except ValueError:
                        errors.append(f"Row {idx + 1}: Invalid gateway IP address")
        
        elif data_type == 'sites':
            missing_cols = [col for col in self.required_site_columns if col not in df.columns]
            if missing_cols:
                errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        
        elif data_type == 'subnets':
            missing_cols = [col for col in self.required_subnet_columns if col not in df.columns]
            if missing_cols:
                errors.append(f"Missing required columns: {', '.join(missing_cols)}")
            
            # Validate subnet CIDR
            for idx, row in df.iterrows():
                if 'subnet_cidr' in row:
                    try:
                        ipaddress.ip_network(str(row['subnet_cidr']), strict=False)
                    except ValueError:
                        errors.append(f"Row {idx + 1}: Invalid subnet CIDR format")
        
        return len(errors) == 0, errors
    
    def import_csv_data(self, file_content: bytes, data_type: str) -> Tuple[bool, str, int]:
        """Import data from CSV file"""
        try:
            # Read CSV file
            df = pd.read_csv(BytesIO(file_content))
            
            # Validate data
            is_valid, errors = self.validate_import_data(df, data_type)
            if not is_valid:
                return False, f"Validation errors:\n" + "\n".join(errors), 0
            
            # Import data to database
            session = get_db_session()
            imported_count = 0
            
            try:
                if data_type == 'ip_addresses':
                    imported_count = self._import_ip_addresses(df, session)
                elif data_type == 'sites':
                    imported_count = self._import_sites(df, session)
                elif data_type == 'subnets':
                    imported_count = self._import_subnets(df, session)
                
                session.commit()
                return True, f"Successfully imported {imported_count} records", imported_count
            
            except Exception as e:
                session.rollback()
                return False, f"Database error: {str(e)}", 0
            
            finally:
                session.close()
        
        except Exception as e:
            return False, f"File processing error: {str(e)}", 0
    
    def _import_ip_addresses(self, df: pd.DataFrame, session: Session) -> int:
        """Import IP addresses to database"""
        imported_count = 0
        
        for _, row in df.iterrows():
            # Get or create site
            site = session.query(Site).filter_by(name=row['site_name']).first()
            if not site:
                site = Site(name=row['site_name'], description=f"Auto-created for {row['site_name']}")
                session.add(site)
                session.flush()
            
            # Validate and format IP address
            is_valid, ip_cidr = self.validate_ip_address(str(row['ip_address']))
            if not is_valid:
                continue
            
            # Check if IP already exists
            existing_ip = session.query(IPAddress).filter_by(
                ip_cidr=ip_cidr, site_id=site.id
            ).first()
            
            if not existing_ip:
                ip_record = IPAddress(
                    site_id=site.id,
                    ip_cidr=ip_cidr,
                    hostname=row.get('hostname') if not pd.isna(row.get('hostname')) else None,
                    gateway=row.get('gateway') if not pd.isna(row.get('gateway')) else None,
                    role=row.get('role') if not pd.isna(row.get('role')) else None,
                    system_owner=row.get('system_owner') if not pd.isna(row.get('system_owner')) else None,
                    description=row.get('description') if not pd.isna(row.get('description')) else None,
                    status=row.get('status', 'active')
                )
                session.add(ip_record)
                imported_count += 1
        
        return imported_count
    
    def _import_sites(self, df: pd.DataFrame, session: Session) -> int:
        """Import sites to database"""
        imported_count = 0
        
        for _, row in df.iterrows():
            existing_site = session.query(Site).filter_by(name=row['name']).first()
            
            if not existing_site:
                site = Site(
                    name=row['name'],
                    description=row.get('description'),
                    location=row.get('location')
                )
                session.add(site)
                imported_count += 1
        
        return imported_count
    
    def _import_subnets(self, df: pd.DataFrame, session: Session) -> int:
        """Import subnets to database"""
        imported_count = 0
        
        for _, row in df.iterrows():
            # Get site
            site = session.query(Site).filter_by(name=row['site_name']).first()
            if not site:
                continue
            
            existing_subnet = session.query(Subnet).filter_by(
                subnet_cidr=row['subnet_cidr'], site_id=site.id
            ).first()
            
            if not existing_subnet:
                subnet = Subnet(
                    site_id=site.id,
                    subnet_cidr=row['subnet_cidr'],
                    name=row['name'],
                    description=row.get('description'),
                    vlan_id=row.get('vlan_id') if not pd.isna(row.get('vlan_id')) else None
                )
                session.add(subnet)
                imported_count += 1
        
        return imported_count
    
    def export_data_to_csv(self, data_type: str, site_filter: str = None) -> bytes:
        """Export data to CSV format"""
        session = get_db_session()
        
        try:
            if data_type == 'ip_addresses':
                return self._export_ip_addresses(session, site_filter)
            elif data_type == 'sites':
                return self._export_sites(session)
            elif data_type == 'subnets':
                return self._export_subnets(session, site_filter)
        finally:
            session.close()
    
    def _export_ip_addresses(self, session: Session, site_filter: str = None) -> bytes:
        """Export IP addresses to CSV"""
        query = session.query(IPAddress, Site.name.label('site_name')).join(Site)
        
        if site_filter and site_filter != 'ALL':
            query = query.filter(Site.name == site_filter)
        
        results = query.all()
        
        data = []
        for ip, site_name in results:
            data.append({
                'site_name': site_name,
                'ip_address': str(ip.ip_cidr),
                'hostname': ip.hostname,
                'gateway': str(ip.gateway) if ip.gateway else '',
                'role': ip.role,
                'system_owner': ip.system_owner,
                'description': ip.description,
                'status': ip.status,
                'created_at': ip.created_at.strftime('%Y-%m-%d %H:%M:%S') if ip.created_at else '',
                'updated_at': ip.updated_at.strftime('%Y-%m-%d %H:%M:%S') if ip.updated_at else ''
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode('utf-8')
    
    def _export_sites(self, session: Session) -> bytes:
        """Export sites to CSV"""
        sites = session.query(Site).all()
        
        data = []
        for site in sites:
            data.append({
                'name': site.name,
                'description': site.description,
                'location': site.location,
                'created_at': site.created_at.strftime('%Y-%m-%d %H:%M:%S') if site.created_at else '',
                'updated_at': site.updated_at.strftime('%Y-%m-%d %H:%M:%S') if site.updated_at else ''
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode('utf-8')
    
    def _export_subnets(self, session: Session, site_filter: str = None) -> bytes:
        """Export subnets to CSV"""
        query = session.query(Subnet, Site.name.label('site_name')).join(Site)
        
        if site_filter and site_filter != 'ALL':
            query = query.filter(Site.name == site_filter)
        
        results = query.all()
        
        data = []
        for subnet, site_name in results:
            data.append({
                'site_name': site_name,
                'subnet_cidr': str(subnet.subnet_cidr),
                'name': subnet.name,
                'description': subnet.description,
                'vlan_id': subnet.vlan_id,
                'created_at': subnet.created_at.strftime('%Y-%m-%d %H:%M:%S') if subnet.created_at else '',
                'updated_at': subnet.updated_at.strftime('%Y-%m-%d %H:%M:%S') if subnet.updated_at else ''
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode('utf-8')
    
    def generate_import_template(self, data_type: str) -> bytes:
        """Generate CSV template for import"""
        if data_type == 'ip_addresses':
            columns = self.required_ip_columns + self.optional_ip_columns
            sample_data = {
                'site_name': ['Headquarters', 'Branch Office'],
                'ip_address': ['192.168.1.10', '192.168.10.20'],
                'hostname': ['server-01', 'workstation-05'],
                'gateway': ['192.168.1.1', '192.168.10.1'],
                'role': ['Server', 'Workstation'],
                'system_owner': ['IT Team', 'John Doe'],
                'description': ['Main server', 'User workstation'],
                'status': ['active', 'active']
            }
        elif data_type == 'sites':
            columns = self.required_site_columns
            sample_data = {
                'name': ['Headquarters', 'Branch Office'],
                'description': ['Main office location', 'Secondary office'],
                'location': ['New York, NY', 'Los Angeles, CA']
            }
        elif data_type == 'subnets':
            columns = self.required_subnet_columns + self.optional_subnet_columns
            sample_data = {
                'site_name': ['Headquarters', 'Branch Office'],
                'subnet_cidr': ['192.168.1.0/24', '192.168.10.0/24'],
                'name': ['HQ-LAN', 'BRANCH-LAN'],
                'description': ['Headquarters LAN', 'Branch office LAN'],
                'vlan_id': [10, 20]
            }
        
        df = pd.DataFrame(sample_data)
        return df.to_csv(index=False).encode('utf-8')

# Global instance
import_export_manager = ImportExportManager()

