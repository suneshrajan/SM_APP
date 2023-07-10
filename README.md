# SM_APP
social media app

Description
-----------

The developed APIs for the social media platform provide a comprehensive set of functionalities to allow users to 
create accounts, log in and out, verify their email addresses, create posts with text and image attachments, follow and unfollow other users, 
view a timeline of posts from followed users, like and comment on posts, view user profiles with relevant information, 
search for other users by username or name, and provide an admin(**http://127.0.0.1:8000/admin/**) interface for managing users, posts, and comments.
NOTE - Developers: Here we are not allowing creating admin automatically, so plese makse sure that have admin account.

- The APIs are designed to be user-friendly, secure, and efficient. They handle various error scenarios and provide appropriate error responses to 
ensure data integrity and smooth user experience. The implementation includes unit tests to verify the correctness and functionality of the APIs.

- Furthermore, a background task using Celery is implemented to fetch and deactivate users with unverified email addresses daily at 7 pm, 
ensuring the platform maintains active and verified user accounts. 
NOTE: **celery -A sm_backend worker -B --loglevel=info** use this comend to schedule, run celery task.

- To facilitate API usage and integration, comprehensive API documentation is provided using Swagger. The documentation includes detailed descriptions, 
request and response examples, and clear instructions on how to interact with each API endpoint.

- In conclusion, the developed APIs for the social media platform offer a robust and scalable solution for building a social media application, 
enabling users to connect, share, and interact within the platform's ecosystem.
