import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_male_no_pregnancies(client):
    data = {
        'gender': 'male',
        'age': 40,
        'gluc': 120,
        'bp': 70,
        'skin': 20,
        'insulin': 80,
        'bmi': 26.0,
        'func': 0.5,
        'pregs': 5
    }
    rv = client.post('/', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'diabetes' in rv.data.lower()

def test_female_young_no_pregnancies(client):
    data = {
        'gender': 'female',
        'age': 24,
        'gluc': 110,
        'bp': 80,
        'skin': 22,
        'insulin': 90,
        'bmi': 22.5,
        'func': 0.2,
        'pregs': 3
    }
    rv = client.post('/', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'diabetes' in rv.data.lower()

def test_female_older_with_pregnancies(client):
    data = {
        'gender': 'female',
        'age': 30,
        'gluc': 140,
        'bp': 90,
        'skin': 24,
        'insulin': 85,
        'bmi': 29.5,
        'func': 0.8,
        'pregs': 2
    }
    rv = client.post('/', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'diabetes' in rv.data.lower()

def test_missing_required_fields(client):
    data = {'gender': 'male', 'age': 40}
    rv = client.post('/', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Please fill in all required fields' in rv.data

def test_female_older_no_pregs_field(client):
    data = {
        'gender': 'female',
        'age': 28,
        'gluc': 132,
        'bp': 75,
        'skin': 18,
        'insulin': 100,
        'bmi': 24.5,
        'func': 0.7,
    }
    rv = client.post('/', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'diabetes' in rv.data.lower()

def test_html_page_loads(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Diabetes Prediction' in rv.data
