# Antigravity Quality Control Protocols

## Core Philosophy: "Do It Once, Do It Right"

This document defines the strict operational protocols for AI agents (specifically Gemini 3 Pro/Flash) working on this codebase. The goal is to prevent "rush jobs" that lead to fragile infrastructure.

### 1. The "Verify, Don't Assume" Rule
**Problem:** Agents often assume a command worked because it didn't return a standard error code, or they skip verification steps to save time.
**Protocol:**
- **Explicit Verification:** Every configuration change MUST be followed by a verification step (e.g., `curl` check, config file grep, or status script).
- **No "Blind" Success:** Never report "Done" unless you have witnessed the positive result.
- **Visual Confirmation:** When possible, check the specific output (like "initialized: true" or specific JSON keys) rather than just file existence.

### 2. The "No Skipping" Policy
**Problem:** When a complex setup step (like a wizard or auth flow) fails, the agent sometimes "skips" it to proceed to the next task, leaving the system in a broken or half-configured state.
**Protocol:**
- **Blockers are Absolute:** If a dependency step fails (e.g., "Setup Libraries"), STOP. Do not proceed to "Setup Downloader".
- **Fix Forward:** Diagnose the root cause of the failure immediately. Do not bypass the wizard/setup unless you are replacing it with a robust programmatic equivalent (e.g., direct DB injection or API calls).
- **Honesty:** If you cannot fix it, report the blocker to the user immediately. Do not fake success.

### 3. "Infrastructure as Code" (IaC) First
**Problem:** Manual tweaks and one-off hacks get lost when containers are recreated or services restart.
**Protocol:**
- **Script Everything:** Any configuration change that relies on more than 2 commands must be wrapped in a script (Bash/Python).
- **Persist by Default:** Create backup scripts (`backup-configs.sh`) and restore scripts (`restore-configs.sh`) as part of the initial setup, NOT as an afterthought.
- **Idempotency:** Scripts should be runnable multiple times without breaking the system (e.g., check if user exists before inserting).

### 4. Defense in Depth
**Problem:** Config files get wiped, permissions get reset, and services crash.
**Protocol:**
- **Backup Before Touch:** Before major architectural changes or "resets" (like `docker-compose down`), run a backup.
- **Safe Operations:** Prefer `docker-compose restart` over `docker-compose down && up` unless a container rebuild is explicitly required.

---
*Add this file to all projects to ensure consistent AI behavior.*
