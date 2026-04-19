# 🔥 pfSense Network Security Lab

> Network segmentation, firewall rules, and intrusion detection/prevention (IDS/IPS) in a Hyper-V virtual environment

---

## 📌 Project Overview

This project simulates a small business network environment with a dedicated DMZ zone, protected by pfSense CE as the network gateway and firewall. Suricata runs in IPS mode — actively blocking suspicious traffic and generating alerts that are then analyzed using a Python script.

The lab intentionally reuses the Active Directory environment from the [AD Security Lab](../active-directory-lab/) — the Windows 10 domain workstation and Domain Controller sit behind pfSense as the corporate LAN, reflecting a realistic enterprise network topology.

**Goal:** Build and document a complete network defense stack — from segmentation to log analysis.

---

## 🗺️ Network Architecture

```
[Kali Linux / Attacker]
         │
    vSwitch-WAN (External)
         │
    ┌────┴────┐
    │  pfSense │  ← firewall + IDS/IPS (Suricata)
    └────┬────┘
    ┌────┴──────────────────┐
    │                       │
vSwitch-ADLab          vSwitch-DMZ
(Internal — AD Lab)     (Internal)
    │                       │
[Windows 10]         [Ubuntu Server]
[Domain Controller]    10.10.10.x
  192.168.x.x
```

| Network | IP Range | Role |
|---------|----------|------|
| WAN | DHCP (host) | External network / attacker-side |
| LAN (AD Lab) | 192.168.x.0/24 | Corporate network — domain workstations |
| DMZ | 10.10.10.0/24 | Semi-public zone — web server |

> The LAN segment reuses the existing `vSwitch-ADLab` virtual switch from the Active Directory lab. pfSense acts as the default gateway for both the Windows 10 workstation and the Domain Controller.

---

## 🛠️ Technologies

- **pfSense CE** — firewall, router, DHCP server
- **Suricata** — IDS/IPS with Emerging Threats Open rules (ETOpen)
- **Hyper-V** — virtualization platform
- **Kali Linux** — penetration testing (Nmap, port scanning)
- **Ubuntu Server 22.04** — HTTP server in DMZ (Apache2)
- **Windows 10 + Windows Server** — corporate LAN (reused from AD Lab)
- **Python 3** — Suricata log analysis (eve.json)

---

## 🔒 Firewall Rule Logic

### Core principle: default deny

Rules are processed top to bottom — the first matching rule wins. All traffic is blocked by default; only explicitly permitted connections are allowed through.

### LAN Rules

| Priority | Action | Protocol | Source | Destination | Port | Reason |
|----------|--------|----------|--------|-------------|------|--------|
| 1 | ✅ Pass | TCP | LAN net | DMZ net | 80, 443 | Access to DMZ web server |
| 2 | ✅ Pass | TCP | LAN net | any | 443 | Outbound HTTPS |
| 3 | ✅ Pass | UDP | LAN net | any | 53 | DNS resolution |
| 4 | ✅ Pass | ICMP | LAN net | DMZ net | — | Diagnostics (ping to DMZ) |
| 5 | 🚫 Block | any | LAN net | any | — | Default deny |

### DMZ Rules

| Priority | Action | Protocol | Source | Destination | Port | Reason |
|----------|--------|----------|--------|-------------|------|--------|
| 1 | ✅ Pass | TCP | DMZ net | any | 80, 443 | System updates |
| 2 | ✅ Pass | UDP | DMZ net | any | 53 | DNS |
| 3 | 🚫 Block | any | DMZ net | LAN net | — | DMZ cannot initiate connections to LAN |
| 4 | 🚫 Block | any | DMZ net | any | — | Default deny |

> Key security principle: a compromised DMZ server cannot reach the internal LAN — lateral movement is blocked at the firewall level.

---

## 🛡️ Suricata IDS/IPS Configuration

**Mode:** IPS (Inline) — Suricata actively blocks matching traffic, not just logs it.

**Monitored interfaces:** WAN and LAN

