from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Household, HouseholdCreate, HouseholdUpdate, Contact

router = APIRouter(prefix="/households", tags=["households"])


@router.post("/", response_model=Household)
def create_household(household: HouseholdCreate, session: Session = Depends(get_session)):
    db_household = Household.model_validate(household)
    session.add(db_household)
    session.commit()
    session.refresh(db_household)
    return db_household


@router.get("/", response_model=list[Household])
def list_households(session: Session = Depends(get_session)):
    households = session.exec(select(Household)).all()
    return households


@router.get("/{household_id}", response_model=Household)
def get_household(household_id: int, session: Session = Depends(get_session)):
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    return household


@router.patch("/{household_id}", response_model=Household)
def update_household(
    household_id: int, household_update: HouseholdUpdate, session: Session = Depends(get_session)
):
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    household_data = household_update.model_dump(exclude_unset=True)
    household.sqlmodel_update(household_data)
    session.add(household)
    session.commit()
    session.refresh(household)
    return household


@router.delete("/{household_id}")
def delete_household(household_id: int, session: Session = Depends(get_session)):
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    session.delete(household)
    session.commit()
    return {"message": "Household deleted successfully"}


@router.get("/{household_id}/members", response_model=list[Contact])
def get_household_members(household_id: int, session: Session = Depends(get_session)):
    """Get all members of a household"""
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    members = session.exec(select(Contact).where(Contact.household_id == household_id)).all()
    return members


@router.post("/{household_id}/members/{contact_id}")
def add_member_to_household(
    household_id: int, contact_id: int, session: Session = Depends(get_session)
):
    """Add a contact as a member of a household"""
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact.household_id = household_id
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return {"message": "Member added successfully", "contact": contact}


@router.delete("/{household_id}/members/{contact_id}")
def remove_member_from_household(
    household_id: int, contact_id: int, session: Session = Depends(get_session)
):
    """Remove a contact from a household"""
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    if contact.household_id != household_id:
        raise HTTPException(status_code=400, detail="Contact is not a member of this household")

    contact.household_id = None
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return {"message": "Member removed successfully"}
