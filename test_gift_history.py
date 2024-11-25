import pytest
import requests
import random
import string
import json

session = requests.Session()

# -------------------- HELPER FUNCTION --------------------
def helper_getUser(id, url, accessToken):
  response = session.get(
    f"{url}/api/users/{id}",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  return response.json()['user']

def helper_getRandomStream(url, accessToken):
  response = session.get(
    f"{url}/api/streams",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  return random.choice(response.json()['streams'])

def helper_getRandomGift(url, accessToken):
  response = session.get(
    f"{url}/api/gifts",
    headers={'Authorization': f'Bearer {accessToken}'}
  )
  return random.choice(response.json()['gifts'])

def helper_createGiftHistory(stream, gift, url, accessToken):
  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': 1
            }
          ]
      }
    )
  return response.json()['giftHistory']

def helper_cleanup(id, url, accessToken):
  response = session.delete(
      f"{url}/api/gift-history/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )

def helper_id_generator(size=24, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def helper_compare_json(json_obj1, json_obj2):
  return json.dumps(json.loads(json_obj1), sort_keys=True) == json.dumps(json.loads(json_obj2), sort_keys=True)

# -------------------- TESTCASE --------------------

# -------------------- TC1 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc1(url, authInfo):
  accessToken = authInfo['accessToken']
  user = helper_getUser(authInfo['userId'], url, accessToken)
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)

  if(user['wallet']['coin'] < gift['valuePerUnit']):
    session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': gift['valuePerUnit'],
            'actionCurrencyType': 'ReceiveCoin',
            'exchangeRate': 0
        }
    )

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': 1
            }
          ]
      }
    )
  assert response.status_code == 201, response.json()['message']
  helper_cleanup(response.json()['giftHistory']['_id'], url, accessToken)

# -------------------- TC2 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc2(url, authInfo):
  accessToken = authInfo['accessToken']
  user = helper_getUser(authInfo['userId'], url, accessToken)
  streamId = helper_id_generator()
  gift = helper_getRandomGift(url, accessToken)

  if(user['wallet']['coin'] < gift['valuePerUnit']):
    session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': gift['valuePerUnit'],
            'actionCurrencyType': 'ReceiveCoin',
            'exchangeRate': 0
        }
    )

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': streamId,
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': 1
            }
          ]
      }
    )
  assert response.status_code == 400, response.json()['message']

  response = session.put(
    f"{url}/api/users/{user['_id']}/wallet",
    headers={'Authorization': f'Bearer {accessToken}'},
    json={
      'amount': gift['valuePerUnit'],
      'actionCurrencyType': 'SpendCoin',
      'exchangeRate': 0
    }
  )

# -------------------- TC3 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc3(url, authInfo):
  accessToken = authInfo['accessToken']
  stream = helper_getRandomStream(url, accessToken)
  giftId = helper_id_generator()

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': giftId,
              'quantity': 1
            }
          ]
      }
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC4 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc4(url, authInfo):
  accessToken = authInfo['accessToken']
  user = helper_getUser(authInfo['userId'], url, accessToken)
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)

  if(user['wallet']['coin'] < gift['valuePerUnit']):
    session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': gift['valuePerUnit'],
            'actionCurrencyType': 'ReceiveCoin',
            'exchangeRate': 0
        }
    )

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': -1
            }
          ]
      }
    )
  
  assert response.status_code == 400, response.json()['message']

  response = session.put(
    f"{url}/api/users/{user['_id']}/wallet",
    headers={'Authorization': f'Bearer {accessToken}'},
    json={
      'amount': gift['valuePerUnit'],
      'actionCurrencyType': 'SpendCoin',
      'exchangeRate': 0
    }
  )

# -------------------- TC5 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc5(url, authInfo):
  accessToken = authInfo['accessToken']
  user = helper_getUser(authInfo['userId'], url, accessToken)
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)

  if(user['wallet']['coin'] < gift['valuePerUnit']):
    session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': gift['valuePerUnit'],
            'actionCurrencyType': 'ReceiveCoin',
            'exchangeRate': 0
        }
    )

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': 0
            }
          ]
      }
    )
  
  assert response.status_code == 400, response.json()['message']

  response = session.put(
    f"{url}/api/users/{user['_id']}/wallet",
    headers={'Authorization': f'Bearer {accessToken}'},
    json={
      'amount': gift['valuePerUnit'],
      'actionCurrencyType': 'SpendCoin',
      'exchangeRate': 0
    }
  )

# -------------------- TC6 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc6(url, authInfo):
  accessToken = authInfo['accessToken']
  user = helper_getUser(authInfo['userId'], url, accessToken)
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)
  userOldCoin = user['wallet']['coin']

  if(user['wallet']['coin'] > gift['valuePerUnit']):
    session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': userOldCoin,
            'actionCurrencyType': 'SpendCoin',
            'exchangeRate': 0
        }
    )

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': 1
            }
          ]
      }
    )
  assert response.status_code == 400, response.json()['message']

  session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': userOldCoin,
            'actionCurrencyType': 'ReceiveCoin',
            'exchangeRate': 0
        }
    )

