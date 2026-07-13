---
applyTo: "**/*.tf, **/*.yaml, **/*.yml, **/Dockerfile, **/docker-compose*.yml"
---

# SRE Engineering Runbook Instructions

These instructions apply when working with infrastructure code, Kubernetes manifests, Terraform configs, and Docker files.

## Golden Signals

Always evaluate changes against the four golden signals:
- **Latency:** How long it takes to service a request.
- **Traffic:** How much demand is placed on the system.
- **Errors:** The rate of requests that fail.
- **Saturation:** How "full" the service is (CPU, memory, disk).

## Infrastructure Change Rules

1. **Never apply Terraform changes to production without a plan review.** Always run `terraform plan` and share the output.
2. **All Kubernetes deployments must have resource limits set.** Never leave `resources:` empty.
3. **All services must expose a `/healthz` or `/health` endpoint.** Ensure it is configured in the liveness probe.
4. **Use `RollingUpdate` strategy for Deployments.** Avoid `Recreate` in production services.
5. **All secrets must be stored in a secret manager** (e.g., AWS Secrets Manager, HashiCorp Vault). Never hardcode credentials.

## Alerting Standards

- Every service must have an alert on error rate > 1% for 5 minutes.
- Every service must have an alert on p99 latency > 2x the baseline.
- Alerts must have a `runbook_url` annotation pointing to the relevant runbook doc.

## On-Call Expectations

- Acknowledge a page within 5 minutes.
- Update the incident channel within 10 minutes of acknowledging.
- Escalate if no clear mitigation path is found within 30 minutes.
