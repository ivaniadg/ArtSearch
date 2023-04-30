CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    userid VARCHAR NOT NULL,
    page VARCHAR NOT NULL,
    version INT NOT NULL,
    tstamp TIMESTAMP NOT NULL,
    actions JSONB NOT NULL
);

CREATE TABLE top10 (
  ID SERIAL PRIMARY KEY,
  userid VARCHAR NOT NULL,
  version INT NOT NULL,
  poseweight DECIMAL NOT NULL,
  colorweight DECIMAL NOT NULL,
  objectweight DECIMAL NOT NULL,
  topx JSON NOT NULL,
  pak DECIMAL NOT NULL,
  src DECIMAL NOT NULL,
  mse DECIMAL NOT NULL,
  duration INT NOT NULL
);
