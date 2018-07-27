# Geo Api

GeoApi is a simple API to list users an its sales

# Getting Started

you'll have install MongoDB in your computer
```apt-get install mongodb```

in the root of the repository install python dependencies
``` pip install -r requirements.txt```

then fire up the development server (don't use it production!)
```python run.py```

you cant test it using curl
```
curl -X POST -d '{"email":"some@email.com","enabled":true}' http://localhost:5000/user -H "Content-Type: application/json"

curl -X POST http://localhost:5000/sale -H "Content-Type: application/json" -d '{"uuid": "889e068d-b098-4da2-82dd-4c712a0446b6","user_email": "some@email.com","amount": 123.45,"date":"2017-10-15 11:35"}'
```
