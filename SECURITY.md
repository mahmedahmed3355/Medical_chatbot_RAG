# Security Policy

## Supported Versions

Security fixes are applied to the latest version of the project available on the main branch.

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

If you discover a security issue, report it privately to the repository owner.

Include:

- A description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact.
- Any proof-of-concept details necessary to understand the issue.

Please avoid publicly disclosing the vulnerability until it has been reviewed.

## Security Practices

This repository follows several security practices:

- Secrets and environment files are excluded from version control.
- .env.example is provided instead of committing real credentials.
- Docker containers run as a non-root user.
- Docker builds use a minimal Python base image.
- .dockerignore excludes unnecessary files from container builds.
- CI runs automated linting and tests.
- Dependency updates are monitored through Dependabot.

## Secrets

Never commit:

- API keys
- Access tokens
- Passwords
- Private keys
- Cloud credentials
- Production configuration files
- .env files containing real secrets

Use environment variables or a secure secret management system for sensitive configuration.

## Container Security

The application container is configured to:

- Run as a non-root user.
- Expose only the application port.
- Use a health check.
- Avoid copying unnecessary development files into the runtime image.

## Dependency Security

Keep dependencies updated and review automated dependency update pull requests before merging them.

When possible, scan container images and dependencies for known vulnerabilities before deployment.
