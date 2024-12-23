# Database Design

In this file you will find the walkthrough of database design. we are using `sqlite3` database. but you can change the code to use any sql database.

## Database Tables

- **users**: for storeing user details like there username, password etc...
- **books**: for storing books details like title, decsiption etc...

### users Table

| Columns  | Datatype    | Constrains        |
| -------- | ----------- | ----------------- |
| id       | integer     | primary-key       |
| fullname | string      | not-null          |
| username | string      | unique & not-null |
| password | string      | not-null          |
| email    | string      | not-null          |
| mobileno | integer(10) | ---               |
| isadmin  | boolean     | defualt(false)    |

## books Table

| Columns  | Datatype | Constrains    |
| -------- | -------- | ------------- |
| id       | integer  | primary-key   |
| title    | string   | ---           |
| desc     | string   | ---           |
| author   | string   | ---           |
| category | string   | ---           |
| borrowby | integer  | defualt(null) |
| price    | integer  | ---           |
