from pymongo import MongoClient


class DB:
    def __init__(self):
        self.client = MongoClient()
        self.instance = self.client.aw_base
        # self.force_fill_db()

    def force_fill_db(self):
        self.instance.Aircraft.remove({})
        self.instance.Airport.remove({})
        self.instance.Flight.remove({})

        aircraft1 = { 'name': 'Boing 1', 'capacity': 1000 }
        aircraft2 = { 'name': 'Boing 2', 'capacity': 3000 }

        self.instance.Aircraft.insert(aircraft1)
        self.instance.Aircraft.insert(aircraft2)

        airport1 = { 'name': 'Boryspil', 'city': 'Boryspil', 'country': 'Ukraine' }
        airport2 = { 'name': 'RomaAir', 'city': 'Rome', 'country': 'Italy'}
        airport3 = { 'name': 'LondonPark', 'city': 'London', 'country': 'England'}
        airport4 = { 'name': 'LA-Airport', 'city': 'Los Angeles', 'country': 'USA' }

        self.instance.Airport.insert(airport1)
        self.instance.Airport.insert(airport2)
        self.instance.Airport.insert(airport3)
        self.instance.Airport.insert(airport4)


