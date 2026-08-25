# Detailed Test Plan: [Feature Name] ([JIRA_KEY])

## JIRA Reference

- Ticket Key: `[JIRA_KEY]`
- Ticket URL: [https://issues.redhat.com/browse/JIRA_KEY or your tracker URL]

## Related High-Level Test Plan

- Link or summary: [Google Doc URL to high-level plan, or "Derived from Epic only"]

## Prerequisites and Environment

- OpenShift/Kubernetes version:
- OpenPERouter version / install method (all-in-one / kustomize / Helm):
- **QE source context:** current clone of `openperouter` under `.cursor/workspaces/openpe-repo-analysis/` (`https://github.com/openperouter/openperouter`). Docs: https://openperouter.github.io/
- Default CLI: `oc` (use `kubectl` where equivalent)
- OpenPERouter namespace for this plan: `openperouter-system` (change here only if the Epic targets a different layout)
- Underlay assumptions (physical iface to ToR, ASN, neighbor IPs):
- Overlay focus (EVPN L2/L3, SRv6 L3VPN, passthrough) and any MetalLB/Multus integration:
- Kernel / sysctl notes if required by the feature:

## Placeholders

Intro sentence: all names below are **fixed literals** for this plan (no `OPENPE_NS`-style variables). Group by theme so the section stays scannable in Google Docs.

**Namespace**

- OpenPERouter: `openperouter-system`

**Underlay**

- Underlay CR: `underlay`
- Host / ToR ASN and neighbor addresses used in this plan

**Overlay / VPN**

- VNI or VPN CR names and IDs used in this plan

**Integration (if in scope)**

- MetalLB / Multus / other BGP speaker objects used in this plan

## Detailed Test Cases

### TC-01: [Name aligned with high-level TC-01]

**Purpose:** [Same intent as high-level Purpose]

**Pass/Fail criteria (summary):** [Short reminder from high-level plan]

#### Step 1 — [Short title]

Run:

```bash
oc get pods -n openperouter-system
```

Expected:

Run: oc get pods -n openperouter-system

Sample output:

```
NAME                                      READY   STATUS    RESTARTS   AGE
openperouter-controller-xxxxx             1/1     Running   0          5m
openperouter-router-xxxxx                 1/1     Running   0          5m
openperouter-nodemarker-xxxxx             1/1     Running   0          5m
```

#### Step 2 — [Short title]

Manifest (YAML):

```yaml
apiVersion: openpe.openperouter.github.io/v1alpha1
kind: Underlay
metadata:
  name: underlay
  namespace: openperouter-system
spec:
  asn: 64514
  interfaces:
    - type: NetworkDevice
      networkDevice:
        interfaceName: toswitch
  neighbors:
    - asn: 64512
      address: 192.0.2.1
```

Run:

```bash
oc apply -f step2-underlay.yaml
```

Expected:

Run: oc get underlay underlay -n openperouter-system -o wide

Sample output:

```
NAME       AGE
underlay   30s
```

#### Cleanup — [when needed]

Run:

```bash
oc delete -f step2-underlay.yaml --ignore-not-found
```

Expected:

Run: oc get underlay -n openperouter-system

Sample output:

```
No resources found in openperouter-system namespace.
```
