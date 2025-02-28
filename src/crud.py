
from sqlalchemy import func
from fastapi import HTTPException
from models import HiredEmployee, Department, Job, EmployeeCreate, DepartmentCreate, JobCreate
from database import engine, Session
from logger import logger


# Función genérica para paginación
def get_paginated_records(
    db: Session, 
    model, 
    page: int = 1, 
    limit: int = 50
) -> dict:
    """
    Get paginated records from any table.
    
    Args:
        db: Database session
        model: SQLAlchemy model class
        page: Page number
        limit: Records per page

    Returns:
        dict: Data + metadata
    """
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")

    total = db.query(func.count(model.id)).scalar()
    offset = (page - 1) * limit

    records = db.query(model).offset(offset).limit(limit).all()

    return {
        "data": records,
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }

# Employee CRUD Operations

def create_employee(db: Session, employee: EmployeeCreate):
    try:
        db_employee = HiredEmployee(**employee.dict())
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        logger.info(f"Employee creado: ID {db_employee.id}")
        return db_employee
    except Exception as e:
        logger.error(f"Error creando employee: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno")

def get_employee(db: Session, employee_id: int):
    employee = db.query(HiredEmployee).filter(HiredEmployee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def get_all_employees(db: Session, page: int = 1, limit: int = 50):
    return get_paginated_records(db, HiredEmployee, page, limit)

def update_employee(db: Session, employee_id: int, employee_data: EmployeeCreate):
    employee = db.query(HiredEmployee).filter(HiredEmployee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee_data.dict().items():
        setattr(employee, key, value)
    
    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: int):
    employee = db.query(HiredEmployee).filter(HiredEmployee.id == employee_id).first()
    if not employee:
        logger.warning(f"Intento de borrar employee inexistente: ID {employee_id}")  # Log de advertencia
        raise HTTPException(status_code=404, detail="Employee no encontrado")
    
    try:
        db.delete(employee)
        db.commit()
        logger.info(f"Employee borrado: ID {employee_id}")  # Log exitoso
        return {"message": "Employee borrado"}
    except Exception as e:
        logger.error(f"Error borrando employee ID {employee_id}: {str(e)}")  # Log de error
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno")

# Department CRUD Operations

def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_department(db: Session, department_id: int):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

def get_all_departments(db: Session, page: int = 1, limit: int = 50):
    return get_paginated_records(db, Department, page, limit)

def update_department(db: Session, department_id: int, department_data: DepartmentCreate):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for key, value in department_data.dict().items():
        setattr(department, key, value)
    
    db.commit()
    db.refresh(department)
    return department

def delete_department(db: Session, department_id: int):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(department)
    db.commit()
    return {"message": "Department deleted successfully"}

# Job CRUD Operations

def create_job(db: Session, job: JobCreate):
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(db: Session, job_id: int):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

def get_all_jobs(db: Session, page: int = 1, limit: int = 50):
    return get_paginated_records(db, Job, page, limit)

def update_job(db: Session, job_id: int, job_data: JobCreate):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    for key, value in job_data.dict().items():
        setattr(job, key, value)
    
    db.commit()
    db.refresh(job)
    return job

def delete_job(db: Session, job_id: int):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}

