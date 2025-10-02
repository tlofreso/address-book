from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Contact, ContactCreate, ContactUpdate

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, session: Session = Depends(get_session)):
    db_contact = Contact.model_validate(contact)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


@router.get("/", response_model=list[Contact])
def list_contacts(session: Session = Depends(get_session)):
    contacts = session.exec(select(Contact)).all()
    return contacts


@router.get("/{contact_id}", response_model=Contact)
def get_contact(contact_id: int, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int, contact_update: ContactUpdate, session: Session = Depends(get_session)
):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact_data = contact_update.model_dump(exclude_unset=True)
    contact.sqlmodel_update(contact_data)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, session: Session = Depends(get_session)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    session.delete(contact)
    session.commit()
    return {"message": "Contact deleted successfully"}
