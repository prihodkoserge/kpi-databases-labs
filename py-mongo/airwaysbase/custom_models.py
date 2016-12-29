from .db_manager import DB
from bson.objectid import ObjectId
from bson.code import Code
from cache_manager import CacheManager
from datetime import datetime

cache = CacheManager()
db = DB()


class Aircraft(object):
    def __init__(self, attr_list={}):
        self.id = attr_list.get('_id', None)
        self.name = attr_list.get('name', '')
        self.capacity = attr_list.get('capacity', -1)

    @staticmethod
    def get_list():
        cursor = db.instance.Aircraft.find()
        return [Aircraft(a).to_dict() for a in cursor]

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
        self.city = attr_list.get('city', '')
        self.country = attr_list.get('country', '')

    @staticmethod
    def search(keyword):
        t0 = datetime.now()
        cached_result = cache.get_from_cache(keyword)
        t0 = datetime.now() - t0
        if not cached_result:
            t1 = datetime.now()
            cursor = db.instance.Airport.find({'$text': {'$search': keyword}})
            t1 = datetime.now() - t1
            airports = [Airport(a).to_dict() for a in cursor]
            print 'Loaded from mongo: ', t1
            if airports:
                cache.cache_data(keyword, airports)
                return airports
            else:
                return []
        else:
            print 'Loaded from cache: ', t0
            return cached_result


    @staticmethod
    def get_list():
        cursor = db.instance.Airport.find()
        return [Airport(a).to_dict() for a in cursor]

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
        if self.city != '':
            d['city'] = self.city
        if self.country != '':
            d['country'] = self.country

        return d

    def __str__(self):
        return self.name.encode('utf8')


class Flight(object):
    def __init__(self, attr_list={}, from_form=False):
        if from_form is not False:
            attr_list = Flight.__prepare_form_data(attr_list)

        self.id = attr_list.get('_id', None)
        self.source = Airport(attr_list.get('source', {}))
        self.destination = Airport(attr_list.get('destination', {}))
        self.aircraft = Aircraft(attr_list.get('aircraft', {}))
        self.start_date = attr_list.get('start_date', None)
        self.end_date = attr_list.get('end_date', None)
        self.cancelled = attr_list.get('cancelled', False)

    def save(self):
        db.instance.Flight.insert(self.to_dict())

    def update(self, new_data):
        new_data = Flight.__prepare_form_data(new_data)

        db.instance.Flight.update(
            {'_id': self.id},
            {
                '$set': new_data
            }
        )

    def to_form_data(self):
        d = self.to_dict()

        if d['source'] is not None:
            d['source'] = d['source']['_id']
        if d['destination'] is not None:
            d['destination'] = d['destination']['_id']
        if d['aircraft'] is not None:
            d['aircraft'] = d['aircraft']['_id']

        return d

    @staticmethod
    def __prepare_form_data(form_data):
        if form_data['source'] is not None:
            form_data['source'] = Airport\
                .get_by_id(form_data['source'])\
                .to_dict()
        if form_data['destination'] is not None:
            form_data['destination'] = Airport\
                .get_by_id(form_data['destination'])\
                .to_dict()
        if form_data['aircraft'] is not None:
            form_data['aircraft'] = Aircraft\
                .get_by_id(form_data['aircraft'])\
                .to_dict()
        return form_data

    @staticmethod
    def get_list(limit=None):
        cursor = db.instance.Flight.find()
        if limit is not None:
            cursor.limit(limit=limit)
        return [Flight(f).to_dict() for f in cursor]

    @staticmethod
    def get_by_id(id):
        id = ObjectId(id)
        return Flight(db.instance.Flight.find_one({'_id': id}))

    @staticmethod
    def delete_by_id(id):
        id = ObjectId(id)
        db.instance.Flight.remove({'_id': id})

    def to_dict(self):
        d = {}

        if self.id is not None:
            d['_id'] = self.id
        if self.source is not None:
            d['source'] = self.source.to_dict()
        if self.destination is not None:
            d['destination'] = self.destination.to_dict()
        if self.aircraft is not None:
            d['aircraft'] = self.aircraft.to_dict()
        if self.start_date is not None:
            d['start_date'] = self.start_date
        if self.end_date is not None:
            d['end_date'] = self.end_date
        d['cancelled']  = self.cancelled

        return d


class Stat(object):

    @staticmethod
    def flights_per_aircraft():
        mapper = Code("""
            function(){
                emit(this.aircraft._id, 1);
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
                emit(this.source._id, 1);
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
                emit(this.destination._id, 1);
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

    @staticmethod
    def most_cancellation_airports():
        raw = db.instance.Flight.aggregate([
            {'$match': {'cancelled': True }},
            {'$group': {'_id':  '$source', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ])
        agg = list(raw)
        for obj in agg:
            obj['name'] = obj['_id']['name']
        return agg

print Stat.most_cancellation_airports()