**Active rule categories (ETOpen):**

| Category | What it detects |
|----------|----------------|
| `emerging-scan` | Port scanning (Nmap, masscan) |
| `emerging-exploit` | Known vulnerability exploitation attempts |
| `emerging-dos` | DoS / flood attacks |
| `emerging-web-server` | Web server attacks (SQLi, LFI, RCE) |

---

## 🐍 Log Analysis — Python Script

The `suricata_analyzer.py` script parses Suricata's native `eve.json` log format and generates a structured alert report.

### Usage

```bash
python scripts/suricata_analyzer.py logs/eve_sample.json
```

### Sample Output

```
==================================================
SURICATA ALERT ANALYSIS
Total alerts: 47
==================================================

Top 10 Source IPs:
  192.168.56.101       38 alerts
  10.0.0.5              9 alerts

Top 10 Signatures:
  [  24] ET SCAN Nmap Scripting Engine User-Agent Detected
  [  11] ET SCAN Potential SSH Scan
  [   7] ET SCAN NMAP -sV Version Scan
  [   5] GPL SCAN nmap TCP

Severity Breakdown:
  Severity 1 (HIGH): 5
  Severity 2 (MEDIUM): 31
  Severity 3 (LOW): 11

⚠️  HIGH SEVERITY ALERTS (5):
  2024-11-15T14:23:11 | 192.168.56.101 → 10.10.10.1 | ET EXPLOIT ...
```

---

## 📂 Repository Structure

```
pfsense-security-lab/
├── README.md
├── docs/
│   ├── network-diagram.png         ← network topology diagram
│   ├── firewall-rules-lan.png      ← pfSense LAN rules screenshot
│   ├── firewall-rules-dmz.png      ← pfSense DMZ rules screenshot
│   ├── suricata-dashboard.png      ← Suricata interface status panel
│   └── suricata-alerts.png         ← alert list after simulated attack
├── scripts/
│   └── suricata_analyzer.py        ← eve.json analysis script
├── logs/
│   └── eve_sample.json             ← anonymized sample log
└── config/
    └── firewall_rules_notes.md     ← rule logic and design decisions
```

---

## ⚔️ Test Scenarios

### Scenario 1 — External Port Scan

```bash
# On Kali Linux (WAN side)
nmap -sS -p 1-1000 <pfSense_WAN_IP>
nmap -A <pfSense_WAN_IP>
```

**Expected result:** Suricata generates `ET SCAN Nmap` alerts; scan reveals no open internal ports.

### Scenario 2 — DMZ to LAN Lateral Movement Attempt

```bash
# On Ubuntu Server (DMZ)
curl http://192.168.1.100   # Windows 10 IP in LAN
```

**Expected result:** Connection blocked by `Block DMZ → LAN` rule.

### Scenario 3 — LAN to DMZ Access Verification

```bash
# On Windows 10 (LAN)
curl http://10.10.10.10     # Apache server in DMZ
```

**Expected result:** Server responds — traffic permitted by `Pass LAN → DMZ port 80` rule.

---

## 🎯 Skills Demonstrated

- Network design and segmentation (LAN / DMZ / WAN)
- Firewall rule configuration (default deny policy)
- IDS/IPS deployment and tuning (Suricata + ETOpen)
- Security log analysis in JSON format (Python)
- Network virtualization (Hyper-V, virtual switches)
- Controlled penetration testing (Nmap, Kali Linux)
- Integration of AD environment into a secured network perimeter

---

## 📸 Screenshots

| | |
|---|---|
| ![LAN Rules](docs/firewall-rules-lan.png) | ![Suricata Alerts](docs/suricata-alerts.png) |
| *Firewall rules — LAN zone* | *IDS alerts after simulated port scan* |

---

## 🔗 Related Projects

- [Active Directory Security Lab](../active-directory-lab/) — AD environment with Event ID 4624/4625 log analysis
- [Python Log Analysis Tool](../log-analysis-python/) — brute-force detection in auth.log
