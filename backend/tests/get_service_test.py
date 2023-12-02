# import os
import unittest
import logging
import requests

# from dotenv import load_dotenv
# from sqlalchemy import create_engine, inspect, text

logging.basicConfig(level=logging.INFO)


class TestFastAPIEndpoints(unittest.TestCase):
    BASE_URL = "http://localhost:8000"
    # # Load environment variables
    # load_dotenv()
    #
    # SQLALCHEMY_DATABASE_URL = os.getenv(
    #     "SQLALCHEMY_DATABASE_URL", "mysql+pymysql://user:password@localhost:3360/dbname"
    # )
    #
    # engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # # Create an inspector object
    # inspector = inspect(engine)
    #
    # with engine.begin() as conn:
    #     # Retrieve the names of all tables in the database
    #     table_names = inspector.get_table_names()
    #
    #     # Iterate over each table and delete all rows
    #     for table_name in table_names:
    #         conn.execute(text(f"DELETE FROM {table_name};"))

    def test_4_read_user(self):
        login = "john123"
        url = f"{self.BASE_URL}/users/users/{login}"
        response = requests.get(url)
        logging.info(
            f"Reading user {login}: status {response.status_code}, response {response.json()}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["login"], login)

    def test_5_search_users(self):
        url = f"{self.BASE_URL}/users/users/search/"
        data = {
            "first_name": "^J.*",  # Regex pattern for first names starting with 'J'
            "last_name": ".*o.*",  # Regex pattern for last names containing 'o'
        }
        response = requests.post(url, json=data)
        logging.info(
            f"Searching users: status {response.status_code}, response {response.json()}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))

    def test_6_get_services(self):
        url = f"{self.BASE_URL}/services/services/"
        response = requests.get(url)
        logging.info(
            f"Getting services: status {response.status_code}, response {response.json()}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))

    def test_8_get_user_orders(self):
        user_id = 1
        url = f"{self.BASE_URL}/orders/orders/{user_id}"
        response = requests.get(url)
        logging.info(
            f"Getting orders for user_id {user_id}: status {response.status_code}, response {response.json()}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))

    def test_9_read_user(self):
        login = "sophia321"
        url = f"{self.BASE_URL}/users/users/{login}"
        response = requests.get(url)
        logging.info(
            f"Reading user {login}: status {response.status_code}, response {response.json()}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["login"], login)
    def test_X_search_users(self):
        url = f"{self.BASE_URL}/users/users/search/"
        data = {
            "first_name": "^J.*",  # Regex pattern for first names starting with 'J'
            "last_name": ".*o.*",  # Regex pattern for last names containing 'o'
        }
        response = requests.post(url, json=data)
        logging.info(
            f"Searching users: status {response.status_code}, response {response.json()}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))


if __name__ == "__main__":
    unittest.main()
