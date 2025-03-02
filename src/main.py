import os
import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from core import DATA_FOLDER
from database import get_db, engine
from models import Base, HiredEmployee, Department, Job
from backup_restore import backup_table, restore_table
from upload_json import load_json_to_db
from data_loader import load_csv_to_db
from auth import validate_api_key
from scripts.queries import hired_employees_by_quarter, departments_above_average
from models import EmployeeCreate, DepartmentCreate, JobCreate
from logger import logger

from crud import (
    create_employee, get_employee, get_all_employees, update_employee, delete_employee,
    create_department, get_department, get_all_departments, update_department, delete_department,
    create_job, get_job, get_all_jobs, update_job, delete_job
)

# Database configuration
Base.metadata.create_all(engine)

# Create the FastAPI application
app = FastAPI()

@app.get("/")
@app.head("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "API running correctly"}

# Employee Endpoints
@app.post("/employees/create")
def create_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Attempting to create employee: {employee.dict()}")
    try:
        result = create_employee(db, employee)
        logger.debug(f"Employee created successfully: ID {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating employee: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/employees/")
def get_all_employees_endpoint(
    db: Session = Depends(get_db),
    valid: bool = Depends(validate_api_key),
    page: int = Query(1, ge=1),
    limit: int = Query(50, le=100)
):
    logger.info(f"Fetching employees - Page: {page}, Limit: {limit}")
    try:
        result = get_all_employees(db, page, limit)
        logger.debug(f"Found {len(result['data'])} employees")
        return result
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/employees/{employee_id}")
def get_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching employee ID: {employee_id}")
    try:
        result = get_employee(db, employee_id)
        return result
    except HTTPException as e:
        logger.warning(f"Employee not found: ID {employee_id}")
        raise
    except Exception as e:
        logger.error(f"Error fetching employee {employee_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/employees/{employee_id}")
def update_employee_endpoint(employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Updating employee ID: {employee_id}")
    try:
        result = update_employee(db, employee_id, employee)
        logger.debug(f"Employee updated successfully: ID {employee_id}")
        return result
    except HTTPException as e:
        logger.warning(f"Update failed for employee ID {employee_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error updating employee {employee_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/employees/{employee_id}")
def delete_employee_endpoint(employee_id: int, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Deleting employee ID: {employee_id}")
    try:
        result = delete_employee(db, employee_id)
        logger.debug(f"Employee deleted successfully: ID {employee_id}")
        return result
    except HTTPException as e:
        logger.warning(f"Delete failed for employee ID {employee_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error deleting employee {employee_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Department Endpoints
@app.post("/departments/")
def create_department_endpoint(department: DepartmentCreate, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Attempting to create department: {department.dict()}")
    try:
        result = create_department(db, department)
        logger.debug(f"Department created successfully: ID {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating department: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/departments/")
def get_all_departments_endpoint(
    db: Session = Depends(get_db),
    valid: bool = Depends(validate_api_key),
    page: int = Query(1, ge=1),
    limit: int = Query(50, le=100)
):
    logger.info(f"Fetching departments - Page: {page}, Limit: {limit}")
    try:
        result = get_all_departments(db, page, limit)
        logger.debug(f"Found {len(result['data'])} departments")
        return result
    except Exception as e:
        logger.error(f"Error fetching departments: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/departments/{department_id}")
def get_department_endpoint(department_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching department ID: {department_id}")
    try:
        result = get_department(db, department_id)
        return result
    except HTTPException as e:
        logger.warning(f"Department not found: ID {department_id}")
        raise
    except Exception as e:
        logger.error(f"Error fetching department {department_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/departments/{department_id}")
def update_department_endpoint(department_id: int, department: DepartmentCreate, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Updating department ID: {department_id}")
    try:
        result = update_department(db, department_id, department)
        logger.debug(f"Department updated successfully: ID {department_id}")
        return result
    except HTTPException as e:
        logger.warning(f"Update failed for department ID {department_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error updating department {department_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/departments/{department_id}")
def delete_department_endpoint(department_id: int, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Deleting department ID: {department_id}")
    try:
        result = delete_department(db, department_id)
        logger.debug(f"Department deleted successfully: ID {department_id}")
        return result
    except HTTPException as e:
        logger.warning(f"Delete failed for department ID {department_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error deleting department {department_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Job Endpoints
@app.post("/jobs/")
def create_job_endpoint(job: JobCreate, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Attempting to create job: {job.dict()}")
    try:
        result = create_job(db, job)
        logger.debug(f"Job created successfully: ID {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating job: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/jobs/")
def get_all_jobs_endpoint(
    db: Session = Depends(get_db),
    valid: bool = Depends(validate_api_key),
    page: int = Query(1, ge=1),
    limit: int = Query(50, le=100)
):
    logger.info(f"Fetching jobs - Page: {page}, Limit: {limit}")
    try:
        result = get_all_jobs(db, page, limit)
        logger.debug(f"Found {len(result['data'])} jobs")
        return result
    except Exception as e:
        logger.error(f"Error fetching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/jobs/{job_id}")
def get_job_endpoint(job_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching job ID: {job_id}")
    try:
        result = get_job(db, job_id)
        return result
    except HTTPException as e:
        logger.warning(f"Job not found: ID {job_id}")
        raise
    except Exception as e:
        logger.error(f"Error fetching job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/jobs/{job_id}")
def update_job_endpoint(job_id: int, job: JobCreate, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Updating job ID: {job_id}")
    try:
        result = update_job(db, job_id, job)
        logger.debug(f"Job updated successfully: ID {job_id}")
        return result
    except HTTPException as e:
        logger.warning(f"Update failed for job ID {job_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error updating job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/jobs/{job_id}")
def delete_job_endpoint(job_id: int, db: Session = Depends(get_db), valid: bool = Depends(validate_api_key)):
    logger.info(f"Deleting job ID: {job_id}")
    try:
        result = delete_job(db, job_id)
        logger.debug(f"Job deleted successfully: ID {job_id}")
        return result
    except HTTPException as e:
        logger.warning(f"Delete failed for job ID {job_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error deleting job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Endpoint to load data
@app.post("/load-data/")
def load_data_endpoint(valid: bool = Depends(validate_api_key), db: Session = Depends(get_db)):
    logger.info("Starting data load process")
    try:
        files = [f for f in os.listdir(DATA_FOLDER) if not f.endswith(".db")]
        processed_files = []
        
        logger.debug(f"Found {len(files)} files to process in {DATA_FOLDER}")
        
        for file in files:
            file_path = os.path.join(DATA_FOLDER, file)
            table_name = os.path.splitext(file)[0]
            
            logger.info(f"Processing file: {file_path}")
            
            try:
                if file.endswith(".csv"):
                    result = load_csv_to_db(file_path, table_name, db)
                elif file.endswith(".json"):
                    result = load_json_to_db(file_path, table_name, db)
                
                if "error" in result:
                    logger.warning(f"Error processing {file}: {result['error']}")
                    processed_files.append({"file": file, "type": "CSV" if file.endswith(".csv") else "JSON", "status": "ERROR", "detail": result["error"]})
                else:
                    logger.info(f"Successfully processed {file}")
                    processed_files.append({"file": file, "type": "CSV" if file.endswith(".csv") else "JSON", "status": "OK"})
                    
            except Exception as e:
                logger.error(f"Error processing {file}: {str(e)}", exc_info=True)
                processed_files.append({"file": file, "type": "CSV" if file.endswith(".csv") else "JSON", "status": "ERROR", "detail": str(e)})

        logger.info("Data load process completed")
        return {"message": "Process completed", "files_processed": processed_files}

    except Exception as e:
        logger.critical(f"Critical error in data load process: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

# Backup/Restore Endpoints
@app.post("/backup/{table_name}")
def api_backup_table_endpoint(table_name: str, valid: bool = Depends(validate_api_key)):
    logger.info(f"Starting backup for table: {table_name}")
    try:
        result = backup_table(table_name)
        if "error" in result:
            logger.error(f"Backup failed for {table_name}: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])
        logger.info(f"Backup successful for {table_name}")
        return result
    except Exception as e:
        logger.error(f"Backup error for {table_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/restore/{table_name}")
def api_restore_table_endpoint(table_name: str, valid: bool = Depends(validate_api_key)):
    logger.info(f"Starting restore for table: {table_name}")
    try:
        result = restore_table(table_name)
        if "error" in result:
            logger.error(f"Restore failed for {table_name}: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])
        logger.info(f"Restore successful for {table_name}")
        return result
    except Exception as e:
        logger.error(f"Restore error for {table_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

# Reporting Endpoints
@app.get("/hired-employees-by-quarter/")
def get_hired_employees_by_quarter_endpoint():
    logger.info("Generating hired employees by quarter report")
    try:
        result = hired_employees_by_quarter()
        logger.debug("Report generated successfully")
        return result
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating report")

@app.get("/departments-above-average/")
def get_departments_above_average_endpoint():
    logger.info("Generating departments above average report")
    try:
        result = departments_above_average()
        logger.debug("Report generated successfully")
        return result
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating report")

if __name__ == "__main__":
    logger.info("Starting API server")
    uvicorn.run(app, host="0.0.0.0", port=8000)