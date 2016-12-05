from faker import Factory
from pymongo import MongoClient
import random

fake = Factory.create()

db = MongoClient().aw_base

# for i in range(50):
#     db.Airport.insert({
#         'name': fake.company(),
#         'city': fake.city(),
#         'country': fake.country()
#     })

# for i in range(30):
#     db.Aircraft.insert({
#         'name': fake.word(),
#         'capacity': random.randrange(600, 4000, 100)
#     })

