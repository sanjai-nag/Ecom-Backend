1. Command to build the Docker image for Ecom-Backend application.

         docker build --build-arg DJANGO_SUPERUSER_USERNAME=admin --build-arg DJANGO_SUPERUSER_EMAIL=admin@example.com --build-arg DJANGO_SUPERUSER_PASSWORD=adminpassword -t django-ecom:v1

2. Command to run the Ecom-backend docker image.

       docker run -p 8000:8000 django-ecom:v1

3. Check the API access using the below URL and creds mentioned.

       http://localhost:8000/admin/

       Username: admin
       Password: adminpassword
