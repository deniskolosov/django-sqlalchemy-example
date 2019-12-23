
To run: 

```
docker-compose up
```

To test endpoints, at first, get token by POSTing to `http://localhost:8000/api/auth/`:


```
$ curl -d '{"email":"joe@mail.com", "password":"hello123"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/auth/

{"pk": 1, "first_name": "Joe", "last_name": "Doe", "middle_name": "Jr", "birth_date": "2000-05-19T00:00:00", "nationality": "United States", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImpvZUBtYWlsLmNvbSJ9.8askqic_PZerHdKIX4LmH1j0QuMfcrLqQjH31zgNgJc"}
```

then, using the token, check user profile:
```
curl -X GET 'http://127.0.01:8000/profiles/me/?password=hello123' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImpvZUBtYWlsLmNvbSJ9.8askqic_PZerHdKIX4LmH1j0QuMfcrLqQjH31zgNgJc'

{"pk": 1, "first_name": "Joe", "last_name": "Doe", "middle_name": "Jr", "birth_date": "2000-05-19T00:00:00", "nationality": "United States", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImpvZUBtYWlsLmNvbSJ9.8askqic_PZerHdKIX4LmH1j0QuMfcrLqQjH31zgNgJc"}
```
Note: although if you use HTTPS, query parameters will be not seen, it's not safe to pass passwords in query string, so this example just for illustrational purposes only

To run tests:
```
docker-compose run web ./manage.py test
```
