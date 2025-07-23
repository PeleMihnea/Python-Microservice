# src/math_microservice/db/base.py
from sqlalchemy.ext.declarative import declarative_base

# this is the parent for all your ORM models
Base = declarative_base()
