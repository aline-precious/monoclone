#!/usr/bin/env python3
"""
Seed script — creates categories and electronics products via the API.
Run with: /opt/homebrew/bin/python3.12 seed.py
Make sure the server is running first: uvicorn app.main:app --reload
"""
import urllib.request
import urllib.parse
import json

BASE = "http://localhost:8000"

def post(path, data, token=None):
    body = json.dumps(data).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

def get(path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(BASE + path, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def login(email, password):
    data = urllib.parse.urlencode({"username": email, "password": password}).encode()
    req = urllib.request.Request(BASE + "/auth/login", data=data,
          headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["access_token"]

print("🚀 Monoclone Seed Script")
print("=" * 40)

# 1. Create admin user
print("\n1️⃣  Creating admin user...")
r = post("/auth/register", {"name": "Admin", "email": "admin@monoclone.com", "password": "admin123"})
if "id" in r:
    print(f"   ✔ Admin created: admin@monoclone.com / admin123")
else:
    print(f"   ℹ Admin already exists, logging in...")

token = login("admin@monoclone.com", "admin123")
print(f"   ✔ Logged in")

# Make admin an admin in DB (patch directly)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
try:
    from app.db.session import SessionLocal
    from app import models
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == "admin@monoclone.com").first()
    if user:
        user.is_admin = True
        db.commit()
        print("   ✔ Admin privileges granted")
    db.close()
except Exception as e:
    print(f"   ⚠ Could not set admin: {e}")

# Re-login to get fresh token
token = login("admin@monoclone.com", "admin123")

# 2. Create categories
print("\n2️⃣  Creating categories...")
categories = [
    {"name": "Accessories", "description": "Small electronics and accessories"},
    {"name": "Audio", "description": "Headphones, speakers and audio gear"},
    {"name": "Phones", "description": "Smartphones and tablets"},
    {"name": "Computers", "description": "Laptops, desktops and peripherals"},
    {"name": "TV & Display", "description": "Televisions and monitors"},
]
cat_ids = {}
for cat in categories:
    r = post("/products/categories", cat, token)
    if "id" in r:
        cat_ids[cat["name"]] = r["id"]
        print(f"   ✔ {cat['name']}")
    else:
        # Already exists, fetch it
        existing = get("/products/categories")
        for c in existing:
            cat_ids[c["name"]] = c["id"]
        print(f"   ℹ Categories already exist")
        break

# 3. Create products
print("\n3️⃣  Creating products...")
products = [
    # Accessories — small & cheap
    {"name": "USB-C Cable 1m", "description": "Fast charging USB-C cable, 60W, braided nylon", "sku": "ACC-001", "price": 8.99, "stock": 200, "category": "Accessories", "image_url": "https://via.placeholder.com/300"},
    {"name": "Phone Stand", "description": "Adjustable aluminium phone and tablet stand", "sku": "ACC-002", "price": 14.99, "stock": 150, "category": "Accessories", "image_url": ""},
    {"name": "Screen Cleaning Kit", "description": "Microfibre cloth + spray for screens", "sku": "ACC-003", "price": 9.99, "stock": 300, "category": "Accessories", "image_url": ""},
    {"name": "USB Hub 4-Port", "description": "USB 3.0 hub, 4 ports, plug and play", "sku": "ACC-004", "price": 22.99, "stock": 120, "category": "Accessories", "image_url": ""},
    {"name": "Wireless Mouse", "description": "Compact wireless mouse, 12-month battery life", "sku": "ACC-005", "price": 29.99, "stock": 80, "category": "Accessories", "image_url": ""},
    {"name": "Mechanical Keyboard", "description": "TKL mechanical keyboard, blue switches, RGB", "sku": "ACC-006", "price": 79.99, "stock": 45, "category": "Accessories", "image_url": ""},

    # Audio
    {"name": "Earbuds Basic", "description": "Wired earbuds with microphone, 3.5mm jack", "sku": "AUD-001", "price": 12.99, "stock": 200, "category": "Audio", "image_url": ""},
    {"name": "Bluetooth Earbuds", "description": "True wireless earbuds, 24h battery, IPX5", "sku": "AUD-002", "price": 49.99, "stock": 90, "category": "Audio", "image_url": ""},
    {"name": "Portable Bluetooth Speaker", "description": "360° sound, 12h battery, waterproof", "sku": "AUD-003", "price": 69.99, "stock": 60, "category": "Audio", "image_url": ""},
    {"name": "Sony WH-1000XM5", "description": "Industry-leading noise cancelling headphones, 30h battery", "sku": "AUD-004", "price": 279.99, "stock": 25, "category": "Audio", "image_url": ""},
    {"name": "Sonos Era 100", "description": "Premium smart speaker with spatial audio", "sku": "AUD-005", "price": 249.99, "stock": 20, "category": "Audio", "image_url": ""},

    # Phones
    {"name": "Samsung Galaxy A15", "description": "6.5\" display, 50MP camera, 5000mAh battery", "sku": "PHN-001", "price": 189.99, "stock": 50, "category": "Phones", "image_url": ""},
    {"name": "Samsung Galaxy S24", "description": "6.2\" Dynamic AMOLED, Snapdragon 8 Gen 3, 50MP", "sku": "PHN-002", "price": 799.99, "stock": 30, "category": "Phones", "image_url": ""},
    {"name": "iPhone 15", "description": "6.1\" Super Retina XDR, A16 Bionic, 48MP", "sku": "PHN-003", "price": 929.99, "stock": 25, "category": "Phones", "image_url": ""},
    {"name": "iPhone 15 Pro Max", "description": "6.7\" ProMotion, A17 Pro, titanium frame, 4K 60fps", "sku": "PHN-004", "price": 1299.99, "stock": 15, "category": "Phones", "image_url": ""},

    # Computers
    {"name": "Raspberry Pi 5", "description": "Mini computer, 4GB RAM, perfect for projects", "sku": "CMP-001", "price": 69.99, "stock": 40, "category": "Computers", "image_url": ""},
    {"name": "iPad 10th Gen", "description": "10.9\" Liquid Retina, A14 Bionic, 64GB", "sku": "CMP-002", "price": 399.99, "stock": 35, "category": "Computers", "image_url": ""},
    {"name": "MacBook Air M2", "description": "13.6\" Liquid Retina, Apple M2, 8GB RAM, 256GB SSD", "sku": "CMP-003", "price": 1099.99, "stock": 20, "category": "Computers", "image_url": ""},
    {"name": "MacBook Pro M3", "description": "14\" ProMotion XDR, Apple M3 Pro, 18GB RAM, 512GB", "sku": "CMP-004", "price": 1999.99, "stock": 10, "category": "Computers", "image_url": ""},
    {"name": "Dell XPS 15", "description": "15.6\" OLED 4K, Intel i7, 32GB RAM, 1TB SSD, RTX 4060", "sku": "CMP-005", "price": 2299.99, "stock": 8, "category": "Computers", "image_url": ""},
    {"name": "Mac Pro M2 Ultra", "description": "Professional desktop, M2 Ultra, 192GB RAM, 8TB SSD", "sku": "CMP-006", "price": 6999.99, "stock": 3, "category": "Computers", "image_url": ""},

    # TV & Display
    {"name": "Monitor 24\" FHD", "description": "24\" IPS FHD monitor, 75Hz, HDMI+VGA", "sku": "TVD-001", "price": 129.99, "stock": 45, "category": "TV & Display", "image_url": ""},
    {"name": "Monitor 27\" 4K", "description": "27\" IPS 4K UHD, 144Hz, HDR400, USB-C", "sku": "TVD-002", "price": 399.99, "stock": 30, "category": "TV & Display", "image_url": ""},
    {"name": "Samsung 55\" QLED", "description": "55\" QLED 4K, 120Hz, Smart TV, Tizen OS", "sku": "TVD-003", "price": 699.99, "stock": 15, "category": "TV & Display", "image_url": ""},
    {"name": "LG OLED C3 65\"", "description": "65\" OLED evo, 4K 120Hz, Dolby Vision, webOS 23", "sku": "TVD-004", "price": 1499.99, "stock": 8, "category": "TV & Display", "image_url": ""},
    {"name": "Sony Bravia XR 77\"", "description": "77\" QD-OLED, 4K 120Hz, Cognitive Processor XR", "sku": "TVD-005", "price": 2799.99, "stock": 4, "category": "TV & Display", "image_url": ""},
]

created = 0
for p in products:
    cat_id = cat_ids.get(p.pop("category"))
    p["category_id"] = cat_id
    r = post("/products", p, token)
    if "id" in r:
        created += 1
        print(f"   ✔ €{p['price']:>8.2f}  {p['name']}")
    else:
        print(f"   ⚠ Skipped: {p['name']} — {r}")

print(f"\n✅ Done! {created}/{len(products)} products created.")
print(f"\n🌐 Open storefront.html in your browser to see them!")
print(f"👤 Admin login: admin@monoclone.com / admin123")
