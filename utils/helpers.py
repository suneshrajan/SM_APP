import hashlib


def get_image_path(instance, filename):
    # Construct the image upload path with user_id folder
    # Example:user_id/folder_path/filename
    user_id = instance.user_id
    return f'{str(user_id)}/{instance.purpose}/{filename}'


def get_hashed_otp(otp):

    # Generated OTP
    otp = otp

    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()
    
    # Hash the OTP with salt
    sha256.update(otp.encode('utf-8'))
    
    # Get the hashed OTP
    hashed_otp = sha256.hexdigest()
    
    return hashed_otp
