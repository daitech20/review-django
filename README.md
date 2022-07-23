# Review Application
## Setup Project
### Requirements
- Docker https://www.docker.com/
- Nodejs and npm

### Build Docker
After pulling source code into your local machine, please open your terminal and change work directory to the project.

Copy file `.env.example` to `.env`

Type the following command to build docker stack:
```bash
docker compose build
```
Waiting for the process finished.

Next, we need to mirgrate database schema by typing command.
```bash
docker compose run --rm server python server/manage.py migrate
```
Atter the migration done, start docker containers with daemon by command.
```bash
docker compose up -d
```

Then, let's open a web browser and visit `http://localhost:8088`.

### Build Web Client Application
We use Vue3 to build our web client application. From the folder of project, change work directory to `dashboard-client`.

```bash
cd ./dashboard-client
```

Copy file `.env.production` to file `.env`.

Install `npm` packages.
```bash
npm install
```

Then run application and visit the url presents in the terminal.
```bash
npm run dev
```
