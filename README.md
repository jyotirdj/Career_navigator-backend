# Career Navigator Backend API

A REST API backend built with FastAPI to help engineering students plan their learning journey from 1st year to final year based on their branch, current year, and career goals.

## Features

- **User Management**: Register/login with email and password, JWT-based authentication
- **Student Profiles**: Store and manage student information (branch, year, career goal)
- **Roadmap Templates**: Predefined learning roadmaps for different career paths
- **Personalized Roadmaps**: Generate custom roadmaps based on student profile
- **Progress Tracking**: Track completion status of learning steps

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt

## Project Structure

```
career_navigator/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── profile.py
│   │   │   └── roadmap.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   │   ├── student_profile.py
│   │   ├── roadmap_templates.py
│   │   └── roadmap_steps.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── profile.py
│   │   └── roadmap.py
│   ├── services/
│   │   └── roadmap_service.py
│   ├── database.py
│   └── main.py
├── alembic/
├── scripts/
│   └── seed_roadmaps.py
├── .env.example
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL Database**:
   - Create a PostgreSQL database named `career_navigator`
   - Update the `DATABASE_URL` in `.env` file with your database credentials

3. **Configure Environment Variables**:
   - Copy `.env.example` to `.env` and update the values:
     - `DATABASE_URL`: Your PostgreSQL connection string (e.g., `postgresql://user:password@localhost:5432/career_navigator`)
     - `SECRET_KEY`: A long random string for JWT token signing (generate a secure key for production)
     - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

4. **Initialize Database**:
   - The application will automatically create tables on first run
   - (Optional) Seed initial roadmap templates:
     ```bash
     python scripts/seed_roadmaps.py
     ```

5. **Start the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   API documentation (Swagger UI) at `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Profile
- `GET /api/profile` - Get current user's profile
- `POST /api/profile` - Create/update student profile
- `PUT /api/profile` - Update student profile

### Roadmap
- `GET /api/roadmap` - Get user's personalized roadmap with progress
- `POST /api/roadmap/generate` - Generate a new roadmap based on profile
- `PUT /api/roadmap/steps/{step_id}` - Update step status

### Admin (Future)
- CRUD operations for roadmap templates

## Development

- The project uses SQLAlchemy for database operations
- Pydantic schemas for request/response validation
- JWT tokens for authentication
- Centralized error handling

## Seeding Sample Data

To populate the database with sample roadmap templates:

```bash
python scripts/seed_roadmaps.py
```

This will create sample roadmaps for:
- Python Backend Developer (CSE-specific and generic)
- Data Engineer (generic)

You can modify the script to add more roadmaps or customize existing ones.

## Testing the API

1. **Register a new user**:
   ```bash
   POST /api/auth/register
   {
     "email": "student@example.com",
     "password": "securepassword",
     "full_name": "John Doe"
   }
   ```

2. **Login**:
   ```bash
   POST /api/auth/login
   {
     "email": "student@example.com",
     "password": "securepassword"
   }
   ```
   Copy the `access_token` from the response.

3. **Create Profile** (use the token in Authorization header: `Bearer <token>`):
   ```bash
   POST /api/profile
   {
     "branch": "CSE",
     "current_year": 2,
     "current_semester": 1,
     "career_goal": "Python Backend Developer"
   }
   ```

4. **Generate Roadmap**:
   ```bash
   POST /api/roadmap/generate
   ```

5. **Get Roadmap with Progress**:
   ```bash
   GET /api/roadmap
   ```

6. **Update Step Status**:
   ```bash
   PUT /api/roadmap/steps/{step_id}
   {
     "status": "completed",
     "notes": "Finished learning Python basics!"
   }
   ```

## License

MIT

