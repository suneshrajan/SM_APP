from drf_yasg import openapi

""" Accounts """
class SignupSchema():

    def get_tag():
        tag = ['Accounts']
        return tag
    
    def get_operation_id():
        operation_id = "Signup - Create User"
        return operation_id
    
    def get_opration_summary():
        opration_summary = """Signup Users"""
        return opration_summary
    
    def get_operation_description():
        desc = """
            Signup API
            -----------
            
            This API endpoint allows users to sign up by providing their username, password, and email.

            **Endpoint:** POST api/accounts/signup/

            **Request Body:**

            - { "**username**": "string", "**password**": "string", "**email**": "string", "**image**": "bytestring"}

            - **username (required):** The desired username for the new user.

            - **password (required):** The password for the new user. It should be kept secure and confidential.

            - **email (required):** The email address of the new user. It should be a valid email format.

            **Response:**
            
            - The API responds with a JSON array containing the following post details:

            - **id:** The unique identifier of the user.

            - **username:** The unique username of the user.

            - **email:** The email id of the user.

            - **first_name:** First name of the user.

            - **last_name:** Last name of the user.

            - **image:** Image content of the User.

            **Note:**

            - This API is used to create a new user account.

            - Ensure that the provided username and email are unique.

            - The password should be kept secure and should meet any password complexity requirements.

        """
        return desc

    def get_manual_parameters():
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_FORM, description='First Name', type=openapi.TYPE_STRING),
            openapi.Parameter('last_name', openapi.IN_FORM, description='Last Name', type=openapi.TYPE_STRING),
            openapi.Parameter('username', openapi.IN_FORM, description='User Name', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, description='Password', type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, required=True),
            openapi.Parameter('email', openapi.IN_FORM, description='Email', type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, required=True),
            openapi.Parameter('image', openapi.IN_FORM, description='Profile Image', type=openapi.TYPE_FILE, format=openapi.FORMAT_BINARY, x_types=['image/jpeg', 'image/png']),
        ]
        return manual_parameters
    
    def get_consumes():
        consumes = ['multipart/form-data']
        return consumes

    def get_responses():
        responses =  {
            201: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'image': openapi.Schema(type=openapi.TYPE_STRING),
                                }),
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                },
            )),
            400: 'Bad Request',
            }
        return responses
    

class LoginSchema():

    def get_tag():
        tag = ['Accounts']
        return tag

    def get_operation_id():
        operation_id = "Signin - Login User"
        return operation_id

    def get_opration_summary():
        opration_summary = """Signin Users"""
        return opration_summary

    def get_operation_description():
        desc_val = """
            Login API
            -----------

            This API endpoint allows users to authenticate by providing their username and password.

            **Endpoint:** POST api/accounts/login/

            **Request Body:**

            - { "**username**": "string", "**password**": "string" }

            - **username (required):** The username of the user for authentication.

            - **password (required):** The password associated with the provided username.

            **Response:**
            
            - The API responds with a JSON array containing the following post details:

            - **id:** The unique identifier of the user.

            - **username:** The unique username of the user.

            - **email:** The email id of the user.

            - **first_name:** First name of the user.

            - **last_name:** Last name of the user.

            **Note:**

            - This API is used for user authentication and generating access tokens.

            - The provided username and password must be valid and associated with an existing user account.

            - The response may include an authentication token or session information for subsequent API calls.
        """
        return desc_val
    
    def get_manual_parameters():
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description='User Name', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, description='Password', type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, required=True),
        ]
        return manual_parameters
    
    def get_responses():
        responses = {
            200: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                }),
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                },
            )),
            404: 'User not found',
            }
        return responses
    

class LogOutSchema():

    def get_tag():
        tag = ['Accounts']
        return tag

    def get_operation_id():
        operation_id = "Signout - Logout User"
        return operation_id

    def get_opration_summary():
        opration_summary = "Signout Users"
        return opration_summary

    def get_operation_description():
        desc_val = """
            Logout API
            ----------

            Logout the authenticated user, and delete the user credentials.

            **Endpoint:** GET api/accounts/logout/

            **Authentication:**

            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

        """
        return desc_val
    
    def get_responses():
        responses={
            200: "Successful logout",
        }
        return responses
    

