# IPDB User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Managing Sites](#managing-sites)
4. [IP Address Management](#ip-address-management)
5. [Subnet Configuration](#subnet-configuration)
6. [Search and Filtering](#search-and-filtering)
7. [Import and Export](#import-and-export)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Getting Started

### First Login

When you first access IPDB, you'll see the main dashboard with sample data. The application is designed to be intuitive, but this guide will help you get the most out of all features.

### Navigation

The application uses a sidebar navigation system with the following main sections:

- **🏠 Dashboard**: Overview of your network infrastructure
- **🔍 Search & Browse**: Find and explore IP addresses
- **📊 Analytics**: Network utilization and statistics
- **⚙️ Settings**: Manage sites, subnets, and IP addresses
- **📥 Import/Export**: Bulk data operations
- **📚 Help**: Documentation and support

### Top Navigation Bar

At the top of every page, you'll find:

- **Site Selector**: Choose a specific site or "ALL" to view all sites
- **Search Bar**: Quick search for IP addresses or hostnames
- **Search Button**: Execute the search query

## Dashboard Overview

The dashboard provides a comprehensive view of your network infrastructure with real-time metrics and visualizations.

### Key Metrics

The dashboard displays four main metrics:

1. **Total IPs**: Complete count of all IP addresses in the system
2. **Active IPs**: Number of currently active IP addresses
3. **Sites**: Total number of configured network sites
4. **Subnets**: Total number of defined network subnets

### Visualizations

#### IP Distribution by Site
A pie chart showing how IP addresses are distributed across different sites. This helps identify which locations have the most network resources.

#### IP Status Distribution
A bar chart displaying the breakdown of IP addresses by status (active, inactive, reserved). This provides insight into network utilization.

#### Recent Activity
A table showing the most recently added IP addresses, including their hostnames, sites, and creation timestamps.

#### Subnet Utilization
A horizontal bar chart showing the percentage utilization of each subnet. This helps identify subnets that are approaching capacity.

## Managing Sites

Sites represent physical locations or logical groupings of network resources.

### Adding a New Site

1. Navigate to **⚙️ Settings** in the sidebar
2. Select the **🏢 Sites** tab
3. Click **➕ Add New Site** to expand the form
4. Fill in the required information:
   - **Site Name**: Unique identifier for the site
   - **Location**: Physical address or description
   - **Description**: Brief explanation of the site's purpose
5. Click **Add Site** to save

### Editing Sites

1. In the Sites tab, find the site you want to edit
2. Click the **✏️ Edit** button next to the site
3. Modify the information in the form that appears
4. Click **Save Changes** to update the site

### Deleting Sites

1. Locate the site in the Sites tab
2. Click the **🗑️ Delete** button
3. **Note**: Sites with existing IP addresses cannot be deleted

## IP Address Management

IPDB follows RFC-1918 standards and requires all IP addresses to be in private ranges.

### Adding IP Addresses

1. Go to **⚙️ Settings** → **🌐 IP Addresses** tab
2. Click **➕ Add New IP Address**
3. Fill in the form:
   - **Site**: Select from existing sites
   - **IP Address**: Enter the IP (will auto-add /32 for single IPs)
   - **Hostname**: Optional but recommended
   - **Gateway**: Default gateway for this IP
   - **Role**: Purpose of the device (Server, Workstation, etc.)
   - **System Owner**: Person or team responsible
   - **Status**: active, inactive, or reserved
   - **Description**: Additional details
4. Click **Add IP Address**

### IP Address Validation

IPDB automatically validates IP addresses to ensure:

- Proper IP format
- RFC-1918 compliance (private IP ranges only)
- CIDR notation (adds /32 for single IPs)
- No duplicates within the same site

### Supported IP Ranges

- **Class A**: 10.0.0.0 to 10.255.255.255
- **Class B**: 172.16.0.0 to 172.31.255.255
- **Class C**: 192.168.0.0 to 192.168.255.255

## Subnet Configuration

Subnets help organize your network into logical segments.

### Adding Subnets

1. Navigate to **⚙️ Settings** → **🔗 Subnets** tab
2. Click **➕ Add New Subnet**
3. Complete the form:
   - **Site**: Choose the associated site
   - **Subnet CIDR**: Network address in CIDR notation (e.g., 192.168.1.0/24)
   - **Subnet Name**: Descriptive name (e.g., "LAN-Network")
   - **Description**: Purpose or details about the subnet
   - **VLAN ID**: Optional VLAN identifier (1-4094)
4. Click **Add Subnet**

### Subnet Utilization

The system automatically calculates subnet utilization by:

- Counting IP addresses within each subnet
- Calculating total subnet capacity
- Displaying utilization percentage
- Color-coding based on usage levels

## Search and Filtering

IPDB provides powerful search capabilities to quickly find network resources.

### Quick Search

Use the search bar at the top of any page to search for:

- IP addresses (exact or partial matches)
- Hostnames
- Descriptions
- Roles
- System owners

### Advanced Search

In the **🔍 Search & Browse** section, you can use advanced filters:

1. **Status Filter**: Filter by active, inactive, or reserved
2. **Role Filter**: Search by device role
3. **Owner Filter**: Find devices by system owner
4. **Site Filter**: Limit results to specific sites

### Search Results

Search results display in a comprehensive table with:

- Site name
- IP address in CIDR notation
- Hostname
- Gateway
- Role and system owner
- Description and status
- Creation and update timestamps

### Exporting Search Results

1. Perform your search with desired filters
2. Click **📥 Export Results**
3. Download the CSV file with your filtered data

## Import and Export

IPDB supports bulk operations through CSV files for efficient data management.

### Downloading Templates

1. Go to **📥 Import/Export** → **📋 Templates** tab
2. Choose the data type (IP Addresses, Sites, or Subnets)
3. Click the download button for the appropriate template
4. Use the template as a guide for formatting your data

### Importing Data

1. Prepare your CSV file using the provided templates
2. Navigate to **📥 Import/Export** → **📥 Import Data** tab
3. Select the data type you're importing
4. Upload your CSV file
5. Review the file preview and validation results
6. Click **🚀 Import Data** if validation passes

### Data Validation

The import process validates:

- Required columns are present
- IP addresses are properly formatted
- RFC-1918 compliance
- No duplicate entries
- Valid hostnames and other fields

### Exporting Data

1. Go to **📥 Import/Export** → **📤 Export Data** tab
2. Select the data type to export
3. Choose site filter if needed
4. Click **👀 Preview Export Data** to review
5. Click **📥 Export Data** to generate the download

## Best Practices

### IP Address Management

- Always use descriptive hostnames
- Keep system owner information current
- Use consistent naming conventions
- Regularly review and update IP status
- Document the purpose of each IP in the description field

### Site Organization

- Create sites based on physical locations or logical boundaries
- Use clear, descriptive site names
- Keep location information accurate and detailed
- Regularly review site configurations

### Subnet Planning

- Plan subnet sizes based on growth projections
- Use consistent VLAN numbering schemes
- Document subnet purposes clearly
- Monitor utilization regularly

### Data Management

- Perform regular exports for backup purposes
- Use import templates to ensure data consistency
- Validate data before importing
- Keep historical records of network changes

## Troubleshooting

### Common Issues

#### Import Validation Errors

**Problem**: CSV import fails validation
**Solution**: 
- Download and use the provided templates
- Ensure all required columns are present
- Verify IP addresses are in RFC-1918 ranges
- Check for duplicate entries

#### IP Address Not Accepted

**Problem**: IP address rejected during entry
**Solution**:
- Ensure IP is in private range (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
- Check for proper IP format
- Verify no duplicate exists for the same site

#### Search Returns No Results

**Problem**: Search doesn't find expected results
**Solution**:
- Check spelling and formatting
- Try partial matches instead of exact
- Verify the correct site is selected
- Use advanced filters to narrow search

#### Cannot Delete Site

**Problem**: Site deletion fails
**Solution**:
- Remove all IP addresses associated with the site first
- Delete any subnets associated with the site
- Then attempt to delete the site

### Performance Issues

If the application seems slow:

- Check your internet connection
- Refresh the browser page
- Clear browser cache
- Contact your system administrator

### Data Recovery

For data recovery needs:

- Use the export function to create backups
- Contact your system administrator
- Check if automatic backups are available

### Getting Help

For additional support:

1. Check this user guide
2. Review the application's help section
3. Contact your system administrator
4. Submit issues to the GitHub repository

---

**Remember**: IPDB is designed to be intuitive and user-friendly. Don't hesitate to explore the interface and experiment with different features in a test environment.

