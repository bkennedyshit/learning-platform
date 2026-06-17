CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE catalog_key AS ENUM ('k12', 'advanced');
CREATE TYPE audience_tier AS ENUM ('k-5', '6-8', '9-12', 'higher-education', 'advanced-personal');
CREATE TYPE account_role AS ENUM ('b2c_learner', 'student', 'educator', 'org_admin', 'affiliate', 'platform_admin');
CREATE TYPE classroom_member_role AS ENUM ('educator', 'student');
CREATE TYPE path_item_kind AS ENUM ('subject', 'lesson');
CREATE TYPE practice_problem_tier AS ENUM ('easy', 'medium', 'hard', 'exam');
CREATE TYPE practice_problem_source AS ENUM ('authored', 'generated');
CREATE TYPE consent_status AS ENUM ('not_required', 'pending', 'granted', 'revoked');

CREATE TABLE catalogs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  key catalog_key NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE organizations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  seat_count integer NOT NULL CHECK (seat_count >= 0),
  plan text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE accounts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email citext NOT NULL UNIQUE,
  password_hash text NOT NULL,
  role account_role NOT NULL,
  organization_id uuid REFERENCES organizations(id) ON DELETE SET NULL,
  birthdate date,
  consent_status consent_status NOT NULL DEFAULT 'not_required',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE password_reset_tokens (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  token_hash text NOT NULL UNIQUE,
  expires_at timestamptz NOT NULL,
  consumed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE classrooms (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id, name)
);

CREATE TABLE classroom_members (
  classroom_id uuid NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
  account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  member_role classroom_member_role NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (classroom_id, account_id)
);

CREATE TABLE subjects (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  catalog_id uuid NOT NULL REFERENCES catalogs(id) ON DELETE RESTRICT,
  name text NOT NULL,
  slug text NOT NULL,
  audience_tier audience_tier NOT NULL,
  is_programming boolean NOT NULL DEFAULT false,
  generator_supported boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (catalog_id, slug)
);

CREATE TABLE learning_paths (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  catalog_id uuid NOT NULL REFERENCES catalogs(id) ON DELETE RESTRICT,
  name text NOT NULL,
  slug text NOT NULL,
  audience_tier audience_tier NOT NULL,
  is_purchasable boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (catalog_id, slug)
);

CREATE TABLE lessons (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id uuid NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
  audience_tier audience_tier NOT NULL,
  slug text NOT NULL,
  chapter text NOT NULL,
  previous_lesson_id uuid REFERENCES lessons(id) ON DELETE SET NULL,
  next_lesson_id uuid REFERENCES lessons(id) ON DELETE SET NULL,
  title text NOT NULL,
  epigraph text,
  objectives text[] NOT NULL DEFAULT '{}',
  body_ref text NOT NULL,
  open_source boolean NOT NULL DEFAULT false,
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (subject_id, slug)
);

CREATE TABLE path_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  path_id uuid NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
  position integer NOT NULL CHECK (position >= 0),
  kind path_item_kind NOT NULL,
  subject_id uuid REFERENCES subjects(id) ON DELETE RESTRICT,
  lesson_id uuid REFERENCES lessons(id) ON DELETE RESTRICT,
  UNIQUE (path_id, position),
  CHECK (
    (kind = 'subject' AND subject_id IS NOT NULL AND lesson_id IS NULL)
    OR
    (kind = 'lesson' AND lesson_id IS NOT NULL AND subject_id IS NULL)
  )
);

CREATE TABLE classroom_paths (
  classroom_id uuid NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
  path_id uuid NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
  assigned_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (classroom_id, path_id)
);

CREATE TABLE path_enrollments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  path_id uuid NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
  current_position integer NOT NULL DEFAULT 0 CHECK (current_position >= 0),
  completed_count integer NOT NULL DEFAULT 0 CHECK (completed_count >= 0),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (account_id, path_id)
);

CREATE TABLE cross_links (
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  target_lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  PRIMARY KEY (lesson_id, target_lesson_id),
  CHECK (lesson_id <> target_lesson_id)
);

CREATE TABLE lesson_chunks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  chunk_index integer NOT NULL CHECK (chunk_index >= 0),
  text text NOT NULL,
  embedding vector(1536),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (lesson_id, chunk_index)
);

CREATE TABLE practice_problems (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id uuid NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
  lesson_id uuid REFERENCES lessons(id) ON DELETE CASCADE,
  tier practice_problem_tier NOT NULL,
  prompt text NOT NULL,
  solution text NOT NULL,
  source practice_problem_source NOT NULL,
  source_hash text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE progress (
  account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  stage text NOT NULL,
  completed_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (account_id, lesson_id, stage)
);

CREATE TABLE grasp_scores (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  score integer NOT NULL CHECK (score BETWEEN 25 AND 100),
  flagged_for_review boolean NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE review_schedules (
  account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  next_review_date timestamptz NOT NULL,
  interval_days integer NOT NULL CHECK (interval_days >= 0),
  last_score integer NOT NULL CHECK (last_score BETWEEN 25 AND 100),
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (account_id, lesson_id)
);

CREATE TABLE affiliates (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id uuid NOT NULL UNIQUE REFERENCES accounts(id) ON DELETE CASCADE,
  referral_id text NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE referrals (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  affiliate_id uuid NOT NULL REFERENCES affiliates(id) ON DELETE CASCADE,
  attribution_token text NOT NULL UNIQUE,
  visit_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE conversions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  referral_id uuid NOT NULL UNIQUE REFERENCES referrals(id) ON DELETE RESTRICT,
  account_id uuid NOT NULL UNIQUE REFERENCES accounts(id) ON DELETE CASCADE,
  converted_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE student_record_audits (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  accessor_account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
  student_account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  lesson_id uuid REFERENCES lessons(id) ON DELETE SET NULL,
  accessed_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX lesson_chunks_embedding_idx ON lesson_chunks USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX lessons_subject_idx ON lessons(subject_id);
CREATE INDEX progress_account_idx ON progress(account_id);
CREATE INDEX grasp_scores_account_lesson_idx ON grasp_scores(account_id, lesson_id, created_at DESC);
CREATE INDEX review_schedules_due_idx ON review_schedules(account_id, next_review_date);
CREATE INDEX classroom_members_account_idx ON classroom_members(account_id);
CREATE INDEX password_reset_tokens_account_idx ON password_reset_tokens(account_id, created_at DESC);
