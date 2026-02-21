from typing import Dict, Optional
import logging
import re
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplianceChecker:
    def __init__(self):
        self.compliance_patterns = {
            "auth": r"/auth/.*",
            "payment": r"/payment/.*"
        }
        
    def check_compliance(self, endpoint: str) -> bool:
        for pattern, regex in self.compliance_patterns.items():
            if re.match(regex, endpoint):
                # Perform compliance checks here
                return True
        return False

def enforce_compliance(endpoint: str) -> None:
    try:
        if not ComplianceChecker().check_compliance(endpoint):
            raise HTTPException(status_code=403, detail="Endpoint not compliant")
    except Exception as e:
        logger.error(f"Compliance check failed for {endpoint}: {str(e)}")
        raise