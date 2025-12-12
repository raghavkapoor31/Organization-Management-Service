# Organization Management Service

A multi-tenant organization management backend service built with FastAPI and MongoDB. This service supports creating and managing organizations with dynamic collection creation for each organization.

## Features

- ✅ Create organizations with admin users
- ✅ Get organization details
- ✅ Update organization admin credentials
- ✅ Delete organizations (with authentication)
- ✅ Admin login with JWT authentication
- ✅ Dynamic MongoDB collection creation per organization
- ✅ Secure password hashing with bcrypt
- ✅ Multi-tenant architecture

## Tech Stack

- **Framework**: FastAPI (Python 3.8+)
- **Database**: MongoDB (with Motor async driver)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt (via passlib)

## Project Structure

```
wedding company backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # MongoDB connection manager
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── organization.py     # Organization and AdminUser models
│   ├── schemas/                # Pydantic schemas for request/response
│   │   ├── __init__.py
│   │   └── organization.py     # API schemas
│   ├── services/               # Business logic layer
│   │   └── organization_service.py
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   ├── organization.py     # Organization endpoints
│   │   └── auth.py             # Authentication endpoints
│   └── auth/                   # Authentication utilities
│       ├── __init__.py
│       ├── jwt_handler.py      # JWT token management
│       ├── password.py          # Password hashing
│       └── dependencies.py     # Auth dependencies
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- MongoDB (running locally or remote)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "wedding company backend"
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   MASTER_DB_NAME=master_db
   JWT_SECRET_KEY=your-secret-key-change-this-in-production
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   ```

5. **Start MongoDB** (if running locally)
   ```bash
   # On macOS with Homebrew
   brew services start mongodb-community
   
   # On Linux
   sudo systemctl start mongod
   
   # Or use Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   ```

## Running the Application

1. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs (Swagger): `http://localhost:8000/docs`
   - Alternative API Docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### 1. Create Organization
**POST** `/org/create`

Request Body:
```json
{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "organization_name": "Acme Corp",
  "org_collection_name": "org_acme_corp",
  "admin_user_id": "507f1f77bcf86cd799439011",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 2. Get Organization
**GET** `/org/get`

Request Body:
```json
{
  "organization_name": "Acme Corp"
}
```

### 3. Update Organization
**PUT** `/org/update`

**Requires Authentication** (Bearer token)

Request Body:
```json
{
  "organization_name": "Acme Corp",
  "new_organization_name": "Acme Corporation",  // Optional: rename organization
  "email": "newadmin@acme.com",
  "password": "newsecurepassword123"
}
```

**Note**: If `new_organization_name` is provided and different from `organization_name`, the organization will be renamed and all data will be migrated to a new collection. The old collection will be deleted after successful migration.

### 4. Delete Organization
**DELETE** `/org/delete`

**Requires Authentication** (Bearer token)

Request Body:
```json
{
  "organization_name": "Acme Corp"
}
```

### 5. Admin Login
**POST** `/admin/login`

Request Body:
```json
{
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "organization_name": "Acme Corp",
  "admin_id": "507f1f77bcf86cd799439011"
}
```

## Authentication

For protected endpoints (Update and Delete), include the JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Example Usage

### 1. Create an Organization
```bash
curl -X POST "http://localhost:8000/org/create" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Tech Startup",
    "email": "admin@techstartup.com",
    "password": "securepass123"
  }'
```

### 2. Login as Admin
```bash
curl -X POST "http://localhost:8000/admin/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@techstartup.com",
    "password": "securepass123"
  }'
```

### 3. Get Organization (using token from login)
```bash
curl -X GET "http://localhost:8000/org/get" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Tech Startup"
  }'
```

### 4. Update Organization (requires authentication)
```bash
# Update admin credentials only
curl -X PUT "http://localhost:8000/org/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "organization_name": "Tech Startup",
    "email": "newadmin@techstartup.com",
    "password": "newsecurepass123"
  }'

# Update admin credentials and rename organization (with data migration)
curl -X PUT "http://localhost:8000/org/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "organization_name": "Tech Startup",
    "new_organization_name": "Tech Startup Inc",
    "email": "newadmin@techstartup.com",
    "password": "newsecurepass123"
  }'
```

### 5. Delete Organization (requires authentication)
```bash
curl -X DELETE "http://localhost:8000/org/delete" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "organization_name": "Tech Startup"
  }'
```

## Documentation

- **README.md** (this file): Setup and usage instructions
- **ARCHITECTURE.md**: Detailed architecture diagrams and system design
- **DESIGN_NOTES.md**: Design choices, trade-offs, and scalability considerations

## Architecture Overview

### Database Structure

**Master Database** (`master_db`):
- `organizations` collection: Stores organization metadata
- `admin_users` collection: Stores admin user credentials (hashed passwords)

**Dynamic Collections**:
- Each organization gets its own collection: `org_<organization_name>`
- Collections are created dynamically when an organization is created
- Collections are deleted when an organization is deleted

### Design Patterns

1. **Service Layer Pattern**: Business logic is separated into service classes
2. **Repository Pattern**: Database operations are abstracted through the DatabaseManager
3. **Dependency Injection**: FastAPI's dependency system for authentication
4. **Multi-tenant Architecture**: Each organization has isolated data collections

## Design Choices & Trade-offs

### Architecture Assessment

**Strengths:**
- ✅ Clean separation of concerns (models, schemas, services, routers)
- ✅ Async/await for better performance with I/O operations
- ✅ Type safety with Pydantic schemas
- ✅ JWT-based stateless authentication
- ✅ Secure password hashing

**Trade-offs & Considerations:**

1. **Collection-per-Organization vs Database-per-Organization**
   - **Current**: Collections in same database
   - **Alternative**: Separate databases per organization
   - **Trade-off**: Collections are simpler but databases provide better isolation

2. **MongoDB vs SQL Database**
   - **Current**: MongoDB (flexible schema, easy collection creation)
   - **Alternative**: PostgreSQL with schema-per-tenant
   - **Trade-off**: MongoDB is easier for dynamic structures, but SQL offers better ACID guarantees

3. **JWT Token Storage**
   - **Current**: Stateless JWT (no server-side storage)
   - **Alternative**: Token blacklisting/refresh tokens
   - **Trade-off**: Stateless is simpler but harder to revoke tokens

### Potential Improvements

1. **Scalability Enhancements**:
   - Implement database sharding for large-scale deployments
   - Add Redis for caching and session management
   - Use separate databases per organization for better isolation

2. **Security Enhancements**:
   - Implement refresh tokens
   - Add rate limiting
   - Add request validation and sanitization
   - Implement token blacklisting

3. **Features**:
   - Organization name change with data migration
   - Multiple admin users per organization
   - Role-based access control (RBAC)
   - Audit logging

4. **DevOps**:
   - Docker containerization
   - Kubernetes deployment configs
   - CI/CD pipeline
   - Monitoring and logging (e.g., Prometheus, ELK stack)

## Testing

To test the API, you can use:
- Swagger UI at `http://localhost:8000/docs`
- Postman or any HTTP client
- cURL commands (examples above)

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication failed)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

## License

This project is part of a backend intern assignment.

## Author

Built as part of a backend intern assignment demonstrating multi-tenant architecture and REST API design.

