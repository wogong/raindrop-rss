# Raindrop.io items to RSS

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
3. Copy the token

## Usage

### All Items Feed

Access all your Raindrop.io items:

```
# params are optional
GET /?perpage=50&page=0
```

## Podman or Docker

```
podman run -d --name raindrop-rss \
  -p 5000:5000 \
  -e ACCESS_TOKEN=<YOUR_ACCESS_TOKEN> \
  -e PERPAGE=50 \
  -e FLASK_ENV=production \
  ghcr.io/wogong/raindrop-rss:latest
```

if you want to use `systemd` to manage this service, please reference to `raindrop-rss.container`.

## Environment Variables

- `ACCESS_TOKEN`: Raindrop.io access token, `Test token` actually, see reference.
- `PERPAGE`: Items per page (default: 50)

## Reference
- https://developer.raindrop.io/v1/authentication/token