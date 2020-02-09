# TODO API

On failed authentication every endpoints returns a redirect to<br/>
`/401` with query param "redirect" including the requested path

<hr/>

## GET /api/todo
Authentication: **TokenAuth**<br/>

You can use following url parameters:
- `list_id` returns a list of all todos belonging to the given list.
- `item_id` returns th todo with this id if it exists (no list).

**Returns:**

- on valid credentials
  
Statuscode: `200`
```json
[
    {
        "list_id": 0,
        "title": "string",
        "finished": false,
        "due_date": "string of datetime:isoformat",
        "address": "string",
        "description": "string",
        "priority": 0,
        "subtasks": "string",
        "reminder": "string of datetime:isoformat"
    }
]
```

- on database error

Statuscode: `500`
```json
{
    "status": "failed",
    "message": "database error"
}
```

- on no entries found

Statuscode: `200`
```json
{
    "status": "failed",
    "message": "no entries found.",
    "data": []
}
```

<hr/>

## POST /api/todo
Authentication: **TokenAuth**<br/>

**JSON Body:**
```json
{
    "list_id": 0,
    "title": "string",
    "finished": false,
    "due_date": "string of datetime:isoformat",
    "address": "string",
    "description": "string",
    "priority": 0,
    "subtasks": "string",
    "reminder": "string of datetime:isoformat"
}
```

`list_id`, `title`, `finished` are mandatory

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
    "message": "describes missing or invalid value"
}
```

- on database error

Statuscode: `500`
```json
{
    "status": "failed",
    "message": "database error"
}
```

<hr/>

## GET /api/todolist
Authentication: **TokenAuth**<br/>

You can use following url parameters:
- `list_id` returns the todolist with this id if it exists (no list).

**Returns:**

- on valid credentials
  
Statuscode: `200`
```json
[
    {
        "list_id": 5,
        "name": "test_name",
        "description": "some description",
        "hex_color": "#FFFFFF",
        "created_at": "2020-02-08T20:52:15.945269"
    }
]
```

- on database error

Statuscode: `500`
```json
{
    "status": "failed",
    "message": "database error"
}
```

- on no entries found

Statuscode: `200`
```json
{
    "status": "failed",
    "message": "no entries found.",
    "data": []
}
```

<hr/>

## POST /api/todolist
Authentication: **TokenAuth**<br/>

**JSON Body:**
```json
{
    "list_id": 5,
    "name": "test_name",
    "description": "some description",
    "hex_color": "#FFFFFF",
    "created_at": "2020-02-08T20:52:15.945269"
}
```

`list_id`, `name`, are mandatory

**Returns:**

- on valid credentials
  
Statuscode: `200`
```json
{
    "status": "success",
    "message": "todolist created",
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
    "message": "describes missing or invalid value"
}
```

- on database error

Statuscode: `500`
```json
{
    "status": "failed",
    "message": "database error"
}
```

<hr/>