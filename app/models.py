from sqlmodel import Field, Relationship, SQLModel


# Link table for many-to-many relationship between List and Household
class ListHouseholdLink(SQLModel, table=True):
    list_id: int = Field(foreign_key="list.id", primary_key=True)
    household_id: int = Field(foreign_key="household.id", primary_key=True)


# Household models
class HouseholdBase(SQLModel):
    name: str
    address: str


class Household(HouseholdBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    members: list["Member"] = Relationship(back_populates="household", cascade_delete=True)
    lists: list["List"] = Relationship(back_populates="households", link_model=ListHouseholdLink)


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


# List models
class ListBase(SQLModel):
    name: str
    description: str | None = None


class List(ListBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    households: list[Household] = Relationship(back_populates="lists", link_model=ListHouseholdLink)


class ListCreate(ListBase):
    pass


class ListUpdate(SQLModel):
    name: str | None = None
    description: str | None = None


class ListRead(ListBase):
    id: int
    household_count: int = 0


class ListWithHouseholds(ListBase):
    id: int
    households: list[HouseholdRead] = []


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
