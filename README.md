# Aral Donation platform

## Prerequisites
- git 2.17.1
- virtualenv 15.1.0
- pip 20.0.2
- python 3.6.8
- PostgreSQL 10
- Insomnia 6.5.1


## How to install

### Git clone

```
git clone https://github.com/atabekdemurtaza/aral-master.git
```

### Create virtual environment
```
cd aral/
virtualenv --python=python3 --prompt="[v]" env
source env/bin/activate
```

### Install package requirements and activate environment
```
pip install -r requirements.txt
```

### Run server
```
python manage.py runserver
```
