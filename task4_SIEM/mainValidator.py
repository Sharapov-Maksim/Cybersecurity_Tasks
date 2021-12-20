from rulesLoader import *
from dumpScanner import NetworkPackage, process_pcap

# Black list check
def checkNetworkPackageForbiden(ruleData, event):
    for content in ruleData:
        if content.side == "source":
            if (content.ip == "any" or content.ip == event.sourceIP) and \
                    (content.port == "any" or content.port == event.sourcePort):
                print("Anomaly from black-list detected, package:")
                print(event)
                return True
        elif content.side == "destination":
            if (content.ip == "any" or content.ip == event.destinationIP) and \
                    (content.port == "any" or content.port == event.destinationPort):
                print("Anomaly from black-list detected, package:")
                print(event)
                return True


# White list check
def checkNetworkPackageAllowed(ruleData, event):
    # suppose package is not allowed by default
    forbidden = True
    for content in ruleData:
        # if it contains in white list it becomes allowed and False returned
        if content.side == "source":
            if (content.ip == "any" or content.ip == event.sourceIP) and \
                    (content.port == "any" or content.port == event.sourcePort):
                return False

        elif content.side == "destination":
            if (content.ip != "any" and content.ip != event.destinationIP) and \
                    (content.port != "any" and content.port != event.destinationPort):
                return False

    print("Anomaly from white-list detected, package:")
    print(event)
    return True


rules = parseRules('rules.json')
events = process_pcap('dump.pcapng')

countB = 0
countW = 0
for event in events:
    for rule in rules:
        if rule.Type == 'rule-black-list':
            if checkNetworkPackageForbiden(rule.Data, event):
                countB += 1
                break
        elif rule.Type == 'rule-white-list':
            if checkNetworkPackageAllowed(rule.Data, event):
                countW += 1
                break

print("Total events scanned: ", len(events))
print("Found ", countB, " anomalies from black-list ")
print("Found ", countW, " anomalies from white-list ")
