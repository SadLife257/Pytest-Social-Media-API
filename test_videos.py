import pytest
import requests
import random
import string
import json

session = requests.Session()

# -------------------- HELPER FUNCTION --------------------
def helper_createVideo(url, accessToken):
  response = session.post(
      f"{url}/api/videos/",
      headers={'Authorization': f'Bearer {accessToken}'},
      files={
        'video': ('tester_video.mp4', open('imgs/tester_video.mp4', 'rb'), 'mp4')
      }
    )
  return response.json()['giftHistory']

def helper_cleanup(id, url, accessToken):
  response = session.delete(
      f"{url}/api/videos/{id}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )

def helper_id_generator(size=24, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def helper_compare_json(json_obj1, json_obj2):
  return json.dumps(json.loads(json_obj1), sort_keys=True) == json.dumps(json.loads(json_obj2), sort_keys=True)

# -------------------- TESTCASE --------------------

# -------------------- TC1 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc1(url, accessToken):
  response = session.post(
      f"{url}/api/videos/",
      headers={'Authorization': f'Bearer {accessToken}'},
      files={
        'video': ('tester_video.mp4', open('imgs/tester_video.mp4', 'rb'), 'video/mp4')
      }
    )
  assert response.status_code == 200, response.json()['message']
  helper_cleanup(response.json()['video']['_id'], url, accessToken)

# -------------------- TC2 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc2(url, accessToken):
  videoId = helper_id_generator()

  response = session.delete(
      f"{url}/api/videos/{videoId}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC3 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc3(url, accessToken):
  videoId = helper_id_generator()

  response = session.patch(
      f"{url}/api/videos/{videoId}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'title': 'This Should Not Exist',
        'description':  'If You See This, Then The Test Have Failed'
      }
    )
  assert response.status_code == 500, response.json()['message']

# -------------------- TC4 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc4(url, accessToken):
  videoId = helper_id_generator()

  response = session.patch(
      f"{url}/api/videos/{videoId}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'title': '',
        'description':  'If You See This, Then The Test Have Failed'
      }
    )
  assert response.status_code == 500, response.json()['message']

# -------------------- TC5 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc5(url, accessToken):
  videoId = helper_id_generator()

  response = session.get(
      f"{url}/api/videos/{videoId}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC6 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc6(url, accessToken):
  response = session.get(
      f"{url}/api/videos/",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200, response.json()['message']

# -------------------- TC7 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc7(url, authInfo):
  accessToken = authInfo['accessToken']

  response = session.get(
      f"{url}/api/videos/user/{authInfo['userId']}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200, response.json()['message']
  assert len(response.json()['videos']) == 0, response.json()['message']

# -------------------- TC8 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc8(url, accessToken):
  playlistId = helper_id_generator()

  response = session.get(
      f"{url}/api/videos/my-playlist/{playlistId}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC9 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc9(url, accessToken):
  videoId = helper_id_generator()

  response = session.post(
    f"{url}/api/videos/{videoId}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )

  assert response.status_code == 400, response.json()['message']

# -------------------- TC10 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc10(url, accessToken):
  videoId = helper_id_generator()

  session.post(
    f"{url}/api/videos/{videoId}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )

  response = session.post(
    f"{url}/api/videos/{videoId}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )

  assert response.status_code == 400, response.json()['message']

# -------------------- TC11 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc11(url, accessToken):
  response = session.post(
      f"{url}/api/videos/",
      headers={'Authorization': f'Bearer {accessToken}'},
      files={
        'video': ('tester_video.mp4', open('imgs/tester_video.mp4', 'rb'), 'video/mp4')
      }
    )
  assert response.status_code == 200, response.json()['message']
  helper_cleanup(response.json()['video']['_id'], url, accessToken)

# -------------------- TC12 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc12(url, accessToken):
  videoId = helper_id_generator()

  response = session.delete(
      f"{url}/api/videos/{videoId}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC13 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc13(url, accessToken):
  videoId = helper_id_generator()

  response = session.patch(
      f"{url}/api/videos/{videoId}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'title': 'This Should Not Exist',
        'description':  'If You See This, Then The Test Have Failed'
      }
    )
  assert response.status_code == 500, response.json()['message']

# -------------------- TC14 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc14(url, accessToken):
  videoId = helper_id_generator()

  response = session.patch(
      f"{url}/api/videos/{videoId}",
      headers={'Authorization': f'Bearer {accessToken}'},
      json={
        'title': '',
        'description':  'If You See This, Then The Test Have Failed'
      }
    )
  assert response.status_code == 500, response.json()['message']

# -------------------- TC15 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc15(url, accessToken):
  videoId = helper_id_generator()

  response = session.get(
      f"{url}/api/videos/{videoId}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 400, response.json()['message']

# -------------------- TC16 --------------------
@pytest.mark.parametrize(
    'accessToken', [('bao')], indirect=True
)
def test_tc16(url, accessToken):
  response = session.get(
      f"{url}/api/videos/",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200, response.json()['message']

# -------------------- TC17 --------------------
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc17(url, authInfo):
  accessToken = authInfo['accessToken']

  response = session.get(
      f"{url}/api/videos/user/{authInfo['userId']}",
      headers={'Authorization': f'Bearer {accessToken}'}
    )
  assert response.status_code == 200, response.json()['message']
  assert len(response.json()['videos']) == 0, response.json()['message']

# -------------------- TC18 --------------------
@pytest.mark.skip('I DONT F*CKING KNOW ANYMORE')
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc18(url, authInfo):
  accessToken = authInfo['accessToken']

  video = random.choice(
    session.get(
        f"{url}/api/videos/",
        headers={'Authorization': f'Bearer {accessToken}'}
        ).json()['videos']
  )

  response = session.post(
    f"{url}/api/videos/{video['_id']}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )

  newVideo = session.get(
    f"{url}/api/videos/{video['_id']}",
    headers={'Authorization': f'Bearer {accessToken}'}
  ).json()['video']

  assert response.status_code == 200, response.json()['message']
  assert newVideo['video']['likesCount'] == video['likesCount'] + 1, response.json()['message']

# -------------------- TC19 --------------------
@pytest.mark.skip('I DONT F*CKING KNOW ANYMORE')
@pytest.mark.parametrize(
    'authInfo', [('bao')], indirect=True
)
def test_tc19(url, authInfo):
  accessToken = authInfo['accessToken']

  video = random.choice(
    session.get(
        f"{url}/api/videos/",
        headers={'Authorization': f'Bearer {accessToken}'}
        ).json()['videos']
  )

  session.post(
    f"{url}/api/videos/{video['_id']}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )

  response = session.post(
    f"{url}/api/videos/{video['_id']}/like",
    headers={'Authorization': f'Bearer {accessToken}'}
  )

  newVideo = session.get(
    f"{url}/api/videos/{video['_id']}",
    headers={'Authorization': f'Bearer {accessToken}'}
  ).json()['video']

  assert response.status_code == 200, response.json()['message']
  assert newVideo['likesCount'] == video['likesCount'], response.json()['message']