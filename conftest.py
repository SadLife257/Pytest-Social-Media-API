import pytest
import requests

URL = "https://social-media-z5a2.onrender.com"

LOGIN_INFO = {
    'admin': {
      "email": "admin@gmail.com",
      "password": "Admin12345678#"
    },
    'bao': {
      "email": "n.bao25702@gmail.com",
      "password": "P@ssword1"
    },
      'khang': {
      "email": "khangtuhuu@gmail.com",
      "password": "Aa123456789!"
    }
}

@pytest.fixture
def stack():
  return []

@pytest.fixture
def url():
  return URL

@pytest.fixture
def accessToken(request):
  account = request.param
  print(f'CONFTEST LOADED for {account}')
  if (account not in LOGIN_INFO):
    print('ACCOUNT NOT FOUNDED')
  else:
    accessToken = requests.post(f"{URL}/api/auth/login", json=LOGIN_INFO.get(account)).json()['accessToken']
    return accessToken