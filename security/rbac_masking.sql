-- =============================================================================
-- Security: RBAC, Data Masking, Governance (Snowflake)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- RBAC: Roles and privileges
-- -----------------------------------------------------------------------------
-- CREATE ROLE ANALYTICS_ROLE;
-- CREATE ROLE ANALYTICS_READONLY;
-- CREATE ROLE PII_ANALYST;

-- GRANT USAGE ON WAREHOUSE ANALYTICS_WH TO ROLE ANALYTICS_ROLE;
-- GRANT USAGE ON DATABASE LEARNING_PLATFORM_DW TO ROLE ANALYTICS_ROLE;
-- GRANT USAGE ON SCHEMA LEARNING_PLATFORM_DW.ANALYTICS TO ROLE ANALYTICS_ROLE;
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA LEARNING_PLATFORM_DW.ANALYTICS TO ROLE ANALYTICS_ROLE;

-- GRANT USAGE ON WAREHOUSE ANALYTICS_WH TO ROLE ANALYTICS_READONLY;
-- GRANT USAGE ON DATABASE LEARNING_PLATFORM_DW TO ROLE ANALYTICS_READONLY;
-- GRANT USAGE ON SCHEMA LEARNING_PLATFORM_DW.ANALYTICS TO ROLE ANALYTICS_READONLY;
-- GRANT SELECT ON ALL TABLES IN SCHEMA LEARNING_PLATFORM_DW.ANALYTICS TO ROLE ANALYTICS_READONLY;

-- GRANT ROLE ANALYTICS_READONLY TO ROLE ANALYTICS_ROLE;
-- GRANT ROLE ANALYTICS_ROLE TO USER your_analyst_user;

-- -----------------------------------------------------------------------------
-- Data Masking: mask email / PII for non-PII roles
-- -----------------------------------------------------------------------------
-- Create masking policy (example: hash email for ANALYTICS_READONLY)
-- CREATE OR REPLACE MASKING POLICY hash_email AS (val STRING) RETURNS STRING ->
--   CASE
--     WHEN CURRENT_ROLE() IN ('PII_ANALYST', 'ACCOUNTADMIN') THEN val
--     ELSE SHA2(val, 256)::VARCHAR
--   END;

-- Apply to column (if we had raw email in a dim)
-- ALTER TABLE dim_learner MODIFY COLUMN email SET MASKING POLICY hash_email;

-- Dynamic masking for learner_id (show last 4 only for read-only)
-- CREATE OR REPLACE MASKING POLICY mask_learner_id AS (val STRING) RETURNS STRING ->
--   CASE
--     WHEN CURRENT_ROLE() IN ('ANALYTICS_ROLE', 'PII_ANALYST', 'ACCOUNTADMIN') THEN val
--     ELSE CONCAT('***', RIGHT(val, 4))
--   END;
-- ALTER TABLE dim_learner MODIFY COLUMN learner_id SET MASKING POLICY mask_learner_id;

-- -----------------------------------------------------------------------------
-- Governance: tags and object documentation
-- -----------------------------------------------------------------------------
-- CREATE TAG LEARNING_PLATFORM_DW.PII_TAG ALLOWED_VALUES 'email', 'name', 'id';
-- ALTER TABLE dim_learner SET TAG PII_TAG = 'email';
-- (Use tags for discovery and policy application.)
