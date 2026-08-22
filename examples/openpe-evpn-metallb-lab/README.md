# OpenPE + MetalLB EVPN lab (customer-a / customer-b)

> **Tracked copy** under `examples/openpe-evpn-metallb-lab/` (synced from the lab workspace). Prefer this path for reuse and git history.


Cluster: **kni-qe-98** (`source ~/Documents/cluster-vars/setup-cluster.sh kni-98 CX7`)  
Image (all workload pods): `quay.io/ocp-edge-qe/eco-gotests-network-client:v4.20`

This directory is the **canonical** lab snapshot (L2 EVPN + L3 VRF + MetalLB VIPs in VRF).  
L3 Passthrough and **customer-c** were removed. Older one-off YAMLs live under `archive/`.

## Topology (summary)

```text
                    ┌─────────────────────────────┐
                    │  fake ToR FRR (frr-tor)     │
                    │  VTEP 10.200.201.254        │
                    │  underlay 10.100.100.254    │
                    │  VRF customer-a / customer-b│
                    └─────────────┬───────────────┘
                                  │ underlay + EVPN
              ┌───────────────────┴───────────────────┐
              │                                       │
     OpenPE worker0                          OpenPE worker1
     VTEP 10.200.201.1                       VTEP 10.200.201.2
     underlay 10.100.100.10                  underlay 10.100.100.11
     ens1f0np0 (in router netns)             ens1f0np0
              │                                       │
   L2 1101 / L3 1001 (cust-a)              same VNIs
   L2 1102 / L3 1002 (cust-b)
```

### Per-tenant addressing

| Tenant | L3 VNI / VRF | L2 VNI / LAN | IRB GW | Host session | MetalLB VIP |
|--------|--------------|--------------|--------|--------------|-------------|
| customer-a | 1001 | 1101 / `172.16.1.0/24` | `172.16.1.1` | `172.16.20.0/24` | `4.4.4.1` |
| customer-b | 1002 | 1102 / `172.16.2.0/24` | `172.16.2.1` | `172.16.21.0/24` | `5.5.5.1` |

| Role | Pods | Network |
|------|------|---------|
| L2 | `customer-*-l2-w0/w1` | Multus `net1` on `br-hs-11xx` |
| L3 | `customer-*-l3-w*` | OVN `eth0` only; VIP via MetalLB → host-session BGP → VRF |

ASN: OpenPE **64514**, MetalLB/FRR-K8s **64515**, ToR underlay peer **64512**.  
EVPN RTs: `64514:1001` / `64514:1002`.

## Canonical manifests (apply order)

Prereq: OpenPE operator installed (`openshift-openperouter`), MetalLB operator available.

```bash
export KUBECONFIG=...   # kni-qe-98
cd .cursor/workspaces/agent-tmp/openpe-metallb-option-a

# 1) MetalLB speaker backend
oc apply -f 01-metallb.yaml

# 2) Underlay IPs on workers (before Underlay steals NIC), then Underlay CR
oc apply -f 09-nncp-underlay-ips.yaml
# wait NNCP Available, then:
oc apply -f 08-underlay.yaml

# 3) Fake ToR EVPN PE (recreate pod after config change)
oc apply -f 30-tor-evpn-vxlan.yaml
oc -n openpe-tor-frr delete pod frr-tor --wait=true   # recreates with new ConfigMap

# 4) Tenants: L3VNI + L2VNI + L2 pods
oc apply -f 04-workload-customer-a.yaml   # ns + L3 Service/pods
oc apply -f 31-evpn-customer-a.yaml       # L3VNI/L2VNI/NAD/L2 pods
oc apply -f 16-svc-customer-b.yaml
oc apply -f 41-evpn-customer-b.yaml

# 5) MetalLB pools + peers into VRF host sessions
oc apply -f 02-ipaddresspool.yaml
oc apply -f 40-metallb-customer-a-vrf.yaml
oc apply -f 42-metallb-customer-b-vrf.yaml

# 6) Optional: ToR-side LAN pods (external site on br-tor-a)
oc apply -f 32-tor-lan-pods-customer-a.yaml
```

