# Armis-Task

1. Copy the example environment file:

   ```bash
        cp .env.example .env

2. Edit the newly created .env file and fill in the necessary values according to your environment.


3. Run pipeline tasks
    ```bash
        docker compose --profile create-indexes up --build
        docker compose --profile qualys-sync up --build
        docker compose --profile crowdstrike-sync up --build