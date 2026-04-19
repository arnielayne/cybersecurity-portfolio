# Firewall Rules — Logic and Design Decisions

This document explains the reasoning behind each firewall rule in the pfSense configuration. The goal is not just to document *what* is configured, but *why* each decision was made.

---

## Core Philosophy: Default Deny

All interfaces follow a **default deny** policy: block everything, then explicitly allow only what is necessary.

This is the opposite of the default pfSense LAN behaviour (allow all), which was removed and replaced with explicit rules. The reason: with default allow, a forgotten protocol or port becomes a security gap. With default deny, nothing passes unless there is a conscious decision to permit it.

Rule processing in pfSense works **top to bottom — first match wins**. This means the order of rules is critical: more specific rules must appear before broader ones, and the block rule must always be last.

---

## LAN Rules (192.168.100.0/24)

The LAN zone contains the corporate network: a Windows 10 domain workstation and a Domain Controller (DC01). This is the highest-trust zone.

### Why LAN net (subnets) and not LAN address?

All rules use **LAN subnets** (the entire 192.168.100.0/24 range) as the source, not *LAN address* (which would only match the pfSense interface IP 192.168.100.1). Using LAN address would mean the rules only apply to traffic originating from pfSense itself — not from workstations in the network.

This was a real misconfiguration caught during testing: rules set to *OPT1 address* on the DMZ interface caused Ubuntu Server traffic to be blocked, because pfSense only matched its own IP, not 10.10.10.10.

### Rule 1 — LAN → DMZ HTTP/S (Pass TCP 80, 443)

Allows workstations to access the web server running in the DMZ (Apache2 on 10.10.10.10). Port 80 and 443 are grouped into an alias (80_443) for readability and easier management.

This rule is intentionally scoped to DMZ only — not to *any* destination. Workstations should only reach the DMZ web server on these ports, not arbitrary internet hosts on port 80.

### Rule 2 — LAN → Internet HTTPS (Pass TCP 443)

Allows outbound HTTPS traffic to the internet. Port 80 (plain HTTP) is intentionally not included — modern web traffic is HTTPS, and permitting unencrypted HTTP outbound from a corporate network is poor practice.

### Rule 3 — DNS (Pass UDP 53)

Allows DNS queries from the LAN to any destination.

**Protocol choice — UDP, not TCP:** DNS operates primarily over UDP port 53. TCP is only used for large responses (over 512 bytes) and zone transfers between DNS servers. A rule permitting only TCP/53 would cause most DNS queries to silently fail — this was observed during the Ubuntu Server setup when an incorrect TCP DNS rule caused intermittent apt update failures.

### Rule 4 — Ping to DMZ (Pass ICMP)

Allows ICMP (ping) from LAN to DMZ only — not to the internet. This enables basic connectivity diagnostics between the internal network and DMZ servers without exposing ICMP externally.

### Rule 5 — Block the rest (Block IPv4 *)

Catches all traffic not matched by rules 1–4. Protocol is set to **IPv4 \*** (any), not just TCP — this ensures UDP, ICMP to non-DMZ destinations, and any other protocols are also blocked.

---

## OPT1 / DMZ Rules (10.10.10.0/24)

The DMZ zone contains the Ubuntu Server running Apache2. This is a semi-trusted zone: it needs limited internet access for updates, but must never be able to initiate connections into the LAN.

### The key security principle

**A compromised DMZ server must not be able to reach the internal LAN.**

If an attacker exploits a vulnerability in Apache or the underlying OS and gains a shell on the Ubuntu Server, the firewall must prevent lateral movement into the LAN. Rule 4 (Block DMZ → LAN) is the enforcement point for this principle.

### Why OPT1 subnets and not OPT1 address?

Same reasoning as LAN: **OPT1 subnets** matches the entire 10.10.10.0/24 range, covering all devices in the DMZ. *OPT1 address* would only match pfSense's own DMZ interface IP (10.10.10.1), leaving all other DMZ hosts unmatched — effectively bypassing the rules entirely.

This was the root cause of the initial connectivity failure: Ubuntu Server (10.10.10.10) could not reach the internet because the pass rules were set to *OPT1 address* and did not apply to its traffic.

### Rule 1 — System updates (Pass TCP 80, 443)

Allows the Ubuntu Server to reach package repositories over HTTP and HTTPS. Without this rule, `apt update` and `apt install` would fail. Scoped to TCP because apt downloads use HTTP/HTTPS (TCP-based protocols).

### Rule 2 — DNS (Pass UDP 53)

Allows DNS resolution from the DMZ. Uses **UDP port 53** for the same reason as the LAN DNS rule — DNS is primarily UDP. The nameserver is set to 8.8.8.8 (Google) in Netplan, as the DMZ does not use the internal DC01 DNS server.

### Rule 3 — Ping outbound (Pass ICMP)

Allows ICMP from DMZ to any destination. Used for connectivity diagnostics (`ping 8.8.8.8`, `ping 10.10.10.1`). This rule was added after diagnosing a connectivity issue — Ubuntu could not ping pfSense even though the route was configured correctly, because ICMP was not in any pass rule.

### Rule 4 — Block DMZ → LAN (Block IPv4 *)

**The most important rule in the DMZ ruleset.**

Explicitly blocks all traffic from the DMZ to the LAN subnet (192.168.100.0/24). This rule must appear *before* the general block rule so it is logged and clearly visible as an intentional security boundary, not just a side effect of default deny.

This rule enforces the DMZ isolation principle: even if Ubuntu Server is fully compromised, the attacker cannot initiate connections to domain workstations, the Domain Controller, or any other internal resource.

Verified during testing:
```bash
# Run from Ubuntu Server (DMZ)
curl http://192.168.100.20
# Result: connection timed out — blocked by this rule
```

### Rule 5 — Block the rest (Block IPv4 *)

Default deny for all remaining traffic from the DMZ. Catches any protocol or destination not covered by rules 1–4.

---

## What is not configured (and why)

**No WAN rules:** pfSense blocks all unsolicited inbound traffic on WAN by default. No services are exposed from the internal network to the internet in this lab — the WAN interface is receive-only from the pfSense perspective (outbound NAT handles return traffic).

**No port forwarding:** The DMZ web server (Apache on 10.10.10.10) is only accessible from the LAN, not from the WAN. In a production scenario, a port forwarding rule (NAT + firewall rule) would be added to expose port 80/443 externally. This was intentionally omitted to keep the attack surface minimal in the lab.

**No IPv6 rules:** All rules are IPv4 only. IPv6 is not used in this lab environment.

---

## Lessons learned

| Issue | Root cause | Fix |
|-------|-----------|-----|
| Ubuntu could not reach internet despite correct Netplan config | OPT1 rules used *OPT1 address* instead of *OPT1 subnets* | Changed source to OPT1 subnets |
| apt update DNS failures | DNS rule used TCP/53 instead of UDP/53 | Changed protocol to UDP |
| Ubuntu could not ping pfSense | No ICMP pass rule on OPT1 | Added ICMP pass rule |
| Temporary allow-all rule needed for diagnosis | Multiple rule issues compounding | Systematic debugging: allow all → confirm routing works → restore specific rules |
