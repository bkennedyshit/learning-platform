# Requirements Document

## Introduction

The Learning Platform is a single education product composed of four separately deployable surfaces that share one content corpus organized into two distinct catalogs. The guiding thesis is that raw general-purpose AI is powerful but unusable by most learners ("gas without a car"); this platform is the structured vehicle that guides and tracks everyday, non-technical learners through vetted material along directed learning paths.

The four deployable surfaces are:

1. **Open Content Site** — a publicly accessible, heavily interlinked, SEO-optimized lesson site built from the Corpus. It is the free top-of-funnel and organic-search engine, and the majority of its data is open-sourced.
2. **Learner App** — the monetized, signed-in SaaS used by both individual (B2C) learners and B2E students. An AI tutor grounded by Retrieval-Augmented Generation (RAG) over the Corpus guides learners through Directed Learning Paths and the modality-cycling reinforcement loop (Read → Listen → Write → Code → Handwrite), tracks progress, assesses grasp, and schedules spaced repetition.
3. **Educator Console** — the B2E administrative surface for schools and districts: organization and classroom management, seat management, educator dashboards, and student progress visibility, with compliance controls (FERPA and COPPA).
4. **Spatial Calculator** — a browser-first WebXR 3D math visualizer, independently deployable (with a planned Meta VR store release) and embeddable as a widget inside math lessons.

Calculators are part of the mix but are not a standalone product: the Spatial Calculator is embedded as a widget within the Content Site and Learner App math lessons, and lighter inline calculators appear as components where useful.

The Corpus is organized into two catalogs sold as distinct offerings:

- **K-12 Catalog** — leveled subjects organized into Directed Learning Paths by grade band (K-5, 6-8, 9-12) plus a Higher Education path and standardized test-prep paths (for example SAT Math, AP alignments). This is the primary B2E product; schools buy directed, standards-aligned paths.
- **Advanced Track Catalog** — a frontier, self-directed corpus spanning advanced STEM, programming languages, human languages, and craft subjects, aimed at self-directed B2C/prosumer and higher-education learners.

The platform also includes a business layer: a B2E offering (multi-seat management, educator dashboards, FERPA/COPPA compliance), B2C self-serve accounts, and an affiliate marketing program. Two cross-cutting principles bind the system together: the authored Corpus is the moat (the AI must not generate or hallucinate lessons), and the experience must be usable by non-technical learners with zero jargon.

## Glossary

