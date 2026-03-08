"""
WAHID Platform - Identity API Router (MVP)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.identity.models import UniversalIdentityModel
from app.identity.universal_identity import UniversalIdentity
from sqlalchemy import select

router = APIRouter()


class CreateIdentityRequest(BaseModel):
    """Request pour créer identité"""
    country_code: str
    phone: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class IdentityResponse(BaseModel):
    """Response identité"""
    did: str
    country_code: str
    status: str
    verification_level: int
    created_at: str


@router.post("/create", response_model=IdentityResponse)
async def create_identity(
    request: CreateIdentityRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Crée une nouvelle identité universelle
    
    Endpoint de test MVP - Version simplifiée
    """
    try:
        # Créer identité
        identity = UniversalIdentity.create_new(
            country_code=request.country_code,
            namespace="wahid"
        )
        
        # Sauvegarder en DB
        db_identity = UniversalIdentityModel(
            did=identity.did,
            user_id=1,  # TODO: User authentifié
            country_code=identity.country_code,
            status=identity.status.value,
            verification_level=identity.verification_level.value,
            public_key=identity.public_key.hex(),
            private_key_encrypted=identity.private_key_encrypted.hex(),
            verifiable_credentials=identity.verifiable_credentials,
            service_endpoints=identity.service_endpoints,
            linked_identities=identity.linked_identities,
            data_residency=identity.data_residency
        )
        
        db.add(db_identity)
        await db.commit()
        await db.refresh(db_identity)
        
        return IdentityResponse(
            did=db_identity.did,
            country_code=db_identity.country_code,
            status=db_identity.status,
            verification_level=db_identity.verification_level,
            created_at=db_identity.created_at.isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating identity: {str(e)}")


@router.get("/resolve/{did}")
async def resolve_did(did: str, db: AsyncSession = Depends(get_db)):
    """Résout un DID"""
    result = await db.execute(
        select(UniversalIdentityModel).where(UniversalIdentityModel.did == did)
    )
    identity = result.scalar_one_or_none()
    
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    
    return {
        "did": identity.did,
        "country_code": identity.country_code,
        "status": identity.status,
        "verification_level": identity.verification_level
    }