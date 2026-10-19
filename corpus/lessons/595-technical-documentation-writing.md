---
title: "59.5 - Technical & Documentation Writing"
subject: "Writing Craft & Rhetoric"
catalog: advanced
audience_tier: higher-education
chapter: "59.5"
type: chapter
objectives:
  - "Classify a documentation need as a tutorial, how-to guide, reference, or explanation (the Diátaxis types) and split a page that mixes them"
  - "Write a numbered procedure that uses second person, active voice, an imperative verb in each step, and conditions placed before instructions"
  - "Write an error message that states what went wrong and how to fix it, accurately and without blaming the user"
  - "Write a changelog entry in the Keep a Changelog format and explain how a docs-as-code workflow keeps documentation current"
open_source: true
---

# 59.5 - Technical & Documentation Writing

**Technical writing** helps a reader understand or do something with a technical system: install software, call an API, run a lab procedure, configure a device, or decide between two designs. Its reader is usually in the middle of a task, often under time pressure, and reads to act. That changes the priorities from essay writing: precision over elegance, predictable structure over surprise, and one meaning per sentence. An ambiguous instruction in documentation behaves like a bug: some readers will do the wrong thing.

This lesson is written for college students and professionals who write documentation, READMEs, lab procedures, or internal guides, whether or not "technical writer" is their job title. The code examples are in Python but the principles apply to any system.

## Prerequisites

Lesson [59.1 - Clarity — The Foundation](/591-clarity-the-foundation) (active voice, curse of knowledge) and [59.4 - Voice & Style Development](/594-voice-style-development) (tone). Basic familiarity with a command line and with reading a short Python function helps for Examples 3 and 4. For designing the interfaces that documentation describes, see [19.5 — API Design](/195-api-design).

## Learning objectives

By the end of this lesson you should be able to:

1. **Classify** documentation into the four Diátaxis types and split mixed pages.
2. Write a **procedure** with second person, active voice, imperative steps, and conditions first.
3. Write an **error message** that says what went wrong and how to fix it.
4. Write a **changelog** entry and explain a **docs-as-code** workflow.

## Core ideas

### Four kinds of documentation (Diátaxis)

Diátaxis, a framework developed by Daniele Procida, "identifies four distinct needs, and four corresponding forms of documentation":

| Type | Oriented to | Diátaxis definition (quoted) | Reader's question |
|---|---|---|---|
| **Tutorial** | learning | "an experience that takes place under the guidance of a tutor"; "a tutorial in other words is a lesson" | *Can you teach me by having me do something?* |
| **How-to guide** | goals | "directions that guide the reader through a problem or towards a result" | *How do I accomplish this specific task?* |
| **Reference** | information | "technical descriptions of the machinery and how to operate it" | *What exactly are the options, parameters, and limits?* |
| **Explanation** | understanding | "a discursive treatment of a subject, that permits reflection" | *Why does it work this way?* |

The practical rule is to keep the types apart. A tutorial that stops every few steps to explain design history, or a reference page that turns into a story, serves no reader well. Diátaxis says reference material "is led by the product it describes," while tutorials and how-to guides are led by the user's needs.

### Procedures

The Google developer documentation style guide summarizes its most important points in a highlights page. For procedures and instructions, the relevant ones are:

- Use **second person** ("you" rather than "we") and **active voice** ("make clear who's performing the action").
- **Put conditions before instructions**: "To delete the entire document, click **Delete**," not "Click **Delete** if you want to delete the entire document." The guide explains that mentioning the circumstance first "lets the reader skip the instruction if it doesn't apply."
- Use **numbered lists for sequences** and bulleted lists for most other lists.
- Begin each step with an **imperative verb**, use complete sentences, and keep steps parallel.
- Put code-related text in `code font` and UI elements in **bold**.

The guide's word list adds a reader-centered warning about *easy*: "What might be easy for you might not be easy for others." It also says not to use *please* in ordinary instructions.

### Error messages

Google's technical-writing course on error messages reduces the goal to two questions: "What went wrong? How does the user fix that problem?" It lists the problems Google found with bad messages: "unactionable, vague, imprecise, confusing, inaccurate, unclear cause, unknown next steps." Nielsen Norman Group's error-message guidelines add the user-facing concerns: make the message visible, write in plain language rather than technical jargon or bare error codes, describe the exact problem rather than "An error occurred," and use a nonjudgmental tone that does not blame the user (NN/g specifically cautions against words such as *invalid*, *illegal*, and *incorrect*).

A useful distinction: **developer-facing** messages (exceptions, command-line output, logs) can name parameters and internal reasons; **end-user** messages should describe the problem in the user's terms. Both must be accurate.

### Progressive disclosure

