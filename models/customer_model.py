from typing import Optional


class CustomerModel:
    """
    The CustomerModel class contains the attributes of a customer, such as customer ID,
    name, email, password, address, and country.
    """

    def __init__(self, cust_id: int, name: str, email: str, password: str,
                 address: Optional[str] = None, country: Optional[str] = None):
        self.id = cust_id
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.country = country

    def serialize(self):
        """Converts the CustomerModel instance into a dictionary for storage or transfer."""
        return {
            "cust_id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "country": self.country,
        }

    @classmethod
    def deserialize(cls, data):
        """Creates a CustomerModel instance from a dictionary."""
        cust_id = data['cust_id']
        name = data['name']
        email = data['email']
        password = data['password']
        address = data.get('address')
        country = data.get('country')
        return cls(cust_id, name, email, password, address, country)
