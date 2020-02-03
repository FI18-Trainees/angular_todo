# LOGIN API

On failed authentication every endpoints returns a redirect to<br/>
`/401` with query param "redirect" including the requested path

<hr/>

## GET /login
Authentication: **BasicAuth**<br/>

**Returns:**

- on valid credentials with 2fa disabled
  
Statuscode: `200`
```json
{
    "login_status": "access_token generated",
    "login_status_code": 0,
    "access_token": "token"
}
```
Save this token as cookie "access_token".

- on valid credentials with 2fa enabled

Statuscode: `200`
```json
{
    "login_status": "2fa required",
    "login_status_code": 1,
    "temp_token": "token"
}
```
Use the temporary valid token to authenticate at `/login/2fa`<br/>
Save a cookie as "temp_token".
This token is valid for 30 seconds if not defined otherwise in the server config.

<hr/>

## GET /login/2fa
Authentication: **BasicAuth**<br/>

**JSON Body:**
```json
{
    "token_2fa": "token",
    "reset_token": false
}
```

`reset_token` is optional and garuantees that a new session token is generated. (set `true` if this behaviour is wanted)

**Returns:**
- on valid credentials and valid 2fa token

Statuscode: `200`
```json
{
    "login_status": "access_token generated",
    "login_status_code": 0,
    "access_token": "access_token"
}
```
Save this as cookie "access_token". You now can authenticate at every endpoint requiring token auth.
This token is valid for 24hours unless otherwise stated in the server config.

- on valid credentials with 2fa disabled

Statuscode: `412`
```json
{
    "login_status": "2fa not enabled",
    "login_status_code": 4
}
```

- on invalid json body

Statuscode: `400`
```text
"invalid json"
```

- on valid credentials but invalid 2fa code

Statuscode: `401`
```json
{
    "login_status": "2fa invalid",
    "login_status_code": 3
}
```

- on valid credentials but invalid temp_token (from `/login`)

Statuscode: `401`
```json
{
    "login_status": "invalid temp token",
    "login_status_code": 2
}
```

<hr/>

## POST /login/rename
Authentication: **TokenAuth**<br/>

**JSON Body:**
```json
{
    "new_name": "name"
}
```

`new_name` needs to be between 1 and 50 chars long. 

**Returns:**
- on valid name

Statuscode: `200`
```json
{
    "status": "success",
    "message": "new name {new_name}"
}
```

- on invalid json body

Statuscode: `400`
```text
"invalid json"
```

- on invalid name (none provided or too long/short)

Statuscode: `400`
```json
{
    "status": "failed",
    "message": "invalid name"
}
```

- on internal server error while saving new data to disk

Statuscode: `500`
```json
{
    "status": "failed",
    "message": "failed saving new name"
}
```
Most likely if you can just try again if this error appears. 

<hr/>

## POST /login/reset/password
Authentication: **TokenAuth**

**JSON Body:**
```json
{
    "new_password": "password"
}
```

**Returns:**
- on valid password

Statuscode: `200`
```json
{
    "status": "success"
}
```

- on invalid json body

Statuscode: `400`
```text
"invalid json"
```

- on no provided password

Statuscode: `400`
```json
{
    "status": "failed",
    "message": "invalid password"
}
```

- on internal server error while saving new data to disk

Statuscode: `500`
```json
{
    "status": "failed",
    "message": "failed saving new password"
}
```
Most likely if you can just try again if this error appears. 

<hr/>

## POST /login/reset/token
Authentication: **TokenAuth**

**Returns:**
- on valid credentials and 2fa disabled

Statuscode: `200`
```json
{
    "login_status": "access_token generated",
    "login_status_code": 0,
    "access_token": "new_token"
}
```

- on valid credentials and 2fa enabled

Statuscode: `200`
```json
{
    "login_status": "2fa required",
    "login_status_code": 1,
    "temp_token": "temp_token"
}
```
Use the temporary valid token to authenticate at `/login/2fa`<br/>
Save a cookie as "temp_token".
This token is valid for 30 seconds if not defined otherwise in the server config

<hr/>

## POST /login/2fa/new
Authentication: **TokenAuth**

This endpoint is used to initialize the creation of 2fa usage.

**Returns:**
- on valid credentials

Statuscode: `200`
```json
{
    "status": "success",
    "message": "temp_2fa_token generated.",
    "link": "link_for_2fa_application"
}
```

Generate a QR-Code based on `link` that the user can scan in Google Authenticator or similiar.

Now ask the user to input the 6 digit code his app produces and use `/login/2fa/validate` to continue


<hr/>

## POST /login/2fa/validate
Authentication: **TokenAuth**

**JSON Body:**
```json
{
    "totp_token": "six_digit_token"
}
```

**Returns:**
- on valid credentials

Statuscode: `200`
```json
{
    "status": "success",
    "message": "2fa enabled"
}
```
2fa is now enabled. Use `/login/2fa` to receive a new session token.

- on invalid json body

Statuscode: `400`
```text
"invalid json"
```

- on invalid totp token

Statuscode: `400`
```json
{
    "status": "failed",
    "message": "invalid totp_token"
}
```

- on internal server error while saving new data to disk

Statuscode: `500`
```json
{
    "status": "failed",
    "message": "could not enable 2fa"
}
```
Most likely if you can just try again if this error appears.

<hr/>

## GET /login/2fa/link
Authentication: **TokenAuth**

Receive the link for the totp session that the user can use in GoogleAuthenticator. For convenience you might want to render a QR-Code bassed on this link.

*Returns:**
- on valid credentials

Statuscode: `200`
```json
{
    "status": "success",
    "message": "link"
}
```

- on 2fa disabled

Statuscode: `412`
```json
{
    "status": "failed",
    "message": "2fa not enabled"
}
```

<hr/>