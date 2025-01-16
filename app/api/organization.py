from fastapi import APIRouter, Depends, Request, Response, HTTPException

from app.setup.db import DBSessionDep
from app.secure import get_api_key
from app.db.models import Organization, Building
from app.config.consts import API_VERSION


org_router = APIRouter()

def convert_organization_for_responce(organization_db: Organization):
    return {
        "id": organization_db.id,
        "name": organization_db.organization_name,
        "building": organization_db.organization_building.address,
        "activities": [act.name for act in organization_db.organization_activities],
    } if organization_db else None


@org_router.get(f'/api/{API_VERSION}/org-info-by-id')
async def get_org_info_by_id(organization_id: int, session: DBSessionDep, api_key: str = Depends(get_api_key)):
    organization_db: Organization = await Organization.get_organization_by_id(session, id=organization_id)
    if organization_db:
        return convert_organization_for_responce(organization_db)
    else:
        raise HTTPException(status_code=204, detail="Organization not found")

@org_router.get(f'/api/{API_VERSION}/org-info-by-name')
async def get_org_info_by_name(organization_name: str, session: DBSessionDep, api_key: str = Depends(get_api_key)):
    organization_db: Organization = await Organization.get_organization_by_name(session, name=organization_name)
    if organization_db:
        return convert_organization_for_responce(organization_db)
    else:
        raise HTTPException(status_code=204, detail="Organization not found")

@org_router.get(f'/api/{API_VERSION}/org-info-by-address')
async def get_orgs_by_buildings(building_address: str, session: DBSessionDep, api_key: str = Depends(get_api_key)):
    building_db: Building = await Building.get_building_by_address(session, address=building_address)
    if not building_db:
        raise HTTPException(status_code=204, detail="Building not found")
    organization_db: Organization = await Organization.get_organization_by_building_id(session, building_id=building_db.id)
    if organization_db:
        return convert_organization_for_responce(organization_db)
    else:
        raise HTTPException(status_code=204, detail="Organization not found")

