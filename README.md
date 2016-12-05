# kpi-databases-labs
Autumn-winter 2016
### Python/Django + MongoDB

Prihodko Serhiy, KP-42
Завдання роботи полягає у наступному:

* Розробити схему бази даних на основі предметної галузі з ЛР№2-Ч1 у спосіб, що застосовується в СУБД MongoDB.
* Розробити модуль роботи з базою даних на основі пакету PyMongo.
* Реалізувати дві операції на вибір із використанням паралельної обробки даних Map/Reduce.
* Реалізувати обчислення та виведення результату складного агрегативного запиту до бази даних з використанням функції aggregate() сервера MongoDB.

Тексти функції Map/Reduce :
```python
mapper = Code("""
            function(){
                emit(this.aircraft._id, 1);
            }
        """)
````
```python
reducer = Code("""
            function(key, values){
                return values.length;
            }
        """)
```

та aggregate():        

```python
raw = db.instance.Flight.aggregate([
            {'$match': {'cancelled': True }},
            {'$group': {'_id':  '$source', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ])
```
Screenshots:

![Screen1](https://s13.postimg.org/m8z4hxalz/Screenshot_from_2016_12_05_11_34_58.png)

![Screen2](https://s13.postimg.org/6c0cl7i7r/Screenshot_from_2016_12_05_11_34_39.png)

![Screen3](https://s13.postimg.org/moaeaxwjb/Screenshot_from_2016_12_05_11_34_06.png)

![Screen4](https://s13.postimg.org/4zn8x2a5z/Screenshot_from_2016_12_05_11_33_50.png)



