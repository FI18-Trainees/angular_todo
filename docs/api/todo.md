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
    "status": "success",
    "message": "todo created",
    "todo_id": 0
}
```
`todo_id` is the integer id of the created todo object.

- on invalid json body

Statuscode: `400`
```json
{
    "status": "failed",
    "message": "invalid json"
}
```

- on missing or invalid data

StatusCode: `400`
```json
{
    "status": "failed",
    "message": "mandatory keys missing"
}
```

<hr/>

