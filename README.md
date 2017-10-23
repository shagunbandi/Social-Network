# Social-Network

## What can we do
1. There are posts on the home page
2. Create, Edit, Delete, Like, Comment can be done by user.
3. Can send and recieve friend request.
4. There is a profile page, where you can see all your liked, commented, created, posts.
5. There are few APIs to 
Markup :  * create, edit, delete a post.
          * get details of a post
          * To view all posts.
          * To view all comments    

## UI
Bootstrap

## Backend
1. Django and Django REST-framework.

## APIs
### Post
 - `/api/posts/`
  - View all Posts
 - `/api/posts/create`
  - Create a Post
 - `/api/posts/<slug>/`
  - View details of post with slug `slug`
 - `/api/posts/<slug>/delete`
  - Delete post with slug `slug`
 - `/api/posts/<slug>/update`
  - Update post with slug `slug`
 
 ### Comment
 - `api/comments/`
  - View all Comments
 - `/api/posts/<pk>`
  - Get details of comment with pk `pk`


#### Bugs and features to be added
1. Friend Request to be done by AJAX.
2. Comment APIs to be created
3. Account login, logout and create APIs to be created.
4. Make it more stable for big data.
