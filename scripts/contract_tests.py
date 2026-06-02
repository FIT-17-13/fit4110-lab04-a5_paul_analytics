import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE = 'http://127.0.0.1:8000'
HEADERS = {'Authorization': 'Bearer local-dev-token', 'Content-Type': 'application/json'}

def post(path, payload, headers=HEADERS):
    url = BASE + path
    data = json.dumps(payload).encode('utf-8')
    req = Request(url, data=data, headers=headers, method='POST')
    try:
        with urlopen(req, timeout=5) as r:
            body = r.read().decode('utf-8')
            print('Status:', r.status)
            print('Headers:', dict(r.getheaders()))
            print('Body:', body)
            return r.status, body
    except HTTPError as e:
        body = e.read().decode('utf-8') if e.fp else ''
        print('Status:', e.code)
        print('Body:', body)
        return e.code, body

def get(path, headers=HEADERS):
    url = BASE + path
    req = Request(url, headers=headers, method='GET')
    try:
        with urlopen(req, timeout=5) as r:
            body = r.read().decode('utf-8')
            print('Status:', r.status)
            print('Body:', body)
            return r.status, body
    except HTTPError as e:
        body = e.read().decode('utf-8') if e.fp else ''
        print('Status:', e.code)
        print('Body:', body)
        return e.code, body

if __name__ == '__main__':
    # TEST1: valid 31.5
    print('--- TEST1: POST valid 31.5')
    s, b = post('/readings', {
        'device_id': 'ESP32-LAB-A01',
        'metric': 'temperature',
        'value': 31.5,
        'unit': 'celsius',
        'timestamp': '2026-05-13T08:30:00+07:00'
    })

    # TEST2: missing auth
    print('\n--- TEST2: POST without Authorization (expect 401)')
    s, b = post('/readings', {
        'device_id': 'ESP32-LAB-A01',
        'metric': 'temperature',
        'value': 31.5,
        'unit': 'celsius',
        'timestamp': '2026-05-13T08:30:00+07:00'
    }, headers={'Content-Type':'application/json'})

    # TEST3: boundary 80
    print('\n--- TEST3: POST 80 (expect 201 + X-Warning)')
    s, b = post('/readings', {
        'device_id': 'ESP32-LAB-A01',
        'metric': 'temperature',
        'value': 80,
        'unit': 'celsius',
        'timestamp': '2026-05-13T08:30:00+07:00'
    })

    # TEST4: 81
    print('\n--- TEST4: POST 81 (expect 422)')
    s, b = post('/readings', {
        'device_id': 'ESP32-LAB-A01',
        'metric': 'temperature',
        'value': 81,
        'unit': 'celsius',
        'timestamp': '2026-05-13T08:30:00+07:00'
    })

    # TEST5: -40
    print('\n--- TEST5: POST -40 (expect 201)')
    s, b = post('/readings', {
        'device_id': 'ESP32-LAB-A01',
        'metric': 'temperature',
        'value': -40,
        'unit': 'celsius',
        'timestamp': '2026-05-13T08:30:00+07:00'
    })

    # TEST6: -41
    print('\n--- TEST6: POST -41 (expect 422)')
    s, b = post('/readings', {
        'device_id': 'ESP32-LAB-A01',
        'metric': 'temperature',
        'value': -41,
        'unit': 'celsius',
        'timestamp': '2026-05-13T08:30:00+07:00'
    })

    # TEST7: GET latest
    print('\n--- TEST7: GET /readings/latest')
    s, b = get('/readings/latest?device_id=ESP32-LAB-A01&limit=10')

    # If any reading id returned earlier, try GET by id
    try:
        created = json.loads(b)
        if isinstance(created, dict) and 'reading_id' in created:
            rid = created['reading_id']
            print('\n--- TEST8: GET /readings/{id} for', rid)
            s, b = get(f'/readings/{rid}')
    except Exception:
        pass
