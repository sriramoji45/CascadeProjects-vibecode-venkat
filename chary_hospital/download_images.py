import os
import requests

# List of image URLs from your app.py
image_urls = [
    "https://img.freepik.com/free-photo/doctor-with-stethoscope-hospital_1150-17852.jpg",
    "https://img.freepik.com/free-photo/portrait-young-woman-having-medical-check-up-clinic_1098-2176.jpg",
    "https://img.freepik.com/free-photo/child-doctor-checkup_1098-2099.jpg",
    "https://img.freepik.com/free-photo/elderly-man-medical-exam_1098-2177.jpg",
    "https://img.freepik.com/free-photo/doctor-measuring-blood-pressure-patient_1150-17853.jpg",
    "https://img.freepik.com/free-photo/doctor-checking-heartbeat-patient_1150-17851.jpg",
    "https://images.pexels.com/photos/1170979/pexels-photo-1170979.jpeg?auto=compress&w=400",
    "https://images.pexels.com/photos/3952232/pexels-photo-3952232.jpeg?auto=compress&w=400",
    "https://images.pexels.com/photos/6749774/pexels-photo-6749774.jpeg?auto=compress&w=400",
    "https://images.pexels.com/photos/5327580/pexels-photo-5327580.jpeg?auto=compress&w=400",
    "https://images.pexels.com/photos/8376292/pexels-photo-8376292.jpeg?auto=compress&w=400",
    "https://images.pexels.com/photos/415824/pexels-photo-415824.jpeg?auto=compress&w=400"
]

static_dir = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(static_dir, exist_ok=True)

for idx, url in enumerate(image_urls, start=1):
    ext = url.split('.')[-1].split('?')[0]
    filename = f"img{idx}.{ext}"
    filepath = os.path.join(static_dir, filename)
    print(f"Downloading {url} to {filepath}")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
print("Done.")
