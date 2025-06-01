#!/usr/bin/env python3
"""
Test script for IP Address Tracker application
Tests basic functionality without requiring database connection
"""

import sys
import os
import traceback

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test that all modules can be imported successfully"""
    print("🧪 Testing module imports...")
    
    try:
        # Test basic imports
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        import pandas as pd
        print("✅ Pandas imported successfully")
        
        import plotly.express as px
        print("✅ Plotly imported successfully")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
        
        import ipaddress
        print("✅ ipaddress module imported successfully")
        
        # Test custom module imports
        from models.database import Site, IPAddress, Subnet
        print("✅ Database models imported successfully")
        
        from utils.import_export import ImportExportManager
        print("✅ Import/Export utilities imported successfully")
        
        from components.enhanced_styles import get_enhanced_css
        print("✅ Enhanced styles imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        traceback.print_exc()
        return False

def test_ip_validation():
    """Test IP address validation functionality"""
    print("\n🧪 Testing IP address validation...")
    
    try:
        from utils.import_export import ImportExportManager
        manager = ImportExportManager()
        
        # Test valid IP addresses
        test_cases = [
            ("192.168.1.10", True),
            ("10.0.0.1", True),
            ("172.16.1.100", True),
            ("192.168.1.10/24", True),
            ("8.8.8.8", False),  # Public IP should fail
            ("invalid.ip", False),
            ("256.256.256.256", False)
        ]
        
        for ip, should_pass in test_cases:
            is_valid, message = manager.validate_ip_address(ip)
            if is_valid == should_pass:
                print(f"✅ {ip}: {'Valid' if is_valid else 'Invalid'} (Expected)")
            else:
                print(f"❌ {ip}: {'Valid' if is_valid else 'Invalid'} (Unexpected)")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ IP validation test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_css_generation():
    """Test CSS generation functionality"""
    print("\n🧪 Testing CSS generation...")
    
    try:
        from components.enhanced_styles import get_enhanced_css
        css = get_enhanced_css()
        
        if css and len(css) > 1000:  # Should be a substantial CSS file
            print("✅ Enhanced CSS generated successfully")
            print(f"✅ CSS length: {len(css)} characters")
            
            # Check for key CSS elements
            required_elements = [
                "--primary-color: #FF6B35",
                "main-header",
                "metric-container",
                "@keyframes",
                "hover"
            ]
            
            for element in required_elements:
                if element in css:
                    print(f"✅ Found required CSS element: {element}")
                else:
                    print(f"❌ Missing CSS element: {element}")
                    return False
            
            return True
        else:
            print("❌ CSS generation failed or too short")
            return False
            
    except Exception as e:
        print(f"❌ CSS generation test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_database_models():
    """Test database model definitions"""
    print("\n🧪 Testing database models...")
    
    try:
        from models.database import Site, IPAddress, Subnet
        
        # Test model attributes
        site_attrs = ['id', 'name', 'description', 'location']
        ip_attrs = ['id', 'site_id', 'ip_cidr', 'hostname', 'gateway', 'role']
        subnet_attrs = ['id', 'site_id', 'subnet_cidr', 'name', 'description']
        
        for attr in site_attrs:
            if hasattr(Site, attr):
                print(f"✅ Site model has attribute: {attr}")
            else:
                print(f"❌ Site model missing attribute: {attr}")
                return False
        
        for attr in ip_attrs:
            if hasattr(IPAddress, attr):
                print(f"✅ IPAddress model has attribute: {attr}")
            else:
                print(f"❌ IPAddress model missing attribute: {attr}")
                return False
        
        for attr in subnet_attrs:
            if hasattr(Subnet, attr):
                print(f"✅ Subnet model has attribute: {attr}")
            else:
                print(f"❌ Subnet model missing attribute: {attr}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database model test failed: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Starting IP Address Tracker Application Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_ip_validation,
        test_css_generation,
        test_database_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

