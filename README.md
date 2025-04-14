# Raindrop.io to RSS

A service that generates RSS feeds from Raindrop.io items.

## Features

- Generate RSS feeds from all Raindrop.io items
- Optionally generate feeds for specific collections
- Docker support for easy deployment

## Configuration

Create a `.env` file based on `.env.example`:

```
ACCESS_TOKEN=xxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PERPAGE=50
```

### Raindrop.io Access Token

To get your Raindrop.io access token:

1. Go to https://app.raindrop.io/settings/integrations
2. Create a new application
3. Copy the test token

## Usage

### All Items Feed

Access all your Raindrop.io items:

```
# params are optional
GET /?perpage=50&page=0
```

## Docker

Build and run the service using Docker:

```bash
docker-compose up -d
```

## Environment Variables

- `ACCESS_TOKEN`: Raindrop.io access token (can be set in .env instead)
- `PERPAGE`: Items per page (default: 50)
