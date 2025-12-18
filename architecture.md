Client (Swagger / Postman)
        |
        v
FastAPI Application
        |
   Auth Middleware (JWT)
        |
Tenant Validation (organization_id)
        |
PostgreSQL Database
(organizations, users, contacts)
