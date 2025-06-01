"""
Database models for IP Tracker application
Using SQLAlchemy ORM with PostgreSQL CIDR support
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import CIDR, INET
from sqlalchemy.sql import func
from datetime import datetime
import os

Base = declarative_base()

class Site(Base):
    """Sites table model"""
    __tablename__ = 'sites'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    location = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    ip_addresses = relationship("IPAddress", back_populates="site", cascade="all, delete-orphan")
    subnets = relationship("Subnet", back_populates="site", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Site(id={self.id}, name='{self.name}', location='{self.location}')>"

class IPAddress(Base):
    """IP addresses table model with CIDR support"""
    __tablename__ = 'ip_addresses'
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id', ondelete='CASCADE'))
    ip_cidr = Column(CIDR, nullable=False)
    hostname = Column(String(255))
    gateway = Column(INET)
    role = Column(String(100))
    system_owner = Column(String(100))
    description = Column(Text)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive', 'reserved')", name='check_status'),
    )
    
    # Relationships
    site = relationship("Site", back_populates="ip_addresses")
    
    def __repr__(self):
        return f"<IPAddress(id={self.id}, ip_cidr='{self.ip_cidr}', hostname='{self.hostname}')>"

class Subnet(Base):
    """Subnets table model"""
    __tablename__ = 'subnets'
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id', ondelete='CASCADE'))
    subnet_cidr = Column(CIDR, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    vlan_id = Column(Integer)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    site = relationship("Site", back_populates="subnets")
    
    def __repr__(self):
        return f"<Subnet(id={self.id}, subnet_cidr='{self.subnet_cidr}', name='{self.name}')>"

class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self, database_url=None):
        if database_url is None:
            # Default connection string for Docker environment
            database_url = os.getenv(
                'DATABASE_URL',
                'postgresql://iptracker:iptracker123@localhost:5432/iptracker'
            )
        
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Close database session"""
        session.close()

# Global database manager instance
db_manager = DatabaseManager()

def get_db_session():
    """Get database session for use in application"""
    return db_manager.get_session()

def init_database():
    """Initialize database tables"""
    db_manager.create_tables()

