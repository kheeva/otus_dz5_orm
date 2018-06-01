# A simple ORM working with python 3 and sqlite3

The ORM provides an interface to a database. Supported databases: sqlite3.


# How to install on ubuntu linux

At first you need to download and install python3 if you already haven't: http://python.org .
```buildoutcfg
apt install python3
apt install sqlite3
```

Clone this repo:
```buildoutcfg
cd ~/your_projects_dir
git clone https://github.com/kheeva/otus_dz5_orm
```

# How to use
1. Manually install a database:
schema.sql
```
CREATE TABLE Stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(256),
    shares INTEGER,
    price FLOAT
);
```
exec code:
```
SQL = open('schema.sql').read()

CONN = sqlite3.connect('data.db')
cur = CONN.cursor()
cur.executescript(SQL)
```

2. Configure your models in models.py:
```
from orm import Structure, String, Integer, Float

class Stock(Structure):
    name = String()
    shares = Integer()
    price = Float()
```

3. Let's test some operations to your db:
At first we create an object related to a table
```
stock = Stock()
```

Insert
```
stock.insert(name='GOOGLE', shares=2, price=22222.1)
stock.insert(name='YANDEX', shares=2, price=22.1)
```

Select
```
for s in stock.select(name='GOOGLE'):
    print(s.price)
```

Delete
```
stock.delete(name='YANDEX', price=22.1)
``` 

# Project Goals

The code is written for educational purposes. Training courses: otus.ru)
