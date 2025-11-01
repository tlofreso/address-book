from sqlmodel import Field, Relationship, SQLModel


# Household models
class HouseholdBase(SQLModel):
    name: str
    address: str


class Household(HouseholdBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    members: list["Member"] = Relationship(back_populates="household", cascade_delete=True)


class HouseholdCreate(HouseholdBase):
    pass


class HouseholdUpdate(SQLModel):
    name: str | None = None
    address: str | None = None


# Member models
class MemberBase(SQLModel):
    first_name: str
    last_name: str
    email: str | None = None
    phone: str | None = None


class Member(MemberBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    household_id: int = Field(foreign_key="household.id")
    household: Household = Relationship(back_populates="members")


class MemberCreate(MemberBase):
    household_id: int


class MemberUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None


class MemberRead(MemberBase):
    id: int


# Household with members for creation (single transaction)
class HouseholdWithMembersCreate(HouseholdBase):
    members: list[MemberBase]


# Household read model with members included
class HouseholdRead(HouseholdBase):
    id: int
    members: list[MemberRead] = []


# Legacy Contact models (keeping for backwards compatibility during migration)
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
