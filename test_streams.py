import pytest
import requests
import random
import string
import json

session = requests.Session()

# -------------------- HELPER FUNCTION --------------------
def helper_createcreateStream(url, accessToken):
  response = session.post(
      f"{url}/api/streams",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'title': 'New Stream',
          'description': 'Pytest Stream',
          'categoryIds': [
              '671a01672a386fca99c73c07'
          ]
      }
    )
  return response.json()['stream']

def helper_cleanup(id, url, accessToken):
  response = session.delete(
      f"{url}/api/streams/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )

def helper_id_generator(size=24, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def helper_compare_json(json_obj1, json_obj2):
  return json.dumps(json.loads(json_obj1), sort_keys=True) == json.dumps(json.loads(json_obj2), sort_keys=True)

# -------------------- TESTCASE --------------------

# -------------------- TC1 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc1(url, accessToken):
  response = session.post(
      f"{url}/api/streams",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'title': 'New Stream',
          'description': 'Pytest Stream',
          'categoryIds': [
              '671a01672a386fca99c73c07'
          ]
      }
    )
  assert response.status_code == 201
  helper_cleanup(response.json()['stream']['_id'], url, accessToken)

# -------------------- TC2 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc2(url, accessToken):
  response = session.post(
      f"{url}/api/streams",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'title': 'New Stream',
          'description': 'Pytest Stream',
          'categoryIds': []
      }
    )
  assert response.status_code == 201
  helper_cleanup(response.json()['stream']['_id'], url, accessToken)

# -------------------- TC3 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc3(url, accessToken):
  response = session.post(
      f"{url}/api/streams",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'title': '',
          'description': 'Pytest Stream',
          'categoryIds': [
              '671a01672a386fca99c73c07'
          ]
      }
    )
  assert response.status_code == 400

# -------------------- TC4 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc4(url, accessToken):
  response = session.get(
    f"{url}/api/streams",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 200

# -------------------- TC10 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc10(url, accessToken):
  id = helper_createcreateStream(url, accessToken)['_id']
  response = session.delete(
    f"{url}/api/streams/{id}",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 200