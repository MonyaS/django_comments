ALTER DATABASE {db_name} SET client_encoding TO 'UTF8';

CREATE TABLE IF NOT EXISTS "comments"
(
    "id"        BIGSERIAL,-- Uniq identifier of record.
    "user_id"   BIGINT, -- Internal user identifier in auth db.

    "parent_id" BIGINT NULL DEFAULT NULL, -- Id of parent record.
    "home_page" TEXT   NULL DEFAULT NULL, -- Url of page on which the comment was added.
    "text"      TEXT, -- Text of the comments.

    PRIMARY KEY ("id")
);
COMMENT ON TABLE "comments" IS 'Table for storing information about user comments.';

COMMENT ON COLUMN "comments"."id" IS 'Uniq identifier of record.';
COMMENT ON COLUMN "comments"."user_id" IS 'Internal user identifier in auth db.';
COMMENT ON COLUMN "comments"."parent_id" IS 'Id of parent record.';
COMMENT ON COLUMN "comments"."home_page" IS 'Url of page on which the comment was added.';
COMMENT ON COLUMN "comments"."text" IS 'Text of the comments.';