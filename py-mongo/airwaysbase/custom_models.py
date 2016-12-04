from .db_manager import DB
from bson.objectid import ObjectId
from bson.code import Code

db = DB()


class Aircraft(object):
    def __init__(self, attr_list={}):
        self.id = attr_list.get('_id', None)
        self.name = attr_list.get('name', '')
        self.capacity = attr_list.get('capacity', -1)

    @staticmethod
    def get_list():
        cursor = db.instance.Aircraft.find()
        return [a for a in cursor]

    @staticmethod
    def get_choices():
        return [(a['_id'], a['name']) for a in Aircraft.get_list()]

    @staticmethod
    def get_by_id(id):
        id = ObjectId(id)
        return Aircraft(db.instance.Aircraft.find_one({'_id': id}))

    def to_dict(self):
        d = {}

        if self.id is not None:
            d['_id'] = self.id
        if self.name != '':
            d['name'] = self.name
        if self.capacity != -1:
            d['capacity'] = self.capacity

        return d

    def __str__(self):
        return self.name.encode('utf8')


class Airport(object):
    def __init__(self, attr_list={}):
        self.id = attr_list.get('_id', None)
        self.name = attr_list.get('name', '')
        self.country = attr_list.get('country', '')

    @staticmethod
    def get_list():
        cursor = db.instance.Airport.find()
        return [a for a in cursor]

    @staticmethod
    def get_choices():
        return [(a['_id'], a['name']) for a in Airport.get_list()]

    @staticmethod
    def get_by_id(id):
        id = ObjectId(id)
        return Airport(db.instance.Airport.find_one({'_id': id}))

    def to_dict(self):
        d = {}

        if self.id is not None:
            d['_id'] = self.id
        if self.name != '':
            d['name'] = self.name
        if self.country != '':
            d['country'] = self.country

        return d

    def __str__(self):
        return self.name.encode('utf8')


class Flight(object):
    def __init__(self, attr_list={}):
        self.id = attr_list.get('_id', None)
        self.source_id = attr_list.get('source_id', None)
        self.destination_id = attr_list.get('destination_id', None)
        self.aircraft_id = attr_list.get('aircraft_id', None)
        self.start_date = attr_list.get('start_date', None)
        self.end_date = attr_list.get('end_date', None)

    def update(self, new_data):
        db.instance.Flight.update(
            {'_id': self.id},
            {
                '$set': new_data
            }
        )

    @staticmethod
    def get_list(limit=None):
        cursor = db.instance.Flight.find()
        if limit is not None:
            cursor.limit(limit=limit)
        return [Flight(f).expanded_dict() for f in cursor]

    @staticmethod
    def get_by_id(id):
        id = ObjectId(id)
        return Flight(db.instance.Flight.find_one({'_id': id}))

    @staticmethod
    def delete_by_id(id):
        id = ObjectId(id)
        db.instance.Flight.remove({'_id': id})

    def expanded_dict(self):
        d = self.to_dict()

        if self.source_id is not None:
            d['source'] = Airport.get_by_id(self.source_id)
        if self.destination_id is not None:
            d['destination'] = Airport.get_by_id(self.destination_id)
        if self.aircraft_id is not None:
            d['aircraft'] = Aircraft.get_by_id(self.aircraft_id)

        return d

    def to_dict(self):
        d = {}

        if self.id is not None:
            d['_id'] = self.id
        if self.source_id is not None:
            d['source_id'] = self.source_id
        if self.destination_id is not None:
            d['destination_id'] = self.destination_id
        if self.aircraft_id is not None:
            d['aircraft_id'] = self.aircraft_id
        if self.start_date is not None:
            d['start_date'] = self.start_date
        if self.end_date is not None:
            d['end_date'] = self.end_date

        return d


class Stat(object):

    @staticmethod
    def flights_per_aircraft():
        mapper = Code("""
            function(){
                emit(this.aircraft_id, 1);
            }
        """)
        reducer = Code("""
            function(key, values){
                return values.length;
            }
        """)
        raw = db.instance.Flight\
            .map_reduce(mapper, reducer, "aircraft_stats")\
            .find()

        res = []
        for pair in raw:
            res.append({
                'name': Aircraft.get_by_id(pair['_id']).name,
                'flights_num': int(pair['value'])
            })
        return res

    @staticmethod
    def flights_from_airport():
        mapper = Code("""
            function(){
                emit(this.source_id, 1);
            }
        """)
        reducer = Code("""
            function(key, values){
                return values.length;
            }
        """)
        raw = db.instance.Flight\
            .map_reduce(mapper, reducer, "source_stats")\
            .find()

        res = []
        for pair in raw:
            res.append({
                'from': Airport.get_by_id(pair['_id']).name,
                'flights_num': int(pair['value'])
            })
        return res

    @staticmethod
    def flights_to_airport():
        mapper = Code("""
            function(){
                emit(this.destination_id, 1);
            }
        """)
        reducer = Code("""
            function(key, values){
                return values.length;
            }
        """)
        raw = db.instance.Flight \
            .map_reduce(mapper, reducer, "destination_stats") \
            .find()

        res = []
        for pair in raw:
            res.append({
                'to': Airport.get_by_id(pair['_id']).name,
                'flights_num': int(pair['value'])
            })
        return res
    