Nielsen Norman Group defines **progressive disclosure** as deferring "advanced or rarely used features to a secondary screen, making applications easier to learn and less error-prone." Documentation applies the same idea to information: start a page with the common case and link to advanced options, edge cases, and internals. A README that opens with every configuration flag hides the three lines most readers need.

### Changelogs and versions

A **changelog** tells readers what changed between versions. Keep a Changelog states its principles directly: changelogs "are for humans, not machines"; there should be an entry for every version; the latest version comes first; each release shows its date; and changes are grouped by type: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**. It recommends an **Unreleased** section at the top for upcoming changes, and its tagline is blunt: "Don't let your friends dump git logs into changelogs." Many projects pair the changelog with Semantic Versioning, in which a version number MAJOR.MINOR.PATCH increments MAJOR for incompatible API changes, MINOR for backward-compatible functionality, and PATCH for backward-compatible bug fixes.

### Docs as code

Write the Docs describes **docs as code** as "writing documentation with the same tools as code": issue trackers, version control, plain-text markup, code reviews, and automated tests. One benefit it lists is that teams "can block merging of new features if they don't include documentation." The idea is that documentation changes travel in the same review as the code they describe, so they are less likely to drift out of date.

## Worked examples

### Example 1: Splitting a mixed README section

**Illustrative draft section** for a fictional command-line tool, `csvtidy`:

*csvtidy was created because our lab's exports had inconsistent date formats, which is a common problem with older instruments. To use it, run `python csvtidy.py data.csv`. Options include `--output` (path), `--dates` (iso or us), and `--drop-empty`. The tool parses each row with Python's csv module, which handles quoted commas correctly. If you're new, try it on the sample file first and look at what changed.*

| Sentence | Type | Where it belongs |
|---|---|---|
| Why the tool was created; why the csv module handles quotes | Explanation | an "About" or "How it works" page |
| `python csvtidy.py data.csv` | How-to | a "Clean a file" guide |
| Options list | Reference | an options table with every flag, its values, and its default |
| Try the sample file and look at what changed | Tutorial | a "First run" walkthrough that tells the learner exactly what they will see |

Reasoning: each reader now finds one kind of material. The README itself can keep a two-line summary, the one command most people need, and links to the four pages (progressive disclosure).

### Example 2: Rewriting a procedure

**Before:**

*The configuration file should be edited so that the port is set to 8080 if a conflict exists. The server is then restarted. Please note that it's easy to forget that admin rights are needed.*

**After:**

To change the server's port, follow these steps:

1. Make sure you have administrator rights on the machine.
2. If another program already uses port 8000, open `config.yaml` and set `port: 8080`.
3. Save the file.
4. Restart the server: `python server.py --restart`.

| Change | Guideline |
|---|---|
| Passive to imperative (*Open*, *Set*, *Restart*) | active voice; imperative verb in each step |
| Prerequisite moved to step 1 | the reader learns about admin rights before failing |
| Condition (*If another program...*) placed before the instruction | conditions before instructions |
| *Please note* and *easy* removed | Google word list |
| File names, settings, and commands in code font | code-related text in code font |

The file name, port numbers, and command are illustrative.

### Example 3: Writing an accurate error message

**Developer-facing.** This Python function wraps the standard library's date parser and adds what the reader needs: which input failed, why, and what to do.

```python
from datetime import date


def parse_start_date(text: str) -> date:
    """Parse a start date written as YYYY-MM-DD, such as 2026-12-01."""
    try:
        return date.fromisoformat(text)
    except ValueError as err:
        raise ValueError(
            f"Start date {text!r} could not be read ({err}). "
            "Use YYYY-MM-DD, for example 2026-12-01."
        ) from None
```

Running it on Python 3.13 produced:

```text
parse_start_date("2026-12-01")  ->  2026-12-01
parse_start_date("2026-13-01")  ->  ValueError: Start date '2026-13-01' could not be read (month must be in 1..12). Use YYYY-MM-DD, for example 2026-12-01.
parse_start_date("2026/12/01")  ->  ValueError: Start date '2026/12/01' could not be read (Invalid isoformat string: '2026/12/01'). Use YYYY-MM-DD, for example 2026-12-01.
```

Reasoning: the message names the bad input, keeps Python's specific reason (an out-of-range month and a wrong format are different problems, so one generic sentence such as "not a real date" would be inaccurate for the second case), and gives a fix with an example. **Version note:** the Python documentation says that before Python 3.11, `date.fromisoformat` "only supported the format YYYY-MM-DD"; newer versions also accept other ISO 8601 forms such as `20261201`. Documentation that promises "YYYY-MM-DD only" should say which Python versions it was tested on.

