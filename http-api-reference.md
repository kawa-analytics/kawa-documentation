# HTTP API Reference

KAWA exposes a REST API that lets you manage users, workspaces, datasources, workflows, and more programmatically. All examples use `curl`.

## 1. Authentication

KAWA supports two authentication methods:

| Method               | How                                                            |
| -------------------- | -------------------------------------------------------------- |
| **API Key**          | Pass `x-kawa-api-key` header on every request                  |
| **Email / Password** | `POST /authentication/login` → returns an `accessToken` cookie |

For programmatic access, **API key authentication is recommended**.

### 1.1 Required headers

```
x-kawa-api-key: <your-api-key>
x-kawa-workspace-id: <workspace-id>
Content-Type: application/json
```

> `x-kawa-workspace-id` is required for all endpoints that operate within a workspace context.

### 1.2 Log in with email/password

`POST /authentication/login`

```bash
curl -X POST https://your-instance.kawa.ai/authentication/login \
  -H "Content-Type: application/json" \
  -d '{
    "credentialType": "LOGIN_AND_PASSWORD",
    "credentials": {
      "email": "user@example.com",
      "password": "s3cr3t"
    }
  }'
```

Returns an `accessToken` cookie used in subsequent requests.

### 1.3 Get current user

`GET /authentication/current-user`

```bash
curl https://your-instance.kawa.ai/authentication/current-user \
  -H "x-kawa-api-key: kawa_abc123xyz"
```

## 2. Commands endpoint

Most write operations (create, update, delete) go through a single command bus:

`POST /commands/secured/run`

```json
{
  "command": "<CommandName>",
  "parameters": { ... }
}
```

> Returns `200 OK` with the created/updated entity, or `409 Conflict` if the entity already exists.

## 3. Users

### 3.1 List users

`GET /backoffice/principals`

```bash
curl https://your-instance.kawa.ai/backoffice/principals \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 3.2 Get user by ID

`GET /backoffice/principals/{id}`

```bash
curl https://your-instance.kawa.ai/backoffice/principals/p_01 \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 3.3 Create user

Command: `CreateActivePrincipalWithPassword`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "CreateActivePrincipalWithPassword",
    "parameters": {
      "email": "bob@example.com",
      "password": "B0bPassw0rd!",
      "firstName": "Bob",
      "lastName": "Jones"
    }
  }'
```

> If a user with this email already exists, the command is a no-op.

### 3.4 Change user status

Command: `ReplaceUserStatus`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "ReplaceUserStatus",
    "parameters": {
      "principalId": "p_01",
      "active": false
    }
  }'
```

Set `"active": true` to reactivate.

### 3.5 Change user role

Command: `ReplaceUserRole`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "ReplaceUserRole",
    "parameters": {
      "principalId": "p_01",
      "role": "ADMIN"
    }
  }'
```

### 3.6 Change user password

Command: `AdminChangeUserPassword`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "AdminChangeUserPassword",
    "parameters": {
      "principalId": "p_01",
      "newPassword": "N3wP@ssword!"
    }
  }'
```

### 3.7 Generate API key for a user

Command: `AdminGenerateApiKeyForPrincipal`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "AdminGenerateApiKeyForPrincipal",
    "parameters": {
      "principalId": "p_01",
      "name": "my-automation-key",
      "replaceIfExists": true
    }
  }'
```

Add `"expirationDate": 20000` (days since Unix epoch) to set an expiry.

> **Important:** The `clearTextApiKey` in the response is only returned once and cannot be recovered later.

### 3.8 Assign user to perimeters

Command: `AssignPrincipalToPerimeters`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "AssignPrincipalToPerimeters",
    "parameters": {
      "principalEntityId": "p_01",
      "memberOfPerimeterNames": ["EMEA", "Finance"]
    }
  }'
```

## 4. Workspaces

### 4.1 List workspaces

`GET /backoffice/workspaces`

```bash
curl https://your-instance.kawa.ai/backoffice/workspaces \
  -H "x-kawa-api-key: kawa_abc123xyz"
```

### 4.2 Get workspace by ID

`GET /backoffice/workspaces/{id}`

```bash
curl https://your-instance.kawa.ai/backoffice/workspaces/ws_01 \
  -H "x-kawa-api-key: kawa_abc123xyz"
```

### 4.3 Create workspace

Command: `CreateWorkspace`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "CreateWorkspace",
    "parameters": {
      "displayInformation": {
        "displayName": "Q1 Analytics",
        "description": "Workspace for Q1 reporting"
      }
    }
  }'
```

> Returns `409 Conflict` if a workspace with this name already exists.

### 4.4 Add users to workspace

Command: `AddMembersToWorkspace`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "AddMembersToWorkspace",
    "parameters": {
      "workspaceId": "ws_01",
      "members": [
        { "principalId": "p_01", "permissions": [] },
        { "principalId": "p_02", "permissions": [] }
      ]
    }
  }'
```

To also set this as the users' active workspace:

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "SetCurrentWorkspaceForPrincipals",
    "parameters": {
      "workspaceId": "ws_01",
      "principalIds": ["p_01", "p_02"]
    }
  }'
```

### 4.5 Remove users from workspace

Command: `RemoveWorkspaceMembers`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "RemoveWorkspaceMembers",
    "parameters": {
      "workspaceId": "ws_01",
      "principalIds": ["p_01"]
    }
  }'
```

### 4.6 Set workspace visibility

Command: `ToggleWorkspaceVisibility`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "ToggleWorkspaceVisibility",
    "parameters": {
      "workspaceId": "ws_01",
      "isPublic": false
    }
  }'
