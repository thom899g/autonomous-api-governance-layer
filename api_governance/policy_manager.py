from typing import Dict, Optional
import logging
from pyyaml import safe_load

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PolicyManager:
    def __init__(self, policy_file: str):
        self.policies = self._load_policies(policy_file)
        
    def _load_policies(self, file_path: str) -> Dict:
        try:
            with open(file_path, 'r') as f:
                return safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load policies from {file_path}: {str(e)}")
            raise

    def update_policy(self, endpoint: str, new_policy: Dict) -> None:
        self.policies[endpoint] = new_policy