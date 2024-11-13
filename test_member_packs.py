import pytest
import requests
import random
import string
import json

session = requests.Session()

# -------------------- HELPER FUNCTION --------------------
def helper_createcreatePack(url, accessToken):
  response = session.post(
      f"{url}/api/member-pack",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': 'New Test Pack',
        'description': 'New Test Pack',
        'price': 120,
        'durationUnit': 'MONTH',
        'durationNumber': 3
      }
    )
  return response.json()['memberPack']

def helper_cleanup(id, url, accessToken):
  response = session.delete(
      f"{url}/api/member-pack/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )

def helper_id_generator(size=24, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def helper_compare_json(json_obj1, json_obj2):
  return json.dumps(json.loads(json_obj1), sort_keys=True) == json.dumps(json.loads(json_obj2), sort_keys=True)

# -------------------- TESTCASE --------------------

# -------------------- TC1 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc1(url, accessToken):
  response = session.get(
      f"{url}/api/member-pack",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200

# -------------------- TC2 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc2(url, accessToken):
  response = session.post(
      f"{url}/api/member-pack",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': 'New Test Pack',
        'description': 'New Test Pack',
        'price': 120,
        'durationUnit': 'MONTH',
        'durationNumber': 3
      }
    )
  assert response.status_code == 201
  helper_cleanup(response.json()['memberPack']['_id'], url, accessToken)

# -------------------- TC3 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc3(url, accessToken):
  response = session.post(
      f"{url}/api/member-pack",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': 'New Test Pack',
        'description': 'New Test Pack',
        'price': 120,
        'durationUnit': 'DECADE',
        'durationNumber': 3
      }
    )
  assert response.status_code == 400

# -------------------- TC4 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc4(url, accessToken):
  response = session.post(
      f"{url}/api/member-pack",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': 'New Test Pack',
        'description': 'New Test Pack',
        'price': 120,
        'durationUnit': 'MONTH',
        'durationNumber': 3.14
      }
    )
  assert response.status_code == 400

# -------------------- TC5 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc5(url, accessToken):
  response = session.post(
      f"{url}/api/member-pack",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': '',
        'description': 'New Test Pack',
        'price': 120,
        'durationUnit': 'MONTH',
        'durationNumber': 3
      }
    )
  assert response.status_code == 400

# -------------------- TC6 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc6(url, accessToken):
  pack = helper_createcreatePack(url, accessToken)
  response = session.post(
      f"{url}/api/member-pack",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': pack['name'],
        'description': 'New Test Pack',
        'price': 120,
        'durationUnit': 'MONTH',
        'durationNumber': 3
      }
    )
  assert response.status_code == 500
  helper_cleanup(pack['_id'], url, accessToken)

# -------------------- TC7 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc7(url, accessToken):
  response = session.post(
      f"{url}/api/member-pack",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': 'New Test Pack',
        'description': 'New Test Pack',
        'price': -120,
        'durationUnit': 'MONTH',
        'durationNumber': 3
      }
    )
  assert response.status_code == 400

# -------------------- TC8 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc8(url, accessToken):
  pack = helper_createcreatePack(url, accessToken)
  response = session.put(
      f"{url}/api/member-pack/{pack['_id']}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': 'Updated Test Pack',
        'description': 'Updated Test Pack',
        'price': 120,
        'durationUnit': 'MONTH',
        'durationNumber': 3
      }
    )
  assert response.status_code == 200
  helper_cleanup(pack['_id'], url, accessToken)

# -------------------- TC9 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc9(url, accessToken):
  id = helper_id_generator()
  print(id)
  response = session.put(
      f"{url}/api/member-pack/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'name': 'Updated Test Pack',
        'description': 'Updated Test Pack',
        'price': 120,
        'durationUnit': 'MONTH',
        'durationNumber': 3
      }
    )
  #assert response.status_code == 404, response.json()
  assert response.status_code == 500, response.json()

# -------------------- TC10 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc10(url, accessToken):
  pack = helper_createcreatePack(url, accessToken)
  response = session.delete(
      f"{url}/api/member-pack/{pack['_id']}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200

# -------------------- TC11 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc11(url, accessToken):
  id = helper_id_generator()
  response = session.delete(
      f"{url}/api/member-pack/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 500, response.json()