"""
Satark AI - Telemetry Packager & Cryptographic Signer (FR-11, FR-12, NFR-3)
Packages edge analytics into low-bandwidth signed JSON telemetry (<15 Kbps budget).
Signs payload with HMAC-SHA256 / ECDSA device key.
"""
import hmac
import hashlib
import json
from typing import Dict, Any

class TelemetryPackager:
    def __init__(self, secret_key: str = "drishti_device_secret_key_2026"):
        self.secret_key = secret_key.encode('utf-8')

    def package_and_sign(self, telemetry_data: Dict[str, Any], prev_hash: str = "GENESIS_HASH") -> Dict[str, Any]:
        telemetry_data["prev_hash"] = prev_hash
        telemetry_data.pop("signature", None)
        
        # Canonical JSON string serialization for cryptographic determinism
        canonical_str = json.dumps(telemetry_data, sort_keys=True, separators=(',', ':'))
        
        # Generate HMAC-SHA256 signature
        signature = hmac.new(self.secret_key, canonical_str.encode('utf-8'), hashlib.sha256).hexdigest()
        
        telemetry_data["signature"] = signature
        return telemetry_data

    def verify_signature(self, telemetry_data: Dict[str, Any]) -> bool:
        data_copy = dict(telemetry_data)
        signature = data_copy.pop("signature", "")
        if not signature:
            return False
            
        canonical_str = json.dumps(data_copy, sort_keys=True, separators=(',', ':'))
        expected = hmac.new(self.secret_key, canonical_str.encode('utf-8'), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected)