- **Learning_Platform**: The complete product encompassing all four deployable surfaces and the business layer.
- **Corpus**: The complete pre-authored content asset, organized into two catalogs (K-12 Catalog and Advanced Track Catalog), comprising markdown Lessons, SVG diagram assets, practice problem banks, and Directed Learning Paths.
- **K12_Catalog**: The catalog of leveled K-12 Subjects and their grade-band and test-prep Directed Learning Paths; the primary B2E product. Currently spans 22 Subjects with grade-band pipelines (K-5, 6-8, 9-12), a Higher Education path, and test-prep paths (SAT Math, AP alignments).
- **Advanced_Track_Catalog**: The catalog of advanced, self-directed Subjects (currently 51) for B2C/prosumer and higher-education learners.
- **Catalog**: One of the two top-level content offerings (K12_Catalog or Advanced_Track_Catalog) that a Subject and its Lessons belong to.
- **Directed_Learning_Path**: An ordered, enrollable sequence of Subjects and Lessons that a learner follows in order (for example, "6-8 Middle School Pipeline" or "SAT Math Pipeline"). Each Directed_Learning_Path is a discrete sellable offering.
- **Path_Enrollment**: A learner's enrollment in a Directed_Learning_Path, tracking their ordered position and path-level completion.
- **Lesson**: A single authored unit of the Corpus, structured with frontmatter (chapter, previous link, next link), learning objectives, an epigraph, body content, and cross-links.
- **Subject**: A top-level grouping of related Lessons (for example, Calculus, Rust, Japanese, Algebra I), belonging to exactly one Catalog.
- **Audience_Tier**: A defined learner population and difficulty level for content. K-12 tiers are the grade bands (K-5, 6-8, 9-12); additional tiers include Higher Education and the advanced personal-learning tier.
- **Content_Site**: The publicly accessible, interlinked, SEO-optimized vertical that renders open Corpus Lessons.
- **Learning_App**: The signed-in, monetized SaaS surface that delivers the guided learning experience to B2C learners and B2E students.
- **Educator_Console**: The B2E administrative surface where educators and organization administrators manage organizations, classrooms, seats, and view student progress.
- **AI_Tutor**: The agentic tutoring component of the Learning_App, composed of an LLM, RAG over the Corpus, learner progress state, and the grasp-assessment loop.
- **RAG**: Retrieval-Augmented Generation; the technique by which the AI_Tutor retrieves passages from the Corpus and uses only that retrieved material to ground its responses.
- **Modality_Loop**: The reinforcement learning cycle consisting of the ordered stages Read, Listen, Write, Code, and Handwrite.
- **Read_Stage**: The Modality_Loop stage in which the learner reads Lesson text.
- **Listen_Stage**: The Modality_Loop stage in which Lesson text is played as audio via text-to-speech with synchronized word highlighting.
- **Write_Stage**: The Modality_Loop stage in which the learner types responses or solutions.
- **Code_Stage**: The Modality_Loop stage in which the learner writes and runs code, applicable to programming Subjects.
- **Handwrite_Stage**: The Modality_Loop stage in which the learner handwrites a breakdown of the material for retention.
- **TTS**: Text-to-speech audio generation.
- **Progress_Tracker**: The component that records and reports each learner's position, completion, and history across Lessons and Modality_Loop stages.
- **Grasp_Assessor**: The component that evaluates a learner's mastery of a Lesson and produces a Grasp_Score.
- **Grasp_Score**: A numeric measure, on a defined scale, of a learner's assessed mastery of a specific Lesson.
- **Spaced_Repetition_Scheduler**: The component that schedules review of previously studied Lessons based on Grasp_Scores and elapsed time.
- **Problem_Generator**: The SymPy-based component that programmatically produces tiered (easy, medium, hard, exam) practice problems for supported Subjects.
- **Practice_Problem**: A problem presented to the learner during the Write_Stage, sourced from a pre-authored practice problem bank or produced by the Problem_Generator.
- **LLM_Provider_Adapter**: The abstraction layer through which the Learning_App connects to a large language model provider, allowing the underlying provider to be swapped.
- **Spatial_Calculator**: The browser-first, VR-capable WebXR 3D math visualizer, deployed as a separate artifact.
- **WebXR**: The browser API standard for rendering immersive 3D and virtual-reality experiences.
- **Organization**: A B2E customer entity such as a school or district.
- **Classroom**: A grouping of Student accounts managed by one or more Educators within an Organization.
- **Educator**: A B2E user who manages Classrooms and reviews Student progress.
- **Student**: A learner account that belongs to an Organization and is managed within a Classroom.
- **Educator_Dashboard**: The interface through which an Educator views Classroom and Student progress.
- **Organization_Manager**: The component that administers Organizations, Classrooms, seats, and roles.
- **Auth_Service**: The component that handles account registration, authentication, and authorization.
- **Affiliate**: A partner who refers new learners in exchange for tracked credit.
- **Affiliate_Manager**: The component that registers Affiliates, tracks referrals, and records attributed conversions.
- **FERPA**: The U.S. Family Educational Rights and Privacy Act governing student education records.
- **COPPA**: The U.S. Children's Online Privacy Protection Act governing data collection from children under 13.

## Requirements

### Requirement 1: Shared Content Corpus as Source of Truth

