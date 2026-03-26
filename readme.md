# Cybersecurity Portfolio – Adam Zasiński

## 📌 Overview
This portfolio presents hands-on cybersecurity projects focused on:

- Building an Active Directory environment from scratch
- Analyzing authentication logs (Event ID 4624 / 4625)
- Detecting failed login attempts (brute-force patterns)

All projects were built in a home lab using Hyper-V.

---

## 🚀 Key Projects

- Active Directory Lab (Domain Controller + log analysis)
- Python Log Analysis Tool (failed login detection)

### 🔍 Log Analysis Tool (Python)
A Python script that analyzes authentication logs and detects repeated failed login attempts (potential brute-force activity).

**Key features:**
- Parses log files (auth.log)
- Extracts IP addresses
- Counts failed login attempts
- Detects suspicious activity

**Technologies:**
- Python
- Collections (Counter)
- Log analysis

---

### 🏢 Active Directory Security Lab
A virtual lab environment built using Hyper-V, simulating a real corporate network with a Domain Controller and client machine.

**Scope:**
- Windows Server (Domain Controller)
- Windows 10 (domain-joined client)
- User and group management in Active Directory
- Domain authentication testing

**Security configuration:**
- Advanced Audit Policy (logon events, credential validation)
- Monitoring authentication logs

**Log analysis:**
- Event ID 4624 – successful logon
- Event ID 4625 – failed logon
- Detection of failed login attempts
- Analysis of logon types (including remote logon attempts)

**Skills demonstrated:**
- Active Directory configuration
- Group Policy (GPO)
- Troubleshooting authentication issues
- Security event analysis

---

## 🎯 TryHackMe

I actively develop my cybersecurity skills through hands-on labs on TryHackMe.

**Focus areas:**
- Networking fundamentals
- Linux basics
- Security concepts
- Blue team fundamentals

---

## 🚀 Skills Demonstrated

- Windows Server & Active Directory
- Log analysis & security monitoring
- Basic Python scripting for security
- Networking fundamentals (DNS, TCP/IP)
- Troubleshooting and problem-solving

---

## 📂 Repository Structure
/log-analysis-tool
/active-directory-lab

## 📫 Contact

TryHackMe: https://tryhackme.com/p/arnie21layne
GitHub: https://github.com/arnielayne