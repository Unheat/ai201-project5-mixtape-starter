Show What You Know: Mixtape Bug Hunt
⏰ ~5–7 hours total

Reading code you didn't write is one of the core skills of professional software development — and one that's rarely taught directly. In most courses, you build things from scratch. In most jobs, you inherit systems that already exist, with existing patterns, existing bugs, and no one around to explain what was intended.

In this project, you'll work inside Mixtape, a social music app where friends share songs, build collaborative playlists, and track listening stats. The app has five open bugs — real ones, with real user impact. Some are obvious once you find them. Others require tracing execution through multiple files to understand why something that looks correct is actually wrong.

Your job is to find, fix, and explain at least 3 of them. The explanation matters as much as the fix.

🎯 Goals
By completing this project, you will be able to:

Navigate an unfamiliar codebase using structured exploration and AI-assisted techniques.
Reproduce a bug from a written issue description before touching any code.
Trace execution flow to identify root cause, not just symptoms.
Implement a targeted fix without breaking unrelated functionality.
Write a clear root cause analysis that communicates what went wrong and why.

✅ Features
Required Features

Codebase orientation: Before starting any bug work, read the codebase and write a codebase map in your submission doc. The map should identify the main files and their roles, and describe the data flow for at least one feature. This is graded as evidence you oriented yourself before diving in — not for completeness.


Fix at least 3 of the 5 bugs below: For each bug you fix, write a complete root cause analysis entry covering all 5 required fields (described below). Fixes without documentation do not count.


One commit per fix: Each bug fix must be its own commit on the bugfix/mixtape branch, using conventional commit format with a descriptive message.

Stretch Features

Fix a 4th bug: Fix any fourth issue from the list below with a complete root cause analysis entry.


Fix all 5 bugs: Fix the remaining fifth issue with a complete root cause analysis entry.


Write a regression test: For at least one of your bug fixes, write a test that would have caught the bug before it was introduced. Include it in the repo and reference it in your submission doc.

💡 Hints
Read before you search. Spending 20 minutes understanding the codebase structure saves 2 hours of debugging in the dark. Write your codebase map before opening a single issue.
Reproduce the bug before looking for the fix. If you can't reproduce it, you don't understand what's wrong yet — and you can't verify your fix worked.
For Issue #3 (duplicates), the bug is conditional — think about what conditions trigger the second code path that produces the duplicate.
For Issue #4 (notifications), the root cause is architectural, not a typo. Look at the pattern used for the working notification and compare it line-by-line to the missing one.
AI tools are genuinely useful for navigating unfamiliar code — ask them to explain what a function does or trace a call chain for you. They're less reliable for guessing what's wrong before you've read the code yourself. Disclose when AI tools helped you find or understand something in your submission doc.

Milestone 1: Fork, Set Up, and Orient Yourself
⏰ ~45 min

Before opening any issue, spend time understanding the codebase as a whole. Developers who jump straight to the bug usually fix the symptom and miss the root cause. The codebase map you write in this milestone is your proof of orientation — and it's the lens through which all your bug work will be more effective.


Fork the Mixtape starter repo and clone your fork locally. Then set up and run the app:

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate.bat       # Windows Command Prompt
# source .venv/Scripts/activate    # Windows Git Bash

pip install -r requirements.txt
python seed_data.py                # seed the database with test data

# Create your working branch
git checkout -b bugfix/mixtape

# Start the app
FLASK_APP=app:create_app flask run
Confirm the app starts and responds at http://127.0.0.1:5000. (On macOS, use 127.0.0.1 rather than localhost if requests hang.)

Don't use python app.py to start the app. That triggers a SQLAlchemy double-import error. Always use FLASK_APP=app:create_app flask run.

Read README.md before anything else. It explains the app structure, traces two example call chains, and lists the five open issues with their affected service files. This context shapes everything in the milestones that follow.


Read through the main files before looking at any issue. AI tools are genuinely useful for this phase. Here are prompting patterns that work well for codebase orientation:

File summary: Give the AI the contents of a service file and ask "What is this module responsible for? What are its main functions and what does each one do?"
Data flow trace: Ask "Given this services/ directory, trace how a song gets added to a user's feed — which functions are called and in what order?" (paste the relevant files as context)
Function explanation: Give the AI a function you don't understand and ask "Walk me through what this function does step by step, including what it returns and what could cause it to return an unexpected value."
Take notes as you go. The goal of this phase is to build a mental model of how the app is organized — not to find bugs yet.


