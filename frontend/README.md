# frontend market service

### Create .env file in 

```
MARKET_SERVICE_HOST=localhost
MARKET_SERVICE_PORT=8000
```

### Run this service via terminal and venv in dev mode:

```bash
python -m venv venv_frontend

source venv_frontend/bin/activate

cd frontend

pip3 install -r requirements.txt

streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```
