"""
Satark AI - Red-Team Scenario Data & Frame Stream Generator
Generates precise synthetic video frame streams for all 6 Red-Team fraud scenarios (R1–R6).
"""
import numpy as np
import cv2
from typing import List, Generator

class RedTeamDataGenerator:
    @staticmethod
    def generate_r1_lens_covered_stream(num_frames: int = 30) -> List[np.ndarray]:
        """R1: Normal classroom transitions to covered lens / blackout midway."""
        frames = []
        for i in range(num_frames):
            if i < 10:
                # Normal classroom
                frame = np.full((480, 640, 3), (220, 220, 220), dtype=np.uint8)
                cv2.putText(frame, "NORMAL SESSION", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 150, 0), 2)
            else:
                # Covered lens / blackout attack
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                # Add minimal noise
                noise = np.random.randint(0, 3, (480, 640, 3), dtype=np.uint8)
                frame = cv2.add(frame, noise)
            frames.append(frame)
        return frames

    @staticmethod
    def generate_r2_looped_feed_stream(num_frames: int = 30) -> List[np.ndarray]:
        """R2: Completely static looped frame with zero pixel variance over time."""
        static_frame = np.full((480, 640, 3), (200, 210, 220), dtype=np.uint8)
        cv2.putText(static_frame, "RECORDED LOOP - OCT 2026", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (40, 40, 40), 2)
        return [static_frame.copy() for _ in range(num_frames)]

    @staticmethod
    def generate_r3_punch_and_leave_dwell_profile() -> List[int]:
        """R3: 25 trainees at start, dropping to 3 trainees after 10 minutes."""
        # 12 windows (each window 5 min)
        return [25, 24, 22, 4, 3, 3, 3, 2, 3, 3, 3, 3]

    @staticmethod
    def generate_clean_session_dwell_profile() -> List[int]:
        """Clean session: steady attendance of 18-20 trainees."""
        return [18, 19, 20, 19, 20, 18, 19, 19, 20, 18, 19, 18]
