CREATE TABLE "Annotator" (
  "id" integer PRIMARY KEY,
  "email" varchar,
  "role" varchar,
  "created_at" timestamp,
  "password" varchar
);

CREATE TABLE "Sample" (
  "id" integer PRIMARY KEY,
  "text" text,
  "alphaSet" bool,
  "isAnnotated" bool
);

CREATE TABLE "Annnotation" (
  "sampleId" integer,
  "annotatorId" integer,
  "iteration" integer,
  "isValid" bool
);

CREATE TABLE "Validations" (
  "sampleId" integer,
  "annotatorId" integer,
  "isValid" bool,
  "iteration" integer
);

CREATE TABLE "Model" (
  "id" integer PRIMARY KEY,
  "object" glob,
  "iteration" integer UNIQUE
);

COMMENT ON COLUMN "Sample"."text" IS 'The text content of the sample';

COMMENT ON COLUMN "Sample"."alphaSet" IS 'Is Sample part of AlphaSet';

COMMENT ON COLUMN "Sample"."isAnnotated" IS 'Is set to true when a sample gets a valid Annotation';

COMMENT ON COLUMN "Annnotation"."isValid" IS 'Set to true if annotation is Validated';

COMMENT ON TABLE "Model" IS 'Saves a finetuned model ';

ALTER TABLE "Annnotation" ADD FOREIGN KEY ("sampleId") REFERENCES "Sample" ("id");

ALTER TABLE "Annnotation" ADD FOREIGN KEY ("annotatorId") REFERENCES "Annotator" ("id");

ALTER TABLE "Annnotation" ADD FOREIGN KEY ("iteration") REFERENCES "Model" ("iteration");

ALTER TABLE "Validations" ADD FOREIGN KEY ("sampleId") REFERENCES "Sample" ("id");

ALTER TABLE "Validations" ADD FOREIGN KEY ("annotatorId") REFERENCES "Annotator" ("id");

ALTER TABLE "Validations" ADD FOREIGN KEY ("iteration") REFERENCES "Model" ("iteration");
