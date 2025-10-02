from sqlmodel import Field, SQLModel


class ContactBase(SQLModel):
    first_name: str
    last_name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class Contact(ContactBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ContactCreate(ContactBase):
    pass


class ContactUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