Write your codebase map in submission.md (create this file in the root of your repo — this is your submission doc for the whole project). Cover at minimum: the main files and what each one does, the data flow for at least one feature (e.g., how sharing a song triggers a notification), and any patterns you notice in how the app is organized.

📋 What a useful codebase map looks like
A weak map just lists files by name without saying what they actually do or how they connect:

"The app has app.py, models.py, routes/, and services/. The routes handle the endpoints and the services do the logic."

A strong map names the responsibility of each piece and traces at least one real data flow:

"models.py defines 5 SQLAlchemy models: User, Song, Playlist, PlaylistSong, and Notification. The PlaylistSong table is a join table that adds an order column — songs in a playlist have an explicit position, not just insertion order.

Data flow — user rates a song: POST /songs/<id>/rate in routes/songs.py calls notification_service.notify_song_rated(). That function creates a Notification record for the song's original sharer. There's no separate rating model — the rating is stored directly on the Song.

Pattern I noticed: every route delegates immediately to a service function. The routes do input parsing and response formatting; all business logic lives in services/."

The strong version proves you read the code. The weak version could have been written by someone who just looked at the file tree.


Read all five issue descriptions before choosing which three to fix. Some bugs share similar root cause patterns — knowing all five before starting helps you navigate more efficiently.

📍 Checkpoint
Your bugfix/mixtape branch is created and the app runs locally. Your codebase map is written and covers the main files and at least one data flow. You've read all five issue descriptions and have a rough plan for which three you'll tackle first.



Milestone 2: Reproduce Your Chosen Bugs Before Fixing Anything
⏰ ~30–45 min

Reproduce each bug before writing a single line of fix code. This is professional debugging discipline, not a formality. If you can't reproduce the reported behavior, you either don't understand the bug or you're looking at the wrong part of the code. Either way, fixing before reproducing is guesswork.


