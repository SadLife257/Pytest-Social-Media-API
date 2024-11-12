import pytest
import requests
import random
import string
import json

session = requests.Session()

# -------------------- HELPER FUNCTION --------------------
def helper_createCategory(url, accessToken):
  response = session.post(
      f"{url}/api/categories",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'name': 'New Categories',
          'categoryUrl': ''
      }
    )
  return response.json()['category']

def helper_cleanup(id, url, accessToken):
  response = session.delete(
      f"{url}/api/categories/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )

def helper_id_generator(size=24, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def helper_compare_json(json_obj1, json_obj2):
  return json.dumps(json.loads(json_obj1), sort_keys=True) == json.dumps(json.loads(json_obj2), sort_keys=True)

# -------------------- TESTCASE --------------------

# -------------------- TC1 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc1(url, accessToken):
  response = session.get(f"{url}/api/categories", headers={'Authorization': f'Bearer {accessToken}'})
  assert response.status_code == 200
  print(response.json()['message'])

# -------------------- TC2 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc2(url, accessToken):
  response = session.post(
      f"{url}/api/categories",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'New Categories'
      },
      files={
          'categoryUrl': ('tester_img.jpg', open('/content/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 201
  helper_cleanup(response.json()['category']['_id'], url, accessToken)

# -------------------- TC3 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc3(url, accessToken):
  response = session.post(
      f"{url}/api/categories",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'name': '',
          'categoryUrl': ''
      }
    )
  assert response.status_code == 400

# -------------------- TC4 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc4(url, accessToken):
  response = session.post(
      f"{url}/api/categories",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'New Categories'
      },
      files={
          'categoryUrl': ('New Text Document.txt', open('/content/New Text Document.txt', 'rb'), 'txt')
      }
    )
  assert response.status_code == 400

# -------------------- TC5 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc5(url, accessToken):
  category = helper_createCategory(url, accessToken)
  response = session.get(f"{url}/api/categories/{category['_id']}", headers={'Authorization': f'Bearer {accessToken}'})
  assert response.status_code == 200, helper_compare_json(response.json()['category'], category)
  helper_cleanup(category['_id'], url, accessToken)

# -------------------- TC6 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc6(url, accessToken):
  id = helper_id_generator()
  response = session.get(f"{url}/api/categories/{id}", headers={'Authorization': f'Bearer {accessToken}'})
  assert response.status_code == 400

# -------------------- TC7 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc7(url, accessToken):
  id = helper_createCategory(url, accessToken)['_id']
  response = session.put(
      f"{url}/api/categories/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'name': 'Updated Categories',
          'categoryUrl': ''
      }
    )
  assert response.status_code == 200
  helper_cleanup(id, url, accessToken)

# -------------------- TC8 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc8(url, accessToken):
  id = helper_createCategory(url, accessToken)['_id']
  response = session.delete(
      f"{url}/api/categories/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200

# -------------------- TC9 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc9(url, accessToken):
  id = helper_id_generator()
  response = session.delete(
      f"{url}/api/categories/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 400

# -------------------- TC10 --------------------
@pytest.mark.skip('DONE')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc10(url, accessToken):
  id = helper_createCategory(url, accessToken)['_id']
  response = session.put(
      f"{url}/api/categories/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': 'Updated Categories'
      },
      files={
          'categoryImg': ('New Text Document.txt', open('/content/New Text Document.txt', 'rb'), 'txt')
      }
    )
  assert response.status_code == 400
  helper_cleanup(id, url, accessToken)

# -------------------- TC11 --------------------
@pytest.mark.skip('CURRENTLY FIXING')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc11(url, accessToken):
  id = helper_createCategory(url, accessToken)['_id']
  response = session.put(
      f"{url}/api/categories/{id}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'name': '',
          'categoryUrl': ''
      }
    )
  assert response.status_code == 400
  helper_cleanup(id, url, accessToken)

# -------------------- TC12 --------------------
@pytest.mark.skip('CURRENTLY FIXING')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc12(url, accessToken):
  response = session.post(
      f"{url}/api/categories",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': '/^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]*$/'
      },
      files={
          'categoryUrl': ('tester_img.jpg', open('/content/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 400
  helper_cleanup(response.json()['category']['_id'], url, accessToken)

# -------------------- TC13 --------------------
@pytest.mark.skip('CURRENTLY FIXING')
@pytest.mark.parametrize(
    'accessToken', [('admin')], indirect=True
)
def test_tc13(url, accessToken):
  category = helper_createCategory(url, accessToken)
  response = session.post(
      f"{url}/api/categories",
      headers={'Authorization': f'Bearer {accessToken}'},
      data={
          'name': category['name']
      },
      files={
          'categoryUrl': ('tester_img.jpg', open('/content/tester_img.jpg', 'rb'), 'image/jpeg')
      }
    )
  assert response.status_code == 400
  helper_cleanup(response.json()['category']['_id'], url, accessToken)
  helper_cleanup(category['_id'], url, accessToken)