import os

import streamlit as st
import requests

from dotenv import load_dotenv

load_dotenv()


MARKET_SERVICE_HOST = os.getenv("MARKET_SERVICE_HOST", "localhost")
MARKET_SERVICE_PORT = int(os.getenv("MARKET_SERVICE_PORT", 8000))

BASE_URL = f"http://{MARKET_SERVICE_HOST}:{MARKET_SERVICE_PORT}"


# Function to handle API requests
def make_request(method, endpoint, payload=None):
    url = f"{BASE_URL}{endpoint}"
    if method == "GET":
        response = requests.get(url)
    else:
        response = requests.post(url, json=payload)
    return response


st.set_page_config(
    page_title="Service Management App",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📝",
)

st.sidebar.title("Service Management")

# Create User
st.header("Create a New User")
user_login = st.text_input("Login")
user_first_name = st.text_input("First Name")
user_last_name = st.text_input("Last Name")
user_email = st.text_input("Email")
if st.button("Create User"):
    user_data = {
        "login": user_login,
        "first_name": user_first_name,
        "last_name": user_last_name,
        "email": user_email,
    }
    response = make_request("POST", "/users/users/", user_data)
    st.write(response.json())

# Create Service
st.header("Create a New Service")
service_name = st.text_input("Service Name")
service_description = st.text_area("Service Description")
service_cost = st.number_input("Service Cost", min_value=0.0, step=0.01)
if st.button("Create Service"):
    service_data = {
        "name": service_name,
        "description": service_description,
        "cost": service_cost,
    }
    response = make_request("POST", "/services/services/", service_data)
    st.write(response.json())

# Create Order
st.header("Create a New Order")
order_user_id = st.number_input("User ID", min_value=1, step=1)
response = make_request("GET", "/services/services/")
services = response.json()
if isinstance(services, list):
    order_service_ids = st.multiselect(
        "Select Services", options=services
    )  # Update options based on your services
    order_services_ids_to_add = [s.get("id") for s in order_service_ids if "id" in s]
    if st.button("Create Order"):
        order_data = {
            "user_id": order_user_id,
            "service_ids": order_services_ids_to_add,
        }
        response = make_request("POST", "/orders/orders/", order_data)
        st.write(response.json())

# Read User Information
st.header("Read User Information")
search_login = st.text_input("Enter User Login to Search")
if st.button("Get User Info"):
    response = make_request("GET", f"/users/users/{search_login}")
    st.write(response.json())

# Search Users
st.header("Search for Users")
search_first_name = st.text_input("First Name Pattern")
search_last_name = st.text_input("Last Name Pattern")
if st.button("Search Users"):
    data = {"first_name": search_first_name, "last_name": search_last_name}
    response = make_request("POST", "/users/users/search/", data)
    st.write(response.json())

# List All Services
st.header("List All Services")
if st.button("Show Services"):
    response = make_request("GET", "/services/services/")
    services = response.json()
    st.write(response.json())

# Add Services to Order
st.header("Add Services to an Order")
add_to_order_id = st.number_input("Order ID to Add Services", min_value=1, step=1)
response = make_request("GET", "/services/services/")
services = response.json()
if isinstance(services, list):
    services_to_add = st.multiselect(
        "Select Services to Add", options=services
    )  # Update options based on your services
    services_ids_to_add = [s.get("id") for s in services_to_add if "id" in s]
    if st.button("Add Services to Order"):
        data = {"service_ids": services_ids_to_add}
        response = make_request(
            "POST", f"/orders/orders/{add_to_order_id}/add_service", data
        )
        st.write(response.json())

# List Orders for a User
st.header("List Orders for a User")
orders_user_id = st.number_input("Enter User ID to List Orders", min_value=1, step=1)
if st.button("List Orders"):
    response = make_request("GET", f"/orders/orders/{orders_user_id}")
    st.write(response.json())