For each of your three chosen bugs, follow the steps needed to trigger the reported behavior. For issues that involve specific conditions (Issue #1: Sunday only; Issue #3: inconsistent duplicates), think through what state the app needs to be in to hit that code path.


Note how you reproduced each bug in your submission doc under the "how you reproduced it" field — what inputs, what sequence of actions, or what data condition triggered the behavior. This is part of your root cause analysis entry.


If you can't reproduce a bug after a genuine attempt, try a different one from the list. If you're stuck, check whether the app state needed for that bug is present in the seed data.

📍 Checkpoint

You can trigger all three of your chosen bugs deliberately. You know what inputs or conditions reproduce each one. You have not yet changed any code.



Milestone 3: Investigate, Fix, and Document Each Bug
⏰ ~1–2 hours per bug

For each bug, follow the same process: trace from the symptom to the root cause, implement the smallest fix that resolves it, check that you haven't broken related functionality, then commit and document. Don't move to the next bug until you've written the root cause analysis entry for the current one! Documentation written while the code is fresh is far more accurate than documentation written at the end.


For each bug, trace the code from the symptom to the root cause. Follow the data flow — find the function that handles the relevant action, read it, then follow the calls it makes. Note which files you looked at and what led you to the right place. This is your navigation strategy.

🤖 AI tools during investigation
AI is useful for explaining code you've already found, but unreliable for diagnosing bugs without full context. Good uses during this phase:

Give the AI a suspicious function and ask "What edge cases could cause this to return the wrong value?"
Ask "What's the difference between Python's datetime.weekday() and isoweekday()?" (when you've already narrowed it to a date comparison)
Give the AI two similar code paths and ask "What's the structural difference between these two blocks?"
The workflow that works: you find the suspicious code → AI helps you understand it → you verify the diagnosis by reading it yourself. Asking AI to find the bug before you've read the relevant code almost always leads you somewhere plausible but wrong. Document how you used AI in your RCA entry and in your AI usage section.

🔍 Execution tracing strategies when you're stuck
If reading the code isn't enough to understand why a bug happens, trace execution:

Add a temporary print statement at the entry of the suspicious function to confirm it's being called with the inputs you expect. Example: print(f"[DEBUG] streak check: user={user_id} weekday={today.weekday()}"). Remove these before committing.
Isolate the function in a Python shell. Open a Python REPL, import the service file, and call the function directly with controlled inputs. This is faster than firing HTTP requests and easier to reason about.
Check what the data actually looks like. Use flask shell to query the database directly:
from models import Song
Song.query.filter_by(title="Neon City").all()
Read the call chain top-down, not bottom-up. Start from the route, follow each function call in order, and write down what each step returns. Don't jump to "the bug is probably in X" — trace every step.
The workflow: read → form a hypothesis → verify by running the code with specific inputs → fix. Fixing before verifying almost always produces a fix for the wrong cause.


Implement your fix. The fix should be targeted — change as little as possible to address the root cause without restructuring unrelated code. If your fix requires changing logic in multiple places, make sure each change is necessary.


Before committing, check that your fix doesn't break related functionality. Look at other code that touches the same data or the same feature. For boundary condition bugs (Issues #1, #2, #5), verify the fix works correctly on both sides of the boundary.


Write your root cause analysis entry for this bug in your submission doc. See the format below. Do this before moving to the next bug.

📋 Root Cause Analysis Format
For each of the 3+ bugs you fix, write an entry in your submission doc with all five of these fields:

Issue number and title
How you reproduced it — What steps did you take to confirm the bug exists before touching any code? What inputs, sequence of actions, or data condition triggered the behavior?
How you found the root cause — Which files did you look at? What was your navigation path? What moment made you confident you'd found the right place — not just a suspicious area, but the specific cause?
The root cause — In plain English, explain exactly what was wrong. Not "there was a bug in the streak logic" — explain the specific condition, comparison, or missing step that caused the problem.
Your fix and side-effect check — What did you change and why does that change fix the root cause? What related functionality did you check afterward to confirm you didn't break anything?
What a precise root cause looks like vs. a surface-level one:

❌ Surface-level: "The streak reset logic had a bug where it wasn't handling Sundays correctly."

✅ Precise: "Python's datetime.weekday() returns 6 for Sunday, but the streak code was checking weekday() == 0 to detect the start of a new week, which matches Monday instead. Any streak update on a Sunday was treated as a mid-week entry, so the streak never reset when the week turned over on Sunday nights. The fix was to change the comparison to isoweekday() == 7 (Sunday = 7 in ISO convention), which correctly identifies the week boundary."

The precise version names the exact function, explains what it returns vs. what the code assumed, and traces why that mismatch caused the visible bug.


Commit your fix:

git add <changed files>
git commit -m "fix: <description of what was wrong and what you changed>"
Each fix should be a separate commit with a descriptive message.

📍 Checkpoint

At least 3 bugs are fixed, documented with complete root cause analysis entries, and committed as separate commits. You can trigger each fixed behavior and confirm it no longer reproduces.


Milestone 4: Final Review and AI Usage
⏰ ~30 min

Review your submission before turning it in. Check your commit history, verify your RCA entries are complete, and write your AI usage section. For this project specifically, the AI usage section should describe how you used tools during codebase navigation and debugging, not just code generation.


Run git log --oneline on your bugfix/mixtape branch. Take a screenshot. Confirm there is one commit per bug fix with a meaningful fix: message. If multiple fixes are bundled in one commit, it's worth separating them now before submitting.


Review each root cause analysis entry in submission.md. Check that all 5 fields are present and substantive for every bug. Someone who hasn't seen the codebase should be able to understand what went wrong and why from your entry alone.


Write your AI usage section at the top of your submission doc. Describe specifically how you used AI tools during this project: what you asked them to explain, trace, or summarize; what they helped you understand; and where you had to verify something yourself or found that the AI's explanation was incomplete or pointed you in the wrong direction. The goal of this section is to be honest about the collaboration, not to prove you did everything alone!

📍 Checkpoint

git log --oneline screenshot shows at least 3 separate commits, each on the bugfix/mixtape branch with a fix: prefix. All root cause analysis entries are complete. AI usage section is written.



📬 Submitting Your Project
Submit all of the following through the Course Portal:

Link to your forked GitHub repository with your fixes on the bugfix/mixtape branch
submission.md (in the root of your repo) containing:
AI usage section (at the top): how you used AI tools during codebase navigation and debugging, what they helped you understand, and where you verified or overrode their output
Codebase map (written before starting any bug work): main files and their roles, data flow for at least one feature
Root cause analysis entry for each bug fixed (at least 3), covering all 5 required fields
Screenshot of git log --oneline on your bugfix/mixtape branch showing separate commits for each bug fix
🗺️ How It's Graded
A detailed breakdown of graded features and points can be found on the course grading page.