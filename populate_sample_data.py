"""Populate the address book with sample household data."""
import httpx

BASE_URL = "http://localhost:8000"

# Sample household data
households = [
    {
        "name": "The Lofreso's",
        "address": "438 Red Rock Dr, Medina, OH",
        "members": [
            {"first_name": "Tony", "last_name": "Lofreso", "email": None, "phone": None},
            {"first_name": "Bridgette", "last_name": "Lofreso", "email": None, "phone": None},
            {"first_name": "Theodore", "last_name": "Lofreso", "email": None, "phone": None},
            {"first_name": "Ruthie", "last_name": "Lofreso", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Smith Family",
        "address": "123 Main St, Cleveland, OH",
        "members": [
            {"first_name": "John", "last_name": "Smith", "email": None, "phone": None},
            {"first_name": "Jane", "last_name": "Smith", "email": None, "phone": None},
            {"first_name": "Emily", "last_name": "Smith", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Johnson's",
        "address": "456 Oak Ave, Akron, OH",
        "members": [
            {"first_name": "Michael", "last_name": "Johnson", "email": None, "phone": None},
            {"first_name": "Sarah", "last_name": "Johnson", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Williams Household",
        "address": "789 Elm St, Canton, OH",
        "members": [
            {"first_name": "David", "last_name": "Williams", "email": None, "phone": None},
            {"first_name": "Lisa", "last_name": "Williams", "email": None, "phone": None},
            {"first_name": "Ryan", "last_name": "Williams", "email": None, "phone": None},
            {"first_name": "Ashley", "last_name": "Williams", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Brown's",
        "address": "321 Maple Dr, Lakewood, OH",
        "members": [
            {"first_name": "Robert", "last_name": "Brown", "email": None, "phone": None},
            {"first_name": "Jennifer", "last_name": "Brown", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Davis Family",
        "address": "654 Pine St, Strongsville, OH",
        "members": [
            {"first_name": "James", "last_name": "Davis", "email": None, "phone": None},
            {"first_name": "Mary", "last_name": "Davis", "email": None, "phone": None},
            {"first_name": "Tyler", "last_name": "Davis", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Miller's",
        "address": "987 Cedar Ln, Brunswick, OH",
        "members": [
            {"first_name": "William", "last_name": "Miller", "email": None, "phone": None},
            {"first_name": "Patricia", "last_name": "Miller", "email": None, "phone": None},
            {"first_name": "Brandon", "last_name": "Miller", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Wilson Household",
        "address": "147 Birch Ave, Parma, OH",
        "members": [
            {"first_name": "Richard", "last_name": "Wilson", "email": None, "phone": None},
            {"first_name": "Linda", "last_name": "Wilson", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Moore's",
        "address": "258 Spruce St, Westlake, OH",
        "members": [
            {"first_name": "Charles", "last_name": "Moore", "email": None, "phone": None},
            {"first_name": "Barbara", "last_name": "Moore", "email": None, "phone": None},
            {"first_name": "Jessica", "last_name": "Moore", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Taylor Family",
        "address": "369 Walnut Dr, North Olmsted, OH",
        "members": [
            {"first_name": "Joseph", "last_name": "Taylor", "email": None, "phone": None},
            {"first_name": "Elizabeth", "last_name": "Taylor", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Anderson's",
        "address": "741 Hickory Ln, Mentor, OH",
        "members": [
            {"first_name": "Thomas", "last_name": "Anderson", "email": None, "phone": None},
            {"first_name": "Susan", "last_name": "Anderson", "email": None, "phone": None},
            {"first_name": "Matthew", "last_name": "Anderson", "email": None, "phone": None},
            {"first_name": "Amanda", "last_name": "Anderson", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Thomas Household",
        "address": "852 Chestnut Ave, Solon, OH",
        "members": [
            {"first_name": "Christopher", "last_name": "Thomas", "email": None, "phone": None},
            {"first_name": "Nancy", "last_name": "Thomas", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Jackson's",
        "address": "963 Willow St, Beachwood, OH",
        "members": [
            {"first_name": "Daniel", "last_name": "Jackson", "email": None, "phone": None},
            {"first_name": "Karen", "last_name": "Jackson", "email": None, "phone": None},
            {"first_name": "Nicholas", "last_name": "Jackson", "email": None, "phone": None},
        ],
    },
    {
        "name": "The White Family",
        "address": "159 Poplar Dr, Shaker Heights, OH",
        "members": [
            {"first_name": "Matthew", "last_name": "White", "email": None, "phone": None},
            {"first_name": "Betty", "last_name": "White", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Harris's",
        "address": "357 Ash Ln, Euclid, OH",
        "members": [
            {"first_name": "Donald", "last_name": "Harris", "email": None, "phone": None},
            {"first_name": "Dorothy", "last_name": "Harris", "email": None, "phone": None},
            {"first_name": "Samantha", "last_name": "Harris", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Martin Household",
        "address": "486 Sycamore Ave, Rocky River, OH",
        "members": [
            {"first_name": "Paul", "last_name": "Martin", "email": None, "phone": None},
            {"first_name": "Helen", "last_name": "Martin", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Thompson's",
        "address": "597 Dogwood St, Bay Village, OH",
        "members": [
            {"first_name": "Mark", "last_name": "Thompson", "email": None, "phone": None},
            {"first_name": "Sandra", "last_name": "Thompson", "email": None, "phone": None},
            {"first_name": "Lauren", "last_name": "Thompson", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Garcia Family",
        "address": "624 Magnolia Dr, Avon Lake, OH",
        "members": [
            {"first_name": "Steven", "last_name": "Garcia", "email": None, "phone": None},
            {"first_name": "Carol", "last_name": "Garcia", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Martinez's",
        "address": "735 Redwood Ln, Avon, OH",
        "members": [
            {"first_name": "Kevin", "last_name": "Martinez", "email": None, "phone": None},
            {"first_name": "Donna", "last_name": "Martinez", "email": None, "phone": None},
            {"first_name": "Jordan", "last_name": "Martinez", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Robinson Household",
        "address": "846 Sequoia Ave, North Royalton, OH",
        "members": [
            {"first_name": "Brian", "last_name": "Robinson", "email": None, "phone": None},
            {"first_name": "Michelle", "last_name": "Robinson", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Clark's",
        "address": "957 Cypress St, Broadview Heights, OH",
        "members": [
            {"first_name": "George", "last_name": "Clark", "email": None, "phone": None},
            {"first_name": "Kimberly", "last_name": "Clark", "email": None, "phone": None},
            {"first_name": "Andrew", "last_name": "Clark", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Rodriguez Family",
        "address": "168 Fir Dr, Independence, OH",
        "members": [
            {"first_name": "Edward", "last_name": "Rodriguez", "email": None, "phone": None},
            {"first_name": "Lisa", "last_name": "Rodriguez", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Lewis's",
        "address": "279 Hemlock Ln, Seven Hills, OH",
        "members": [
            {"first_name": "Jason", "last_name": "Lewis", "email": None, "phone": None},
            {"first_name": "Angela", "last_name": "Lewis", "email": None, "phone": None},
            {"first_name": "Kayla", "last_name": "Lewis", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Lee Household",
        "address": "381 Juniper Ave, Olmsted Falls, OH",
        "members": [
            {"first_name": "Ryan", "last_name": "Lee", "email": None, "phone": None},
            {"first_name": "Melissa", "last_name": "Lee", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Walker's",
        "address": "492 Laurel St, Berea, OH",
        "members": [
            {"first_name": "Justin", "last_name": "Walker", "email": None, "phone": None},
            {"first_name": "Amy", "last_name": "Walker", "email": None, "phone": None},
            {"first_name": "Connor", "last_name": "Walker", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Hall Family",
        "address": "513 Oakwood Dr, Olmsted Township, OH",
        "members": [
            {"first_name": "Aaron", "last_name": "Hall", "email": None, "phone": None},
            {"first_name": "Stephanie", "last_name": "Hall", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Allen's",
        "address": "624 Maplewood Ln, Brooklyn, OH",
        "members": [
            {"first_name": "Jonathan", "last_name": "Allen", "email": None, "phone": None},
            {"first_name": "Rebecca", "last_name": "Allen", "email": None, "phone": None},
            {"first_name": "Madison", "last_name": "Allen", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Young Household",
        "address": "735 Cedarwood Ave, Middleburg Heights, OH",
        "members": [
            {"first_name": "Nathan", "last_name": "Young", "email": None, "phone": None},
            {"first_name": "Deborah", "last_name": "Young", "email": None, "phone": None},
        ],
    },
    {
        "name": "The King's",
        "address": "846 Pinewood St, Fairview Park, OH",
        "members": [
            {"first_name": "Zachary", "last_name": "King", "email": None, "phone": None},
            {"first_name": "Laura", "last_name": "King", "email": None, "phone": None},
            {"first_name": "Olivia", "last_name": "King", "email": None, "phone": None},
        ],
    },
    {
        "name": "The Wright Family",
        "address": "957 Elmwood Dr, Cleveland Heights, OH",
        "members": [
            {"first_name": "Gregory", "last_name": "Wright", "email": None, "phone": None},
            {"first_name": "Sharon", "last_name": "Wright", "email": None, "phone": None},
        ],
    },
]


def populate():
    """Add all sample households to the database."""
    print(f"Adding {len(households)} households to the database...")

    with httpx.Client() as client:
        for i, household in enumerate(households, 1):
            try:
                response = client.post(f"{BASE_URL}/households/", json=household)
                if response.status_code == 200:
                    print(f"✓ Added: {household['name']} ({i}/{len(households)})")
                else:
                    print(f"✗ Failed to add {household['name']}: {response.status_code}")
            except Exception as e:
                print(f"✗ Error adding {household['name']}: {e}")

    print(f"\n✓ Done! Added {len(households)} households.")


if __name__ == "__main__":
    populate()
