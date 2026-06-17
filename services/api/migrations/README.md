# API Migrations

The initial schema targets Postgres with `pgvector` and models the core Kiro entities:

- catalogs, subjects, lessons, chunks, paths, and practice problems
- accounts, organizations, classrooms, memberships, and classroom path assignment
- progress, grasp scores, review schedules, and student record audits
- affiliates, referrals, and conversions

Apply `0001_initial_schema.sql` with the migration runner selected for the API service once task 1.3 chooses the concrete database migration tool.
