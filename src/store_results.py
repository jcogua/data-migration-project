from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import engine  # Ensure you have a properly configured connection

def store_results_in_db(table_name, data, columns):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    with Session(engine) as session:
        try:
            # Check if the table exists
            if table_name in metadata.tables:
                session.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY')
            else:
                # Create the table if it does not exist
                table = Table(
                    table_name,
                    metadata,
                    *(Column(col, String if isinstance(val, str) else Integer) for col, val in data[0].items()),
                    extend_existing=True
                )
                metadata.create_all(engine)
                
            # Insert the new data
            session.bulk_insert_mappings(metadata.tables[table_name], data)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error storing data in {table_name}: {e}")
        finally:
            session.close()