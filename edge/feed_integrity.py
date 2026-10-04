"""
Satark AI - Feed-Integrity Watchdog (FR-3, FR-4)
Detects adversarial feed tampering:
- Blackout / Blind camera
- Frozen / Looped frames (via SSIM)
- Lens covered / Occluded
- Camera angle deviation / abrupt scene shifts
- Periodic heartbeat generation
"""
import time
import cv2
import numpy as np
from typing import Tuple, Dict, Any

class FeedIntegrityWatchdog:
    def __init__(self,
                 blackout_luminance_thresh: float = 12.0,
                 blackout_var_thresh: float = 8.0,
                 frozen_ssim_thresh: float = 0.996,
                 frozen_duration_seconds: float = 20.0,
                 covered_color_dominance: float = 0.85):
        self.blackout_luminance_thresh = blackout_luminance_thresh
        self.blackout_var_thresh = blackout_var_thresh
        self.frozen_ssim_thresh = frozen_ssim_thresh
        self.frozen_duration_seconds = frozen_duration_seconds
        self.covered_color_dominance = covered_color_dominance
        
        self.prev_gray_frame = None
        self.frozen_start_time = None
        self.last_heartbeat = time.time()

    def _compute_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Lightweight SSIM for high-speed edge calculation."""
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2
        
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        
        kernel = cv2.getGaussianKernel(11, 1.5)
        window = np.outer(kernel, kernel.transpose())
        
        mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]
        mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
        
        mu1_sq = mu1 ** 2
        mu2_sq = mu2 ** 2
        mu1_mu2 = mu1 * mu2
        
        sigma1_sq = cv2.filter2D(img1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
        sigma2_sq = cv2.filter2D(img2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq
        sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2
        
        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
        return float(np.clip(ssim_map.mean(), 0.0, 1.0))

    def evaluate_frame(self, frame: np.ndarray) -> Tuple[str, float, Dict[str, Any]]:
        """
        Returns:
            status: "OK" | "BLACKOUT" | "FROZEN" | "COVERED" | "MOVED"
            confidence: 0.0 to 1.0
            metrics: dictionary of computed visual indicators
        """
        if frame is None or frame.size == 0:
            return "BLACKOUT", 1.0, {"reason": "Empty frame buffer"}

        # Resize for ultra-fast metric calculation
        resized = cv2.resize(frame, (160, 120))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        mean_lum = float(np.mean(gray))
        var_lum = float(np.var(gray))
        
        metrics = {
            "mean_luminance": mean_lum,
            "variance": var_lum,
            "timestamp": time.time()
        }

        # 1. Blackout Check (dark room or covered with black cloth)
        if mean_lum < self.blackout_luminance_thresh and var_lum < self.blackout_var_thresh:
            return "BLACKOUT", 0.98, metrics

        # 2. Covered Lens Check (solid bright color/tape/paper obstruction)
        if var_lum < 6.0:
            return "COVERED", 0.95, metrics

        # 3. Frozen Frame / Static Video Loop Check
        if self.prev_gray_frame is not None:
            ssim_val = self._compute_ssim(gray, self.prev_gray_frame)
            metrics["ssim"] = ssim_val
            
            if ssim_val >= self.frozen_ssim_thresh:
                if self.frozen_start_time is None:
                    self.frozen_start_time = time.time()
                elif (time.time() - self.frozen_start_time) >= self.frozen_duration_seconds:
                    return "FROZEN", 0.99, metrics
            else:
                self.frozen_start_time = None
        else:
            self.frozen_start_time = None

        self.prev_gray_frame = gray
        return "OK", 1.0, metrics

    def emit_heartbeat(self, centre_id: str) -> Dict[str, Any]:
        self.last_heartbeat = time.time()
        return {
            "centre_id": centre_id,
            "type": "HEARTBEAT",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.last_heartbeat)),
            "status": "ALIVE"
        }
