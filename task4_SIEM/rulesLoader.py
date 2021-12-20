import json


class Rule:
    def __init__(self, rule_type, rule_data):
        self.Type = rule_type
        self.Data = rule_data


class NetworkRuleData:
    def __init__(self, side, ip, port):
        self.side = side
        self.ip = ip
        self.port = port


def parseRules(filename):
    # Read JSON data into the rules variable
    with open(filename, 'r') as f:
        rules = json.load(f)
        resultingRules = []
        for rule in rules['rules']:
            Type = rule['type']
            res = Rule(Type, [])
            for ruleData in rule['content']:
                side = ruleData['side']
                content = ruleData['content']
                ip = content['ip']
                port = content['port']
                res.Data.append(NetworkRuleData(side, ip, port))
            resultingRules.append(res)
        return resultingRules
