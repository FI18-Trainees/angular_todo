# TODO API

On failed authentication every endpoints returns a redirect to<br/>
`/401` with query param "redirect" including the requested path

<hr/>

## GET /api/todo
Authentication: **TokenAuth**<br/>

**Returns:**

- on valid credentials
  
Statuscode: `200`
```json
[
    {
        "id": int,
        "title": string,
        "finished": bool,
        "due_date": string of datetime:isoformat,
        "address": string,
        "description": string,
        "priority": int,
        "subtasks": string[],
        "reminder": string of datetime:isoformat
    }
]
```

<hr/>

## POST /api/todo
Authentication: **TokenAuth**<br/>

**JSON Body:**
```json
{
    "id": int,
    "title": string,
    "finished": bool,
    "due_date": string of datetime:isoformat,
    "address": string,
    "description": string,
    "priority": int,
    "subtasks": string[],
    "reminder": string of datetime:isoformat
}
```

`id`, `title`, `finished` are mandatory

**Returns:**

- on valid credentials
  
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

- on missing or invalid data

StatusCode: `400`
```json
{
    "status": "failed"
}
```

<hr/>

