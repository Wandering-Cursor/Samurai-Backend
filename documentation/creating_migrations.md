# How to create a new migration and apply it

## 1. Create a new migration

Head to the `src/samurai_backend/` folder and run the following command:

```bash
alembic revision --autogenerate -m "YOUR MIGRATION MESSAGE"
```

This will generate a new migration file in `src/samurai_backend/migrations/versions/` folder.

## 2. Apply the migration

To apply the migration, run the following command:

```bash
alembic upgrade head
```

This will apply the LATEST migration to the database.
If you want to apply a specific migration, you can use the following command:

```bash
alembic upgrade *migration_id*
```

By replacing `*migration_id*` with the migration id you want to apply. You can find the migration id in the migration file name.
For example from `dbb9e7944923_email_confirmation_code.py` - `dbb9e7944923` is the migration id.

## 3. Downgrade the migration

If you want to revert the migration, you can use the following command:

```bash
alembic downgrade *migration_id*
```

## Final notes

Please, try to aggregate your migrations as much as possible. This will make the migration process easier and cleaner.
