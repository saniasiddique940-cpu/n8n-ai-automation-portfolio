# Security guide

## 1. Protect webhooks with Header Auth

An n8n webhook with no authentication is **public**: anyone who learns the URL can trigger your workflow and spend your AI and search credits.

1. **Credentials > Create credential > Header Auth.**
   - Name (header): `X-API-Key`
   - Value: a long random secret, e.g. generated with `openssl rand -hex 32`
2. Open the **Webhook** node, set **Authentication** to **Header Auth**, and pick that credential.
3. Save and (re)publish the workflow.
4. Test both cases:

```bash
# should return 401/403
curl -i -X POST "https://YOUR-INSTANCE.app.n8n.cloud/webhook/research-agent" \
  -H "Content-Type: application/json" -d '{"question":"test"}'

# should succeed
curl -X POST "https://YOUR-INSTANCE.app.n8n.cloud/webhook/research-agent" \
  -H "Content-Type: application/json" -H "X-API-Key: YOUR_SECRET" \
  -d '{"question":"What are the latest developments in solid-state batteries?"}'
```

Never put the secret in client-side code or in this repository. If an external service calls the webhook (for example a voice platform), add the same header in its custom-header settings.

## 2. Limit sub-workflows

Sub-workflows (calendar agent, email draft tool) set `callerPolicy = workflowsFromAList` so only the orchestrator can call them. Keep that on any workflow that can touch email, calendar or data.

## 3. Cap agent cost and blast radius

- Set `maxIterations` on every AI Agent.
- Prefer drafting tools over sending tools (the email workflows create drafts only).
- Give delete tools a narrow description and require exact record ids.

## 4. Before making the repository public

- [ ] Run `python scripts/check_exports.py` (also runs in CI)
- [ ] Open each JSON and read prompts and sticky notes for personal or client data
- [ ] Confirm `raw/` is git-ignored and was never committed (`git log --stat -- raw`)
- [ ] If a secret was ever committed, **rotate it first**, then clean history; deleting the file is not enough
