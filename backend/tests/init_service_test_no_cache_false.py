# import os
import json
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

    def test_1_create_users(self):
        with open("data/users.json", "r") as f:
            user_data = json.load(f)

        for user in user_data:
            response = requests.post(f"{self.BASE_URL}/users/users/", json=user, params={"no_cache": False})
            logging.info(
                f"Creating user {user['login']}: status {response.status_code}, response {response.json()}"
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(user["login"], response.json()["login"])

    def test_2_create_services(self):
        service_data = [
            {
                "name": "Web Development",
                "description": "Professional website development services",
                "cost": 250.00,
            },
            {
                "name": "Graphic Design",
                "description": "Creative graphic design services",
                "cost": 150.00,
            },
            {
                "name": "Digital Marketing",
                "description": "Effective online marketing strategies",
                "cost": 300.00,
            },
        ]

        for service in service_data:
            response = requests.post(
                f"{self.BASE_URL}/services/services/", json=service
            )
            logging.info(
                f"Creating service {service['name']}: status {response.status_code}, response {response.json()}"
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(service["name"], response.json()["name"])

    def test_3_create_orders(self):
        # Assuming services with IDs 1, 2, 3 have been created in the test_2_create_services
        order_data = [
            {
                "user_id": 1,
                "service_ids": [
                    1,
                ],
            },
            {"user_id": 2, "service_ids": [2, 3]},
            {"user_id": 3, "service_ids": [1, 3]},
        ]

        for order in order_data:
            response = requests.post(f"{self.BASE_URL}/orders/orders/", json=order)
            logging.info(
                f"Creating order for user_id {order['user_id']}: status {response.status_code}, response {response.json()}"
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(order["user_id"], response.json()["user_id"])
            # Verify if the correct number of services are associated with the order
            self.assertEqual(
                len(response.json()["services"]), len(order["service_ids"])
            )

    def test_4_read_user(self):
        login = "john123"
        url = f"{self.BASE_URL}/users/users/{login}"
        response = requests.get(url, params={"no_cache": False})
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
        response = requests.post(url, json=data, params={"no_cache": False})
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

    def test_7_add_services_to_order(self):
        # Example order and service IDs
        order_id = 1
        service_ids_to_add = [2, 3]  # Assuming these service IDs exist

        # Construct the request URL and payload
        url = f"{self.BASE_URL}/orders/orders/{order_id}/add_service"
        service_data = {"service_ids": service_ids_to_add}

        # Make the request to add services
        response = requests.post(url, json=service_data)
        logging.info(
            f"Adding services to order {order_id}: status {response.status_code}, response {response.json()}"
        )

        self.assertEqual(response.status_code, 200)

        # Fetch the updated order to verify the added services
        order_response = requests.get(f"{self.BASE_URL}/orders/orders/{order_id}")
        logging.info(
            f"Getting order {order_id} after adding services: status {order_response.status_code}, response {order_response.json()}"
        )

        self.assertEqual(order_response.status_code, 200)
        order_services = [
            service["id"] for service in order_response.json()[0]["services"]
        ]

        # Check if all provided service IDs are in the order's services
        for service_id in service_ids_to_add:
            self.assertIn(service_id, order_services)

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
        response = requests.get(url, params={"no_cache": False})
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
        response = requests.post(url, json=data, params={"no_cache": False})
        logging.info(
            f"Searching users: status {response.status_code}, response {response.json()}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))


if __name__ == "__main__":
    unittest.main()
