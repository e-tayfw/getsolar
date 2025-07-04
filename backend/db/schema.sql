-- 1) Leads table
CREATE TABLE leads (
  lead_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email             TEXT NOT NULL UNIQUE,
  name              TEXT,
  status            TEXT NOT NULL,  -- e.g. 'new', 'qualify_sent', 'booked', 'rejected'
  interest_level    TEXT,           -- e.g. 'high', 'medium', 'low'
  budget            NUMERIC(12,2),  -- budget in SGD
  timeline_months   INT,            -- desired timeline
  site_visit_time   TIMESTAMPTZ,    -- scheduled visit
  questionnaire     JSONB,          -- {q1: ans1, q2: ans2...}
  rejection_reason  TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2) Lead events table (episodic log)
CREATE TABLE lead_events (
  event_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id     UUID NOT NULL REFERENCES leads(lead_id) ON DELETE CASCADE,
  event_type  TEXT NOT NULL,       -- 'qualify_sent','booked','cancelled','rejected','reminder_sent'
  payload     JSONB,               -- any extra data (timestamps, slot info, etc.)
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes for fast lookups
CREATE INDEX ON leads (status);
CREATE INDEX ON lead_events (lead_id, event_type);