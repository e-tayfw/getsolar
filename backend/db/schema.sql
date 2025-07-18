-- 1) Drop old tables (in the right order)
DROP TABLE IF EXISTS lead_events;
DROP TABLE IF EXISTS leads;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS actions;
DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS qualifications;


-- 2) Create new tables

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    company VARCHAR(255),
    referral_source VARCHAR(100),
    budget NUMERIC,
    timeline_months INTEGER,
    interest_level VARCHAR(50),
    requested_capacity VARCHAR(50),
    status VARCHAR(50) DEFAULT 'new'
);

CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50),
    qualification_status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2.4 Schedules (Google‐Calendar slots, etc.)
CREATE TABLE schedules (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    slot TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50),
    calendar_event_id VARCHAR(255)
);

-- 2.5 Qualifications (questions + responses)
CREATE TABLE qualifications (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    -- qualifications belong to a lead/user and record status changes
    questions JSONB,       -- e.g. [{question_id, text}, …]
    responses JSONB,       -- e.g. [{question_id, answer}, …]
    result BOOLEAN,
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);