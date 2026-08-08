import yaml
import os

from .models import Node, PlacementMap, Seed
from ..utils.canonical_id import slugify

def write_node(node: Node, output_path: str) -> None:
    node_dir = f"{output_path}/nodes/"
    if not os.path.exists(node_dir):
        os.mkdir(node_dir)
    cid = node.canonical_id
    parts = cid.split('.')
    bits = [slugify(part) for part in parts]
    node_path = f"{output_path}/nodes/{bits[-1]}.yaml"
    try:
        content = node.model_dump()
        with open(node_path, 'w') as y:
            yaml.dump(content, y, default_flow_style=False, indent=2)
    except Exception as e:
        print(f"Error writing {cid}: {e}")
    return node_path

def write_placement_map(placement_map: PlacementMap, output_path: str) -> str:
    pm_path = f"{output_path}/placement_map.yaml"
    try:
        content = placement_map.model_dump()
        with open(pm_path, 'w') as y:
            yaml.dump(content, y, default_flow_style=False, indent=2)
    except Exception as e:
        print(f"Error writing placement map: {e}")
    return pm_path
    
def write_seed(seed: Seed, output_path: str) -> None:
    seed_path = f"{output_path}/seed.yaml"
    try:
        content = seed.model_dump()
        with open(seed_path, 'w') as y:
            yaml.dump(content, y, default_flow_style=False, indent=2)
    except Exception as e:
        print(f"Error writing seed: {e}")
    return seed_path