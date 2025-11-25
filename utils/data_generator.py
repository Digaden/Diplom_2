from faker import Faker
fake = Faker()

def generate_user():
    return {
        "email": fake.unique.email(),
        "password": "P@ssw0rd!",
        "name": fake.first_name()
    }