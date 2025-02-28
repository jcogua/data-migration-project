from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# Create the base for the models
Base = declarative_base()

# Model for the hired_employees table
class HiredEmployee(Base):
    __tablename__ = 'hired_employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    datetime = Column(String)
    department_id = Column(Integer)
    job_id = Column(Integer)

    def __repr__(self):
        return f"<HiredEmployee(id={self.id}, name={self.name}, datetime={self.datetime}, department_id={self.department_id}, job_id={self.job_id})>"

# Model for the departments table
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    department = Column(String)

    def __repr__(self):
        return f"<Department(id={self.id}, department={self.department})>"

# Model for the jobs table
class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    job = Column(String)

    def __repr__(self):
        return f"<Job(id={self.id}, job={self.job})>"
    
class EmployeeCreate(BaseModel):
    name: str
    datetime: str
    department_id: int
    job_id: int
    
class DepartmentCreate(BaseModel):
    department: str
    
class JobCreate(BaseModel):
    job: str