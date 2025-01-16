# List of tasks

## Backend

### Create Django models

#### Create a model for the user

- User
  - username
  - password
  - email
  - first_name
  - last_name
  - is_active
  - is_staff
  - is_superuser
  - last_login
  - date_joined

#### Create a model for the user profile

- Profile
  - user
  - bio
  - location
  - birth_date
  - created_at
  - updated_at
  - avatar
  - cover_image

#### Create a model for the post

- Post
  - title
  - content
  - image
  - video
  - created_at
  - updated_at

#### Create a model for the comment

- Comment
  - content
  - author
  - post
  - created_at
  - updated_at

#### Create a model for the like

- Like
  - user
  - post
  - comment
  - created_at

#### Create a model for the follow

- Follow
  - follower
  - following
  - created_at

### Create Django graphene Queries

#### Create a Query for the user

- Get all users
- Get user by id
- Get user by username
- Get user by email

#### Create a Query for the user profile

- Get all profiles
- Get profile by user id
- Get profile by username
- Get profile by email

#### Create a Query for the post

- Get all posts with filtering by title and content
- Get post by id
- Get post by user id
- Get post by title

#### Create a Query for the comment

- Get all comments
- Get all comments by post id
- Get comment by id
- Get comment by user id

### Create Django graphene Mutations

#### Create a Mutation for the user

- Create user
- Update user
- Delete user

#### Create a Mutation for the user profile

- Create profile
- Update profile
- Delete profile

#### Create a Mutation for the post

- Create post
- Update post
- Delete post

#### Create a Mutation for the comment

- Create comment
- Update comment
- Delete comment

#### Create a Mutation for the like

- Create like
- Delete like

#### Create a Mutation for the follow

- Create follow
- Delete follow

### Create authentication and authorization

- JWT authentication
- JWT authorization
- Permissions
- Roles

## Frontend

### Create angular components