**End-user version** (for a web form, written for a non-programmer): *Enter the start date as year-month-day, for example 2026-12-01. "2026-13-01" has a month of 13.* It avoids *invalid*, names the specific problem, and shows a correct example.

### Example 4: A changelog entry

**Illustrative raw commit messages:** *fix tz bug* / *add --drop-empty* / *rename --out to --output* / *bump deps* / *remove python 3.8 support* / *patch csv injection issue*

**Keep a Changelog entry:**

```markdown
## [2.0.0] - 2026-10-19

### Added
- `--drop-empty` option removes rows with no values.

### Changed
- Renamed `--out` to `--output`. Update scripts that use `--out`.

### Removed
- Support for Python 3.8.

### Fixed
- Dates near midnight were shifted by one day when the input had a time-zone offset.

### Security
- Cells beginning with `=`, `+`, `-`, or `@` are now escaped in output to prevent spreadsheet formula injection.
```

Reasoning: entries are grouped by type, written for users (what changed for *them*), and the dependency bump is omitted because it does not affect users. Under Semantic Versioning, the renamed option and the removed Python version are incompatible changes, so the MAJOR number increases. The version, date, and changes are illustrative.

## Common misconceptions and boundary cases

- **"Documentation means reference documentation."** A complete options table does not teach a beginner or explain a design decision. Diátaxis treats tutorials, how-to guides, reference, and explanation as four different needs.
- **"One comprehensive page is best."** Mixing types makes every reader wade through material meant for someone else. Split pages and link them.
- **"Words like *simply* and *just* make tasks sound approachable."** Google's word list warns that what is easy for you "might not be easy for others"; such words can make a struggling reader feel at fault.
- **"A short error message is a good one."** *Error 22* is short and useless. Google's two questions require a cause and a fix; NN/g warns against generic messages such as "An error occurred."
- **"The changelog is the commit log."** Keep a Changelog: changelogs "are for humans, not machines." Commit messages describe work done; a changelog describes what changed for users.
- **Boundary: passive voice in reference material.** Reference pages sometimes describe what a system does without an actor (*The value is cached for 60 seconds*). That can be appropriate when the system is the topic; procedures should still address the reader directly.
- **Boundary: style guides differ.** Google's guide is one widely used reference. Your organization, open-source project, or publisher may have its own rules (for example, on headings, serial commas, or UI formatting); follow the project's guide when one exists.
- **Boundary: safety-critical procedures.** Lab, medical, electrical, and industrial procedures are often governed by institutional or regulatory requirements. Writing quality matters, but follow the required format and have qualified reviewers approve the content.

## Practice

1. Classify each as tutorial, how-to guide, reference, or explanation: (a) *A table of every API endpoint, its parameters, and its response codes.* (b) *"Build your first chatbot in 30 minutes," with every step and expected output.* (c) *"How to rotate an expired API key."* (d) *"Why we chose eventual consistency for the sync service."*
2. Rewrite as a numbered procedure following the guidelines in this lesson: *The backup should be run before upgrading. Click Settings and the Backup tab can then be opened. If the drive is full, old backups should be deleted first. It's simple.*
3. Rewrite each error message: (a) *Invalid input.* (b) *ERROR 0x80070005* (shown to a home user whose file is open in another program, preventing it from being saved). (c) *You entered an illegal password.* (for a password shorter than the required 12 characters)
4. Turn these illustrative commit messages into a Keep a Changelog entry for version 1.4.0 dated 2026-11-02: *add dark mode* / *fix crash when list is empty* / *typo in tests* / *deprecate xml export (remove in 2.0)* / *update logo colors*.
5. A README opens with 40 configuration flags before showing how to install the tool. Using progressive disclosure, list the first three things the README should show and where the flags should go.
6. **Extended task.** Choose a small tool, script, lab procedure, or campus process you know well. Write (a) a one-paragraph explanation of what it is for, (b) a numbered how-to procedure of 5-8 steps, and (c) a reference table of its options or materials. Score it with the rubric.

<details>
<summary>Answer key, rubric, and self-check</summary>

