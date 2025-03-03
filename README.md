# 📡 Data Migration API

## 📖 Description
This REST API enables the migration, management, and querying of data from CSV and JSON files into a **PostgreSQL** database hosted on **Aiven**. It also provides **backup and restore functionalities in AVRO format**. The API is deployed as a **web service on Render**.

## 🛠 Technologies Used
- **Python** (FastAPI, SQLAlchemy, Pandas)
- **PostgreSQL** (Database hosted on Aiven)
- **Render** (Deployment)
- **Docker** (For containerization)
- **AVRO** (For backup and restore)

## 📄 API Documentation
The API documentation is available at:
- **[Swagger UI](https://data-migration-project-1.onrender.com/docs)**
- **[Redoc](https://data-migration-project-1.onrender.com/redoc)**

## 🚀 Installation and Configuration

### 1️⃣ Clone the Repository
```
git clone https://github.com/jcogua/data-migration-project.git
cd data-migration-project
```

### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the project root with the following content:
```
API_KEY=your_api_key
DATABASE_URL=postgresql://user:password@host:port/database
DEBUG=True/False
```
Use the **Aiven PostgreSQL connection string** in `DATABASE_URL`.

### 4️⃣ Run the API Locally
```
docker build -t data-migration-api .
docker run -d -p 8000:8000 --env-file .env data-migration-api
```

### 5️⃣ Run the API on Render
The API is deployed at:
```
https://data-migration-project-1.onrender.com
```
You can send requests using Postman or cURL.

## 🔥 Available Endpoints

### 🔹 **Root**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/`     | Check if the API is running |

### 🔹 **Authentication**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/token` | Get a JWT authentication token |

### 🔹 **Employees**
| Method  | Endpoint | Description |
|---------|---------|-------------|
| `POST`  | `/employees/create` | Create a new employee |
| `GET`   | `/employees/` | Get a list of employees with pagination |
| `GET`   | `/employees/{employee_id}` | Get an employee by ID |
| `PUT`   | `/employees/{employee_id}` | Update an employee by ID |
| `DELETE` | `/employees/{employee_id}` | Delete an employee by ID |

### 🔹 **Departments**
| Method  | Endpoint | Description |
|---------|---------|-------------|
| `POST`  | `/departments/` | Create a new department |
| `GET`   | `/departments/` | Get a list of departments with pagination |
| `GET`   | `/departments/{department_id}` | Get a department by ID |
| `PUT`   | `/departments/{department_id}` | Update a department by ID |
| `DELETE` | `/departments/{department_id}` | Delete a department by ID |

### 🔹 **Jobs**
| Method  | Endpoint | Description |
|---------|---------|-------------|
| `POST`  | `/jobs/` | Create a new job |
| `GET`   | `/jobs/` | Get a list of jobs with pagination |
| `GET`   | `/jobs/{job_id}` | Get a job by ID |
| `PUT`   | `/jobs/{job_id}` | Update a job by ID |
| `DELETE` | `/jobs/{job_id}` | Delete a job by ID |

### 🔹 **Data Upload**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/load-data/` | Load data from CSV and JSON files |

### 🔹 **Backup and Restore**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/backup/{table_name}` | Create a backup in AVRO format |
| `POST` | `/restore/{table_name}` | Restore data from a backup |

### 🔹 **Reports**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/hired-employees-by-quarter/` | Get a report of employees hired per quarter |
| `GET`  | `/departments-above-average/` | Get a report of departments that hired above the average |

## 🔑 Authentication and Security
- The API uses **API Keys** to secure endpoints.
- The API Key must be sent in the request header:
  ```
  X-API-KEY: your_api_key
  ```
- OAuth2 authentication with JWT can also be configured.

## 🛠 Error Handling
The API returns structured error responses:
```
{
    "detail": "Invalid department_id"
}
```

## 📊 Reporting with Looker Studio
- **Data is visualized using Looker Studio**.
- Ensure PostgreSQL tables exist before connecting.
- The `/hired-employees-by-quarter/` and `/departments-above-average/` endpoints generate structured tables ready for reporting.

## 📜 License
This project is licensed under the **MIT License**. You are free to use and modify it.

## 🤝 Contributions
If you want to contribute:
1. **Fork the repository**.
2. **Create a new branch** (`git checkout -b new-feature`).
3. **Make your changes and commit** (`git commit -m 'Add new feature'`).
4. **Submit a pull request** 🚀.

---
✉️ **Questions or suggestions?** Contact me at [jes.cogm@gmail.com](mailto:jes.cogm@gmail.com) 😊
