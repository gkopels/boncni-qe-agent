# ToR EVPN notes

Canonical lab docs and apply order: **[README.md](./README.md)**.

## ToR-specific apply

```bash
oc apply -f 30-tor-evpn-vxlan.yaml
oc -n openpe-tor-frr delete pod frr-tor --wait=true
# pod recreates from the pod manifest in 30-tor-evpn-vxlan.yaml
```

Optional external LAN on host bridge `br-tor-a`:

```bash
oc apply -f 32-tor-lan-pods-customer-a.yaml
```

## Useful vtysh on `frr-tor`

```text
show bgp l2vpn evpn summary
show evpn mac vni all
show evpn mac vni 1101
show ip route
show ip route vrf customer-a
show ip route vrf customer-b
show bgp l2vpn evpn route type macip
show bgp l2vpn evpn route type prefix
```

## Expect

- Underlay: VTEPs `10.200.201.1` / `.2` via `10.100.100.10` / `.11`
- VRF customer-a: `4.4.4.1/32`, `172.16.1.0/24`, host `/32`s
- VRF customer-b: `5.5.5.1/32`, `172.16.2.0/24`, host `/32`s
- L2 MACs: remote via OpenPE VTEPs; local on `br-l2-1101` / `br-l2-1102`
