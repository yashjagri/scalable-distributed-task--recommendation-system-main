CREATE EXTENSION IF NOT EXISTS "pgcrypto"; --importing library

DROP TABLE IF EXISTS recommendations;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- format is name of col, type, parameters, forced data type

CREATE TABLE items (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  metadata   JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE events (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- references are important here
  item_id    UUID          REFERENCES items(id) ON DELETE SET NULL, -- ON DELETE CASCADE is deleting the parent id and all children, ON SET NULL is deleting just parent
  event_type TEXT NOT NULL,
  value      JSONB,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_events_user_created_at  ON events (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_user_event_type  ON events (user_id, event_type);

-- Recommendations: precomputed per-user scores. One row = one (user, item) pair.
CREATE TABLE recommendations (
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  item_id    UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  score      DOUBLE PRECISION NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, item_id)
);

CREATE INDEX IF NOT EXISTS idx_recommendations_user_score_desc ON recommendations (user_id, score DESC);


-- creating data schema. we will then create a connection using a postgres url and spin up a postgres db in a docker container!
