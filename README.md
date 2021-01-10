# l7benford

### Building and running production

```
docker-compose up
```

Wait for the client to build, then browse [`http://localhost:8000`](http://localhost:8000)

### Building and running development server

```
docker-compose -f ./docker-compose.dev.yml up
```

Then browse to [`http://localhost:8050`](http://localhost:8050). Yarn will run the Vue client at this port in development mode with automatic reloading. The API server will still run at `http://localhost:8000`, but the client will use `http://localhost:8000/api/` as the base URL for API calls.