**User Story:** As a platform operator, I want all surfaces to draw from one shared, authored Corpus organized into catalogs, so that vetted content remains the single source of truth and the platform's moat.

#### Acceptance Criteria

1. THE Learning_Platform SHALL store the Corpus as the single shared content source consumed by the Content_Site, the Learning_App, the Educator_Console, and the Spatial_Calculator.
2. THE Learning_Platform SHALL represent each Lesson with frontmatter fields for chapter, previous-Lesson link, and next-Lesson link, plus learning objectives, an epigraph, body content, and cross-links.
3. THE Learning_Platform SHALL associate each Lesson with exactly one Subject, and each Subject with exactly one Catalog and exactly one Audience_Tier.
4. WHEN a Lesson is updated in the Corpus, THE Learning_Platform SHALL make the updated Lesson available to all consuming surfaces from the same shared source.
5. THE Learning_Platform SHALL store SVG diagram assets as referenceable Corpus assets linkable from Lessons.
6. THE Learning_Platform SHALL allow the count of Catalogs, Subjects, Lessons, Directed_Learning_Paths, and assets to grow as new content is authored.

### Requirement 2: Corpus-Grounded Content Only (No Hallucinated Lessons)

**User Story:** As a learner, I want the platform to teach only vetted authored material, so that I can trust that what I study is accurate.

#### Acceptance Criteria

1. THE AI_Tutor SHALL generate instructional responses using only passages retrieved from the Corpus through RAG.
2. WHEN the AI_Tutor can neither retrieve a relevant Corpus passage nor source relevant Problem_Generator content for a learner question, THE AI_Tutor SHALL inform the learner that the topic is outside the available material rather than generating an unsourced lesson.
3. WHEN the AI_Tutor presents instructional content, THE AI_Tutor SHALL include a reference to the source Lesson from which the content was retrieved.
4. THE AI_Tutor SHALL access all Corpus content it uses to answer learner questions through RAG retrieval.
5. THE Learning_Platform SHALL present learners with instructional content sourced only from the authored Corpus and from the Problem_Generator output.

### Requirement 3: Open Content Site and SEO

**User Story:** As a prospective learner searching the web, I want to find free, well-structured lesson pages, so that I can start learning immediately and discover the platform.

#### Acceptance Criteria

1. THE Content_Site SHALL render published Corpus Lessons as publicly accessible pages that require no account.
2. THE Content_Site SHALL render each Lesson page with a previous-Lesson link and a next-Lesson link derived from the Lesson frontmatter.
3. THE Content_Site SHALL render cross-subject links on each Lesson page derived from the Lesson cross-links.
4. WHERE a Lesson defines no cross-links, THE Content_Site SHALL publish the Lesson page with an empty cross-link section.
5. THE Content_Site SHALL emit, for each Lesson page, a unique title, a meta description, canonical URL metadata, and structured data markup for search-engine indexing.
6. THE Content_Site SHALL generate a sitemap that enumerates all published Lesson pages.
7. WHERE a Lesson is designated open-source, THE Content_Site SHALL publish the Lesson content under the platform's open license.
8. WHEN a Lesson page is requested, THE Content_Site SHALL return the rendered page server-side so that search-engine crawlers receive complete content.

### Requirement 4: Account Registration and Authentication (B2C)

**User Story:** As an individual learner, I want to create an account and sign in, so that my progress is saved and personalized.

#### Acceptance Criteria

1. WHEN a visitor submits valid registration details, THE Auth_Service SHALL create a B2C learner account.
2. WHEN a learner submits valid credentials, THE Auth_Service SHALL authenticate the learner and establish a session.
3. IF a learner submits invalid credentials, THEN THE Auth_Service SHALL deny access and return an error message that does not reveal which credential field was incorrect.
4. THE Auth_Service SHALL restrict access to Learning_App progress data so that each learner can access only that learner's own records.
5. IF the access-restriction mechanism for learner records fails, THEN THE Auth_Service SHALL deny access to the requested records.
6. WHEN a learner requests a password reset, THE Auth_Service SHALL send a reset mechanism to the learner's verified email address.