class TestTokenSchema():

    def get_tag():
        tag = ['Accounts']
        return tag

    def get_operation_id():
        operation_id = "Validate Token"
        return operation_id

    def get_opration_summary():
        opration_summary = "Verify User Token"
        return opration_summary
    
    def get_operation_description():
        desc_val = """Test the token is valied"""
        return desc_val
    
    def get_responses():
        responses={
            200: "Valied Token !",
            401: "Cridentials not provided."
        }
        return responses
    

class GenerateOTPSchema():

    def get_tag():
        tag = ['Accounts']
        return tag

    def get_operation_id():
        operation_id = "Gemerate OTP"
        return operation_id
    
    def get_opration_summary():
        opration_summary = "Generate OTP"
        return opration_summary
    
    def get_operation_description():
        desc_val = """
            Generate OTP API
            ----------------

            **Endpoint:** GET api/accounts/generate/otp/

            **Authentication:**

            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **User Registration:** When a user registers on your website or application, they provide their email address as part of the registration form.

            **API Generation:** After the user submits the registration form, our backend system generates a one-time password (OTP) using an API, (User can skip this process when signup).
                                This API likely utilizes a combination of random number generation and hashing algorithms to create a unique and secure OTP.

            **Email Delivery:** Once the OTP is generated, our system sends an email to the user's registered email address. The email contains the OTP, typically along with some instructions.
        """
        return desc_val
    
    def get_responses():
        responses={
            200: "OTP generated and sent successfully to given email.",
            400: "Bad Request - Invalid input or email not found",
        }
        return responses
    

class VerifyOTPSchema():

    def get_tag():
        tag = ['Accounts']
        return tag
    
    def get_operation_id():
        operation_id = "Validate OTP"
        return operation_id

    def get_opration_summary():
        opration_summary = "Validate OTP"
        return opration_summary
    
    def get_operation_description():
        desc_val = """
            Verify OTP API
            --------------

            **Endpoint:** POST api/accounts/verify/otp/

            **Authentication:**

            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **User Verification:** The user receives the email and retrieves the OTP from it. They may be required to enter the OTP into a verification form on our website or application.

            **OTP Validation:** The backend system compares the OTP entered by the user with the one generated earlier. If the OTP matches, the user is considered verified. 
                                If the OTP doesn't match, appropriate error handling is performed.
        """
        return desc_val
    
    def get_manual_parameters():
        manual_parameters=[
            openapi.Parameter('otp', openapi.IN_FORM, description='OTP', type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, required=True),
        ]
        return manual_parameters
    
    def get_responses():
        responses={
            200: "Email verification successful.",
            400: "Please enter valied otp",
        }
        return responses


""" User """
class UserProfileSchema():

    def get_tag():
        tag = ["User & Followers"]
        return tag
    
    def get_operation_id():
        operation_id = "User Personal Profile"
        return operation_id
    
    def get_operation_summary():
        sumry_val = "Authorized user profil"
        return sumry_val
    
    def get_operation_description():
        desc = """
            User Profile API
            ----------------

            The User Profile API allows authenticated users to retrieve their profile details.

            **API Endpoint:** GET /api/personal/profile/

            **Authentication:**

            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **Request Parameters:**

            - This API does not require any specific request parameters.

            **Response:**
            
            - The API responds with a JSON array containing the following post details:

            - **id:** The unique identifier of the user.

            - **username:** The unique username of the user.

            - **email:** The email id of the user.

            - **first_name:** First name of the user.

            - **last_name:** Last name of the user.

            - "followres": "Conunt of user followings"
            
            - "posts": "Count of user post"

        """
        return desc
    
    def get_responses():
        responses =  {
            200: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'followres': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'posts': openapi.Schema(type=openapi.TYPE_INTEGER)
                                }),
                },
            )),
            400: 'Bad Request',
            }
        return responses
    

class UserListSchema():

    def get_tag():
        tag = ["User & Followers"]
        return tag
    
    def get_operation_id():
        operation_id = "User Profile List"
        return operation_id

    def get_operation_summary():
        desc_val = "User search based on name & username"
        return desc_val

    def get_operation_description():
        desc_val = """
            User Profile Search API
            -----------------------

            The User Profile Search API allows authenticated users to search for other user profiles based on username, first name, or last name.

            **API Endpoint:** GET api/users/search/user/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **Request Parameters:**
            
            - search: The search query string used to find matching user profiles. This parameter accepts partial matches and is case-insensitive.
            
            **Response:**
            
            - The API responds with a JSON array containing the following post details:

            - **id:** The unique identifier of the user.

            - **username:** The unique username of the user.

            - **email:** The email id of the user.

            - **first_name:** First name of the user.

            - **last_name:** Last name of the user.
        
        """
        return desc_val
    
    def get_manual_parameters():
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description='Search text', type=openapi.TYPE_STRING)
        ]
        return manual_parameters
    
    def get_responses():
        responses =  {
            200: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                                }),
                },
            )),
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            }
        return responses


