# Social-Network

It is a social networking site just like any other. We can add, delete posts. Like, make friends, etc. 

project available on https://github.com/shagunbandi/Social-Network/ (Recommended, works perfectly)

to view online https://quiet-beach-93787.herokuapp.com/posts/ (Outdated)


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
![View Page](https://github.com/shagunbandi/Social-Network/blob/master/screenshots/2.View.png?raw=true | height=100)

https://github.com/shagunbandi/Social-Network/tree/master/screenshots

## Backend
1. Django and Django REST-framework.

## APIs
### Accounts


URL  | Description
------------- | -------------
`/api/accounts/register`   |   Register a new user
`/api/accounts/login` |   Login a user

### Post

URL  | Description
------------- | -------------
`/api/posts/`   |   View all Posts
`/api/posts/create` |   Create a Post
`/api/posts/<slug>/`    |   View details of post with slug `slug`
`/api/posts/<slug>/delete`  |   Delete post with slug `slug`
`/api/posts/<slug>/update`  |   Update post with slug `slug`
 
 ### Comment

URL  | Description
------------- | -------------
`/api/comments/`   |   View all Comments
`/api/comments/create` |   Create a Comment
`/api/comments/<pk>` |   Get details of comment with pk `pk`
`/api/comments/<slug>/update`  |   Update or Delete comment with slug `slug`

