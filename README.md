To install projects dependencies run:
`pipenv install`

Run the project with:
`pipenv run python manage.py runserver`

`/api/restaurant/` endpoint allows `GET` and `POST` requests to 
retrieve a list of existing restaurants or to create new 
restaurant instances.

`api/restaurant/{id}/` endpoint allows `GET, PUT and DELETE` requests
to retrieve, update or delete specific restaurant instances.

There is also an `/api/vote/` endpoint which accepts `POST` requests and 
requires the `id` of a restaurant, for which the vote is being cast.

The first vote from the same ip counts as `1`, the second as `0.5`, the third and 
subsequent votes as `0.25`
