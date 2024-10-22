## How to run
### Applications to download:
- Docker Desktop
- Git
- IDE
- Neo4j Desktop (optional)

### Commands to setup project
- Install requirements and build the project
```docker-compose build```
- Run the server for development
```docker compose up```

### Commands to use
To run command inside docker, the command has to be included in like so:<br />
```docker-compose run --rm app sh -c "my_command"```

### Useful commands:
- Run tests:
```docker-compose run --rm app sh -c "pytest"```
- Run lint:
```docker-compose run --rm app sh -c "flake8"```
- Run both:
```docker-compose run --rm app sh -c "pytest && flake8"```
