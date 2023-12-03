import json
import os
import random

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db, redis_client

# from ..models import User
from ..schemas import UserCreate, UserResponse
import logging

if "CACHE_EXPIRATION" not in os.environ:
    from dotenv import load_dotenv

    load_dotenv()


# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Assuming you have two shards
SHARD_IDS = [0, 1]

# Cache expiration time in seconds (e.g., 1 hour)
CACHE_EXPIRATION = os.getenv("CACHE_EXPIRATION", 3600)


def determine_shard_id_for_new_user():
    # UNIFORM DISTRIBUTION FOR EACH SHARD, the uniform probability of each node
    return random.choice(SHARD_IDS)


def cache_user_data(cache_name, user_data):
    redis_client.set(cache_name, json.dumps(user_data), ex=CACHE_EXPIRATION)


def get_cached_user_data(cache_name):
    cached_user_data = redis_client.get(cache_name)
    return json.loads(cached_user_data) if cached_user_data else None


@router.post("/users/", response_model=UserResponse)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    logger.info("Received request to create user with login: %s", user_create.login)

    db_user = []
    for sh_id in SHARD_IDS:
        query = f"SELECT login FROM users WHERE login = '{user_create.login}' -- sharding:{sh_id}"
        db_user_shard = db.execute(text(query)).fetchall()
        if db_user_shard:
            db_user.extend(db_user_shard)

    if db_user:
        logger.warning(
            "Attempted to create a user with an already registered login: %s",
            user_create.login,
        )
        raise HTTPException(status_code=400, detail="Login already registered")

    shard_id = determine_shard_id_for_new_user()

    # Inserting new user data into the database
    insert_query = f"INSERT INTO users (login, first_name, last_name, email) VALUES ('{user_create.login}', '{user_create.first_name}', '{user_create.last_name}', '{user_create.email}') RETURNING *  -- sharding:{shard_id}"
    new_user = db.execute(text(insert_query)).fetchone()
    db.commit()  # Commit the transaction

    cache_user_data(user_create.login, dict(new_user._mapping))
    logger.info("User created and cached with login: %s", user_create.login)
    return new_user


@router.get("/users/{login}", response_model=UserResponse)
def read_user(login: str, db: Session = Depends(get_db)):
    logger.info("Received request to retrieve user with login: %s", login)

    cached_user = get_cached_user_data(login)
    if cached_user:
        logger.info("Found user in cache: %s", login)
        return cached_user

    user = None
    for sh_id in SHARD_IDS:
        query = f"SELECT * FROM users WHERE login = '{login}' -- sharding:{sh_id}"
        user = db.execute(text(query)).fetchone()
        if user:
            break

    if user is None:
        logger.error("User not found with login: %s", login)
        raise HTTPException(status_code=404, detail="User not found")

    cache_user_data(login, dict(user._mapping))
    logger.info("User data cached for login: %s", login)

    return user


@router.post("/users/search/", response_model=list[UserResponse])
def search_users(
    db: Session = Depends(get_db),
    first_name: str = Body(default=None),
    last_name: str = Body(default=None),
):
    logger.info("Received request to search users")

    search_key = f"search_{first_name}_{last_name}"
    cached_users = get_cached_user_data(search_key)
    if cached_users:
        logger.info("Found users in cache for search: %s", search_key)
        return cached_users

    users = []
    for sh_id in SHARD_IDS:
        conditions = []
        if first_name:
            logger.info("Filtering by first name: %s", first_name)
            conditions.append(f"first_name REGEXP '{first_name}'")
        if last_name:
            logger.info("Filtering by last name: %s", last_name)
            conditions.append(f"last_name REGEXP '{last_name}'")

        if conditions:
            query = "SELECT * FROM users WHERE " + " AND ".join(conditions)
            query += f" -- sharding:{sh_id}"
            users += db.execute(text(query)).fetchall()

    cache_user_data(search_key, [dict(user._mapping) for user in users])
    logger.info("User search results cached for key: %s", search_key)

    return users