### Requirement 5: AI Tutor Guidance

**User Story:** As a learner, I want an AI tutor to guide me through lessons step by step, so that I have structure instead of a blank prompt.

#### Acceptance Criteria

1. WHEN a learner begins a Lesson, THE AI_Tutor SHALL present the Lesson and direct the learner to the first Modality_Loop stage.
2. WHEN a learner asks a question about the current Lesson, THE AI_Tutor SHALL answer using Corpus passages retrieved through RAG.
3. WHEN a learner completes a Modality_Loop stage, THE AI_Tutor SHALL direct the learner to the next stage in the Modality_Loop order.
4. THE AI_Tutor SHALL present all guidance in plain language without technical jargon.

### Requirement 6: Modality-Cycling Reinforcement Loop

**User Story:** As a learner, I want to study each lesson through reading, listening, writing, coding, and handwriting, so that I reinforce and retain the material.

#### Acceptance Criteria

1. THE Learning_App SHALL sequence the Modality_Loop stages in the order Read_Stage, Listen_Stage, Write_Stage, Code_Stage, Handwrite_Stage.
2. WHEN the Read_Stage is active, THE Learning_App SHALL display the Lesson body text to the learner.
3. WHEN the Listen_Stage is active, THE Learning_App SHALL play the Lesson text as TTS audio with synchronized highlighting of each word as it is spoken.
4. WHEN the Write_Stage is active, THE Learning_App SHALL present a Practice_Problem and accept the learner's typed response.
5. WHERE the current Subject is a programming Subject, THE Learning_App SHALL present a Code_Stage in which the learner writes and runs code.
6. WHERE the current Subject is not a programming Subject, THE Learning_App SHALL omit the Code_Stage from the Modality_Loop for that Lesson.
7. WHEN the Handwrite_Stage is active, THE Learning_App SHALL instruct the learner to handwrite a breakdown of the material and SHALL accept confirmation that the breakdown is complete.
8. WHEN a learner completes the Handwrite_Stage for a Lesson, THE Learning_App SHALL offer to repeat the Modality_Loop or proceed to practice.

### Requirement 7: Progress Tracking

**User Story:** As a learner, I want my progress saved across lessons and stages, so that I can resume where I left off.

#### Acceptance Criteria

1. WHEN a learner completes a Modality_Loop stage, THE Progress_Tracker SHALL record the completion with the learner identifier, the Lesson identifier, the stage, and a timestamp.
2. WHEN a learner signs in, THE Progress_Tracker SHALL present the learner's most recent incomplete Lesson and stage as a resume point.
3. THE Progress_Tracker SHALL report, per learner, the count of completed Lessons and the count of in-progress Lessons per Subject.
4. WHEN a learner completes all stages of a Lesson, THE Progress_Tracker SHALL mark the Lesson as completed for that learner.

### Requirement 8: Grasp Assessment

**User Story:** As a learner, I want the platform to judge how well I understand each lesson, so that I know what to review.

#### Acceptance Criteria

1. WHEN a learner submits Write_Stage or Code_Stage responses for a Lesson, THE Grasp_Assessor SHALL evaluate the responses and produce a Grasp_Score on a 0-to-100 scale for that Lesson.
2. IF the assessment computation yields a value outside the 0-to-100 range, THEN THE Grasp_Assessor SHALL clamp the Grasp_Score to the nearest bound within the 0-to-100 range.
3. THE Grasp_Assessor SHALL apply a minimum Grasp_Score floor of 25 so that no recorded Grasp_Score is below 25.
4. THE Grasp_Assessor SHALL store each Grasp_Score with the learner identifier, the Lesson identifier, and a timestamp.
5. IF a learner's Grasp_Score for a Lesson is below 70, THEN THE Grasp_Assessor SHALL flag the Lesson for review.
6. THE Grasp_Assessor SHALL base each Grasp_Score on the learner's responses compared against Corpus-derived expected answers.

