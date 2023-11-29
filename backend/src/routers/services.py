import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Service
from ..schemas import ServiceCreate, ServiceResponse

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/services/", response_model=ServiceResponse)
def create_service(service_create: ServiceCreate, db: Session = Depends(get_db)):
    logger.info("Received request to create service with name: %s", service_create.name)

    # This endpoint will create a service with the given name, description, and cost
    new_service = Service(
        name=service_create.name,
        description=service_create.description,
        cost=service_create.cost,
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    logger.info("Service created with name: %s", service_create.name)

    return new_service


@router.get("/services/", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    logger.info("Received request to retrieve all services")

    # This endpoint will retrieve all services
    services = db.query(Service).all()
    return services
