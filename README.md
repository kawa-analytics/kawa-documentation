KAWA User Manual
==============

* TOC
{:toc}





## 1 User management and permissions

Users in KAWA have a global profile that applies across all workspaces and some workspace
related permissions.

### 1.1 Authentication

#### a. KAWA internal authentication

KAWA can be configured to authenticate users without relying on
SSO. In this mode, administrators can either choose to let people
create accounts using email activation codes or to manage the user
accounts themselves through KAWA's Python API.

KAWA will store the user's unique identifiers (must be the email address
if people are making use of email activation), their first and last names, and their secure password hashes.

#### b. Using external IDPs and SSO

When configured to work with SSO, KAWA will automatically create users
in its database when new authenticated users will connect.

__Open ID Connect__:
KAWA is compatible with OIDC to authenticate users. It can be integrated with providers such as OKTA, AWS Cognito, Auth0, Azure Active Directory, etc...

__Kerberos SSO__: Kawa can be configured to integrate with Kerberos to authenticate users.

__HTTP Header-based Authentication__: Users can be authenticated with HTTP Header based authentication. In that setup, the user information will be extracted from the incoming HTTP requests.


#### c. Using API Keys

KAWA provides a mechanism to allow users to generate API keys in order to authenticate. This is mainly used to work with KAWA's Python API.




### 1.1 Application wide profile

#### a. The user roles

There are 3 global roles in KAWA.
Each user has one role that is valid for the entire application.

**ADMINISTRATORS**

Administrators can access all the admin functionalities of the platform. 
They can create, delete, activate, deactivate users. They can also modify user passwords
and change the global roles of other users.

Administrators can also access all workspaces and all assets in all of the workspaces without restrictions.

They can access all data bypassing all the row level and column level security.

> **Warning:** Typically, very few admin accounts should be created. They should be reserved for IT, global support and maintenance.

**SETUP ADMINISTRATORS**

There is only one such user for the entire KAWA platform. This user has all the privileges 
of admin users. It can never be disabled, deleted or switched to another user role.


**REGULAR USERS**

Most of the users should have this role. It allows them to benefit from all the features
of the platform.

#### b. The restricted data source types

There are 7 data source types in KAWA:

- __USER FILES__: To create data sources of that type, users can upload CSV files from the GUI.

- __EXTERNAL SYSTEMS__: This type of data source is created by connecting to an external system directly from the GUI: Database, API, etc... 

- __KYWY__ (Python client): This corresponds to data sources created from the Python client using the data loader.

- __LIVE CONNECT__: Live connections are created by querying tables or views that are stored in the main data warehouse, without ETL or synchronization.

- __PYTHON ETL__: This type of data source is created by scheduling a Python script decorated by the `@kawa_tool` decorator.

- __FROM SCRATCH__: This allows users to create data sources directly in the GUI and edit the values manually, like Excel.

- __TRANSFORMATIONS__: Those are created by materializing existing views into new warehouse tables.


Each user (_Regular users_) can only create data sources of a type that was not explicitly restricted by administrators.

This allows administrators to control what the various users can load into the platform.

#### c. The overall permissions

Overall permissions are a list of features that individual users have access to.
For example, to benefit from all the Generative AI features,
the permission: `GENERATIVE_AI` must be granted. This grant will apply to the entire KAWA platform.



### 1.2 Workspace permissions

Each workspace functions as a separate isolated tenant. 

In order to access a given workspace, a user must be explicitly invited in it. 
A workspace can also be configured as public. If that is the case,  all the registered users in the platform can access it without restriction.

In each workspace, users benefit from a set of permissions:

__Workspace administrative permissions:__

- Edit workspace settings
- Manage workspace members

__Sharing permissions:__

- Share Dashboards
- Share Sheets and Views
- Share Applications 

__Data access permissions:__

- Manage row level and column level security
- Access restricted data and restricted data providers


__Section access:__

- Access and manage Python scripts
- Access and manage AI agents




> **Warning:** Administrative and data access permissions give users ability to directly or indirectly access all data. Those permissions should
be reserved to workspace administrators only.

> **Warning:** Application wide Administrators will
benefit from ALL those permissions by default.



### 1.3 Teams

Within each workspace, users can be grouped in Teams. 
Teams can be used to share entities with user groups, such as applications,
dashboards, sheets and data sources.



## 2 Sharing

The main assets of KAWA can be shared across the workspace to which they belong.
Sharing allows to setup publishing and collaborating flows between members of the KAWA workspaces.


### 2.1 Sharing Sheets and Views


A Sheet contains multiple views, such as charts, grids and pivot tables.
They also contain the business logic, expressed through formulas and python scripts.

A sheet can be shared in Read or Write mode with other users or teams of the workspace.

Within a sheet, views can be shared or private. When a view is shared,
it inherits the sharing mode (Read or Write) from its parent sheet.

If a sheet is shared with TeamA for Write, then all the shared views within that sheet will be editable by members of TeamA.








### 2.2 Sharing Dashboards

### 2.3 Sharing Applications

### 2.4 Sharing Data Sources










