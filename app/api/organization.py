from fastapi import APIRouter, Depends, Request, Response, HTTPException

from app.setup.db import DBSessionDep
from app.secure import get_api_key
from app.db.models import Organization, Building, Activity
from app.config.consts import API_VERSION
from app.schemes.geo import GeoSquare
from app.utils.converters import convert_organization_for_responce


org_router = APIRouter()

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

@org_router.get(f'/api/{API_VERSION}/org-by-activity')
async def get_orgs_by_activity(activity_name: str, session: DBSessionDep, api_key: str = Depends(get_api_key)):
    activity_db: Activity = await Activity.get_activity_by_name(session, name=activity_name)
    if not activity_db:
        raise HTTPException(status_code=204, detail="Activity not found")
    organizations_db: list[Organization] = await Organization.get_organizations_by_activity_id(session, activity_id=activity_db.id)
    if organizations_db:
        return convert_organization_for_responce(organizations_db)
    else:
        raise HTTPException(status_code=204, detail="Organization not found")
    
@org_router.get(f'/api/{API_VERSION}/orgs-by-activities')
async def get_orgs_by_activities(activity_name: str, session: DBSessionDep, api_key: str = Depends(get_api_key)):
    activity_db: Activity = await Activity.get_activity_by_name(session, name=activity_name)
    if not activity_db:
        raise HTTPException(status_code=204, detail="Activity not found")
    childs_activity_db: list[Activity] = await Activity.get_childs_activities_by_id(session, id=activity_db.id)
    if not childs_activity_db:
        childs_activity_db = []
    childs_activity_db.append(activity_db) # добавляем деятельность в один список вместе с дочерними
    result = []
    for act in childs_activity_db:
        organizations_db: list[Organization] = await Organization.get_organizations_by_activity_id(session, activity_id=act.id)
        if organizations_db:
            for org in organizations_db: result.append(org)
    if result:
        return convert_organization_for_responce(result)
    else:
        raise HTTPException(status_code=204, detail="Organization not found")
    
@org_router.post(f'/api/{API_VERSION}/orgs-by-geo')
async def get_orgs_by_geo(geo_square: GeoSquare, session: DBSessionDep, api_key: str = Depends(get_api_key)):
    print(geo_square)
    if not GeoSquare.check_valid_geo_square(geo_square):
        raise HTTPException(status_code=422, detail="Invalid geo square") 
    buildins_db: list[Building] = await Building.get_building_by_geo_square(session, geo_square)
    if not buildins_db:
        raise HTTPException(status_code=204, detail="Building not found")
    organizations_db = []
    for building in buildins_db:
        organization_db: Organization = await Organization.get_organization_by_building_id(session, building_id=building.id)
        if organization_db:
            organizations_db.append(organization_db)
    if organizations_db:
        return convert_organization_for_responce(organizations_db)
    else:
        raise HTTPException(status_code=204, detail="Organization not found")