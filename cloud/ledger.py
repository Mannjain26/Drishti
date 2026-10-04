"""
Satark AI - Tamper-Evident Hash-Chained Alert Ledger (FR-10, USP-5b)
Appends alerts with SHA-256 hash chaining.
Any local modification or deletion of past records breaks the cryptographic chain.
"""
import hashlib
import json
import time
from typing import List, Dict, Any, Optional, Tuple

class HashChainedLedger:
    def __init__(self):
        self.chain: List[Dict[str, Any]] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_block = {
            "block_index": 0,
            "timestamp": "2026-01-01T00:00:00Z",
            "centre_id": "SYSTEM_ROOT",
            "session_id": "GENESIS_SESSION",
            "alert_type": "GENESIS_BLOCK",
            "severity": "LOW",
            "description": "Drishti Root Trust Anchor",
            "details": {"version": "1.0", "standard": "SIH26245"},
            "previous_hash": "0" * 64,
            "block_hash": ""
        }
        genesis_block["block_hash"] = self._compute_hash(genesis_block)
        self.chain.append(genesis_block)

    def _compute_hash(self, block: Dict[str, Any]) -> str:
        block_copy = dict(block)
        block_copy.pop("block_hash", None)
        canonical = json.dumps(block_copy, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    def append_alert(self, centre_id: str, session_id: str, alert_type: str, severity: str, description: str, details: Dict[str, Any]) -> Dict[str, Any]:
        prev_block = self.chain[-1]
        new_block = {
            "block_index": len(self.chain),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "centre_id": centre_id,
            "session_id": session_id,
            "alert_type": alert_type,
            "severity": severity,
            "description": description,
            "details": details,
            "previous_hash": prev_block["block_hash"],
            "block_hash": ""
        }
        new_block["block_hash"] = self._compute_hash(new_block)
        self.chain.append(new_block)
        return new_block

    def verify_integrity(self) -> Tuple[bool, Optional[int], str]:
        """
        Walks the entire chain to verify cryptographic integrity.
        Returns (is_valid, corrupted_index, message)
        """
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Check previous hash link
            if curr["previous_hash"] != prev["block_hash"]:
                return False, i, f"Hash link broken between block #{i-1} and #{i}"

            # Check self-hash
            expected_hash = self._compute_hash(curr)
            if curr["block_hash"] != expected_hash:
                return False, i, f"Tampered data detected in block #{i}"

        return True, None, "Ledger integrity verified. Cryptographic chain intact."

    def get_centre_alerts(self, centre_id: str) -> List[Dict[str, Any]]:
        return [b for b in self.chain if b.get("centre_id") == centre_id]
