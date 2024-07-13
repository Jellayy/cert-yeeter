![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jellayy/cert-yeeter/dockerhub.yml)
![Docker Pulls](https://img.shields.io/docker/pulls/jellayy/cert-yeeter)

# Cert Yeeter 9000

Simple API for serving SHA1 domain certificate fingerprints to embedded/IoT devices with limited TLS/SSL support

### Background

My roommate, despite being a highly paid defense contractor and electrical engineer, gets his microcontrollers from his sock drawer and refuses to spend the dollar on an ESP32.

So naturally the custom temperature sensors in our house are ESP8266 based and the InfluxDB Arduino library for these doesn't properly support SSL/TLS and they recommend you hard code your cert fingerprints.

This is an API so these things can pull my InfluxDB SHA1 cert fingerprint on boot instead of having to rip these off the walls every 90 days to change it manually.

## Usage

This API provides one endpoint: `/fingerprint` (there's also a swagger page at `/docs` but that doesn't count) that returns the SHA1 fingerprint for the server's configured domain in a `text/plain` response with all formatting stripped.

Call via cURL:
```bash
curl --request GET \
  --url http://server:8000/fingerprint \
  --header 'X-API-Key: XXX'
```

Example Response:
```
e7035bcc1c18771f792f90866b6c1df8dfaabdc0
```

## Deployment

### Docker CLI

```bash
docker run -d \
  --name cert-yeeter \
  -p OUTER_PORT:8000 \
  -e API_KEY=YOUR_KEY \
  -e DOMAIN_TO_PULL=YOUR_DOMAIN \
  --restart always \
  jellayy/cert-yeeter:latest
```

### Docker Compose

```yaml
services:
  cert-yeeter:
    image: jellayy/cert-yeeter:latest
    ports:
      - OUTER_PORT:8000
    environment:
      - API_KEY=YOUR_KEY
      - DOMAIN_TO_PULL=YOUR_DOMAIN
    restart: always
```