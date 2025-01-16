from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.exc import NoResultFound

from app.setup.db import DBSessionDep
from app.secure import get_api_key
from app.db.models import Organization

org_router = APIRouter()

@org_router.get('/api/v1/org-info-by-id')
async def get_org_info_by_id(organization_id: int, session: DBSessionDep, api_key: str = Depends(get_api_key)):
    organization_db: Organization = await Organization.get_organization_by_id(session, organization_id=organization_id)
    return {
        "id": organization_db.id,
        "name": organization_db.organization_name,
        "building": organization_db.organization_building.address,
        "activities": [act.name for act in organization_db.organization_activities],
    } if organization_db else None
