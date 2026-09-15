import requests
import json

def test_pti():
    from_time = "2026/07/20 00:00:00"
    end_time = "2026/07/20 23:59:59"
    resource_host = 'http://editorial.pti.in/ptiapi/webservice1.asmx/JsonFile1'
    
    # Using the exact key the user provided
    centercode = '24022026001MNT'
    
    params = {
        'centercode': centercode,
        'FromTime': from_time,
        'EndTime': end_time
    }
    
    print(f"Fetching with centercode: {centercode}")
    try:
        response = requests.get(resource_host, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.text.strip():
            print("Response length:", len(response.text))
            print("First 200 chars:", response.text[:200])
        else:
            print("Response is empty!")
    except Exception as e:
        print("Error:", e)

test_pti()
