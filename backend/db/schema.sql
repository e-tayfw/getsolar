-- 1) Drop old tables (in the right order)
DROP TABLE IF EXISTS lead_events;
DROP TABLE IF EXISTS leads;

-- 2) Create new tables

-- 2.1 Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL
);

-- 2.2 Leads (now pointing at users)
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2.3 Actions (audit log of any user action)
CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action_type VARCHAR(50),
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2.4 Schedules (Google‐Calendar slots, etc.)
CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    slot TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50),
    calendar_event_id VARCHAR(255)
);

-- 2.5 Qualifications (questions + responses)
CREATE TABLE qualifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    questions JSONB,       -- e.g. [{question_id, text}, …]
    responses JSONB,       -- e.g. [{question_id, answer}, …]
    result BOOLEAN,
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);