# -------------------- TC7 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc7(url, authInfo):
  accessToken = authInfo['accessToken']
  streamId = helper_id_generator()
  gift = helper_getRandomGift(url, accessToken)

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': streamId,
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': 1
            }
          ]
      }
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC8 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc8(url, authInfo):
  accessToken = authInfo['accessToken']
  stream = helper_getRandomStream(url, accessToken)
  giftId = helper_id_generator()

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': giftId,
              'quantity': 1
            }
          ]
      }
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC9 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc9(url, authInfo):
  accessToken = authInfo['accessToken']
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': -1
            }
          ]
      }
    )
  
  assert response.status_code == 400, response.json()['message']

# -------------------- TC10 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc10(url, authInfo):
  accessToken = authInfo['accessToken']
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)

  response = session.post(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
          'streamId': stream['_id'],
          'gifts': [
            {
              'giftId': gift['_id'],
              'quantity': 0
            }
          ]
      }
    )
  
  assert response.status_code == 400, response.json()['message']

# -------------------- TC11 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc11(url, authInfo):
  accessToken = authInfo['accessToken']

  response = session.get(
      f"{url}/api/gift-history/",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  
  try:
    assert response.status_code == 200, response.json()['message']
  except:
    assert response.status_code == 404, response.json()['message']

# -------------------- TC12 --------------------
@pytest.mark.parametrize(
    'authInfo', [('admin')], indirect=True
)
def test_tc12(url, authInfo):
  accessToken = authInfo['accessToken']
  user = helper_getUser(authInfo['userId'], url, accessToken)
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)

  if(user['wallet']['coin'] < gift['valuePerUnit']):
    session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': gift['valuePerUnit'],
            'actionCurrencyType': 'ReceiveCoin',
            'exchangeRate': 0
        }
    )
  
  giftHistory = helper_createGiftHistory(stream, gift, url, accessToken)

  response = session.get(
    f"{url}/api/gift-history/streams/{stream['_id']}",
    headers={'Authorization': f'Bearer {accessToken}'},
  )
  
  assert response.status_code == 200, response.json()['message']
  helper_cleanup(giftHistory['_id'], url, accessToken)

# -------------------- TC13 --------------------
@pytest.mark.parametrize(
    'authInfo', [('admin')], indirect=True
)
def test_tc13(url, authInfo):
  accessToken = authInfo['accessToken']
  streamId = helper_id_generator()

  response = session.get(
    f"{url}/api/gift-history/streams/{streamId}",
    headers={'Authorization': f'Bearer {accessToken}'},
  )
  
  # assert response.status_code == 200, response.json()['message']
  assert response.status_code == 500, response.json()['message']

# -------------------- TC14 --------------------
@pytest.mark.parametrize(
    'authInfo', [('admin')], indirect=True
)
def test_tc14(url, authInfo):
  accessToken = authInfo['accessToken']
  user = helper_getUser(authInfo['userId'], url, accessToken)
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)

  if(user['wallet']['coin'] < gift['valuePerUnit']):
    session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': gift['valuePerUnit'],
            'actionCurrencyType': 'ReceiveCoin',
            'exchangeRate': 0
        }
    )
  
  giftHistory = helper_createGiftHistory(stream, gift, url, accessToken)

  response = session.get(
    f"{url}/api/gift-history/{giftHistory['_id']}",
    headers={'Authorization': f'Bearer {accessToken}'},
  )
  
  assert response.status_code == 200, response.json()['message']
  helper_cleanup(giftHistory['_id'], url, accessToken)

# -------------------- TC15 --------------------
@pytest.mark.parametrize(
    'authInfo', [('admin')], indirect=True
)
def test_tc15(url, authInfo):
  accessToken = authInfo['accessToken']
  giftHistoryId = helper_id_generator()

  response = session.get(
    f"{url}/api/gift-history/{giftHistoryId}",
    headers={'Authorization': f'Bearer {accessToken}'},
  )
  
  assert response.status_code == 500, response.json()['message']

# -------------------- TC16 --------------------
@pytest.mark.parametrize(
    'authInfo', [('admin')], indirect=True
)
def test_tc16(url, authInfo):
  accessToken = authInfo['accessToken']
  user = helper_getUser(authInfo['userId'], url, accessToken)
  stream = helper_getRandomStream(url, accessToken)
  gift = helper_getRandomGift(url, accessToken)

  if(user['wallet']['coin'] < gift['valuePerUnit']):
    session.put(
        f"{url}/api/users/{user['_id']}/wallet",
        headers={'Authorization': f'Bearer {accessToken}'},
        json={
            'amount': gift['valuePerUnit'],
            'actionCurrencyType': 'ReceiveCoin',
            'exchangeRate': 0
        }
    )
  
  giftHistory = helper_createGiftHistory(stream, gift, url, accessToken)

  response = session.delete(
    f"{url}/api/gift-history/{giftHistory['_id']}",
    headers={'Authorization': f'Bearer {accessToken}'},
  )
  
  assert response.status_code == 200, response.json()['message']

# -------------------- TC17 --------------------
@pytest.mark.parametrize(
    'authInfo', [('admin')], indirect=True
)
def test_tc17(url, authInfo):
  accessToken = authInfo['accessToken']
  giftHistoryId = helper_id_generator()

  response = session.delete(
    f"{url}/api/gift-history/{giftHistoryId}",
    headers={'Authorization': f'Bearer {accessToken}'},
  )
  
  assert response.status_code == 500, response.json()['message']

# -------------------- TC18 --------------------
# -------------------- TC19 --------------------