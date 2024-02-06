1. Docker command to build the image

              docker build   --build-arg DJANGO_SUPERUSER_USERNAME=admin   --build-arg DJANGO_SUPERUSER_EMAIL=admin@example.com   --build-arg DJANGO_SUPERUSER_PASSWORD=adminpassword   -t django-ecom:v1

2. Docker command to run the container.

       docker run -p 8000:8000 django-ecom:v1

3. Check the API access using the below URL and creds mentioned.

       http://localhost:8000/admin/

       Username: admin
       Password: adminpassword
