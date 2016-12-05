# kpi-databases-labs
Autumn-winter 2016

Prihodko Serhiy, KP-42
Завдання роботи полягає у наступному:

Розробити схему бази даних на основі предметної галузі з ЛР№2-Ч1 у спосіб, що застосовується в СУБД MongoDB.
Розробити модуль роботи з базою даних на основі пакету PyMongo.
Реалізувати дві операції на вибір із використанням паралельної обробки даних Map/Reduce.
Реалізувати обчислення та виведення результату складного агрегативного запиту до бази даних з використанням функції aggregate() сервера MongoDB.

Тексти функції Map/Reduce :

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
        
та aggregate():        
      
raw = db.instance.Flight.aggregate([
            {'$match': {'cancelled': True }},
            {'$group': {'_id':  '$source', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ])
        

