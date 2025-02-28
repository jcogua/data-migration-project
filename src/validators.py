# validators.py
import pandas as pd
from typing import Dict, Any, List

def is_invalid_id(value: Any) -> bool:
    """Verifica si un ID es válido"""
    if pd.isna(value):
        return True
    try:
        return float(value) <= 0
    except (ValueError, TypeError):
        return True

def validate_record(record: Dict[str, Any], table_name: str) -> List[str]:
    """
    Valida un registro según la tabla especificada (compatible con CSV y JSON).
    Retorna una lista de errores. Si está vacía, el registro es válido.
    """
    errors = []
    
    # Validación común para ID
    id_value = record.get("id")
    if pd.isna(id_value) or str(id_value).strip() in ["", "nan", "None"]:
        errors.append("El campo 'id' es inválido o está vacío")
    
    # Validaciones específicas por tabla
    if table_name == "hired_employees":
        name = record.get("name")
        if pd.isna(name) or not isinstance(name, str) or not name.strip():
            errors.append("El campo 'name' es requerido y debe ser un string válido")
            
        datetime = record.get("datetime")
        if pd.isna(datetime):
            errors.append("El campo 'datetime' es requerido")
            
        if is_invalid_id(record.get("department_id")):
            errors.append("department_id inválido")
            
        if is_invalid_id(record.get("job_id")):
            errors.append("job_id inválido")
    
    elif table_name == "departments":
        department = record.get("department")
        if pd.isna(department) or not isinstance(department, str) or not department.strip():
            errors.append("El campo 'department' es requerido y debe ser un string válido")
    
    elif table_name == "jobs":
        job = record.get("job")
        if pd.isna(job) or not isinstance(job, str) or not job.strip():
            errors.append("El campo 'job' es requerido y debe ser un string válido")
    
    return errors