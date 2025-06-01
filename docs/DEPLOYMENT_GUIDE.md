# IPDB Deployment Guide

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-deployment Checklist](#pre-deployment-checklist)
3. [Docker Deployment](#docker-deployment)
4. [Podman Deployment](#podman-deployment)
5. [Production Deployment](#production-deployment)
6. [Security Considerations](#security-considerations)
7. [Backup and Recovery](#backup-and-recovery)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB available space
- **Network**: Internet access for initial setup
- **OS**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows with WSL2

### Recommended Requirements

- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 50GB available space (SSD preferred)
- **Network**: Stable internet connection
- **OS**: Ubuntu 22.04 LTS or newer

### Software Dependencies

#### For Docker Deployment
- Docker Engine 20.10+
- Docker Compose 2.0+

#### For Podman Deployment
- Podman 3.0+
- Podman Compose (optional)

#### For Local Development
- Python 3.11+
- PostgreSQL 13+
- Git

## Pre-deployment Checklist

Before deploying IPDB, ensure you have:

- [ ] Verified system requirements
- [ ] Installed Docker or Podman
- [ ] Configured firewall rules (if applicable)
- [ ] Planned your network architecture
- [ ] Prepared backup storage location
- [ ] Reviewed security requirements
- [ ] Obtained necessary access credentials

## Docker Deployment

### Quick Start

```bash
# Clone the repository
git clone https://github.com/CaptainASIC/IPDB.git
cd IPDB

# Run the deployment script
./scripts/docker-deploy.sh
```

### Manual Docker Deployment

If you prefer manual control over the deployment process:

```bash
# Clone the repository
git clone https://github.com/CaptainASIC/IPDB.git
cd IPDB

# Create environment file
cp .env.example .env

# Edit environment variables (optional)
nano .env

# Build and start services
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### Docker Configuration

#### Environment Variables

Edit the `.env` file to customize your deployment:

```bash
# Database Configuration
POSTGRES_DB=iptracker
POSTGRES_USER=iptracker
POSTGRES_PASSWORD=your_secure_password_here

# Application Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Security (for production)
DEBUG=false
```

#### Port Configuration

By default, IPDB uses the following ports:

- **8501**: Streamlit web interface
- **5432**: PostgreSQL database (internal)

To change the web interface port, modify `docker-compose.yml`:

```yaml
services:
  app:
    ports:
      - "8080:8501"  # Change 8080 to your desired port
```

#### Volume Configuration

Data persistence is handled through Docker volumes:

- **postgres_data**: Database storage
- **./app**: Application code (development mode)

For production, consider using named volumes or bind mounts to specific directories.

### Docker Health Checks

The deployment includes health checks for both services:

- **PostgreSQL**: Checks database connectivity
- **Streamlit**: Checks web interface availability

Monitor health status with:

```bash
docker-compose ps
```

## Podman Deployment

### Quick Start

```bash
# Clone the repository
git clone https://github.com/CaptainASIC/IPDB.git
cd IPDB

# Run the Podman deployment script
./scripts/podman-deploy.sh
```

### Manual Podman Deployment

For manual control over Podman deployment:

```bash
# Clone the repository
git clone https://github.com/CaptainASIC/IPDB.git
cd IPDB

# Create environment file
cp .env.example .env

# Create Podman network
podman network create ipdb-network

# Create volume for database
podman volume create postgres_data

# Start PostgreSQL container
podman run -d \
  --name ipdb-postgres \
  --network ipdb-network \
  -e POSTGRES_DB=iptracker \
  -e POSTGRES_USER=iptracker \
  -e POSTGRES_PASSWORD=iptracker123 \
  -v postgres_data:/var/lib/postgresql/data \
  -v ./database/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql:Z \
  -v ./database/seeds/sample_data.sql:/docker-entrypoint-initdb.d/02-sample_data.sql:Z \
  -p 5432:5432 \
  postgres:15-alpine

# Build application image
podman build -f Dockerfile.podman -t ipdb-app .

# Start application container
podman run -d \
  --name ipdb-app \
  --network ipdb-network \
  -e DATABASE_URL=postgresql://iptracker:iptracker123@ipdb-postgres:5432/iptracker \
  -p 8501:8501 \
  ipdb-app
```

### Podman-specific Considerations

#### Rootless Mode

Podman runs in rootless mode by default, which provides better security but requires special considerations:

- Use the `Dockerfile.podman` which sets proper permissions
- Volume mounts use the `:Z` flag for SELinux compatibility
- No `--user` flag needed in rootless mode

#### Systemd Integration

For production deployments, consider using Podman with systemd:

```bash
# Generate systemd unit files
podman generate systemd --new --files --name ipdb-postgres
podman generate systemd --new --files --name ipdb-app

# Move unit files to systemd directory
sudo mv *.service /etc/systemd/system/

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable --now container-ipdb-postgres.service
sudo systemctl enable --now container-ipdb-app.service
```

## Production Deployment

### Security Hardening

#### Database Security

1. **Change Default Passwords**:
   ```bash
   # Generate strong password
   openssl rand -base64 32
   
   # Update .env file
   POSTGRES_PASSWORD=your_generated_password
   ```

2. **Restrict Database Access**:
   - Remove external port mapping for PostgreSQL
   - Use internal Docker/Podman networks only

3. **Enable SSL/TLS**:
   Configure PostgreSQL with SSL certificates for encrypted connections.

#### Application Security

1. **Disable Debug Mode**:
   ```bash
   DEBUG=false
   ```

2. **Use HTTPS**:
   Deploy behind a reverse proxy (nginx, Apache, or Traefik) with SSL certificates.

3. **Firewall Configuration**:
   ```bash
   # Allow only necessary ports
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw deny 8501/tcp  # Block direct access
   ```

### Reverse Proxy Configuration

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Traefik Configuration

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v2.9
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=your-email@domain.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./acme.json:/acme.json

  app:
    build: .
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ipdb.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.ipdb.entrypoints=websecure"
      - "traefik.http.routers.ipdb.tls.certresolver=letsencrypt"
```

### Performance Optimization

#### Database Optimization

1. **Connection Pooling**:
   Configure PostgreSQL connection pooling for better performance.

2. **Index Optimization**:
   The schema includes optimized indexes, but monitor query performance.

3. **Regular Maintenance**:
   ```sql
   -- Run weekly
   VACUUM ANALYZE;
   
   -- Run monthly
   REINDEX DATABASE iptracker;
   ```

#### Application Optimization

1. **Resource Limits**:
   ```yaml
   services:
     app:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

2. **Caching**:
   Streamlit includes built-in caching, but consider Redis for larger deployments.

## Backup and Recovery

### Database Backup

#### Automated Backup Script

```bash
#!/bin/bash
# backup-ipdb.sh

BACKUP_DIR="/backup/ipdb"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="ipdb-postgres"

# Create backup directory
mkdir -p $BACKUP_DIR

# Perform database backup
docker exec $CONTAINER_NAME pg_dump -U iptracker iptracker > $BACKUP_DIR/ipdb_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/ipdb_backup_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: ipdb_backup_$DATE.sql.gz"
```

#### Scheduled Backups

```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /path/to/backup-ipdb.sh
```

### Recovery Procedures

#### Database Recovery

```bash
# Stop the application
docker-compose down

# Start only the database
docker-compose up -d postgres

# Restore from backup
gunzip -c /backup/ipdb/ipdb_backup_YYYYMMDD_HHMMSS.sql.gz | \
docker exec -i ipdb-postgres psql -U iptracker -d iptracker

# Start the full application
docker-compose up -d
```

#### Application Recovery

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Monitoring and Maintenance

### Health Monitoring

#### Docker Health Checks

```bash
# Check container health
docker-compose ps

# View detailed health status
docker inspect ipdb-app | grep -A 10 Health
```

#### Application Monitoring

```bash
# Monitor application logs
docker-compose logs -f app

# Monitor database logs
docker-compose logs -f postgres

# Monitor resource usage
docker stats
```

### Log Management

#### Log Rotation

```bash
# Configure Docker log rotation
cat > /etc/docker/daemon.json << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

# Restart Docker
sudo systemctl restart docker
```

#### Centralized Logging

For production environments, consider using:

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Grafana + Loki**
- **Fluentd**

### Performance Monitoring

#### Database Performance

```sql
-- Monitor slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Monitor database size
SELECT pg_size_pretty(pg_database_size('iptracker'));

-- Monitor connection count
SELECT count(*) FROM pg_stat_activity;
```

#### Application Performance

Monitor key metrics:

- Response time
- Memory usage
- CPU utilization
- Database connection pool status

### Regular Maintenance Tasks

#### Weekly Tasks

- [ ] Review application logs
- [ ] Check database backup integrity
- [ ] Monitor disk space usage
- [ ] Review security logs

#### Monthly Tasks

- [ ] Update container images
- [ ] Review and rotate logs
- [ ] Performance analysis
- [ ] Security audit

#### Quarterly Tasks

- [ ] Full system backup test
- [ ] Disaster recovery drill
- [ ] Security assessment
- [ ] Capacity planning review

## Troubleshooting

### Common Issues

#### Container Won't Start

**Symptoms**: Container exits immediately or fails to start

**Diagnosis**:
```bash
# Check container logs
docker-compose logs app

# Check container status
docker-compose ps
```

**Solutions**:
- Verify environment variables
- Check port conflicts
- Ensure sufficient disk space
- Review Docker/Podman logs

#### Database Connection Failed

**Symptoms**: Application can't connect to database

**Diagnosis**:
```bash
# Test database connectivity
docker exec ipdb-postgres pg_isready -U iptracker

# Check database logs
docker-compose logs postgres
```

**Solutions**:
- Verify database credentials
- Check network connectivity
- Ensure database is fully started
- Review firewall settings

#### Performance Issues

**Symptoms**: Slow response times or high resource usage

**Diagnosis**:
```bash
# Monitor resource usage
docker stats

# Check database performance
docker exec ipdb-postgres psql -U iptracker -d iptracker -c "SELECT * FROM pg_stat_activity;"
```

**Solutions**:
- Increase resource limits
- Optimize database queries
- Review application logs
- Consider scaling options

### Emergency Procedures

#### Service Recovery

```bash
# Quick restart
docker-compose restart

# Full rebuild
docker-compose down
docker-compose up -d --build

# Emergency database recovery
docker-compose down
docker volume rm ipdb_postgres_data
# Restore from backup
```

#### Data Recovery

```bash
# Export current data
docker exec ipdb-app python3 -c "
from utils.import_export import import_export_manager
data = import_export_manager.export_data_to_csv('ip_addresses')
with open('/tmp/emergency_export.csv', 'wb') as f:
    f.write(data)
"

# Copy from container
docker cp ipdb-app:/tmp/emergency_export.csv ./emergency_backup.csv
```

### Getting Support

For additional support:

1. **Check Documentation**: Review this guide and the README
2. **Search Issues**: Check the GitHub repository for similar issues
3. **Create Issue**: Submit a detailed issue report with logs
4. **Community Support**: Engage with the community on GitHub

### Support Information Template

When requesting support, include:

```
**Environment**:
- OS: [Ubuntu 22.04, etc.]
- Container Runtime: [Docker/Podman version]
- IPDB Version: [git commit hash]

**Issue Description**:
[Detailed description of the problem]

**Steps to Reproduce**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior**:
[What should happen]

**Actual Behavior**:
[What actually happens]

**Logs**:
```
[Paste relevant logs here]
```

**Additional Context**:
[Any other relevant information]
```

---

**Remember**: Always test deployments in a non-production environment first, and maintain regular backups of your data.

