-- Sample data for IP Tracker
-- Using RFC-1918 private IP address ranges

-- Insert sample sites
INSERT INTO sites (name, description, location) VALUES 
('Headquarters', 'Main office location', 'New York, NY'),
('Branch Office', 'Secondary office location', 'Los Angeles, CA'),
('Data Center', 'Primary data center', 'Chicago, IL'),
('Remote Site', 'Remote work location', 'Austin, TX');

-- Insert sample subnets
INSERT INTO subnets (site_id, subnet_cidr, name, description, vlan_id) VALUES 
(2, '192.168.1.0/24', 'HQ-LAN', 'Headquarters LAN network', 10),
(2, '192.168.2.0/24', 'HQ-DMZ', 'Headquarters DMZ network', 20),
(3, '192.168.10.0/24', 'BRANCH-LAN', 'Branch office LAN network', 10),
(4, '10.0.1.0/24', 'DC-SERVERS', 'Data center server network', 100),
(4, '10.0.2.0/24', 'DC-STORAGE', 'Data center storage network', 200),
(5, '172.16.1.0/24', 'REMOTE-VPN', 'Remote VPN access network', 300);

-- Insert sample IP addresses with CIDR notation (/32 for single hosts)
INSERT INTO ip_addresses (site_id, ip_cidr, hostname, gateway, role, system_owner, description, status) VALUES 
-- Headquarters
(2, '192.168.1.1/32', 'hq-gw-01', '192.168.1.1', 'Gateway', 'Network Team', 'Main gateway router', 'active'),
(2, '192.168.1.10/32', 'hq-dc-01', '192.168.1.1', 'Domain Controller', 'IT Team', 'Primary domain controller', 'active'),
(2, '192.168.1.11/32', 'hq-dc-02', '192.168.1.1', 'Domain Controller', 'IT Team', 'Secondary domain controller', 'active'),
(2, '192.168.1.20/32', 'hq-file-01', '192.168.1.1', 'File Server', 'IT Team', 'Main file server', 'active'),
(2, '192.168.1.30/32', 'hq-print-01', '192.168.1.1', 'Print Server', 'IT Team', 'Network printer server', 'active'),
(2, '192.168.2.10/32', 'hq-web-01', '192.168.2.1', 'Web Server', 'Dev Team', 'Public web server', 'active'),
(2, '192.168.2.11/32', 'hq-mail-01', '192.168.2.1', 'Mail Server', 'IT Team', 'Exchange mail server', 'active'),

-- Branch Office
(3, '192.168.10.1/32', 'branch-gw-01', '192.168.10.1', 'Gateway', 'Network Team', 'Branch gateway router', 'active'),
(3, '192.168.10.10/32', 'branch-dc-01', '192.168.10.1', 'Domain Controller', 'IT Team', 'Branch domain controller', 'active'),
(3, '192.168.10.20/32', 'branch-file-01', '192.168.10.1', 'File Server', 'IT Team', 'Branch file server', 'active'),

-- Data Center
(4, '10.0.1.1/32', 'dc-gw-01', '10.0.1.1', 'Gateway', 'Network Team', 'Data center gateway', 'active'),
(4, '10.0.1.10/32', 'dc-sql-01', '10.0.1.1', 'Database Server', 'DBA Team', 'Primary SQL server', 'active'),
(4, '10.0.1.11/32', 'dc-sql-02', '10.0.1.1', 'Database Server', 'DBA Team', 'Secondary SQL server', 'active'),
(4, '10.0.1.20/32', 'dc-app-01', '10.0.1.1', 'Application Server', 'Dev Team', 'Production app server', 'active'),
(4, '10.0.1.21/32', 'dc-app-02', '10.0.1.1', 'Application Server', 'Dev Team', 'Staging app server', 'active'),
(4, '10.0.2.10/32', 'dc-san-01', '10.0.2.1', 'Storage', 'Storage Team', 'Primary SAN controller', 'active'),
(4, '10.0.2.11/32', 'dc-san-02', '10.0.2.1', 'Storage', 'Storage Team', 'Secondary SAN controller', 'active'),

-- Remote Site
(5, '172.16.1.1/32', 'remote-gw-01', '172.16.1.1', 'Gateway', 'Network Team', 'Remote VPN gateway', 'active'),
(5, '172.16.1.10/32', 'remote-laptop-01', '172.16.1.1', 'Workstation', 'John Doe', 'Remote worker laptop', 'active'),
(5, '172.16.1.11/32', 'remote-laptop-02', '172.16.1.1', 'Workstation', 'Jane Smith', 'Remote worker laptop', 'active'),

-- Reserved addresses
(2, '192.168.1.100/32', NULL, '192.168.1.1', 'Reserved', 'Network Team', 'Reserved for future use', 'reserved'),
(3, '192.168.10.100/32', NULL, '192.168.10.1', 'Reserved', 'Network Team', 'Reserved for future use', 'reserved'),
(4, '10.0.1.100/32', NULL, '10.0.1.1', 'Reserved', 'Network Team', 'Reserved for future use', 'reserved');

