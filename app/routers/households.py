from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import (
    Household,
    HouseholdCreate,
    HouseholdRead,
    HouseholdUpdate,
    HouseholdWithMembersCreate,
    Member,
    MemberBase,
    MemberCreate,
    MemberUpdate,
)

router = APIRouter(prefix="/households", tags=["households"])


@router.post("/", response_model=HouseholdRead)
def create_household(
    household_data: HouseholdWithMembersCreate, session: Session = Depends(get_session)
):
    """Create a household with members in a single transaction."""
    # Create the household
    household = Household(name=household_data.name, address=household_data.address)
    session.add(household)
    session.flush()  # Flush to get the household ID

    # Create all members
    for member_data in household_data.members:
        if member_data.first_name or member_data.last_name:  # Skip empty members
            member = Member(
                household_id=household.id,
                first_name=member_data.first_name,
                last_name=member_data.last_name,
                email=member_data.email,
                phone=member_data.phone,
            )
            session.add(member)

    session.commit()
    session.refresh(household)
    return household


@router.get("/", response_model=list[HouseholdRead])
def list_households(session: Session = Depends(get_session)):
    """List all households with their members."""
    households = session.exec(select(Household)).all()
    return households


@router.get("/{household_id}", response_model=HouseholdRead)
def get_household(household_id: int, session: Session = Depends(get_session)):
    """Get a single household with its members."""
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    return household


@router.patch("/{household_id}", response_model=HouseholdRead)
def update_household(
    household_id: int,
    household_update: HouseholdUpdate,
    session: Session = Depends(get_session),
):
    """Update household details (name, address)."""
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
    """Delete a household and all its members."""
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    session.delete(household)
    session.commit()
    return {"message": "Household deleted successfully"}


@router.post("/{household_id}/members", response_model=Member)
def add_member(
    household_id: int, member_data: MemberBase, session: Session = Depends(get_session)
):
    """Add a new member to a household."""
    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    member = Member(
        household_id=household_id,
        first_name=member_data.first_name,
        last_name=member_data.last_name,
        email=member_data.email,
        phone=member_data.phone,
    )
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


@router.patch("/{household_id}/members/{member_id}", response_model=Member)
def update_member(
    household_id: int,
    member_id: int,
    member_update: MemberUpdate,
    session: Session = Depends(get_session),
):
    """Update a member's details."""
    member = session.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if member.household_id != household_id:
        raise HTTPException(status_code=404, detail="Member not found in this household")

    member_data = member_update.model_dump(exclude_unset=True)
    member.sqlmodel_update(member_data)
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


@router.delete("/{household_id}/members/{member_id}")
def remove_member(
    household_id: int, member_id: int, session: Session = Depends(get_session)
):
    """Remove a member from a household."""
    member = session.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if member.household_id != household_id:
        raise HTTPException(status_code=404, detail="Member not found in this household")

    session.delete(member)
    session.commit()
    return {"message": "Member removed successfully"}
