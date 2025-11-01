from sqlmodel import Field, SQLModel, Relationship


# Household Models
class HouseholdBase(SQLModel):
    name: str
    address: str | None = None


class Household(HouseholdBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    members: list["Contact"] = Relationship(back_populates="household")


class HouseholdCreate(HouseholdBase):
    pass


class HouseholdUpdate(SQLModel):
    name: str | None = None
    address: str | None = None


# Contact Models
class ContactBase(SQLModel):
    first_name: str
    last_name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    household_id: int | None = None


class Contact(ContactBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    household_id: int | None = Field(default=None, foreign_key="household.id")
    household: Household | None = Relationship(back_populates="members")


class ContactCreate(ContactBase):
    pass


class ContactUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    household_id: int | None = None