class FollowerSchema():

    def get_tag():
        tag = ["User & Followers"]
        return tag
    
    def get_operation_id():
        operation_id = "Follow Users"
        return operation_id

    def get_operation_summary():
        desc_val = "Follow existing users"
        return desc_val
    
    def get_operation_description():
        desc_val = """
            Follow User API
            ---------------

            The Follow User API enables authenticated users to follow other users based on their user ID.

            **API Endpoint:** POST api/users/{user_id}/follow/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **URL Path Parameters:**
            
            - user_id (required): The unique identifier of the user to be followed.

            **Response:**

            - The API responds with a success message indicating that the user has successfully followed the specified user.
            
            - { "**message**": "Successfully followed user with ID {user_id}" }
        """
        return desc_val

    def get_responses():
        responses =  {
            201: "Successfuly followed",
            401: "Unauthorized",
            404: "Not Found",
        }
        return responses


class UnFollowerSchema():

    def get_tag():
        tag = ["User & Followers"]
        return tag
    
    def get_operation_id():
        operation_id = "Unfollow Users"
        return operation_id

    def get_operation_summary():
        desc_val = "Unfollow existing users"
        return desc_val
    
    def get_operation_description():
        desc_val = """
            Unollow User API
            ---------------

            The Follow User API enables authenticated users to unfollow other users based on their user ID.

            **API Endpoint:** DELETE api/users/{user_id}/users/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **URL Path Parameters:**
            
            - user_id (required): The unique identifier of the user to be unfollowed.

            **Response:**

            - The API responds with a success message indicating that the user has successfully unfollowed the specified user.
            
            - { "**message**": "Successfully unfollowed user with ID {user_id}" }
        """
        return desc_val

    def get_responses():
        responses =  {
            200: "Successfuly unfollowed",
            401: "Unauthorized",
            404: "Not Found",
        }
        return responses
    

""" Blog """
class UserBlogSchema():

    def get_tag():
        tag = ["Blogs"]
        return tag
    
    def get_operation_id():
        operation_id = "User Personal Blogs List"
        return operation_id

    def get_operation_summary():
        summary = "User post list"
        return summary

    def get_operation_description():
        desc = """ 
            User Post API
            -------------

            The User Post API allows authenticated users to retrieve their own post details.

            **API Endpoint:** GET api/blogs/user/personal/post/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **Request Parameters:**
            
            - This API does not require any specific request parameters.

            **Response:**
            
            - The API responds with a JSON array containing the following post details:

            - **id:** The unique identifier of the post.

            - **user_id:** Posted user id.

            - **image:** Image content of the post.

            - **content:** The content or body of the post.

            - **created_at:** The date and time when the post was created.

            - **updated_at:** The date and time when the post was last updated.
        """
        return desc

    def get_responses():
        responses =  {
            200: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'image': openapi.Schema(type=openapi.TYPE_STRING),
                                    'content': openapi.Schema(type=openapi.TYPE_STRING),
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING),
                                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING),
                                }),
                },
            )),
            401: "Unauthorized",
            }
        return responses
    

class FollowerBlogSchema():

    def get_tag():
        tag = ["Blogs"]
        return tag
    
    def get_operation_id():
        operation_id = "Followers Personal Blogs"
        return operation_id

    def get_operation_summary():
        summary = "Followers post"
        return summary

    def get_operation_description():
        desc = """ 
            Followers Post API
            -------------

            The User Post API allows authenticated users to retrieve their following users post details.

            **API Endpoint:** GET api/blogs/user/following/post/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **Request Parameters:**
            
            - This API does not require any specific request parameters.

            **Response:**
            
            - The API responds with a JSON array containing the following post details:

            - **id:** The unique identifier of the post.

            - **user_id:** Posted user id.

            - **image:** Image content of the post.

            - **content:** The content or body of the post.

            - **created_at:** The date and time when the post was created.

            - **updated_at:** The date and time when the post was last updated.
        """
        return desc

    def get_responses():
        responses =  {
            200: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'image': openapi.Schema(type=openapi.TYPE_STRING),
                                    'content': openapi.Schema(type=openapi.TYPE_STRING),
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING),
                                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING),
                                }),
                },
            )),
            401: "Unauthorized",
            }
        return responses