## File map

| File | Purpose |
|------|---------|
| `01-metallb.yaml` | MetalLB `frr-k8s-external` |
| `02-ipaddresspool.yaml` | Pools `4.4.4.0/24`, `5.5.5.0/24` |
| `04-workload-customer-a.yaml` | ns `customer-a` + L3 Service/pods |
| `08-underlay.yaml` | Underlay + EVPN neighbor to ToR |
| `09-nncp-underlay-ips.yaml` | Host underlay IPs `.10`/`.11` |
| `16-svc-customer-b.yaml` | ns `customer-b` + L3 Service/pod |
| `30-tor-evpn-vxlan.yaml` | ToR FRR ConfigMap + Pod (L2+L3 EVPN) |
| `31-evpn-customer-a.yaml` | customer-a L3VNI/L2VNI/NAD/L2 pods |
| `32-tor-lan-pods-customer-a.yaml` | Optional ToR LAN Multus pods |
| `40-metallb-customer-a-vrf.yaml` | BGP peers/advert/FRR receive for a |
| `41-evpn-customer-b.yaml` | customer-b L3VNI/L2VNI/NAD/L2 pods |
| `42-metallb-customer-b-vrf.yaml` | BGP peers/advert/FRR receive for b |
| `archive/` | Superseded passthrough / split YAMLs |

## Validation cheat sheet

### L2 (MAC / VXLAN)

```bash
# Pod MAC
oc -n customer-a exec customer-a-l2-w0 -- ip link show net1

# ToR EVPN MAC table
oc -n openpe-tor-frr exec frr-tor -- vtysh -c 'show evpn mac vni 1101'
oc -n openpe-tor-frr exec frr-tor -- vtysh -c 'show evpn mac vni 1102'

# L2 pod ↔ L2 pod (same VNI, VTEP-to-VTEP)
oc -n customer-a exec customer-a-l2-w0 -- ping -c 3 172.16.1.11
```

Known-unicast L2 path: pod → `br-hs-1101` → OpenPE → VXLAN → peer VTEP → peer bridge → pod.  
ToR is mainly **control plane** for that ping (not a required hairpin).

### L3 / MetalLB VIP in VRF

```bash
# ToR VRF routes (VIP + LAN)
oc -n openpe-tor-frr exec frr-tor -- vtysh -c 'show ip route vrf customer-a'
oc -n openpe-tor-frr exec frr-tor -- vtysh -c 'show ip route vrf customer-b'

# From L2 pod: TCP to VIP (ICMP to VIP often fails; backends use testcmd not HTTP)
oc -n customer-a exec customer-a-l2-w0 -- \
  testcmd -protocol tcp -port 80 -server 4.4.4.1 -interface net1
```

VIP path: MetalLB advertises `4.4.4.1/32` to OpenPE host session (`172.16.20.1`) → VRF → EVPN Type-5 to ToR.  
OpenPE VRF uses `route-map allowall`; prefix filter is on **FRR-k8s** (`…-allowed-ipv4`).

### OpenPE interfaces (worker0 example)

| Interface | Role |
|-----------|------|
| `pe-e-1101` / `br-pe-1101` / `vni1101` | customer-a **L2** |
| `pe-e-1001` / `br-pe-1001` / `vni1001` | customer-a **L3** + host session |
| `ens1f0np0` | underlay |
| `lo` `10.200.201.1` | VTEP |

L2 default GW in pod (`172.16.1.1`) = OpenPE IRB on `br-pe-1101`.

## Notes

- Workload image includes `ip` and `testcmd`. L3 backends listen with `testcmd` on `:8080` — use `testcmd` client, not `curl`, unless you change the listener to HTTP.
- L3 pods have **only** OVN `eth0`; they are not on `172.16.1.0/24`. Ping L3 pod via cluster IP if needed.
- `09-nncp-underlay-ips.yaml`: OpenPE Underlay moves `ens1f0np0` into the router netns; underlay addressing is then owned by OpenPE.