### Requirement 9: Spaced Repetition Scheduling

**User Story:** As a learner, I want previously studied lessons scheduled for review at the right time, so that I retain what I learned.

#### Acceptance Criteria

1. WHEN a Grasp_Score is recorded for a Lesson, THE Spaced_Repetition_Scheduler SHALL compute a next-review date for that Lesson based on the Grasp_Score and the time elapsed since the prior review.
2. WHEN a Lesson's next-review date is reached, THE Spaced_Repetition_Scheduler SHALL add the Lesson to the learner's due-review queue.
3. THE Spaced_Repetition_Scheduler SHALL present the learner's due-review queue ordered by next-review date, earliest first.
4. WHEN a learner completes a scheduled review, THE Spaced_Repetition_Scheduler SHALL compute an updated next-review date for that Lesson.

### Requirement 10: Practice Problem Generation

**User Story:** As a learner, I want an effectively unlimited supply of grounded practice problems, so that I can practice as much as I need without running out.

#### Acceptance Criteria

1. WHERE a Subject has an authored practice problem bank, THE Learning_App SHALL source Practice_Problems for the Write_Stage from the authored practice problem bank.
2. WHERE a Subject has no authored practice problem bank but is supported by the Problem_Generator, THE Learning_App SHALL request Practice_Problems from the Problem_Generator for the Write_Stage.
3. THE Problem_Generator SHALL produce Practice_Problems at a requested difficulty tier of easy, medium, hard, or exam.
4. THE Problem_Generator SHALL produce each Practice_Problem together with its computed solution.
5. WHEN a learner requests another Practice_Problem at the same difficulty tier, THE Learning_App SHALL produce an additional problem at that tier.

### Requirement 11: Swappable LLM Provider

**User Story:** As a platform operator, I want the language model provider to be swappable, so that I can run a local model during development and a hosted model for paying users.

#### Acceptance Criteria

1. THE Learning_App SHALL access the language model exclusively through the LLM_Provider_Adapter.
2. WHERE configuration selects a local language model provider, THE LLM_Provider_Adapter SHALL route AI_Tutor requests to the local provider.
3. WHERE configuration selects a hosted language model provider, THE LLM_Provider_Adapter SHALL route AI_Tutor requests to the hosted provider.
4. IF the configured language model provider cannot be reached, THEN THE LLM_Provider_Adapter SHALL return an explicit provider-unavailable error to the AI_Tutor.
5. WHEN the configured language model provider is changed, THE LLM_Provider_Adapter SHALL apply the change without modification to AI_Tutor calling code.

### Requirement 12: Catalogs and Audience Tiers

**User Story:** As a learner at a given level, I want content matched to my catalog and tier, so that lessons are neither too advanced nor too basic.

#### Acceptance Criteria

1. THE Learning_Platform SHALL provide two Catalogs: the K12_Catalog and the Advanced_Track_Catalog.
2. THE Learning_Platform SHALL support, within the K12_Catalog, the grade-band Audience_Tiers K-5, 6-8, and 9-12, plus a Higher Education Audience_Tier; and within the Advanced_Track_Catalog, an advanced personal-learning Audience_Tier.
3. WHEN a learner selects a Catalog and Audience_Tier, THE Learning_App SHALL present Subjects and Lessons associated with that Catalog and Audience_Tier.
4. IF no Lessons exist for the selected Catalog and Audience_Tier, THEN THE Learning_App SHALL display a message indicating that no Lessons are available for that selection.
5. THE Content_Site SHALL label each Lesson page with the Lesson's Catalog and Audience_Tier.

### Requirement 20: Directed Learning Paths

