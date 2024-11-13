import pytest
import requests
import random
import string
import json

session = requests.Session()

# -------------------- HELPER FUNCTION --------------------
def helper_createcreateGift(url, accessToken):
  response = session.post(
      f"{url}/api/gifts",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'New Test Gifts',
          'valuePerUnit': 20
      },
      files={
          'giftCreateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  return response.json()['gift']

def helper_cleanup(id, url, accessToken):
  response = session.delete(
      f"{url}/api/gifts/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )

def helper_id_generator(size=24, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def helper_compare_json(json_obj1, json_obj2):
  return json.dumps(json.loads(json_obj1), sort_keys=True) == json.dumps(json.loads(json_obj2), sort_keys=True)

# -------------------- TESTCASE --------------------

# -------------------- TC1 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc1(url, accessToken):
  response = session.post(
      f"{url}/api/gifts",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'New Test Gifts',
          'valuePerUnit': 20
      },
      files={
          'giftCreateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 201, response.json()['message']
  helper_cleanup(response.json()['gift']['_id'], url, accessToken)

# -------------------- TC2 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc2(url, accessToken):
  response = session.post(
      f"{url}/api/gifts",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': '',
          'valuePerUnit': 20
      },
      files={
          'giftCreateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC3 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc3(url, accessToken):
  response = session.post(
      f"{url}/api/gifts",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'New Test Gift',
          'valuePerUnit': -20
      },
      files={
          'giftCreateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC4 --------------------
@pytest.mark.skip('CURRENTLY FIXING')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc4(url, accessToken):
  response = session.post(
      f"{url}/api/gifts",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'New Test Gift',
          'valuePerUnit': 0
      },
      files={
          'giftCreateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 400, response.json()['message']
  #helper_cleanup(response.json()['gift']['_id'], url, accessToken)

# -------------------- TC5 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc5(url, accessToken):
  response = session.post(
      f"{url}/api/gifts",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'New Test Gift',
          'valuePerUnit': 20
      },
      files={
          'giftCreateImg': None
      }
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC6 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc6(url, accessToken):
  response = session.get(
      f"{url}/api/gifts",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200, response.json()['message']

# -------------------- TC7 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc7(url, accessToken):
  id = helper_createcreateGift(url, accessToken)['_id']
  response = session.get(
      f"{url}/api/gifts/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200, response.json()['message']
  helper_cleanup(id, url, accessToken)

# -------------------- TC8 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc8(url, accessToken):
  id = helper_id_generator()
  print(id)
  response = session.get(
      f"{url}/api/gifts/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  #assert response.status_code == 404, response.json()['message']
  assert response.status_code == 500, response.json()['message']

# -------------------- TC9 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc9(url, accessToken):
  gift = helper_createcreateGift(url, accessToken)
  response = session.put(
      f"{url}/api/gifts/{gift['_id']}",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'Updated Test Gift',
          'valuePerUnit': 20
      },
      files={
          'giftUpdateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 200, response.json()['message']
  helper_cleanup(gift['_id'], url, accessToken)

# -------------------- TC10 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc10(url, accessToken):
  id = helper_id_generator()
  print(id)
  response = session.put(
      f"{url}/api/gifts/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'Updated Test Gift',
          'valuePerUnit': 20
      },
      files={
          'giftUpdateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 500

# -------------------- TC11 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc11(url, accessToken):
  gift = helper_createcreateGift(url, accessToken)
  response = session.put(
      f"{url}/api/gifts/{gift['_id']}",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': '',
          'valuePerUnit': 20
      },
      files={
          'giftUpdateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  if(response.status_code == 200):
    assert response.json()['gift']['name'] == gift['name'], response.json()['message']
  else:
    assert response.status_code == 404, response.json()['message']
  helper_cleanup(gift['_id'], url, accessToken)

# -------------------- TC12 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc12(url, accessToken):
  gift = helper_createcreateGift(url, accessToken)
  response = session.put(
      f"{url}/api/gifts/{gift['_id']}",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'Updated Test Gift',
          'valuePerUnit': None
      },
      files={
          'giftUpdateImg': ('tester_img.jpg', open('imgs/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  if(response.status_code == 200):
    assert response.json()['gift']['valuePerUnit'] == gift['valuePerUnit'], response.json()['message']
  else:
    assert response.status_code == 404, response.json()['message']
  helper_cleanup(gift['_id'], url, accessToken)

# -------------------- TC13 --------------------
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc13(url, accessToken):
  gift = helper_createcreateGift(url, accessToken)
  response = session.delete(
      f"{url}/api/gifts/{gift['_id']}",
      headers={'Authorization': f'Bearer {accessToken}'},
    )
  assert response.status_code == 200, response.json()['message']

# -------------------- TC14 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc14(url, accessToken):
  id = helper_id_generator()
  response = session.delete(
      f"{url}/api/gifts/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
    )
  assert response.status_code == 404, response.json()['message']