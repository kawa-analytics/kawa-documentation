# Artifacts

See definitions in Terminology section.

The **Artifacts** tab is a workspace-level library for the files you bring into KAWA. It gives you a single place to upload, store, preview, version, and download files — PDFs, images, presentations, spreadsheets, text, application files, and other binaries — without leaving the platform.

Where sheets hold your modeled data and dashboards hold your live views, the Artifacts tab holds your **files**: the documents and deliverables you want to keep, version, and share with your team.

_The Artifacts tab._

### 1. Opening the Artifacts tab

Open the Artifacts tab from the left navigation rail (the box icon).

The page is split into two areas:

* A **left panel** that organizes your artifacts into **Private** (artifacts only you can see) and **Shared** (artifacts shared with you or by you). The **HOME / All artifacts** entry at the top returns you to the full list at any time.
* A **main list** that shows every artifact you can access, one row per artifact.

Each row in the list displays:

* **Name** — the artifact's name and its type (for example, `TEXT`, `BINARY`) and visibility (for example, `PRIVATE`).
* **Creation date** — when the artifact was first created.
* **Last modification** — when it was last updated.
* **Owner** — the user who owns the artifact.
* **Actions** — a favorite (star) toggle and a kebab menu (⋮) for additional actions.

#### 1.1 Finding artifacts

Several tools at the top of the list help you locate an artifact quickly:

* **Search** — type in the _Search for artifacts_ box to filter the list by name.
* **Tabs** — switch between **All**, **Favorites**, **Mine**, and **Shared** to narrow the list to a relevant subset.
* **Type filter** — use the filter icon to show only artifacts of a given type: **Application**, **PDF**, **Image**, **PowerPoint**, **Excel**, **Binary**, or **Text** (or **All types**).
* **Sort** — click any column header (Name, Creation date, Last modification, Owner) to sort by that column.
* **Refresh** — reload the list to pick up recent changes.

_Filtering artifacts by type._

### 2. Creating an artifact

Artifacts are created by uploading a file from your computer.

Click (+ Artifact) at the top right — or the (+) button at the top of the left panel — to open the **Create artifact** dialog. Enter an **Artifact name** (required), then under **File** click (Choose a file) or drop a file onto the upload area. Click (Create) to finish.

_The Create artifact dialog._

The new artifact appears in the list and is created as version 1. KAWA detects the file type automatically and labels the artifact accordingly (for example, `TEXT`, `PDF`, or `BINARY`).

### 3. Managing artifacts

The kebab menu (⋮) in the **Actions** column of each row gives you the full set of management options for that artifact:

* **Rename** — change the artifact's name.
* **Add description** — set or edit a short description of what the artifact is and who it is for.
* **Add to favorites** — flag the artifact so it appears under the **Favorites** tab. You can also toggle this with the star icon in the row.
* **Share** — open the sharing dialog to control who can access the artifact (see section 6, Sharing).
* **Audit Log** — view the history of actions taken on the artifact for traceability.
* **Delete** — permanently remove the artifact from the workspace.

_The artifact actions menu._

> **Delete** is permanent and removes all versions of the artifact. Use it with care.

### 4. Viewing an artifact

Click an artifact's name to open its detail page. The detail page has three parts.

#### 4.1 Details panel

The left of the detail page summarizes the artifact:

* **Creator** — the user who created it.
* **Access** — the artifact's visibility (for example, _Restricted_).
* **Created** and **Updated** — the creation and last-modification timestamps.

#### 4.2 Versions panel

Below the details, the **VERSIONS** panel lists every version of the artifact (v1, v2, and so on), each with its timestamp and author. The current version is marked with a check. Select any version to preview it, or use the (+) button to add a new version (see section 5, Versions).

#### 4.3 Preview pane

The main area previews the selected version's contents. For supported types, KAWA renders the file directly in the browser — for example, a text data file is shown as a table. The preview header offers two actions:

* **Download** — save the current version to your computer in its original format.
* **Expand** — open the preview in a larger, full-width view.

_An artifact detail page with versions and preview._

### 5. Versions

An artifact keeps a full history of its **versions**. Each time you add a new file to an existing artifact — using the (+) button in the VERSIONS panel — KAWA stores it as a new version and keeps the previous ones.

This lets you update a file — a revised report, an updated deck, a corrected dataset — without losing what it replaced. The latest version is shown by default, and you can select any earlier version to preview or download it.

_The versions panel._

### 6. Sharing

By default, an artifact is **Private** (Access: _Restricted_) and visible only to its owner. To share an artifact, open its detail page and click (Share) in the top-right corner — or choose **Share** from the row's kebab menu — then choose who can access it. Shared artifacts appear under the **Shared** group in the left panel and under the **Shared** tab in the list.

For the full access model — roles, teams, and permission levels — see Sharing and permissions.
