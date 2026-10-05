import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from website.models import Product, Service

class Command(BaseCommand):
    help = "Seed initial products and services into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding services...")
        services_data = [
            {
                "title": "WiFi Installation & Networking",
                "description": "High-performance wireless network setup, enterprise cabling, router configurations, and signal boosting for homes and offices.",
                "icon": "fa-wifi",
                "order": 1,
            },
            {
                "title": "IT Accessories Supply",
                "description": "Quality networking cables, routers, switches, connectors, computer peripherals, and smart tech accessories delivered to your door.",
                "icon": "fa-laptop",
                "order": 2,
            },
            {
                "title": "Hardware Maintenance & Repair",
                "description": "Diagnosis, preventive maintenance, component upgrades, and troubleshooting for PCs, servers, and network equipment.",
                "icon": "fa-tools",
                "order": 3,
            },
            {
                "title": "Software & Web Development",
                "description": "Custom business web applications, digital solutions, automation tools, and IT consultation tailored to boost your productivity.",
                "icon": "fa-code",
                "order": 4,
            },
            {
                "title": "Technical Support & Consultation",
                "description": "Round-the-clock remote and on-site IT consultation, network security audits, and reliable tech advisory.",
                "icon": "fa-headset",
                "order": 5,
            },
        ]

        for s in services_data:
            obj, created = Service.objects.get_or_create(
                title=s["title"],
                defaults={"description": s["description"], "icon": s["icon"], "order": s["order"]}
            )
            if created:
                self.stdout.write(f"  + Created service: {obj.title}")
            else:
                self.stdout.write(f"  = Service already exists: {obj.title}")

        self.stdout.write("Seeding products...")
        json_path = settings.BASE_DIR / 'static' / 'assets' / 'products.json'
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                products_data = json.load(f)

            prices = {
                "Tenda AC1200 Router": 3500.00,
                "Tenda Router WE AX300": 4800.00,
                "Tenda Router": 2800.00,
                "CAT6 Ethernet Cable": 1500.00,
                "Cat 6 Ethernet Cable (Alt)": 1800.00,
            }

            for p in products_data:
                name = p.get("name")
                desc = p.get("description", "")
                img_path = p.get("image", "")
                price = prices.get(name, 2500.00)
                category = "Routers" if "router" in name.lower() else "Cables & Networking"

                prod, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        "description": desc,
                        "image_url": img_path,
                        "price": price,
                        "category": category,
                        "in_stock": True,
                        "featured": True,
                    }
                )
                if created:
                    self.stdout.write(f"  + Created product: {prod.name}")
                else:
                    self.stdout.write(f"  = Product already exists: {prod.name}")
        else:
            self.stdout.write(self.style.WARNING(f"Products json not found at {json_path}"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
