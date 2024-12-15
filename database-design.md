# Database Design

In this file you will find the walkthrough of database design. we are using `sqlite3` database. but you can change the code to use any sql database.

## Database Tables

- **users**: for storeing user details like there username, password etc...
- **books**: for storing books details like title, decsiption etc...
- **category**: for storing different category for books.
- **borrow**: for storeing the information of browwed books.

### users Table

| Columns  | Datatype    | Constrains        |
| -------- | ----------- | ----------------- |
| id       | integer     | primary-key       |
| username | string      | unique & not-null |
| password | string      | not-null          |
| email    | string      | ---               |
| mobileno | integer(10) | ---               |

## books Table

| Columns  | Datatype     | Constrains  |
| -------- | ------------ | ----------- |
| id       | integer      | primary-key |
| title    | string       | ---         |
| desc     | string       | ---         |
| author   | string       | ---         |
| category | category(id) | forign-key  |
| price    | integer      | ---         |

## category

| Columns | Datatype | Constrains  |
| ------- | -------- | ----------- |
| id      | integer  | primary-key |
| name    | string   | ---         |

## borrow table

| Columns    | Datatype | Constrains  |
| ---------- | -------- | ----------- |
| id         | integer  | primary-key |
| userid     | user(id) | forign-key  |
| bookid     | book(id) | forign-key  |
| borrowedat | date     | ---         |
| returnat   | date     | ---         |
| isreturned | bool     | ---         |
