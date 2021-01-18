# Shopify Image Repository API

## System Design
- For the sake of simplicity, the entire backend is a Django monolith with a sub-app called [image marketplace](./image_marketplace/) to handle application-specific requests.

- Django has an ORM built-in but I use a PostgreSQL database to persist all of the created [users and images](./image_marketplace/models.py).

- Storing and fetching entire images from the database would be expensive so I instead upload the image binary to Google Cloud Storage and reference the unique identifier in the corresponding db image record.

- Images are owned by a single user. This is handled by a foreign key in the Images table pointing to the Users table. If an image's owner has been deleted from the system we delete the image as well since it can no longer be sold by a user.

<br>

## Features
For this project I built a REST API to handle the ADD and DELETE functions outlined in the challenge description. Once we have the fundamentals down for our image repository we can add more cool features together :)

<br>

### User Authentication
I made use of Django's user authentication system to create users with password encryption. The following methods were implemented:

- Create user
- Log in as a user
- Log out of the current session

<br>

### ADD Images to Repo 
To add new images to the repo users must first be authenticated (see above).

- One / bulk / enormous amount of images
    - For a single image upload we first create a blob in Google Cloud then create a reference to this blob in an image record. The created image is then associated with its owner.

    - To upload an enormous amount of images we do a batch insert for all the image records in the payload using [bulk create](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#bulk-create).

    - There is a unique constraint on (user id, title) so users can't uploud the same image twice.

- Private or public (permissions)
    - Users can mark their images as private so other users on the platform can't access them. This is done through a boolean flag "is_private" on each [image record](./image_marketplace/models.py). For example, the home page frontend may make a call to get all images. This will get all the user-uploaded images marked as public - similar to Instagram's explore page.

- Secure uploading and stored images
    - To upload images in the first place, users must authenticate themselves with a name, password, and email.

    - Since http is vulnerable to eavesdropping attacks, we'll use ssl to encrypt data flowing through our system.

    - Google Cloud also employs server-side encryption for our image blobs.

<br>

### DELETE Images from Repo
To remove images from the repo users must first be authenticated.

- Access control
    - To validate image deletion we check if the currently authenticated user is the actual owner of the image. If so, we continue with the deletion. If not, then we send back an error with http status FORBIDDEN.

- One / bulk / selected / all images
    - Similar to the single image upload, we first delete the image blob from GCS then delete the image record from our database. Since these are independent operations we can perform the deletes from GCS asyncronously.

- Secure deletion of images
    - To delete images from the repo, users must be authenticated in the platform.

    - Once they're authenticated, private information such as image ids are encrypted over the network.

<br>

## Usage

### Set up environment
- Google Cloud Storage Key
    - Put service_account.json in root directory

- 