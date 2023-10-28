import requests

response = requests.get('http://127.0.0.1:5000/ad/2/',
                        json={
                            'header': 'test3',
                            'description': 'test3',
                            'owner': 'test3'
                        }
                        )
print(response.status_code)
print(response.json())
