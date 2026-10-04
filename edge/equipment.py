"""
Satark AI - Equipment Detection & Utilization Assessor (FR-5, FR-6)
Verifies:
- Physical presence of sanctioned Bill of Materials (BOM) equipment
- Apparent operability & utilization based on human-machine interaction
- Distinguishes 'PRESENT_AND_USED' from 'PRESENT_IDLE' (Audit-Day prop fraud) and 'ABSENT'
"""
import numpy as np
from typing import List, Dict, Any

class EquipmentUtilizationAssessor:
    def __init__(self, sanctioned_bom: Dict[str, Any], interaction_distance_pixels: float = 120.0):
        self.sanctioned_bom = sanctioned_bom
        self.interaction_distance_pixels = interaction_distance_pixels
        
        # Track detection histories: {item_category: {"presence_frames": 0, "interaction_frames": 0, "total_frames": 0}}
        self.history: Dict[str, Dict[str, int]] = {}
        for item in self.sanctioned_bom.get("items", []):
            cat = item["category"]
            self.history[cat] = {"presence_frames": 0, "interaction_frames": 0, "total_frames": 0}

    def assess_frame(self, detected_equipment: List[Dict[str, Any]], person_boxes: List[List[Any]]):
        """
        detected_equipment: List of {"category": str, "box": [x1, y1, x2, y2]}
        person_boxes: List of [x1, y1, x2, y2, conf]
        """
        for cat, stats in self.history.items():
            stats["total_frames"] += 1

        for eq in detected_equipment:
            cat = eq.get("category")
            if cat not in self.history:
                continue
            
            self.history[cat]["presence_frames"] += 1
            eq_box = eq["box"]
            eq_center = np.array([(eq_box[0] + eq_box[2]) / 2.0, (eq_box[1] + eq_box[3]) / 2.0])

            # Check if any person is in interaction range
            interacted = False
            for p_box in person_boxes:
                p_center = np.array([(p_box[0] + p_box[2]) / 2.0, (p_box[1] + p_box[3]) / 2.0])
                dist = np.linalg.norm(eq_center - p_center)
                if dist <= self.interaction_distance_pixels:
                    interacted = True
                    break
            
            if interacted:
                self.history[cat]["interaction_frames"] += 1

    def get_compliance_status(self) -> List[Dict[str, Any]]:
        status_list = []
        for item in self.sanctioned_bom.get("items", []):
            cat = item["category"]
            req_qty = item.get("required_quantity", 1)
            stats = self.history.get(cat, {"presence_frames": 0, "interaction_frames": 0, "total_frames": 1})
            
            total_f = max(1, stats["total_frames"])
            pres_ratio = stats["presence_frames"] / total_f
            inter_ratio = stats["interaction_frames"] / max(1, stats["presence_frames"])

            if pres_ratio < 0.25:
                operability = "ABSENT"
                present = False
            elif inter_ratio < 0.15:
                operability = "IDLE"  # Rented prop / unutilized
                present = True
            else:
                operability = "USED"  # Active hands-on learning
                present = True

            status_list.append({
                "item": cat,
                "sanctioned_count": req_qty,
                "detected_count": req_qty if present else 0,
                "present": present,
                "apparent_operability": operability,
                "interaction_minutes": round(stats["interaction_frames"] * 0.5, 1)  # 30s window per frame
            })
            
        return status_list
