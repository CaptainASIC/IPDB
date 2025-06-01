-- IP Tracker Database Schema
-- Following RFC-1918 standards with CIDR notation

-- Sites table to store different network sites/locations
CREATE TABLE sites (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- IP addresses table with CIDR notation support
CREATE TABLE ip_addresses (
    id SERIAL PRIMARY KEY,
    site_id INTEGER REFERENCES sites(id) ON DELETE CASCADE,
    ip_cidr CIDR NOT NULL,
    hostname VARCHAR(255),
    gateway INET,
    role VARCHAR(100),
    system_owner VARCHAR(100),
    description TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'reserved')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ip_cidr, site_id)
);

-- Subnets table for network organization
CREATE TABLE subnets (
    id SERIAL PRIMARY KEY,
    site_id INTEGER REFERENCES sites(id) ON DELETE CASCADE,
    subnet_cidr CIDR NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    vlan_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(subnet_cidr, site_id)
);

-- Indexes for performance
CREATE INDEX idx_ip_addresses_site_id ON ip_addresses(site_id);
CREATE INDEX idx_ip_addresses_ip_cidr ON ip_addresses USING GIST(ip_cidr);
CREATE INDEX idx_ip_addresses_hostname ON ip_addresses(hostname);
CREATE INDEX idx_subnets_site_id ON subnets(site_id);
CREATE INDEX idx_subnets_subnet_cidr ON subnets USING GIST(subnet_cidr);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_sites_updated_at BEFORE UPDATE ON sites
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ip_addresses_updated_at BEFORE UPDATE ON ip_addresses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subnets_updated_at BEFORE UPDATE ON subnets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default site for initial setup
INSERT INTO sites (name, description, location) VALUES 
('Default', 'Default site for unassigned IP addresses', 'Unknown');

