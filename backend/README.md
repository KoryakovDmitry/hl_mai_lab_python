# backend market service

### Create .env file in 

```
#DB_HOST=mai-db-node-ex01
DB_HOST=localhost
#DB_PORT=3306
DB_PORT=3360
DB_USER=stud
DB_PASSWORD=stud
DB_DATABASE=archdb
```

### Run this service via terminal and venv in dev mode:

```bash
python -m venv venv_backend

source venv_backend/bin/activate

cd backend

pip3 install -r requirements.txt

uvicorn src.main:app --reload
```

### See the docs

You can use FastAPI's automatic interactive API documentation, Swagger UI by navigating to:

http://localhost:8000/docs

### Tests

```bash
python -m unittest -v tests/init_service_test.py
python -m unittest -v tests/get_service_test.py
```
