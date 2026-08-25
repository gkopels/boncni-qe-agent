# OpenPE SRv6 L3VPN + L2 + MetalLB lab (customer-a only)
#
# Cluster: kni-qe-98
# Replaces EVPN L3VNI lab. L3VPN and L3VNI cannot coexist.
#
# Addressing:
#   Underlay IPv4 link: 10.100.100.0/24 (ToR .254, workers .10/.11) — VXLAN L2
#   ToR BGP/SRv6 source: 2001:db8:1234::1
#   OpenPE tunnel IPv6: 2001:db8:1234:5678::/64
#   OpenPE VTEP IPv4: 10.200.201.0/24
#   OpenPE SRv6 locator base: fd00:0:32::/48
#   ToR SRv6 locator: fd00:0:10::/48
#   customer-a L3VPN host session: 172.16.20.0/24
#   customer-a L2 LAN: 172.16.1.0/24 GW 172.16.1.1 VNI 1101
#   MetalLB VIP: 4.4.4.1
#
# ASN: OpenPE 64514, MetalLB 64515, ToR/leaf 64520

## Apply order (after EVPN teardown)

```bash
export KUBECONFIG=...
cd .cursor/workspaces/agent-tmp/openpe-srv6-lab

oc apply -f 01-metallb.yaml
oc apply -f 09-nncp-underlay.yaml
# wait NNCP
oc apply -f 08-underlay-srv6.yaml
oc apply -f 30-tor-srv6.yaml
oc -n openpe-tor-frr delete pod frr-tor --wait=true

oc apply -f 04-workload-customer-a.yaml
oc apply -f 10-l3vpn-customer-a.yaml
oc apply -f 11-l2vni-customer-a.yaml
oc apply -f 02-ipaddresspool.yaml
oc apply -f 40-metallb-customer-a.yaml
oc apply -f 50-evpn-l2-service.yaml
```

## Validate

```bash
# IS-IS / SRv6 on OpenPE
oc -n openshift-openperouter exec deploy/router -c frr -- vtysh -c 'show isis neighbor'
# (use actual router pod name)

# ToR VPN routes
oc -n openpe-tor-frr exec frr-tor -- vtysh -c 'show bgp ipv4 vpn'
oc -n openpe-tor-frr exec frr-tor -- vtysh -c 'show ip route vrf customer-a'

# L2
oc -n customer-a exec customer-a-l2-w0 -- ping -c 2 172.16.1.11

# VIP via testcmd (v4 + v6)
oc -n customer-a exec customer-a-l2-w0 -- \
  testcmd -protocol tcp -port 80 -server 4.4.4.1 -interface net1
# Ensure IPv6 default via IRB (eth0 RA often wins otherwise):
#   ip -6 r del default dev eth0; ip -6 r replace default via 2001:db8:1::1 dev net1
oc -n customer-a exec customer-a-l2-w0 -- \
  testcmd -protocol tcp -port 80 -server 2001:db8:4:4:: -interface net1

# EVPN L2 service VIP (Type-2 on VNI 1101) — not MetalLB L2 (macvlan≠host)
oc -n customer-a exec customer-a-l2-w0 -- \
  testcmd -protocol tcp -port 80 -server 172.16.1.100 -interface net1
```
