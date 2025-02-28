import os
import json
import logging
import pandas as pd

from core import DATA_FOLDER
from database import engine, SessionLocal
from validators import validate_record 
from models import HiredEmployee

# Configure logging
logging.basicConfig(filename='data_load.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# data folder
os.makedirs(DATA_FOLDER, exist_ok=True)

def load_json_to_db(json_file, table_name, db): 
    try:
        engine = db.bind 

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("El JSON debe contener una lista de objetos.")

        valid_records = []
        for record in data:
            errors = validate_record(record, table_name)
            
            if not errors:
                valid_records.append(record)
            else:
                logging.warning(f"Registro inválido en JSON ({table_name}): {errors}")

        if valid_records:
            df_valid = pd.DataFrame(valid_records)
            df_valid.to_sql(table_name, con=engine, if_exists='append', index=False)  
            logging.info(f"{len(valid_records)} registros válidos insertados en {table_name}.")

        return {"message": f"{len(valid_records)} registros insertados exitosamente."}

    except Exception as e:
        logging.error(f"Error cargando {table_name} desde {json_file}: {str(e)}")
        return {"error": str(e)}