```

## 5. Datasources

### 5.1 List datasources

`GET /backoffice/datasources`

```bash
curl https://your-instance.kawa.ai/backoffice/datasources \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 5.2 Get datasource schema

`GET /backoffice/datasources/{id}/schema`

```bash
curl https://your-instance.kawa.ai/backoffice/datasources/ds_01/schema \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 5.3 Get datasource health report

`GET /backoffice/datasources/health-report/v2/{id}`

```bash
curl https://your-instance.kawa.ai/backoffice/datasources/health-report/v2/ds_01 \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 5.4 Archive datasource

Command: `ArchiveDataSourceAndDeleteAssociatedData`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "ArchiveDataSourceAndDeleteAssociatedData",
    "parameters": {
      "dataSourceId": "ds_01"
    }
  }'
```

> **Warning:** This permanently deletes the datasource and all its associated data.

### 5.5 Share datasource

Command: `UpdateDataSourceShareStatus`

`generalAccess` values: `RESTRICTED`, `READ`, `EDIT`.

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "UpdateDataSourceShareStatus",
    "parameters": {
      "dataSourceId": "ds_01",
      "shared": true,
      "advancedSharingConfiguration": {
        "sharedTeamIds": ["team_01"],
        "teamIdsWithWritePermission": [],
        "generalAccess": "RESTRICTED"
      }
    }
  }'
```

## 6. Workflows

### 6.1 List workflows

`GET /backoffice/workflows`

```bash
curl https://your-instance.kawa.ai/backoffice/workflows \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 6.2 Get workflow run history

`GET /backoffice/workflows/{workflow_id}/run-history`

```bash
curl https://your-instance.kawa.ai/backoffice/workflows/wf_01/run-history \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 6.3 Run a workflow

Command: `RunWorkflow`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "RunWorkflow",
    "parameters": {
      "workflowId": "wf_01",
      "parameterValues": {
        "taskVariable_startDate": "2024-01-01",
        "taskVariable_region": "EMEA"
      }
    }
  }'
```

> Workflow trigger parameters must be prefixed with `taskVariable_`.

### 6.4 Delete workflow

Command: `DeleteWorkflow`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "DeleteWorkflow",
    "parameters": {
      "workflowId": "wf_01"
    }
  }'
```

## 7. Sheets

### 7.1 List sheets

`GET /backoffice/sheets`

```bash
curl https://your-instance.kawa.ai/backoffice/sheets \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 7.2 Get sheet schema

`GET /backoffice/sheets/{id}/schema`

```bash
curl https://your-instance.kawa.ai/backoffice/sheets/sh_01/schema \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

### 7.3 Create sheet

Command: `CreateSimpleSheet`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "CreateSimpleSheet",
    "parameters": {
      "shared": false,
      "createDefaultLayout": true,
      "displayInformation": {
        "displayName": "Revenue Overview",
        "description": ""
      },
      "datasourceId": [
        {
          "targetDataSourceId": "ds_01",
          "foreignKeyNames": [],
          "defaultValueForAttributes": []
        }
      ]
    }
  }'
```

### 7.4 Delete sheet

Command: `DeleteSheet`

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "DeleteSheet",
    "parameters": {
      "sheetId": "sh_01"
    }
  }'
```

## 8. Server & Health

### 8.1 Health check

`GET /health`

```bash
curl https://your-instance.kawa.ai/health \
  -H "x-kawa-api-key: kawa_abc123xyz"
```

### 8.2 Server version

`GET /backoffice/application-environment`

```bash
curl https://your-instance.kawa.ai/backoffice/application-environment \
  -H "x-kawa-api-key: kawa_abc123xyz"
```

### 8.3 Usage statistics

`GET /backoffice/usage?from={from_date}&to={to_date}&zoneId={timezone}`

```bash
curl "https://your-instance.kawa.ai/backoffice/usage?from=2024-01-01&to=2024-12-31&zoneId=Europe/Paris" \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01"
```

## 9. Entity listing

All entity types follow the same URL pattern:

```
GET /backoffice/{entity_kind}
GET /backoffice/{entity_kind}?name={name}
GET /backoffice/{entity_kind}?tag={tag}
GET /backoffice/{entity_kind}/{id}
```

| Entity kind             | Description           |
| ----------------------- | --------------------- |
| `principals`            | Users                 |
| `workspaces`            | Workspaces            |
| `datasources`           | Datasources           |
| `sheets`                | Sheets                |
| `dashboards`            | Dashboards            |
| `applications`          | Applications          |
| `extended-applications` | Extended applications |
| `workflows`             | Workflows             |
| `data-providers`        | Data providers        |
| `layouts`               | Layouts / views       |
| `attributes`            | Attributes            |
| `scripts`               | Scripts               |
| `script-runners`        | Script runners        |
| `agents`                | Agents                |
| `teams`                 | Teams                 |
| `perimeters`            | Perimeters            |

**Example — search by name:**

```bash
curl "https://your-instance.kawa.ai/backoffice/workspaces?name=Q1+Analytics" \
  -H "x-kawa-api-key: kawa_abc123xyz"
```

## 10. Error responses

| Status | Meaning                             |
| ------ | ----------------------------------- |
| `200`  | Success                             |
| `202`  | Accepted (async operation started)  |
| `409`  | Conflict — entity already exists    |
| `4xx`  | Client error — body contains reason |
| `5xx`  | Server error                        |

Error body format:

```
"<human-readable reason string>"
```
