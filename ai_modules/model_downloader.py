import os
import urllib.request

MODELS = {
    "face_detection_yunet_2023mar.onnx": "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "face_recognition_sface_2021dec.onnx": "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx"
}

def ensure_models(target_dir=None):
    if target_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_dir = os.path.join(base_dir, "models")
    os.makedirs(target_dir, exist_ok=True)
    
    yunet_path = os.path.join(target_dir, "face_detection_yunet_2023mar.onnx")
    sface_path = os.path.join(target_dir, "face_recognition_sface_2021dec.onnx")

    for model_name, url in MODELS.items():
        path = os.path.join(target_dir, model_name)
        if not os.path.exists(path) or os.path.getsize(path) < 1000:
            print(f"[Drishti AI] Downloading ONNX Model: {model_name}...", flush=True)
            try:
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url, path)
                print(f"[Drishti AI] Saved model to: {path}", flush=True)
            except Exception as e:
                print(f"[Drishti AI Warning] Could not download {model_name}: {e}", flush=True)

    return {
        "yunet": yunet_path,
        "sface": sface_path
    }
