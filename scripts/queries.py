from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, case, cast
from sqlalchemy.types import TIMESTAMP
from database import engine, Session
from models import HiredEmployee, Department, Job
from fastapi import HTTPException

SessionLocal = sessionmaker(bind=engine)

def hired_employees_by_quarter():
    session = SessionLocal()
    try:
        query = (
            session.query(
                Department.department,
                Job.job,
                func.sum(
                    case(
                        (func.extract('month', cast(HiredEmployee.datetime, TIMESTAMP)) >= 1, 1),
                        else_=0
                    )
                ).label("Q1"),
                func.sum(
                    case(
                        (func.extract('month', cast(HiredEmployee.datetime, TIMESTAMP)) >= 4, 1),
                        else_=0
                    )
                ).label("Q2"),
                func.sum(
                    case(
                        (func.extract('month', cast(HiredEmployee.datetime, TIMESTAMP)) >= 7, 1),
                        else_=0
                    )
                ).label("Q3"),
                func.sum(
                    case(
                        (func.extract('month', cast(HiredEmployee.datetime, TIMESTAMP)) >= 10, 1),
                        else_=0
                    )
                ).label("Q4"),
            )
            .join(Department, Department.id == HiredEmployee.department_id)
            .join(Job, Job.id == HiredEmployee.job_id)
            .filter(func.extract('year', cast(HiredEmployee.datetime, TIMESTAMP)) == 2021)
            .group_by(Department.department, Job.job)
            .order_by(Department.department, Job.job)
            .all()
        )
        session.close()
        
        # Convertir el resultado en una lista de diccionarios
        result = [
            {
                "department": row[0],
                "job": row[1],
                "Q1": row[2],
                "Q2": row[3],
                "Q3": row[4],
                "Q4": row[5]
            }
            for row in query
        ]
        
        return result
    except Exception as e:
        session.close()
        raise HTTPException(status_code=500, detail=str(e))

def departments_above_average():
    session = SessionLocal()
    try:
        department_hires = (
            session.query(
                HiredEmployee.department_id,
                func.count(HiredEmployee.id).label("total_hires")
            )
            .filter(func.strftime('%Y', HiredEmployee.datetime) == '2021')
            .group_by(HiredEmployee.department_id)
            .subquery()
        )

        avg_hires = (
            session.query(func.avg(department_hires.c.total_hires))
            .scalar()
        )
        
        if avg_hires is None:
            avg_hires = 0

        # Query
        query_result = (
            session.query(
                Department.id,
                Department.department.label("name"),
                func.count(HiredEmployee.id).label("hired")
            )
            .join(HiredEmployee, Department.id == HiredEmployee.department_id)
            .filter(func.extract('year', cast(HiredEmployee.datetime, TIMESTAMP)) == 2021)
            .group_by(Department.id, Department.department)
            .having(func.count(HiredEmployee.id) > avg_hires)
            .order_by(func.count(HiredEmployee.id).desc())
            .all()
        )

        session.close()

        # result into a list of dict
        result = [
            {
                "id": row.id,
                "department": row.name,
                "hired": row.hired
            }
            for row in query_result
        ]

        return result

    except Exception as e:
        session.close()
        raise HTTPException(status_code=500, detail=str(e))
