from app.db.models import Organization


def convert_organization_for_responce(organization_db: Organization | list[Organization]) -> dict | None:
    if type(organization_db) == list:
        return [{
            "id": organization.id,
            "name": organization.organization_name,
            "building": organization.organization_building.address,
            "activities": [act.name for act in organization.organization_activities],
        } for organization in organization_db]
    return {
        "id": organization_db.id,
        "name": organization_db.organization_name,
        "building": organization_db.organization_building.address,
        "activities": [act.name for act in organization_db.organization_activities],
    } if organization_db else None