---
title: Untitled
---

<table><thead><tr><th width="190">Header</th><th width="190" align="right">Required</th><th width="190">When</th><th width="178">Description</th></tr></thead><tbody><tr><td><code>x-kawa-api-key</code></td><td align="right">Yes</td><td>API key authenticated requests</td><td>Your API key</td></tr><tr><td><code>x-kawa-workspace-id</code></td><td align="right">Depends</td><td>Workspace-scoped endpoints</td><td>Target workspace ID (required for workspace-scoped endpoints; optional for some global endpoints like <code>GET /backoffice/workspaces</code>. If provided, must be a workspace you can access.)</td></tr><tr><td><code>Content-Type: application/json</code></td><td align="right">Yes</td><td><code>POST</code> requests</td><td>JSON request body</td></tr></tbody></table>
