# IP Address Tracker (IPDB)

A comprehensive IP address tracking and management system built with Streamlit, featuring a dark mode interface with orange theming, PostgreSQL database integration, and Docker/Podman deployment support.

**Repository**: https://github.com/CaptainASIC/IPDB

## 🌟 Features

- **🌐 IP Address Management**: Track and manage IP addresses across multiple network sites
- **🏢 Site Management**: Organize IP addresses by physical locations or network sites
- **🔗 Subnet Management**: Define and manage network subnets with VLAN support
- **🔍 Advanced Search**: Search by IP address, hostname, role, or owner with filtering options
- **📥 Import/Export**: Bulk operations with CSV files including validation and templates
- **📊 Analytics Dashboard**: Visual insights into network utilization and IP allocation
- **🎨 Dark Mode UI**: Modern dark theme with orange accents and smooth animations
- **🐳 Container Ready**: Docker and Podman deployment configurations included
- **🔒 RFC-1918 Compliance**: Enforces private IP address ranges with CIDR notation

## 🚀 Quick Start

### Prerequisites

- Docker or Podman
- Git (for cloning the repository)

### Deployment Options

#### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/CaptainASIC/IPDB.git
cd IPDB

# Deploy with Docker
./scripts/docker-deploy.sh
```

#### Option 2: Podman Deployment

```bash
# Clone the repository
git clone https://github.com/CaptainASIC/IPDB.git
cd IPDB

# Deploy with Podman
./scripts/podman-deploy.sh
```

#### Option 3: Local Development

```bash
# Clone the repository
git clone https://github.com/CaptainASIC/IPDB.git
cd IPDB

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run the application
cd app
streamlit run main.py
```

## 📋 Application Structure

```
ip-tracker/
├── app/                          # Main application code
│   ├── components/               # UI components and styling
│   │   ├── enhanced_styles.py    # Advanced CSS with animations
│   │   └── __init__.py
│   ├── models/                   # Database models
│   │   ├── database.py           # SQLAlchemy models and connection
│   │   └── __init__.py
│   ├── pages/                    # Streamlit pages
│   │   ├── dashboard.py          # Main dashboard with metrics
│   │   ├── search.py             # Search and filtering functionality
│   │   ├── settings.py           # Site and IP management
│   │   ├── import_export.py      # CSV import/export features
│   │   └── __init__.py
│   ├── utils/                    # Utility functions
│   │   ├── import_export.py      # Import/export logic and validation
│   │   └── __init__.py
│   └── main.py                   # Main Streamlit application
├── database/                     # Database configuration
│   ├── schema.sql                # Database schema definition
│   └── seeds/
│       └── sample_data.sql       # Sample data for testing
├── scripts/                      # Deployment scripts
│   ├── docker-deploy.sh          # Docker deployment script
│   └── podman-deploy.sh          # Podman deployment script
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Docker image definition
├── Dockerfile.podman             # Podman-specific Dockerfile
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── test_app.py                   # Application test suite
```

## 🎯 Key Features

### Dashboard
- **Network Overview**: Total IPs, active devices, sites, and subnets
- **Visual Analytics**: Charts showing IP distribution and subnet utilization
- **Recent Activity**: Latest IP address additions and modifications
- **Quick Stats**: Real-time metrics with color-coded status indicators

### Search & Browse
- **Advanced Search**: Multi-criteria search with IP, hostname, role, and owner filters
- **Site Filtering**: Filter results by specific sites or view all
- **Export Results**: Download search results as CSV files
- **Detailed Views**: Expandable details for each IP address entry

### Settings & Administration
- **Site Management**: Add, edit, and delete network sites
- **Subnet Configuration**: Define network subnets with VLAN support
- **IP Assignment**: Manual IP address assignment with validation
- **Bulk Operations**: Import/export functionality for large datasets

### Import/Export
- **CSV Import**: Bulk upload with data validation and error reporting
- **Template Downloads**: Pre-formatted CSV templates for easy data entry
- **Export Options**: Download data filtered by site or export all
- **Data Validation**: RFC-1918 compliance checking and format validation

## 🔧 Configuration

### Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql://iptracker:iptracker123@postgres:5432/iptracker
POSTGRES_DB=iptracker
POSTGRES_USER=iptracker
POSTGRES_PASSWORD=iptracker123

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_THEME_BASE=dark
STREAMLIT_THEME_PRIMARY_COLOR=#FF6B35

# Application Configuration
APP_NAME=IP Address Tracker
APP_VERSION=1.0.0
DEBUG=false
```

