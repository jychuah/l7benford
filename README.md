# l7benford


### Theory of Operation

This application consists of:
- A postgres container
- A Vue.js client container
- A Flask backend container
### Building and running production

```
docker-compose up
```

This will trigger instantiation of postgres with a fixture file that contains the contents
of `census_2009b`, a build of the Vue.js client to a volume that the Flask server has mounted
as static files, and startup of Flask. (Flask will wait for postgres to be ready.)
Wait for the client to build, then browse [`http://localhost:8000`](http://localhost:8000)

### Tests

```
./runtests.sh
```

Make sure the production server is up and running. In a separate terminal, run the
`runtests.sh` script. This will run `pytest` on the server and `yarn test:unit` on the client.

### Building and running development server

```
docker-compose -f ./docker-compose.dev.yml up
```

Then browse to [`http://localhost:8050`](http://localhost:8050). Yarn will run the Vue client at this port in development mode with automatic reloading. The API server will still run at `http://localhost:8000`, but the client will use `http://localhost:8000/api/` as the base URL for API calls.