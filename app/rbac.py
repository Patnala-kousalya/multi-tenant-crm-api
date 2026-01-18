from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter()


def require_role(current_user, allowed_roles: list):
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )


@router.post("/", response_model=schemas.ContactOut)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    require_role(current_user, ["owner", "member"])

    new_contact = models.Contact(
        name=contact.name,
        email=contact.email,
        organization_id=current_user.organization_id
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.get("/", response_model=list[schemas.ContactOut])
def list_contacts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    require_role(current_user, ["owner", "member", "viewer"])

    return db.query(models.Contact).filter(
        models.Contact.organization_id == current_user.organization_id
    ).all()