class CreateUserBlogSchema():

    def get_tag():
        tag = ["Blogs"]
        return tag
    
    def get_operation_id():
        operation_id = "Create Post"
        return operation_id
    
    def get_operation_summary():
        summary = "Crate personal post"
        return summary
    
    def get_operation_description():
        desc = """
            Create Post API
            ---------------

            The Create Post API enables authenticated users to create a new post.

            **API Endpoint:** POST api/blogs/user/personal/post/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **Request Body:**
            
            - The request body must include the following parameters:

            - **text (required):** The content or text of the post.
            
            - **image (optional):** An image file to be associated with the post. This can be provided as a multipart form-data field.

        """
        return desc

    def get_manual_parameters():
        manual_parameters=[
            openapi.Parameter('content', openapi.IN_FORM, description='User Content', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('image', openapi.IN_FORM, description='Blog Image', type=openapi.TYPE_FILE, format=openapi.FORMAT_BINARY, x_types=['image/jpeg', 'image/png']),
        ]
        return manual_parameters
    
    def get_consumes():
        consumes = ['multipart/form-data']
        return consumes
    
    def get_responses():
        responses =  {
            201: "Post added successfuly.",
            400: "Bad Request",
            401: "Unauthorized"
        }
        return responses
    

class UserCommentSchema():
    
    def get_tag():
        tag = ["Blogs"]
        return tag
    
    def get_operation_id():
        operation_id = "Comment on Post"
        return operation_id
    
    def get_operation_summary():
        summary = "Comment on post"
        return summary
    
    def get_operation_description():
        desc = """
            Post Comment API
            ----------------

            The Post Comment API enables authenticated users to add comments on posts.

            **API Endpoint:** POST api/blogs/user/following/post/comment/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **Request Body:**
            
            - The request body must include the following parameters:
            
            - **post_id (required):** The post id.
            
            - **comment (required):** The comment text.
        """
        return desc

    def get_manual_parameters():
        manual_parameters=[
            openapi.Parameter('post_id', openapi.IN_FORM, description='Post Id', type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('comment', openapi.IN_FORM, description='Comment content', type=openapi.TYPE_STRING, required=True)
        ]
        return manual_parameters
    
    def get_responses():
        responses =  {
            201: "Comment added successfully.",
            400: "Bad request.",
            401: "Unauthorized",
            404: "Post not found.",
        }
        return responses
    

class LikePostSchema():

    def get_tag():
        tag = ["Blogs"]
        return tag
    
    def get_operation_id():
        operation_id = "Like Post"
        return operation_id
    
    def get_operation_summary():
        summary = "Like post"
        return summary

    def get_operation_description():
        desc = """
            Like Post API
            -------------

            The Like Post API enables authenticated users to like posts based on their post ID.

            **API Endpoint:** GET api/blogs/user/following/{post_id}/post/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **URL Path Parameters:**
            
            - **post_id (required):** The unique identifier of the post to be liked.
        """
        return desc
    
    def get_responses():
        responses =  {
            201: "Post liked successfully.",
            400: "Bad request.",
            401: "Unauthorized",
            404: "Post not found.",
            500: "Enternal server error: {error content}."

        }
        return responses


class UnLikePostSchema():

    def get_tag():
        tag = ["Blogs"]
        return tag
    
    def get_operation_id():
        operation_id = "Unlike Post"
        return operation_id
    
    def get_operation_summary():
        summary = "Unlike post"
        return summary

    def get_operation_description():
        desc = """
            Unlike Post API
            -------------

            The Unlike Post API enables authenticated users to Unlike posts based on their post ID.

            **API Endpoint:** DELETE api/blogs/user/following/{post_id}/post/

            **Authentication:**
            
            - This API requires authentication. Users must include a valid authentication token in the request headers for successful access.

            **URL Path Parameters:**
            
            - **post_id (required):** The unique identifier of the post to be Unlike.
        """
        return desc
    
    def get_responses():
        responses =  {
            200: "Post Unlike successfully.",
            400: "Bad request.",
            401: "Unauthorized",
            404: "Post not found.",
        }
        return responses