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
`
CREATE TABLE Stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(256),
    shares INTEGER,
    price FLOAT
);
`
exec code:
```
SQL = open('schema.sql').read()

CONN = sqlite3.connect('data.db')
cur = CONN.cursor()
cur.executescript(SQL)
```

2. Test select and insert operations to your db:
```
stock2 = Stock()
stock2.insert(name='GOOGLE', shares=2, price=22222.1)
stock2.insert(name='YANDEX', shares=2, price=22.1)

stock = Stock().select(shares=2)

for s in stock:
    print(s.price)
``` 

# Project Goals

The code is written for educational purposes. Training courses: otus.ru)
