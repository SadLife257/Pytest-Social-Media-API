import pytest
import requests
import random
import string
import json

session = requests.Session()

# -------------------- HELPER FUNCTION --------------------
def helper_createStream(url, accessToken):
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
  
def helper_getStream(id, url, accessToken):
  response = session.get(
    f"{url}/api/streams/{id}",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  return response.json()['stream']

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
@pytest.mark.skip
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

# -------------------- TC5 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc5(url, accessToken):
  response = session.get(
    f"{url}/api/streams/recommendation",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 200

# -------------------- TC6 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc6(url, accessToken):
  response = session.post(
      f"{url}/api/streams/relevant",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'categoryIds': [
              '671a01672a386fca99c73c07'
          ]
      }
    )
  assert response.status_code == 200

# -------------------- TC7 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc7(url, accessToken):
  id = helper_id_generator()
  response = session.get(
    f"{url}/api/streams/{id}",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC9 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc9(url, accessToken):
  id = helper_id_generator()
  response = session.patch(
      f"{url}/api/streams/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'title': 'Updated Stream',
          'description': 'Pytest Stream',
          'categoryIds': [
              '671a01672a386fca99c73c07'
          ]
      }
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC10 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc10(url, accessToken):
  id = helper_id_generator()
  response = session.delete(
    f"{url}/api/streams/{id}",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC11 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc11(url, accessToken):
  id = helper_id_generator()
  response = session.post(
    f"{url}/api/streams/{id}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 500, response.json()['message']

# -------------------- TC12 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc12(url, accessToken):
  id = helper_id_generator()
  response = session.post(
    f"{url}/api/streams/{id}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 500, response.json()['message']

# -------------------- TC13 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc13(url, accessToken):
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

# -------------------- TC14 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc14(url, accessToken):
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

# -------------------- TC15 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc15(url, accessToken):
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

# -------------------- TC16 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc16(url, accessToken):
  response = session.get(
    f"{url}/api/streams",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 200

# -------------------- TC17 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc17(url, accessToken):
  response = session.get(
    f"{url}/api/streams/recommendation",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 200

# -------------------- TC18 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc18(url, accessToken):
  response = session.post(
      f"{url}/api/streams/relevant",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'categoryIds': [
              '671a01672a386fca99c73c07'
          ]
      }
    )
  assert response.status_code == 200

# -------------------- TC19 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc19(url, accessToken):
  id = helper_createStream(url, accessToken)['_id']
  response = session.get(
    f"{url}/api/streams/{id}",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 200
  helper_cleanup(id, url, accessToken)

# -------------------- TC21 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc21(url, accessToken):
  id = helper_createStream(url, accessToken)['_id']
  response = session.patch(
      f"{url}/api/streams/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'title': 'Updated Stream',
          'description': 'Pytest Stream',
          'categoryIds': [
              '671a01672a386fca99c73c07'
          ]
      }
    )
  assert response.status_code == 200
  helper_cleanup(id, url, accessToken)

# -------------------- TC22 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc22(url, accessToken):
  id = helper_createStream(url, accessToken)['_id']
  response = session.delete(
    f"{url}/api/streams/{id}",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  assert response.status_code == 200

# -------------------- TC23 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc23(url, accessToken):
  id = helper_createStream(url, accessToken)['_id']
  old_stream = helper_getStream(id, url, accessToken)
  response = session.post(
    f"{url}/api/streams/{id}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  new_stream = helper_getStream(id, url, accessToken)
  assert response.status_code == 200, response.json()['messages']
  assert new_stream['likesCount'] == old_stream['likesCount'] + 1

  helper_cleanup(id, url, accessToken)

# -------------------- TC24 --------------------
@pytest.mark.skip
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc24(url, accessToken):
  id = helper_createStream(url, accessToken)['_id']
  old_stream = helper_getStream(id, url, accessToken)
  session.post(
    f"{url}/api/streams/{id}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  response = session.post(
    f"{url}/api/streams/{id}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  new_stream = helper_getStream(id, url, accessToken)
  assert response.status_code == 200, response.json()['messages']
  assert new_stream['likesCount'] == old_stream['likesCount']

  helper_cleanup(id, url, accessToken)

# -------------------- TC25 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc25(url, accessToken):
  id = helper_createStream(url, accessToken)['_id']
  response = session.patch(
      f"{url}/api/streams/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'title': 'Updated Stream',
          'description': 'Pytest Stream',
          'categoryIds': [
              '671a01672a386fca99c73c07'
          ]
      },
      files = {
        'streamThumbnail': ('New Text Document.txt', open('imgs/New Text Document.txt', 'rb'), 'txt')
      }
    )
  assert response.status_code == 400, response.json()['messages']
  helper_cleanup(id, url, accessToken)