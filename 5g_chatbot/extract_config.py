import yaml

def extract_network_details(yaml_file):
    with open(yaml_file, "r") as f:
        config = yaml.safe_load(f)

    gNBs = config.get("gNBs", 1)
    UEs = config.get("UEs", 1)
    
    return {"gNBs": gNBs, "UEs": UEs}

if __name__ == "__main__":
    yaml_file = "generated_config.yaml"
    details = extract_network_details(yaml_file)
    print(f"Extracted Config: {details}")
