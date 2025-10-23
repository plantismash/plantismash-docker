# Plantismash docker repository

This is the repository that contains a setup to deploy plantismash to a set of docker-compose services

The services are:

- flask webserver
- plantismash "backend", which consists of:
  - redis database
  - plantismash

There are plans to split these up further into an independent plantismash container and redis container

## Deployment

This deployment assumes you are on a unix-based system.

This deployment also requires you to be a superuser or to at least be able to manage docker containers

### First deployment

1. create a .envs file in the source directory:

```
SETTINGS_FILE=web/settings.cfg
STATUS_URL=https://your_server_url_here/server_status
```

This is used by rebuild.sh to get some deployment-specific information.

2. Edit the settings.cfg in web/ to suit your needs

3. Edit docker-compose.yml to change the ports that are used by the containers, and if necessary the volumes

4. run `rebuild.sh`

Running rebuild.sh may result in a bunch of errors the first time you run this, as it assumes it's re-building an existing deployment.

### Redeploying

If everything is set up correctly, whenever you make a change to the webserver or backend services, running `rebuild.sh` should ensure that the containers are re-created and the job count is up-to-date.
