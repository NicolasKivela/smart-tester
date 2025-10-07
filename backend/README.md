Managing dependencies:

- Adding new dependency: poetry add [add library name here]



To access API documentation add /docs to the backend url (http://127.0.0.1:8000/docs)


How to test your own component separately:
for example:
docker compose run --rm backend python -m bdd_scenarios
