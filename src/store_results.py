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
            
            # Check if the table exists and if it's a view, drop it
            check_view_query = text(f"SELECT table_name FROM information_schema.views WHERE table_name = '{table_name}'")
            view_result = session.execute(check_view_query).fetchone()
            
            if view_result:
                print(f"{table_name} is a view. Dropping view...")
                session.execute(text(f'DROP VIEW IF EXISTS {table_name} CASCADE'))
                session.commit()
            
            # Check again if the table exists
            if table_name in metadata.tables:
                print(f"Truncating existing table: {table_name}")
                session.execute(text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY'))
            else:
                print(f"Creating table: {table_name}")
                # Create the table if it does not exist
                table = Table(
                    table_name,
                    metadata,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    *(Column(col, String if isinstance(val, str) else Integer) for col, val in data[0].items()),
                    extend_existing=True
                )
                metadata.create_all(engine)
                metadata.reflect(bind=engine)  # Refresh metadata after creating the table
            
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
