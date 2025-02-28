## 📌 FastAPI Employee Management API

## 📖 Description
This API allows the management of employees, departments, and jobs using **FastAPI** and **SQLAlchemy**, with PostgreSQL as the database. It includes API key authentication, data validation, and endpoints for loading data from CSV and JSON files.

## 🛠 Technologies Used
- **Python** (FastAPI, SQLAlchemy, Pydantic)
- **PostgreSQL** (Database)
- **Docker** (For containerization)
- **Uvicorn** (For running the ASGI server)

## 🚀 Installation and Configuration
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/usuario/proyecto.git
cd proyecto
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## 🏃 Running the API
### 1️⃣ Configure Environment Variables
Create a `.env` file in the project root with:
```
DATABASE_URL=postgresql://user:password@host:port/database
API_KEY=your_api_key
```

### 2️⃣ Start the API
```bash
docker build -t employee-management-api .
docker run -d -p 8000:8000 --env-file .env employee-management-api
```

## 🔥 Available Endpoints
### 🔹 **Employees**
| Method | Endpoint                   | Description |
|--------|----------------------------|-------------|
| `POST` | `/employees/create`         | Create a new employee |
| `GET`  | `/employees/`               | Retrieve all employees |
| `GET`  | `/employees/{employee_id}`  | Retrieve an employee by ID |
| `PUT`  | `/employees/{employee_id}`  | Update an employee |
| `DELETE` | `/employees/{employee_id}` | Delete an employee |

### 🔹 **Departments**
| Method | Endpoint                      | Description |
|--------|--------------------------------|-------------|
| `POST` | `/departments/`               | Create a department |
| `GET`  | `/departments/`               | Retrieve all departments |
| `GET`  | `/departments/{department_id}` | Retrieve a department by ID |
| `PUT`  | `/departments/{department_id}` | Update a department |
| `DELETE` | `/departments/{department_id}` | Delete a department |

### 🔹 **Jobs**
| Method | Endpoint               | Description |
|--------|------------------------|-------------|
| `POST` | `/jobs/`               | Create a job |
| `GET`  | `/jobs/`               | Retrieve all jobs |
| `GET`  | `/jobs/{job_id}`        | Retrieve a job by ID |
| `PUT`  | `/jobs/{job_id}`        | Update a job |
| `DELETE` | `/jobs/{job_id}`      | Delete a job |

### 🔹 **Data Upload**
| Method | Endpoint       | Description |
|--------|---------------|-------------|
| `POST` | `/load-data/` | Load data from CSV and JSON |

### 🔹 **Backup and Restoration**
| Method | Endpoint              | Description |
|--------|-----------------------|-------------|
| `POST` | `/backup/{table_name}` | Create a backup |
| `POST` | `/restore/{table_name}` | Restore data from a backup |

### 🔹 **Reports**
| Method | Endpoint                        | Description |
|--------|---------------------------------|-------------|
| `GET`  | `/hired-employees-by-quarter/`  | Employees hired per quarter |
| `GET`  | `/departments-above-average/`   | Departments with above-average hiring |

## 🔑 Authentication and Security
- The API uses **API Keys** to protect endpoints.
- The API Key must be sent in the request header:
  ```
  X-API-KEY: your_api_key
  ```

## 🛠 Error Handling
The API returns structured error responses:
```json
{
    "detail": "Invalid department_id"
}
```

## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributions
If you want to contribute:
1. **Fork the repository**.
2. **Create a branch** (`git checkout -b new-feature`).
3. **Make your changes and commit** (`git commit -m 'Add new feature'`).
4. **Submit a pull request** 🚀.

---
✉️ **Questions or suggestions?** Contact me at [correo@ejemplo.com](mailto:correo@ejemplo.com) 😊

