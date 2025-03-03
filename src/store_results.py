from sqlalchemy import Table, Column, Integer, String, MetaData, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import engine

def store_results_in_db(table_name, data, columns):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    with Session(engine) as session:
        try:
            print(f"Processing table: {table_name}")
            
            columns = [col.lower() for col in columns]

            data = [{k.lower(): v for k, v in row.items()} for row in data]
            
            # Check if the table exists and drop it if necessary
            if table_name in metadata.tables:
                print(f"Dropping existing table: {table_name}")
                session.execute(text(f'DROP TABLE IF EXISTS {table_name} CASCADE'))
                session.commit()
            
            # Create the table with correct columns
            print(f"Creating table: {table_name}")
            table = Table(
                table_name,
                metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                *(Column(col, Integer) if isinstance(data[0].get(col, ""), int) else Column(col, String) for col in columns),
            )
            metadata.create_all(engine)
            metadata.reflect(bind=engine)
            
            # Insert the new data using individual execution
            columns_str = ', '.join(columns)
            values_str = ', '.join([f':{col}' for col in columns])
            insert_query = text(f'INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})')
            
            for row in data:
                session.execute(insert_query, row)
            
            session.commit()
            print(f"Data successfully stored in {table_name}")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error storing data in {table_name}: {e}")
        finally:
            session.close()