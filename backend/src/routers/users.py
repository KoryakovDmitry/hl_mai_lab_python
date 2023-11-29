from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    logger.info("Received request to create user with login: %s", user_create.login)

    # This endpoint will create a user with the given login, password, name, and email
    db_user = db.query(User).filter(User.login == user_create.login).first()
    if db_user:
        logger.warning("Attempted to create a user with an already registered login: %s", user_create.login)

        raise HTTPException(status_code=400, detail="Login already registered")
    new_user = User(
        login=user_create.login,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info("User created with login: %s", user_create.login)

    return new_user


@router.get("/users/{login}", response_model=UserResponse)
def read_user(login: str, db: Session = Depends(get_db)):
    logger.info("Received request to retrieve user with login: %s", login)

    # This endpoint will retrieve a user by login
    user = db.query(User).filter(User.login == login).first()
    if user is None:
        logger.error("User not found with login: %s", login)

        raise HTTPException(status_code=404, detail="User not found")
    return user


# @router.get("/users/search/", response_model=list[UserResponse])
# def search_users(
#     first_name: str = None, last_name: str = None, db: Session = Depends(get_db)
# ):
#     # This endpoint will search users by regex on first and last name
#     query = db.query(User)
#     if first_name:
#         query = query.filter(func.regexp_match(User.first_name, first_name))
#     if last_name:
#         query = query.filter(func.regexp_match(User.last_name, last_name))
#     users = query.all()
#     return users


@router.post("/users/search/", response_model=list[UserResponse])
def search_users(
    db: Session = Depends(get_db),
    first_name: str = Body(default=None),
    last_name: str = Body(default=None),
):
    logger.info("Received request to search users")

    query = db.query(User)
    if first_name:
        logger.info("Filtering by first name: %s", first_name)

        query = query.filter(User.first_name.op("REGEXP")(first_name))
    if last_name:
        logger.info("Filtering by last name: %s", last_name)

        query = query.filter(User.last_name.op("REGEXP")(last_name))
    users = query.all()
    return users
