---
layout: default
title: OAuth2 / OIDC configuration
parent: Exploitation
nav_order: 40
---

# OIDC and OAuth2 configuration

* TOC
{:toc}


## 1. General flow

When OAuth2 with OIDC is configured on KAWA, a "Login with SSO" button appears on the login page.

When users click on that button, here is what happens:

- **Step 1:** The user is redirected to the authorization URL of the Authentication server/IdP. This URL can either be retrieved from `openIdIssuer` or can be manually specified in the configuration (`authenticationDomain` and `loginApiPath`). If the authentication is successful, the authentication server will send a code back to KAWA which will use it to retrieve a token pair (Access and Refresh tokens).

> ℹ️ It is important to configure the application integration to provide both refresh and access tokens to allow safe and transparent token renewals.


-  **Step 2:** Once the token pair is obtained, KAWA will use the access token to retrieve the user information from the user info url. This is usually discovered via the `openIdIssuer` but can also be overridden with `userInfoApiPath`. 

> ℹ️ Make sure to allow the correct scopes: KAWA will read the following from the user info endpoint: `email`, `name`, `sub` (for user id, can be configured) and `email_verified` (You can decide to turn off email verification if that scope cannot be granted).


-  **Step 3:** Once the user identity was extracted, we attempt to load the corresponding user on KAWA. Two behaviors are available:

    - The users in KAWA are created on the fly if they are not found
    - The Authentication blocks at that point (Users MUST be created by an admin).

    This is controlled via `blockIfPrincipalDoesNotExist` in the OAuth2 configuration.


- **Step 4:** Once the user is authenticated, a short lived access token is generated and sent to the client along with the refresh token sent by the Authentication server in step 2. Once the access token expires, KAWA will use the refresh token to generate a new access token (transparent for the end user).


## 2. Configuration


In order for the OAuth2/OIDC mechanism to be  used, make sure that:

- You have configured your client Secret and set up a `OAuth2ClientConfiguration` (all is detailed below):

```python
cmd.replace_configuration('OAuth2ClientConfiguration', {
    'clientId': 'fdamnkj$@W%sgrwgtrwrtw', 
    'openidIssuer': 'https://some.idp.com/oauth2/default',
    'clientHost': 'https://wayne.kawa.ai'
})
```

- Your GlobalAuthenticationConfiguration is set to `JWT`.

```python
cmd.replace_configuration('GlobalAuthenticationConfiguration', {
        "setupAdminUniqueId": "setup-admin@kawa.io",
         "authenticationMethod": "JWT"
})
```

cf [This notebook to configure](https://github.com/kawa-analytics/kywy-documentation/blob/main/notebooks/administration/02_initial_instance_configuration.ipynb) the required objects.

> ⚠️ Make sure to RESTART your KAWA instances after configuration has been changed to take it in account.

> ℹ️ If you want to completely remove the OAuth mechanism, use the following:

```python
cmd.run_command(
        'DeleteConfiguration', 
        {'configurationClassSimpleName': 'OAuth2ClientConfiguration'}
)
```


### 2.1 Client Secret

The client secret is NOT stored in the main OAuth2 configuration object. It must be injected as an environment variable or stored in your secret store (for example: Vault): `KAWA_OAUTH2_CLIENT_SECRET`.


### 2.2 General configuration

Here are the various parameters that are made available to configure OAuth2 with OIDC:

- (REQUIRED) `clientId`: the client ID is a unique identifier assigned to KAWA (the “client” or “relying party”) by the identity provider (IdP) when you register the app. 

- (REQUIRED) `clientHost`: This is KAWA's base URL. It is used by the IdP to send KAWA the code used to retrieve tokens (cf step 1 in the flow). Example: `https://wayne.kawa.ai:222`

- (RECOMMENDED) `openidIssuer`: The issuer URL is used for discovery: Will fetch the OpenID Provider Configuration from https://{issuer}/.well-known/openid-configuration to learn endpoints (authorization endpoint, token endpoint, JWKS URI, userinfo endpoint, etc.). These can be manually overridden if needed.


> If the `openIdIssuer` is not present, you must specify: `authenticationDomain`, `tokenApiPath`, `userInfoApiPath` and `loginApiPath`. These will let KAWA know about the three necessary URLs. Each of them will be built like so: 
```bash
    ${authenticationDomain}/${tokenApiPath}
    ${authenticationDomain}/${userInfoApiPath}
    ${authenticationDomain}/${loginApiPath}
```

Additional parameters:

- `userIdField` (defaults to `sub`): The field to extract the user id from.

- `stateValidationEnabled` (defaults to `true`): If turned on, the state will be validated. State validation protects against Cross-Site Request Forgery (CSRF) attacks by ensuring that the authorization response corresponds to an actual request your app initiated.

- `emailMustBeVerified` (defaults to `true`): This ensures that the emails of principals have been verified with the IdP. If you turn it on, make sure that the user info contains the `email_verified` claim.

- `offlineAccessScope` (default to `true`): This usually ensures that a refresh token will be emitted along the access token. It is important to automatically let users re authenticate when the short lived access token expires. This is STRONGLY RECOMMENDED.

- `blockIfPrincipalDoesNotExist` (defaults to `false`): Set to true if you want to manually create all your users before they are able to authenticate.






