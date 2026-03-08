"""
WAHID Platform - Identity Models (MVP)
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from datetime import datetime
from app.core.database import Base


class UniversalIdentityModel(Base):
    """Modèle pour identité universelle"""
    
    __tablename__ = "universal_identities"
    
    id = Column(Integer, primary_key=True, index=True)
    did = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Métadonnées
    country_code = Column(String(2), nullable=False)
    status = Column(String(50), default="pending_verification")
    verification_level = Column(Integer, default=0)
    
    # Cryptographie (stocké en hex)
    public_key = Column(String, nullable=False)
    private_key_encrypted = Column(String, nullable=False)
    
    # Données structurées (JSON)
    verifiable_credentials = Column(JSON, default=list)
    service_endpoints = Column(JSON, default=dict)
    linked_identities = Column(JSON, default=dict)
    revocation_registry = Column(JSON, default=list)
    
    # Souveraineté
    data_residency = Column(String(2), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Identity {self.did}>"