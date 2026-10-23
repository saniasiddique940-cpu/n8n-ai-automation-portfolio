# n8n AI Automation Portfolio

Production-minded n8n workflows that combine **AI agents, tool calling, and business apps** (Gmail, Google Calendar, Airtable, web search). Every workflow is exported as importable JSON, sanitized of credentials, and documented with architecture, setup steps, and an honest status.

## Projects

| Project | What it does | Stack | Status |
| --- | --- | --- | --- |
| [Research Agent (Webhook)](workflows/research-agent-webhook) | Answers a question via live web search and returns **verified, numbered citations** | Webhook, AI Agent, Tavily, Code node | Citation logic tested with pinned data; live end-to-end run still to be re-verified |
| [Airtable AI Agent](workflows/airtable-ai-agent) | Chat agent that searches, creates, updates and deletes Airtable records | Chat Trigger, Gemini, Memory, Airtable tools + MCP | Built and used by the author; re-test after import |
| [Email Triage (Gemini)](workflows/email-triage-gemini) | Classifies incoming Gmail into order vs inquiry and **drafts** replies (never auto-sends) | Gmail Trigger, Text Classifier, Gemini | Built by the author; re-test after import |
| [Jarvis Assistant](workflows/jarvis-assistant) | Voice-style assistant that delegates to search, calendar and email sub-workflows | Webhook, AI Agent, OpenRouter, Tavily, Execute Workflow tools | Built by the author; re-test after import |

A Python/Streamlit version of the research agent lives in its own repository: `tool-using-research-agent`.

## Repository layout

```
workflows/<project>/        workflow JSON + README (architecture, setup, limitations)
scripts/sanitize_workflow.py   strips credential ids, emails, base ids before commit
scripts/check_exports.py       validates JSON, connections, and scans for leaked secrets
docs/security.md               webhook authentication and public-repo checklist
docs/export-routine.md         the save-and-push routine for every new workflow
.github/workflows/             CI that runs check_exports.py on every push
```

## How to import a workflow

1. In n8n choose **Workflows > Import from file** and select the `.json`.
2. Open each node showing a credential warning and select **your own** credential (all ids are `REPLACE_ME`).
3. Replace `YOUR_...` placeholders (base ids, calendar email, sub-workflow ids) described in that project's README.
4. Test with the sample request in the README before activating.

## Security

All webhooks use **Header Auth** by default, credentials are placeholders, and CI blocks commits that contain keys, real ids or email addresses. See [docs/security.md](docs/security.md).

## About the exports

These files were exported from a live n8n instance and cleaned for publication. Differences from the live versions: credentials and ids replaced with placeholders, Header Auth added to webhooks, and small cleanups noted in each project README. I have not re-imported every file into a fresh instance, which is why each status says so.

## Author

Sania Siddique, building AI automation workflows. License: MIT.
