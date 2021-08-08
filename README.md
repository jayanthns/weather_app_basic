#### Project setup

##### Prequisites
- python3 and above
- pip

##### Clone the project
```git clone https://github.com/jayanthns/weather_app_basic.git```

##### inside the root project
```cd weather_app_basic```

##### create and activate the environment
```python3 -m venv env```

Activate environment in Linux
```source env/bin/activate```

Activate environment on windows
```env/Scripts/Activate```

##### install dependencies
```pip install -r requirements.txt```

##### apply the migrations (1st time)
```python manage.py migrate```

##### run the project
```python manage.py runserver```

##### click to see the swagger ui in the web
[swagger](http://localhost:8000/swagger)
