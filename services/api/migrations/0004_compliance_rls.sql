ALTER TABLE progress ADD COLUMN is_education_record boolean NOT NULL DEFAULT false;
ALTER TABLE grasp_scores ADD COLUMN is_education_record boolean NOT NULL DEFAULT false;

-- Trigger to automatically classify records for 'student' accounts
CREATE OR REPLACE FUNCTION classify_education_record()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM accounts WHERE id = NEW.account_id AND role = 'student') THEN
    NEW.is_education_record := true;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER classify_progress_record
  BEFORE INSERT OR UPDATE ON progress
  FOR EACH ROW EXECUTE FUNCTION classify_education_record();

CREATE TRIGGER classify_grasp_score_record
  BEFORE INSERT OR UPDATE ON grasp_scores
  FOR EACH ROW EXECUTE FUNCTION classify_education_record();

-- Enable RLS
ALTER TABLE progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE grasp_scores ENABLE ROW LEVEL SECURITY;

-- Note: In a real environment, we'd set the app.current_account_id config in the transaction block before querying.
-- RLS policies for progress
CREATE POLICY progress_isolation_policy ON progress
  FOR ALL
  USING (
    account_id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
    OR
    EXISTS (
      SELECT 1 FROM classroom_members cm
      JOIN classroom_members cm2 ON cm.classroom_id = cm2.classroom_id
      WHERE cm.account_id = progress.account_id
        AND cm2.account_id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
        AND cm2.member_role = 'educator'
    )
    OR
    EXISTS (
      SELECT 1 FROM accounts a
      JOIN accounts org_admin ON a.organization_id = org_admin.organization_id
      WHERE a.id = progress.account_id
        AND org_admin.id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
        AND org_admin.role = 'org_admin'
    )
  );

-- RLS policies for grasp_scores
CREATE POLICY grasp_scores_isolation_policy ON grasp_scores
  FOR ALL
  USING (
    account_id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
    OR
    EXISTS (
      SELECT 1 FROM classroom_members cm
      JOIN classroom_members cm2 ON cm.classroom_id = cm2.classroom_id
      WHERE cm.account_id = grasp_scores.account_id
        AND cm2.account_id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
        AND cm2.member_role = 'educator'
    )
    OR
    EXISTS (
      SELECT 1 FROM accounts a
      JOIN accounts org_admin ON a.organization_id = org_admin.organization_id
      WHERE a.id = grasp_scores.account_id
        AND org_admin.id = NULLIF(current_setting('app.current_account_id', true), '')::uuid
        AND org_admin.role = 'org_admin'
    )
  );

-- Consent Gate Trigger for under-13
CREATE OR REPLACE FUNCTION enforce_consent_gate()
RETURNS TRIGGER AS $$
DECLARE
  v_birthdate date;
  v_consent_status consent_status;
BEGIN
  SELECT birthdate, consent_status INTO v_birthdate, v_consent_status
  FROM accounts
  WHERE id = NEW.account_id;

  IF v_birthdate IS NOT NULL 
     AND age(current_date, v_birthdate) < interval '13 years' 
     AND v_consent_status <> 'granted' THEN
    RAISE EXCEPTION 'COPPA Consent Required: Cannot write personal data for under-13 user without granted consent.';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_consent_progress
  BEFORE INSERT OR UPDATE ON progress
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();

CREATE TRIGGER enforce_consent_grasp_scores
  BEFORE INSERT OR UPDATE ON grasp_scores
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();

CREATE TRIGGER enforce_consent_review_schedules
  BEFORE INSERT OR UPDATE ON review_schedules
  FOR EACH ROW EXECUTE FUNCTION enforce_consent_gate();

