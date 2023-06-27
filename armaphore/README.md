# Semaphore controlling access to physical resources

## Concepts

* Provide an API to request a "build container" on a host. Today, only support request for ARM resource.
* Each API request uses a token, that token is associated to metadata for providers (eg: a project in Equinix)
* Request endpoint looks like: /v0/webhook/github with an Authentication header being the API token
* Service parses webhook payload and determines if it needs to perform a build
* If a build is needed, service checks if there's an already running matched architecture. If there is not already a running host, a host is booted and the service waits for it to be available. Service connects to host, launches a LXC container with correct base image, environment variables, and launch an ephemeral worker
