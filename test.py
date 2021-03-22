from requests import get, post, put, delete

print(post('http://localhost:5000/api/user',
           json={'id': 4,
                 'surname': 'Sokolov',
                 'name': 'Azya_Gay',
                 'age': 17,
                 'position': "gachi gym",
                 'speciality': 'Nitik',
                 'address': '-',
                 'email': 'AzyaDr@yandex.ru',
                 'hashed_password': 'OI#@RIU@#HIRNw4fgknwerpgjn',
                 'city_from': 'Kostroma'
                 }).json())

print(get('http://localhost:5000/api/user/4').json())