### Database Schema

The application uses PostgreSQL with the following main tables:

- **sites**: Network sites/locations
- **ip_addresses**: IP address records with CIDR notation
- **subnets**: Network subnet definitions

All IP addresses are stored in CIDR notation following RFC-1918 standards.

## 📊 Data Import Format

### IP Addresses CSV Format

```csv
site_name,ip_address,hostname,gateway,role,system_owner,description,status
Headquarters,192.168.1.10,server-01,192.168.1.1,Server,IT Team,Main server,active
Branch Office,192.168.10.20,workstation-05,192.168.10.1,Workstation,John Doe,User workstation,active
```

### Sites CSV Format

```csv
name,description,location
Headquarters,Main office location,New York NY
Branch Office,Secondary office,Los Angeles CA
```

### Subnets CSV Format

```csv
site_name,subnet_cidr,name,description,vlan_id
Headquarters,192.168.1.0/24,HQ-LAN,Headquarters LAN,10
Branch Office,192.168.10.0/24,BRANCH-LAN,Branch office LAN,20
```

## 🧪 Testing

Run the included test suite to verify application functionality:

```bash
python3 test_app.py
```

The test suite validates:
- Module imports and dependencies
- IP address validation logic
- CSS generation and styling
- Database model definitions

## 🐳 Docker Configuration

### Services

- **postgres**: PostgreSQL 15 database with automatic schema initialization
- **app**: Streamlit application with health checks and auto-restart

### Volumes

- **postgres_data**: Persistent database storage
- **app**: Application code (development mode)

### Networks

- **ip-tracker-network**: Isolated bridge network for service communication

## 🔒 Security Features

- **RFC-1918 Compliance**: Only private IP address ranges allowed
- **Input Validation**: Comprehensive validation for all user inputs
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **Container Security**: Non-root user execution in containers

## 📱 User Interface

### Design Features

- **Dark Mode**: Professional dark theme with orange accents
- **Responsive Design**: Works on desktop and mobile devices
- **Smooth Animations**: Hover effects and micro-interactions
- **Accessibility**: Proper focus indicators and keyboard navigation
- **Modern Typography**: Inter font family for improved readability

### Color Scheme

- **Primary**: #FF6B35 (Orange)
- **Secondary**: #FF8C42 (Light Orange)
- **Accent**: #FFA500 (Gold)
- **Background**: #0F0F0F (Dark)
- **Text**: #FFFFFF (White)

## 🚀 Performance

- **Lazy Loading**: Efficient data loading with pagination
- **Caching**: Streamlit caching for improved performance
- **Database Indexing**: Optimized queries with proper indexes
- **Responsive UI**: Fast rendering with minimal resource usage

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify PostgreSQL is running
   - Check database credentials in .env file
   - Ensure network connectivity between containers

2. **Import Validation Errors**
   - Download and use provided CSV templates
   - Verify IP addresses are in RFC-1918 ranges
   - Check for duplicate entries

3. **Permission Issues (Podman)**
   - Use the Podman-specific Dockerfile
   - Ensure proper volume mounting permissions
   - Run without --user flag in rootless mode

### Logs

```bash
# Docker logs
docker-compose logs -f

# Podman logs
podman logs -f ip-tracker-app
podman logs -f ip-tracker-db
```

## 📚 API Reference

The application uses SQLAlchemy models for database operations:

### Models

- **Site**: Network site management
- **IPAddress**: IP address tracking with CIDR support
- **Subnet**: Network subnet definitions

### Utilities

- **ImportExportManager**: CSV import/export functionality
- **Enhanced Styles**: Advanced CSS generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For technical support or feature requests:

1. Check the troubleshooting section
2. Review the application logs
3. Create an issue in the repository
4. Contact your system administrator

## 🔄 Version History

### v1.0.0
- Initial release
- Complete IP address tracking functionality
- Dark mode UI with orange theme
- Docker/Podman deployment support
- CSV import/export capabilities
- Advanced search and filtering
- Analytics dashboard

---

**Built with ❤️ using Streamlit, PostgreSQL, and modern web technologies**