**User Story:** As a student (or a school buying for students), I want an ordered curriculum path I enroll in and follow in sequence, so that I am guided through a complete course of study rather than browsing a pile of lessons.

#### Acceptance Criteria

1. THE Learning_Platform SHALL represent each Directed_Learning_Path as an ordered sequence of Subjects and Lessons.
2. THE Learning_Platform SHALL provide K-12 grade-band Directed_Learning_Paths (K-5, 6-8, 9-12), a Higher Education Directed_Learning_Path, and test-prep Directed_Learning_Paths including SAT Math and AP alignments.
3. WHEN a learner enrolls in a Directed_Learning_Path, THE Learning_App SHALL create a Path_Enrollment recording the learner's ordered position in that path.
4. WHEN an enrolled learner completes a Lesson in their Directed_Learning_Path, THE Learning_App SHALL advance the Path_Enrollment position to the next Lesson in the path order.
5. WHEN an enrolled learner resumes, THE Learning_App SHALL present the next Lesson at the learner's current Path_Enrollment position.
6. THE Learning_Platform SHALL report path-level completion as the proportion of the Directed_Learning_Path's Lessons the learner has completed.
7. THE Learning_Platform SHALL allow each Directed_Learning_Path to be designated as a separately purchasable offering.
8. WHERE a learner has not enrolled in any Directed_Learning_Path, THE Learning_App SHALL allow self-directed selection of individual Subjects and Lessons within a Catalog.

### Requirement 13: Spatial Calculator (WebXR)

**User Story:** As a learner studying math, I want an interactive 3D visualizer in my browser, so that I can see mathematical concepts spatially without needing a VR headset.

#### Acceptance Criteria

1. THE Spatial_Calculator SHALL render 3D mathematical visualizations in a standard web browser without requiring a VR headset.
2. WHERE a VR-capable device is present, THE Spatial_Calculator SHALL support an immersive WebXR session.
3. THE Learning_Platform SHALL build and deploy the Spatial_Calculator as a separate deployable artifact from the Content_Site, the Learning_App, and the Educator_Console.
4. WHERE a math Lesson references the Spatial_Calculator, THE Learning_Platform SHALL embed the Spatial_Calculator as a widget within that Lesson.

### Requirement 14: B2E Organization and Classroom Management

**User Story:** As a school administrator, I want to manage seats, classrooms, and educators, so that my institution can deploy the platform to students.

#### Acceptance Criteria

1. THE Organization_Manager SHALL allow an Organization administrator to create Classrooms within the Organization.
2. THE Organization_Manager SHALL allow an Organization administrator to assign Educator and Student roles to accounts within the Organization.
3. WHEN an Organization administrator adds a Student to a Classroom, THE Organization_Manager SHALL associate the Student account with that Classroom.
4. THE Organization_Manager SHALL enforce the seat count purchased by the Organization when adding Student accounts.
5. IF adding a Student would exceed the Organization's purchased seat count, THEN THE Organization_Manager SHALL deny the addition and return a seat-limit message.

### Requirement 15: Educator Dashboards and Student Progress Visibility

**User Story:** As an educator, I want to see my students' progress, so that I can identify who needs help.

#### Acceptance Criteria

1. THE Educator_Dashboard SHALL display, for each Classroom assigned to the Educator, each Student's completed-Lesson count and most recent activity timestamp.
2. WHEN an Educator selects a Student, THE Educator_Dashboard SHALL display that Student's Grasp_Scores per Lesson.
3. THE Educator_Dashboard SHALL always restrict each Educator's visibility to Students within Classrooms assigned to that Educator.
4. THE Educator_Dashboard SHALL highlight Students who have one or more Lessons flagged for review.

### Requirement 16: Compliance for Minors (FERPA and COPPA)

**User Story:** As a school district, I want the platform to comply with student-privacy law, so that I can adopt it without legal risk.

#### Acceptance Criteria

