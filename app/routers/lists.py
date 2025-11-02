from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models import (
    Household,
    List,
    ListCreate,
    ListHouseholdLink,
    ListRead,
    ListUpdate,
    ListWithHouseholds,
)


class BulkHouseholdsRequest(BaseModel):
    household_ids: list[int]


router = APIRouter(prefix="/lists", tags=["lists"])


@router.post("/", response_model=ListRead)
def create_list(list_data: ListCreate, session: Session = Depends(get_session)):
    """Create a new list."""
    new_list = List.model_validate(list_data)
    session.add(new_list)
    session.commit()
    session.refresh(new_list)

    # Return with household count
    return ListRead(
        id=new_list.id,
        name=new_list.name,
        description=new_list.description,
        household_count=0,
    )


@router.get("/", response_model=list[ListRead])
def list_lists(session: Session = Depends(get_session)):
    """Get all lists with household counts."""
    lists = session.exec(select(List)).all()

    result = []
    for lst in lists:
        household_count = len(lst.households)
        result.append(
            ListRead(
                id=lst.id,
                name=lst.name,
                description=lst.description,
                household_count=household_count,
            )
        )

    return result


@router.get("/{list_id}", response_model=ListWithHouseholds)
def get_list(list_id: int, session: Session = Depends(get_session)):
    """Get a single list with all its households."""
    lst = session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    return lst


@router.patch("/{list_id}", response_model=ListRead)
def update_list(
    list_id: int, list_update: ListUpdate, session: Session = Depends(get_session)
):
    """Update list details (name, description)."""
    lst = session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    list_data = list_update.model_dump(exclude_unset=True)
    lst.sqlmodel_update(list_data)
    session.add(lst)
    session.commit()
    session.refresh(lst)

    return ListRead(
        id=lst.id,
        name=lst.name,
        description=lst.description,
        household_count=len(lst.households),
    )


@router.delete("/{list_id}")
def delete_list(list_id: int, session: Session = Depends(get_session)):
    """Delete a list."""
    lst = session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    session.delete(lst)
    session.commit()
    return {"message": "List deleted successfully"}


@router.post("/{list_id}/households/bulk")
def add_households_to_list(
    list_id: int,
    request: BulkHouseholdsRequest,
    session: Session = Depends(get_session),
):
    """Add multiple households to a list."""
    lst = session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    added_count = 0
    for household_id in request.household_ids:
        household = session.get(Household, household_id)
        if not household:
            continue

        # Check if already in list
        existing = session.exec(
            select(ListHouseholdLink).where(
                ListHouseholdLink.list_id == list_id,
                ListHouseholdLink.household_id == household_id,
            )
        ).first()

        if not existing:
            link = ListHouseholdLink(list_id=list_id, household_id=household_id)
            session.add(link)
            added_count += 1

    session.commit()
    return {"message": f"Added {added_count} households to list"}


@router.post("/{list_id}/households/{household_id}")
def add_household_to_list(
    list_id: int, household_id: int, session: Session = Depends(get_session)
):
    """Add a household to a list."""
    lst = session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")

    household = session.get(Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    # Check if already in list
    existing = session.exec(
        select(ListHouseholdLink).where(
            ListHouseholdLink.list_id == list_id,
            ListHouseholdLink.household_id == household_id,
        )
    ).first()

    if existing:
        return {"message": "Household already in list"}

    # Add to list
    link = ListHouseholdLink(list_id=list_id, household_id=household_id)
    session.add(link)
    session.commit()

    return {"message": "Household added to list"}


@router.delete("/{list_id}/households/{household_id}")
def remove_household_from_list(
    list_id: int, household_id: int, session: Session = Depends(get_session)
):
    """Remove a household from a list."""
    link = session.exec(
        select(ListHouseholdLink).where(
            ListHouseholdLink.list_id == list_id,
            ListHouseholdLink.household_id == household_id,
        )
    ).first()

    if not link:
        raise HTTPException(status_code=404, detail="Household not in this list")

    session.delete(link)
    session.commit()
    return {"message": "Household removed from list"}
