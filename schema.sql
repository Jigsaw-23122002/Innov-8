CREATE TABLE "Student"(
    "student_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "student_name" VARCHAR(255) NOT NULL,
    "student_email" VARCHAR(255) NOT NULL,
    "student_password" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Student" ADD PRIMARY KEY("student_id");
CREATE TABLE "Project"(
    "proj_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "proj_title" VARCHAR(255) NOT NULL,
    "proj_desc" TEXT NOT NULL,
    "proj_rich_text_desc" TEXT NOT NULL,
    "proj_images" VARCHAR(255) NOT NULL,
    "proj_drive_link" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Project" ADD PRIMARY KEY("proj_id");
CREATE TABLE "Profile"(
    "profile_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "student_id" UUID NOT NULL,
    "interest_id" UUID NOT NULL
);
ALTER TABLE
    "Profile" ADD PRIMARY KEY("profile_id");
COMMENT
ON COLUMN
    "Profile"."interest_id" IS 'Many-to-many
interests are global - not specific to a profile - use the same FK reference';
CREATE TABLE "Interest"(
    "interest_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "title" INTEGER NOT NULL
);
ALTER TABLE
    "Interest" ADD PRIMARY KEY("interest_id");
COMMENT
ON COLUMN
    "Interest"."title" IS 'Bio,chem, etc';
CREATE TABLE "Participants"(
    "participant_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "student_id" UUID NOT NULL,
    "event_id" UUID NOT NULL,
    "team_id" UUID NOT NULL,
    "participation_certificate" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Participants" ADD PRIMARY KEY("participant_id");
CREATE TABLE "Follow"(
    "follow_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "follower_id" UUID NOT NULL,
    "following_id" UUID NOT NULL
);
ALTER TABLE
    "Follow" ADD PRIMARY KEY("follow_id");
CREATE TABLE "Organizer"(
    "organizer_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "organizer_name" INTEGER NOT NULL,
    "organizer_password" INTEGER NOT NULL,
    "organizer_email" INTEGER NOT NULL
);
ALTER TABLE
    "Organizer" ADD PRIMARY KEY("organizer_id");
CREATE TABLE "Event"(
    "event_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "event_type_id" UUID NOT NULL,
    "organizer_id" UUID NOT NULL,
    "team_id" UUID NOT NULL,
    "event_start_date" DATE NOT NULL,
    "event_end_date" DATE NOT NULL,
    "event_location" VARCHAR(255) NOT NULL,
    "event_description" TEXT NOT NULL
);
ALTER TABLE
    "Event" ADD PRIMARY KEY("event_id");
CREATE TABLE "EventType"(
    "type_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "type_name" INTEGER NOT NULL
);
ALTER TABLE
    "EventType" ADD PRIMARY KEY("type_id");
COMMENT
ON COLUMN
    "EventType"."type_name" IS 'Exhibition, fair, competition, etc';
CREATE TABLE "Team"(
    "team_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "proj_id" UUID NOT NULL,
    "event_id" UUID NOT NULL
);
ALTER TABLE
    "Team" ADD PRIMARY KEY("team_id");
CREATE TABLE "Sponsor"(
    "sponsor_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "sponsor_email" VARCHAR(255) NOT NULL,
    "sponsor_password" VARCHAR(255) NOT NULL,
    "sponsor_name" VARCHAR(255) NOT NULL,
    "sponsor_interests" INTEGER NOT NULL,
    "sponsorship_tier" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Sponsor" ADD PRIMARY KEY("sponsor_id");
CREATE TABLE "Sponsorship"(
    "sponsorer_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "sponsor_id" UUID NOT NULL,
    "event_id" UUID NOT NULL
);
ALTER TABLE
    "Sponsorship" ADD PRIMARY KEY("sponsorer_id");
CREATE TABLE "Votes"(
    "vote_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "team_id" UUID NOT NULL,
    "student_id" UUID NOT NULL
);
ALTER TABLE
    "Votes" ADD PRIMARY KEY("vote_id");
CREATE TABLE "ProjectLink"(
    "link_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "project_id" UUID NOT NULL,
    "student_id" UUID NOT NULL
);
ALTER TABLE
    "ProjectLink" ADD PRIMARY KEY("link_id");
CREATE TABLE "Comment"(
    "comment_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "project_id" UUID NOT NULL,
    "commenter_id" UUID NOT NULL,
    "comment_content" INTEGER NOT NULL
);
ALTER TABLE
    "Comment" ADD PRIMARY KEY("comment_id");
ALTER TABLE
    "Votes" ADD CONSTRAINT "votes_student_id_foreign" FOREIGN KEY("student_id") REFERENCES "Student"("student_id");
ALTER TABLE
    "Team" ADD CONSTRAINT "team_proj_id_foreign" FOREIGN KEY("proj_id") REFERENCES "Project"("proj_id");
ALTER TABLE
    "Profile" ADD CONSTRAINT "profile_student_id_foreign" FOREIGN KEY("student_id") REFERENCES "Student"("student_id");
ALTER TABLE
    "Profile" ADD CONSTRAINT "profile_interest_id_foreign" FOREIGN KEY("interest_id") REFERENCES "Interest"("interest_id");
ALTER TABLE
    "Participants" ADD CONSTRAINT "participants_student_id_foreign" FOREIGN KEY("student_id") REFERENCES "Student"("student_id");
ALTER TABLE
    "Participants" ADD CONSTRAINT "participants_event_id_foreign" FOREIGN KEY("event_id") REFERENCES "Event"("event_id");
ALTER TABLE
    "Participants" ADD CONSTRAINT "participants_team_id_foreign" FOREIGN KEY("team_id") REFERENCES "Team"("team_id");
ALTER TABLE
    "Follow" ADD CONSTRAINT "follow_follower_id_foreign" FOREIGN KEY("follower_id") REFERENCES "Profile"("profile_id");
ALTER TABLE
    "Follow" ADD CONSTRAINT "follow_following_id_foreign" FOREIGN KEY("following_id") REFERENCES "Profile"("profile_id");
ALTER TABLE
    "Event" ADD CONSTRAINT "event_organizer_id_foreign" FOREIGN KEY("organizer_id") REFERENCES "Organizer"("organizer_id");
ALTER TABLE
    "Event" ADD CONSTRAINT "event_event_type_id_foreign" FOREIGN KEY("event_type_id") REFERENCES "EventType"("type_id");
ALTER TABLE
    "Event" ADD CONSTRAINT "event_team_id_foreign" FOREIGN KEY("team_id") REFERENCES "Team"("team_id");
ALTER TABLE
    "Team" ADD CONSTRAINT "team_event_id_foreign" FOREIGN KEY("event_id") REFERENCES "Event"("event_id");
ALTER TABLE
    "Sponsorship" ADD CONSTRAINT "sponsorship_sponsor_id_foreign" FOREIGN KEY("sponsor_id") REFERENCES "Sponsor"("sponsor_id");
ALTER TABLE
    "Sponsorship" ADD CONSTRAINT "sponsorship_event_id_foreign" FOREIGN KEY("event_id") REFERENCES "Event"("event_id");
ALTER TABLE
    "Votes" ADD CONSTRAINT "votes_team_id_foreign" FOREIGN KEY("team_id") REFERENCES "Team"("team_id");
ALTER TABLE
    "ProjectLink" ADD CONSTRAINT "projectlink_project_id_foreign" FOREIGN KEY("project_id") REFERENCES "Project"("proj_id");
ALTER TABLE
    "ProjectLink" ADD CONSTRAINT "projectlink_student_id_foreign" FOREIGN KEY("student_id") REFERENCES "Student"("student_id");
ALTER TABLE
    "Comment" ADD CONSTRAINT "comment_project_id_foreign" FOREIGN KEY("project_id") REFERENCES "Project"("proj_id");
ALTER TABLE
    "Comment" ADD CONSTRAINT "comment_commenter_id_foreign" FOREIGN KEY("commenter_id") REFERENCES "Student"("student_id");

CREATE TABLE "Likes"(
    "like_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "liker_id" UUID NOT NULL REFERENCES "Student",
    "project_id" UUID NOT NULL REFERENCES "Project"
);
ALTER TABLE
    "Likes" ADD PRIMARY KEY("like_id");

CREATE TABLE "Message"(
    "message_id" UUID NOT NULL DEFAULT(uuid_generate_v4()),
    "user_id" UUID NOT NULL REFERENCES "Student",
    "to_id" UUID NOT NULL REFERENCES "Student",
    "user_msg" varchar
);
ALTER TABLE
    "Message" ADD PRIMARY KEY("message_id");