1. WHERE an account is a Student account, THE Learning_Platform SHALL classify the Student's progress and Grasp_Score data as protected education records under FERPA.
2. WHEN an Organization administrator requests deletion of a Student's records, THE Learning_Platform SHALL delete the Student's personal data within the period defined by the platform's data-retention policy.
3. WHERE a Student is under 13 years of age, THE Learning_Platform SHALL require verifiable Organization or guardian consent before collecting the Student's personal data, in accordance with COPPA.
4. THE Learning_Platform SHALL restrict access to Student education records to the Student, the Student's assigned Educators, and authorized Organization administrators.
5. THE Learning_Platform SHALL record an audit entry for each access to a Student education record, capturing the accessing account identifier and a timestamp.

### Requirement 17: Affiliate Marketing Program

**User Story:** As a marketing partner, I want to refer learners and receive tracked credit, so that I am compensated for conversions I drive.

#### Acceptance Criteria

1. WHEN a partner registers as an Affiliate, THE Affiliate_Manager SHALL create an Affiliate record with a unique referral identifier.
2. WHEN a visitor arrives through an Affiliate referral link, THE Affiliate_Manager SHALL attribute the visit to the referring Affiliate.
3. WHEN a referred visitor converts to a paid account, THE Affiliate_Manager SHALL record the conversion against the attributing Affiliate.
4. THE Affiliate_Manager SHALL report, per Affiliate, the count of attributed referrals and the count of attributed conversions.

### Requirement 18: Data Persistence

**User Story:** As a platform operator, I want all stateful data durably stored, so that learner progress, organizational structures, and business data are preserved.

#### Acceptance Criteria

1. THE Learning_Platform SHALL persist learner accounts, progress records, Grasp_Scores, and spaced-repetition schedules in durable storage.
2. THE Learning_Platform SHALL persist Organization, Classroom, seat, and role data in durable storage.
3. THE Learning_Platform SHALL persist Corpus content metadata, including Subject, Audience_Tier, and cross-link relationships, in durable storage.
4. THE Learning_Platform SHALL persist Affiliate records, referral attributions, and conversion records in durable storage.
5. WHEN a learner record is written, THE Learning_Platform SHALL make the written record available for subsequent reads by that learner within the platform's defined consistency window.

### Requirement 19: Simple Experience for Non-Technical Learners

**User Story:** As a non-technical learner, I want a dead-simple, hand-holding interface, so that I can learn without being confused by jargon or complexity.

#### Acceptance Criteria

1. THE Learning_App SHALL present interface text in plain language without technical jargon.
2. WHEN a learner signs in, THE Learning_App SHALL present a single primary next action that resumes or starts learning.
3. WHEN a learner is on any screen of the Learning_App, THE Learning_App SHALL display the current step and the next step of the learning flow.
4. WHERE a term requires domain vocabulary, THE Learning_App SHALL provide a plain-language explanation accessible from the term.

### Requirement 21: Educator Console as a Distinct B2E Surface

**User Story:** As a school or district, I want a dedicated administrative console separate from the learner experience, so that educators and administrators manage their organization without navigating the learner-facing app.

#### Acceptance Criteria

1. THE Learning_Platform SHALL build and deploy the Educator_Console as a deployable surface distinct from the Content_Site, the Learner-facing Learning_App, and the Spatial_Calculator.
2. THE Educator_Console SHALL provide the Organization and Classroom management capabilities defined in Requirement 14.
3. THE Educator_Console SHALL provide the educator dashboards and student progress visibility defined in Requirement 15.
4. THE Educator_Console SHALL restrict access to accounts holding the educator or organization-administrator role.
5. WHEN an Organization administrator assigns a Directed_Learning_Path to a Classroom, THE Educator_Console SHALL enroll the Classroom's Students in that Directed_Learning_Path.
6. THE Educator_Console SHALL draw all student progress and grasp data from the same shared source consumed by the Learning_App.
