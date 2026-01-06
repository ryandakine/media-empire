# Antigravity's Global Task Master Guide

This is the **Master Record** for setting up and using Task Master across all projects.
If you are an AI Agent reading this, follow the **Agent Protocol** section below.

## 1. Agent Protocol: How to Initiate/Verify Taskmaster

When the user asks you to "set this project up with Task Master" or "verify Task Master is working", follow these steps:

### Step 1: Check for Integration
1.  **Check for installation**: Run `npm list -g task-master-ai` (or `task-master --version`). If missing, install it: `npm install -g task-master-ai`.
2.  **Check for initialization**: Look for `.taskmaster/` folder in the project root.
    *   **If missing**: Be proactive. Run `task-master init`.
        *   Choose "No" to git init (unless project is empty).
        *   **ALWAYS** Choose "Yes" to "Store tasks in Git" (Mandatory).
        *   Choose "Yes" to "AI IDE rules".
        *   Choose "Yes" or specific IDE for rule profiles.
    *   **If present**: Proceed to verification.

### Step 2: System Configuration (CRITICAL)
1.  **Check .env**:
    *   Ensure `.env` exists.
    *   Ensure it has `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, or `PERPLEXITY_API_KEY`.
2.  **Check Models**:
    *   Run `task-master models`.
    *   Ensure a **Main Model** is set.
    *   Ensure a **Research Model** is set (Required for `expand` commands).
    *   *Recommendation*: Use **OpenRouter** to access the latest models.
    *   **Main**: `google/gemini-3-flash-preview` or `anthropic/claude-3.5-sonnet`
    *   **Research**: `google/gemini-3-flash-preview` or `perplexity/sonar-reasoning-pro`

### Step 3: MCP Server Verification
1.  **Check Config**: Look at `.cursor/mcp.json` (or equivalent).
    *   Ensure `task-master-ai` server is defined.
    *   Ensure it uses `npx -y task-master-ai mcp`.
2.  **Test It**:
    *   Use the tool `list_resources` (server: `task-master-ai`).
    *   If tool fails or returns empty, the MCP server is not running or env vars are missing.

### Step 4: Standard Workflow
Once set up, follow the standard Antigravity Workflow:
1.  **Parse PRD**: `task-master parse-prd docs/your-prd.txt`
2.  **Analyze**: `task-master analyze-complexity --research`
3.  **Expand**: `task-master expand --all --num 5 --research`
    *   *Note*: Always use `--num 5` to break tasks into smaller, manageable chunks.
4.  **Execute**:
    *   check `task-master next`
    *   mark in progress
    *   do work
    *   mark done

---

## 2. Technical Setup Guide (For Humans/Manual Review)

### Installation
```bash
npm install -g task-master-ai
```

### Initialization
```bash
task-master init
```

### Environment Variables
```bash
OPENROUTER_API_KEY=sk-or-...
```

### Model Configuration
```bash
# Set Main Model (Gemini 3 Flash or Claude 3.5)
task-master models --set-main google/gemini-3-flash-preview --openrouter

# Set Research Model (CRITICAL - Use a model with search or high reasoning)
task-master models --set-research google/gemini-3-flash-preview --openrouter
# OR
task-master models --set-research perplexity/sonar-reasoning-pro --openrouter
```

### MCP Config (.cursor/mcp.json)
```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai", "mcp"]
    }
  }
}
```

## 3. Common Issues & Fixes
*   **Expansion Logic**: If `task-master expand` hangs or fails, verify the **Research Model** is set in `task-master models`.
*   **MCP Connection**: If tools aren't showing up, restart the IDE/Agent.
*   **Permissions**: Ensure the agent has read/write access to `.taskmaster/tasks/tasks.json`.
