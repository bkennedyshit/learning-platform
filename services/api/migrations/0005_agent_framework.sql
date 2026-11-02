-- 0005_agent_framework.sql
-- Durable storage for the learning-agent framework: sessions, turns, plans,
-- traces, approvals, artifacts, and the learner model (goals, mastery,
-- attempts, misconceptions, preferences, session summaries).
--
-- Unit tests do not require a live Postgres; the in-memory and JSON-file stores
-- back the deterministic test suite. This migration mirrors those shapes for
-- the production data path (P1) and enforces isolation + consent as runtime
-- requirements.

-- ---------------------------------------------------------------------------
-- Agent runtime records
-- ---------------------------------------------------------------------------

CREATE TABLE agent_sessions (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id    uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  role          text NOT NULL,
  status        text NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
  goal_id       uuid,
  lesson_id     uuid,
  summary       text,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX agent_sessions_account_idx ON agent_sessions(account_id);

CREATE TABLE conversation_turns (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id    uuid NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
  account_id    uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  turn_index    integer NOT NULL,
  author        text NOT NULL CHECK (author IN ('learner', 'agent', 'system', 'educator')),
  content       text NOT NULL,
  artifact_ids  uuid[] NOT NULL DEFAULT '{}',
  citations     jsonb NOT NULL DEFAULT '[]',
  created_at    timestamptz NOT NULL DEFAULT now(),
  UNIQUE (session_id, turn_index)
);

CREATE TABLE agent_plans (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id    uuid NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
  account_id    uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  goal          text NOT NULL,
  revision      integer NOT NULL DEFAULT 0,
  steps         jsonb NOT NULL DEFAULT '[]',
  created_at    timestamptz NOT NULL DEFAULT now()
);

-- Trace events store observable decisions, evidence, and tool activity only.
-- Storing hidden model reasoning / chain-of-thought is prohibited by design.
CREATE TABLE agent_trace_events (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id    uuid NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
  account_id    uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  seq           integer NOT NULL,
  event_type    text NOT NULL,
  summary       text NOT NULL,
  data          jsonb,
  created_at    timestamptz NOT NULL DEFAULT now(),
  UNIQUE (session_id, seq),
  CHECK (event_type IN (
    'plan_created', 'plan_revised', 'tool_call', 'tool_result', 'observation',
    'decision', 'approval', 'job_progress', 'memory_update', 'error'
  )),
  -- Defense in depth: forbid a persisted hidden-reasoning field.
  CHECK (data IS NULL OR NOT (data ? 'reasoning' OR data ? 'chainOfThought' OR data ? 'thoughts'))
);

CREATE TABLE agent_jobs (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id          uuid NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
  account_id          uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  kind                text NOT NULL,
  status              text NOT NULL DEFAULT 'queued'
                        CHECK (status IN ('queued', 'running', 'succeeded', 'failed', 'cancelled')),
  progress            numeric NOT NULL DEFAULT 0 CHECK (progress >= 0 AND progress <= 1),
  result_artifact_ids uuid[] NOT NULL DEFAULT '{}',
  error               jsonb,
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Artifacts and approvals
-- ---------------------------------------------------------------------------

CREATE TABLE learning_artifacts (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id        uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  version           integer NOT NULL DEFAULT 1 CHECK (version >= 1),
  kind              text NOT NULL CHECK (kind IN
                      ('svg', 'mermaid', 'plot', 'interactive', 'note', 'flashcard', 'study_plan', 'assessment')),
  title             text NOT NULL,
  description       text NOT NULL DEFAULT '',
  alt_text          text NOT NULL,
  source            text NOT NULL,          -- original, for audit only
  sanitized_source  text NOT NULL,          -- what is presented/rendered
  lesson_ids        text[] NOT NULL DEFAULT '{}',
  concept_ids       text[] NOT NULL DEFAULT '{}',
  created_by        text NOT NULL CHECK (created_by IN ('learner', 'educator', 'agent')),
  provider          text,
  exports           jsonb NOT NULL DEFAULT '[]',
  created_at        timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE agent_approvals (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  artifact_id   uuid NOT NULL REFERENCES learning_artifacts(id) ON DELETE CASCADE,
  session_id    uuid REFERENCES agent_sessions(id) ON DELETE SET NULL,
  action        text NOT NULL CHECK (action IN
                  ('publish', 'share', 'contact_educator', 'change_goal', 'submit_graded')),
  status        text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'pending', 'approved', 'rejected')),
  requested_by  text NOT NULL,
  version       integer NOT NULL CHECK (version >= 1),
  decided_by    uuid REFERENCES accounts(id),
  decided_at    timestamptz,
  reason        text,
  provenance    jsonb,
  created_at    timestamptz NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Learner model
-- ---------------------------------------------------------------------------

CREATE TABLE learner_goals (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id          uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  description         text NOT NULL,
  target_concept_ids  text[] NOT NULL DEFAULT '{}',
  status              text NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'achieved', 'abandoned')),
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX learner_goals_account_idx ON learner_goals(account_id);

CREATE TABLE concept_mastery (
  account_id   uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  concept_id   text NOT NULL,
  mastery      numeric NOT NULL CHECK (mastery >= 0 AND mastery <= 1),
  confidence   numeric NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  updated_at   timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (account_id, concept_id)
);

CREATE TABLE learner_attempts (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id   uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  concept_id   text NOT NULL,
  lesson_id    text,
  prompt       text NOT NULL,
  response     text NOT NULL,
  correct      boolean NOT NULL,
  score        numeric NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX learner_attempts_account_idx ON learner_attempts(account_id);

CREATE TABLE learner_misconceptions (
  id                     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id             uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  concept_id             text NOT NULL,
  description            text NOT NULL,
  evidence_attempt_ids   uuid[] NOT NULL DEFAULT '{}',
  status                 text NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'resolved')),
  created_at             timestamptz NOT NULL DEFAULT now(),
  updated_at             timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE learner_preferences (
  account_id         uuid PRIMARY KEY REFERENCES accounts(id) ON DELETE CASCADE,
  explanation_depth  text NOT NULL DEFAULT 'standard' CHECK (explanation_depth IN ('brief', 'standard', 'deep')),
  preferred_modality text NOT NULL DEFAULT 'read' CHECK (preferred_modality IN ('read', 'listen', 'write', 'code', 'handwrite')),
  accommodations     text[] NOT NULL DEFAULT '{}',
  updated_at         timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE agent_session_summaries (
  session_id        uuid PRIMARY KEY REFERENCES agent_sessions(id) ON DELETE CASCADE,
  account_id        uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  summary           text NOT NULL,
  source_lesson_ids text[] NOT NULL DEFAULT '{}',
  updated_at        timestamptz NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Row-level security: each learner sees only their own records; educators see
-- their classroom members; org admins see their org.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION agent_row_visible(row_account_id uuid)
RETURNS boolean AS $$
BEGIN
  RETURN
    row_account_id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
    OR EXISTS (
      SELECT 1 FROM classroom_members cm
      JOIN classroom_members cm2 ON cm.classroom_id = cm2.classroom_id
      WHERE cm.account_id = row_account_id
        AND cm2.account_id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
        AND cm2.member_role = 'educator'
    )
    OR EXISTS (
      SELECT 1 FROM accounts a
      JOIN accounts org_admin ON a.organization_id = org_admin.organization_id
      WHERE a.id = row_account_id
        AND org_admin.id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
        AND org_admin.role = 'org_admin'
    );
END;
$$ LANGUAGE plpgsql STABLE;

DO $$
DECLARE
  t text;
BEGIN
  FOREACH t IN ARRAY ARRAY[
    'agent_sessions', 'conversation_turns', 'agent_plans', 'agent_trace_events',
    'agent_jobs', 'learning_artifacts', 'learner_goals', 'concept_mastery',
    'learner_attempts', 'learner_misconceptions', 'learner_preferences',
    'agent_session_summaries'
  ] LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY;', t);
    EXECUTE format(
      'CREATE POLICY %I ON %I FOR ALL USING (agent_row_visible(account_id));',
      t || '_isolation', t
    );
  END LOOP;
END;
$$;

-- ---------------------------------------------------------------------------
-- Consent gate (COPPA): reuse enforce_consent_gate() from 0004 on account-owned
-- writable agent tables.
-- ---------------------------------------------------------------------------

CREATE TRIGGER enforce_consent_learner_goals
  BEFORE INSERT OR UPDATE ON learner_goals
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();

CREATE TRIGGER enforce_consent_concept_mastery
  BEFORE INSERT OR UPDATE ON concept_mastery
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();

CREATE TRIGGER enforce_consent_learner_attempts
  BEFORE INSERT OR UPDATE ON learner_attempts
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();

CREATE TRIGGER enforce_consent_learner_misconceptions
  BEFORE INSERT OR UPDATE ON learner_misconceptions
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();

CREATE TRIGGER enforce_consent_conversation_turns
  BEFORE INSERT OR UPDATE ON conversation_turns
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();

CREATE TRIGGER enforce_consent_agent_sessions
  BEFORE INSERT OR UPDATE ON agent_sessions
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();
