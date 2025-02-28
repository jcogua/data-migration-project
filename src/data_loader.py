import pandas as pd
import logging

from sqlalchemy import create_engine, text
from validators import validate_record
from datetime import datetime

# Configure logging to record errors
logging.basicConfig(filename='data_load.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import pandas as pd
import logging
from sqlalchemy import text
from validators import validate_record

def load_csv_to_db(csv_file, table_name, db, chunksize=1000):
    try:
        engine = db.bind  # Obtener el engine desde la sesión

        if table_name == 'hired_employees':
            column_names = ['id', 'name', 'datetime', 'department_id', 'job_id']
        elif table_name == 'departments':
            column_names = ['id', 'department']
        elif table_name == 'jobs':
            column_names = ['id', 'job']
        else:
            raise ValueError(f"Tabla {table_name} no reconocida.")

        valid_records = []  
        valid_rows = 0

        for chunk in pd.read_csv(csv_file, header=None, names=column_names, chunksize=chunksize):
            chunk = chunk.where(pd.notnull(chunk), None)  # ✅ Corregir paréntesis
            
            for _, row in chunk.iterrows():
                record = row.to_dict()
                errors = validate_record(record, table_name)
                
                if not errors:
                    valid_records.append(record)
                else:
                    logging.warning(f"Registro inválido en CSV ({table_name}): {errors}")

            if valid_records: 
                df_valid = pd.DataFrame(valid_records)
                df_valid.to_sql(table_name, con=engine, if_exists='append', index=False)  # Usar engine
                logging.info(f"{len(valid_records)} registros válidos insertados en {table_name}.")
                valid_rows += len(valid_records)

            valid_records = []  # Limpiar lista para el siguiente lote

        return {"message": f"{valid_rows} registros insertados exitosamente."}

    except Exception as e:
        logging.error(f"Error cargando {table_name} desde {csv_file}: {str(e)}")
        return {"error": str(e)}