1. (a) reference; (b) tutorial; (c) how-to guide; (d) explanation.
2. Sample:
   To back up your data before upgrading, follow these steps:
   1. Click **Settings**, and then click the **Backup** tab.
   2. If the backup drive is full, delete old backups.
   3. Click **Back up now**.
   (The button label in step 3 is illustrative; use the product's actual label.) Check: imperative verbs, condition before instruction in step 2, no *It's simple*, UI elements in bold.
3. (a) Name the field and the requirement. For example, if the field is a quantity limited to 1-99: *Enter a quantity from 1 to 99.* (b) *We couldn't save "budget.xlsx" because it's open in another program. Close the file in that program, then try saving again.* (Show the code only in a details area, if at all.) (c) *Your password needs at least 12 characters. This one has 9.* (Avoid *illegal*; state the rule and the gap.)
4. Sample:

   ```markdown
   ## [1.4.0] - 2026-11-02

   ### Added
   - Dark mode.

   ### Changed
   - Updated logo colors.

   ### Deprecated
   - XML export. It will be removed in version 2.0.

   ### Fixed
   - Crash when a list was empty.
   ```

   The test typo is omitted because it does not affect users. (Some teams would omit the logo change too; either is acceptable if consistent.)
5. Sample: (1) a one-sentence description of what the tool does; (2) installation; (3) the most common command with its output. Move the flags to a reference page or a later "Configuration" section, with a link.
6. Use the rubric.

**Documentation rubric** (score each row 1-4; 16 points total):

| Row | 4 | 3 | 2 | 1 |
|---|---|---|---|---|
| Type separation | explanation, how-to, and reference are distinct and each serves its reader | minor mixing | substantial mixing | one undifferentiated block |
| Procedure quality | numbered, imperative, conditions first, prerequisites up front, one action per step | one lapse | several lapses | unordered prose |
| Accuracy and completeness | a tester could follow it without asking a question; every term defined or linked | one gap | several gaps | cannot be followed |
| Reference precision | every option or item has name, values or quantity, and default or requirement | mostly complete | incomplete | missing |

**Self-check (suggested activity):** Ask someone who has not used the tool or process to follow your how-to while you watch silently. Note every place they hesitate or ask a question, and revise there. For a lab, equipment, or safety procedure, do this only with your instructor's or supervisor's approval, using a dry run that does not operate the equipment.

</details>

> **Integrity note:** Test every command, code sample, and step before you publish it, and state the versions you tested on. Do not copy another project's documentation into yours unless its license permits it, and follow that license's attribution terms (the Google style guide, for example, is published under a Creative Commons Attribution license). The tool, file names, and changelog entries in this lesson are illustrative; the Python function in Example 3 was run on Python 3.13 and its output is shown as produced.

## Where this fits

This lesson is part of the [Writing Craft & Rhetoric course](/subject/writing-craft-and-rhetoric). It follows [59.4 - Voice & Style Development](/594-voice-style-development) and leads to [59.6 - Copywriting & Product Writing](/596-copywriting-product-writing), where interface text (button labels, empty states, error states) returns from a persuasion angle. For the design of the APIs that reference documentation describes, see [19.5 — API Design](/195-api-design); for interface design more broadly, see [34.6 — Human-Computer Interfaces: HCI Design](/346-human-computer-interfaces-hci-design). For writing in scientific and technical disciplines, see [APP-12.7 — Disciplinary Writing](/app-127-disciplinary-writing).

## Sources

- Procida, Daniele, [Diátaxis](https://diataxis.fr/), with the pages [Tutorials](https://diataxis.fr/tutorials/), [How-to guides](https://diataxis.fr/how-to-guides/), [Reference](https://diataxis.fr/reference/), and [Explanation](https://diataxis.fr/explanation/) (four needs and forms; definitions quoted)
- Google, [Google developer documentation style guide: Highlights](https://developers.google.com/style/highlights) (second person, active voice, conditions before instructions, sentence case, numbered lists for sequences, code font, bold UI elements), [Sentence structure](https://developers.google.com/style/sentence-structure) (circumstance or condition first), [Procedures](https://developers.google.com/style/procedures) (imperative verb in each step; parallel structure), and [Word list](https://developers.google.com/style/word-list) (*easy*, *please*, *click here*)
- Google, [Writing Helpful Error Messages](https://developers.google.com/tech-writing/error-messages) (the two questions; common problems with bad error messages; developer-facing focus)
- Neusesser, Tim, and Evan Sunwall, [Error-Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/), Nielsen Norman Group, 2023 (visibility, plain language, precise descriptions, nonjudgmental tone, avoiding *invalid*, *illegal*, *incorrect*)
- Nielsen, Jakob, [Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/), Nielsen Norman Group, 2006 (definition quoted)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) (guiding principles; types of changes; Unreleased section; yanked releases; "Don't let your friends dump git logs into changelogs")
- [Semantic Versioning 2.0.0](https://semver.org/) (MAJOR.MINOR.PATCH summary)
- Holscher, Eric, and the Write the Docs community, [Docs as code](https://www.writethedocs.org/guide/docs-as-code/) (definition; tools; blocking merges without documentation)
- Python Software Foundation, [datetime — Basic date and time types](https://docs.python.org/3/library/datetime.html) (`date.fromisoformat`; changed in version 3.11)
