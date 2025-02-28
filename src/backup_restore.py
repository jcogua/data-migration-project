import os
import fastavro
import pandas as pd
from sqlalchemy import text
from database import engine

# Directorio de backups
BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

def get_table_schema(table_name):
    """Retrieves the structure of a table from the database."""
    with engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
    
    if not result:
        return None

    schema = []
    for row in result:
        column_name = row[1]
        column_type = "int" if "int" in row[2] else "string"
        schema.append({"name": column_name, "type": column_type})

    return schema

def backup_table(table_name):
    """Generates a backup of a table in AVRO format with the correct types (converting ID to string)."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name}")).fetchall()

        if not result:
            return {"error": f"La tabla {table_name} está vacía o no existe."}

        records = [dict(row._mapping) for row in result]

        for record in records:
            for key, value in record.items():
                if value is None:
                    record[key] = ""
                elif isinstance(value, int):  # Convert int to string
                    record[key] = str(value)
                else:
                    record[key] = str(value)  # Ensure everything is a string

        # Define AVRO schema ensuring all fields are strings
        schema = {
            "type": "record",
            "name": table_name,
            "fields": [{"name": key, "type": "string"} for key in records[0].keys()]
        }

        file_path = os.path.join(BACKUP_DIR, f"{table_name}.avro")
        with open(file_path, "wb") as out_file:
            fastavro.writer(out_file, schema, records)

        return {"message": f"Backup of {table_name} saved in {file_path}"}

    except Exception as e:
        return {"error": str(e)}

def restore_table(table_name):
    """Restores table data from an AVRO file, converting ID from string to int if necessary."""
    try:
        file_path = os.path.join(BACKUP_DIR, f"{table_name}.avro")
        
        if not os.path.exists(file_path):
            return {"error": f"No backup exists for {table_name}."}

        with open(file_path, "rb") as in_file:
            reader = fastavro.reader(in_file)
            records = [record for record in reader]

        if not records:
            return {"error": f"The backup of {table_name} is empty."}

        # Convert id from string to int if necessary
        for record in records:
            if "id" in record and record["id"].isdigit():
                record["id"] = int(record["id"])  # Convert to int before inserting into the DB

        df = pd.DataFrame(records)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)

        return {"message": f"Data restored in {table_name} from {file_path}"}

    except Exception as e:
        return {"error": str(e)}
