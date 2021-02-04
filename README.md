# Restaurant voting app
Vote for the best restaurant today.

## Set up the project using Pipenv
To install projects dependencies run:

`pipenv install`

Run database migrations:

`pipenv run python manage.py migrate`

Run the project with:

`pipenv run python manage.py runserver`

## Using Docker
Build the project:

`docker-compose build`

Run the project:

`docker-compose up`

### Running migrations, tests and linter with Docker
Enter the web app's Docker container:

`docker exec -it django_app bash`

Run database migrations

`python manage.py migrate`

Run tests:

`coverage run manage.py test`

Run linter:

`flake8 --exclude ./restaurants/tests,./lunchvote/settings.py,./restaurants/migrations`


## Endpoints
* `/api/restaurants/`

    Accepts `GET` and `POST` requests.
    Retrieves a list of existing restaurants or to create new 
restaurant instances.

* `api/restaurants/{id}/`

    Accepts `GET, PUT and DELETE` requests.
    Retrieve, update or delete specific restaurant instances.

* `api/restaurants/{id}/history/`

    Accepts `GET` requests.
    Retrieves historic data for a specific restaurant, displaying
data (date, total vote result, number of distinct voter ip addresses) for days 
when the restaurant received votes.

* `/api/vote/`

    Accepts `POST` requests. 
    Requires the `id` of a restaurant, for which the vote is being cast.
    Example data:
    ```
    {
        "restaurant": 6
    }
    ```
    The first vote from the same ip counts as `1`, the second as `0.5`, the third and 
subsequent votes as `0.25`.

    Currently the voting is limited to 10 votes from one IP.
