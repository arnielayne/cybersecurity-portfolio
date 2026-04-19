import json
from collections import Counter

def load_eve_log(filepath):
    events = []
    with open(filepath, 'r') as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events

def analyze_alerts(events):
    alerts = [e for e in events if e.get('event_type') == 'alert']

    print(f"\n{'='*50}")
    print(f"SURICATA ALERT ANALYSIS")
    print(f"Total alerts: {len(alerts)}")
    print(f"{'='*50}\n")

    src_ips = Counter(a['src_ip'] for a in alerts)
    print("Top 10 Source IPs:")
    for ip, count in src_ips.most_common(10):
        print(f"  {ip:<20} {count} alerts")

    signatures = Counter(a['alert']['signature'] for a in alerts)
    print("\nTop 10 Signatures:")
    for sig, count in signatures.most_common(10):
        print(f"  [{count:>4}] {sig}")

    severities = Counter(a['alert']['severity'] for a in alerts)
    print("\nSeverity Breakdown:")
    for sev in sorted(severities):
        label = {1: "HIGH", 2: "MEDIUM", 3: "LOW"}.get(sev, "UNKNOWN")
        print(f"  Severity {sev} ({label}): {severities[sev]}")

    high = [a for a in alerts if a['alert']['severity'] == 1]
    if high:
        print(f"\n⚠️  HIGH SEVERITY ALERTS ({len(high)}):")
        for a in high[:5]:
            print(f"  {a['timestamp']} | {a['src_ip']} → {a['dest_ip']} | {a['alert']['signature']}")

if __name__ == "__main__":
    import sys
    filepath = sys.argv[1] if len(sys.argv) > 1 else "eve.json"
    events = load_eve_log(filepath)
    analyze_alerts(events)
