Scoring Service Project
# Blog Post Scoring Project

## Requirements:

Design and implement a Django application using DRF where the user can view the list of blog posts and rate them. Each post contains a title and a context. Design and implement the following views:

1. **Display the list of contents**: In displaying the content list, the title of the content, the number of users who rated the content, and the average of those points should be displayed. Your design and implementation should be such that with a large number of points for the content (millions of content), performance will not suffer. If the user has given points to that post, his score will be displayed.

2. **Register points for the post**: The user registers a number between 0 and 5 as his score for a post. If the user, for a post, registers a score again, his previous score will be updated. Ability to delete points is not required. In some cases, many users may start giving unrealistic and emotional ratings to a post. Hypothetical example, It has been announced in a popular Telegram channel that you give a low rating to a certain post so that its rating will decrease! Design a mechanism so that such short-term events do not have an immediate impact on the score of a post. Mention the method you chose. There is no clear solution to this problem. Your analysis from the problem, the proposed solution, and how to implement it is important for us. In designing these cases, consider the conditions of a real product (production). You can save on other details comment and consider the simplest possible mode (for example, there is no need for a user profile, etc.).

## Implementation:

- I assumed to ignore all other fields that a post can have and in this implementation a post can have few fields.
- I ignored AAA related things like authentication, authorization, and ... because of simplicity.
- I used rate limit solution to prevent from Emotional Scoring in our system (there are more solutions like "Rate Limiting", "User Reputation", "Statistical Analysis", "Temporal Weighting", "Fraud Detection Algorithms", "Manual Review" but because of lack of time I just moved forward with rate limit solution).
- I added rate limit policy number to PostService but in real world (production) service it must read from config (.env) file.
- I didn't prepare admin panel to create score for posts, and you can only use it for analytics data and only create posts
- You must only submit your (user) scores from the provided apis

### Ratelimit policy:

For Posts (allow any user):
- There are no ratelimits to get Posts list/details.

For submitting scores (authenticated user only):
- Only 100 requests can be sent to submit score API per day (per user).
- Only for 5 posts can submit score per day (per user).
- Only for 100 posts can submit score per month (per user).
- Only 3 times can submit score for a post (per user).
- Only 1 time can submit score for a post in the last 30 days, so if he/she wants to change his/her score for a post, they must wait at least 30 days (per user).

important fields
- "total_score": average scores of a post
- "user_score": the score that current user submitted for the post
- "users_count": total number of users that contributed in scoring the post

Setup project requirements:
1. create .env file from .env.example in scoring directory with your own values (used for compose file)
2. create src_django/.env file from src_django/.env.example with your own values (used for docker file)
3. run: docker compose up -d --build
4. to have default admin run: docker compose exec -it scoring-django python manage.py create_default_admin_user


To test the system:
1. create default admin user
2. login into /admin with these credentials user:admin password:asdfqwer
3. then go to /swagger to see endpoints
4. at first create posts (need to be login by session)
5. try to set score for the posts
