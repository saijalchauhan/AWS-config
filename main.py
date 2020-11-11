import boto3
import yaml
import argparse


def sync_same():
    with open('info.yaml') as cf:
        config = yaml.safe_load(cf)
    source = config.get("source").get("region")
    desti = config.get("destination-same-acc").get("region")
    sess = boto3.session.Session(aws_access_key_id=config.get('cred-source').get("id"),
                                 aws_secret_access_key=config.get('cred-source').get("pass"))
    client_config_source = sess.client('config', source)
    config_rules = client_config_source.describe_config_rules(ConfigRuleNames=[])

    for i in config_rules.get("ConfigRules"):
        i.pop("ConfigRuleArn")
        i.pop("ConfigRuleId")
        remedy = client_config_source.describe_remediation_configurations(
            ConfigRuleNames=[i.get("ConfigRuleName")])
        if remedy.get("RemediationConfigurations"):
            remedy.get("RemediationConfigurations")[0].pop("Arn")
        for j in desti:
            client_config = sess.client('config', j)
            client_config.put_config_rule(ConfigRule=i)
            if remedy.get("RemediationConfigurations"):
                client_config.put_remediation_configurations(
                RemediationConfigurations=remedy.get("RemediationConfigurations"))
            if remedy.get("RemediationConfigurations"):
                x = remedy.get('RemediationConfigurations')[0].get('TargetId')
            else:
                x = "no remediation"
            print(f"{i.get('ConfigRuleName')} rule enabled in {j} location with remediation"
                  f" action {x} in same account")


def sync_across():
    with open('info.yaml') as cf:
        config = yaml.safe_load(cf)
    source = config.get("source").get("region")
    desti = config.get("destination-across-acc").get("region")
    sess_source = boto3.session.Session(aws_access_key_id=config.get('cred-source').get("id"),
                                 aws_secret_access_key=config.get('cred-source').get("pass"))
    sess_desti = boto3.session.Session(aws_access_key_id=config.get('cred-destination').get("id"),
                                 aws_secret_access_key=config.get('cred-destination').get("pass"))
    client_config_source = sess_source.client('config', source)
    config_rules = client_config_source.describe_config_rules(ConfigRuleNames=[])

    for i in config_rules.get("ConfigRules"):
        i.pop("ConfigRuleArn")
        i.pop("ConfigRuleId")
        remedy = client_config_source.describe_remediation_configurations(
            ConfigRuleNames=[i.get("ConfigRuleName")])
        if remedy.get("RemediationConfigurations"):
            remedy.get("RemediationConfigurations")[0].pop("Arn")
        for j in desti:
            client_config_desti = sess_desti.client('config', j)
            client_config_desti.put_config_rule(ConfigRule=i)
            if remedy.get("RemediationConfigurations"):
                client_config_desti.put_remediation_configurations(
                RemediationConfigurations=remedy.get("RemediationConfigurations"))
            if remedy.get("RemediationConfigurations"):
                x=remedy.get('RemediationConfigurations')[0].get('TargetId')
            else :
                x="no remediation"
            print(f"{i.get('ConfigRuleName')} rule enabled in {j} location with remediation"
                  f" action {x} across account")



if __name__=="__main__":
    parser= argparse.ArgumentParser(description="""Deplying config rules from one region to other regions in same/across accounts""")
    parser.add_argument("option",type=int,help="1.for same account 2.for across accounts")
    args =  parser.parse_args()
    if str(args.option) =="1":
        sync_same()
    elif str(args.option) =="2":
        sync_across()