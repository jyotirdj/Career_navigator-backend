# Alembic Migrations

This directory will contain database migration files when Alembic is initialized.

To set up Alembic:

1. Initialize Alembic (if not already done):
   ```bash
   alembic init alembic
   ```

2. Configure `alembic.ini` and `alembic/env.py` to use your database URL from settings.

3. Create your first migration:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

4. Apply migrations:
   ```bash
   alembic upgrade head
   ```

For now, the application creates tables automatically using `Base.metadata.create_all()`.
In production, use Alembic migrations instead.




