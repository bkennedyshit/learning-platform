-- ============================================================
-- Tier 1 — Lead / client collection (shared across ALL sites)
-- Postgres. Apply once to the leads database.
-- Captures inbound leads from any site; source_site distinguishes them.
-- ============================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- gen_random_uuid()

-- updated_at helper -------------------------------------------------
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- contacts: every inbound lead / inquiry from any site ---------------
CREATE TABLE IF NOT EXISTS contacts (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email        text,
  name         text,
  phone        text,
  source_site  text NOT NULL,                    -- e.g. 'content-site','nepa-ai','bmx4beginners','sandblasting'
  message      text,
  tags         text[] NOT NULL DEFAULT '{}',
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT contacts_reachable CHECK (email IS NOT NULL OR phone IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS contacts_email_idx   ON contacts (lower(email));
CREATE INDEX IF NOT EXISTS contacts_source_idx  ON contacts (source_site);
CREATE INDEX IF NOT EXISTS contacts_created_idx ON contacts (created_at DESC);

DROP TRIGGER IF EXISTS contacts_set_updated_at ON contacts;
CREATE TRIGGER contacts_set_updated_at BEFORE UPDATE ON contacts
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- subscribers: newsletter / notify-me / waitlist --------------------
CREATE TABLE IF NOT EXISTS subscribers (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email        text NOT NULL,
  source_site  text NOT NULL,
  status       text NOT NULL DEFAULT 'active'
               CHECK (status IN ('active','unsubscribed','bounced')),
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now(),
  UNIQUE (email, source_site)                    -- one subscription per email per site
);
CREATE INDEX IF NOT EXISTS subscribers_status_idx ON subscribers (status);

DROP TRIGGER IF EXISTS subscribers_set_updated_at ON subscribers;
CREATE TRIGGER subscribers_set_updated_at BEFORE UPDATE ON subscribers
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- quote_requests: service-site leads (e.g. sandblasting) ------------
CREATE TABLE IF NOT EXISTS quote_requests (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id   uuid REFERENCES contacts(id) ON DELETE SET NULL,
  source_site  text NOT NULL,
  service      text NOT NULL,                    -- e.g. 'sandblasting'
  details      jsonb NOT NULL DEFAULT '{}',      -- flexible: size, location, surface, budget, etc.
  status       text NOT NULL DEFAULT 'new'
               CHECK (status IN ('new','contacted','quoted','won','lost')),
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS quote_status_idx  ON quote_requests (status);
CREATE INDEX IF NOT EXISTS quote_created_idx ON quote_requests (created_at DESC);

DROP TRIGGER IF EXISTS quote_set_updated_at ON quote_requests;
CREATE TRIGGER quote_set_updated_at BEFORE UPDATE ON quote_requests
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
