import random
from datetime import timedelta, date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from vehicles.models import Vehicle, VehicleOption
from customers.models import Customer
from reservations.models import Reservation, ReservationOption
from maintenance.models import Maintenance
from payments.models import Payment, Deposit
from invoices.models import Invoice
from core.models import Alert


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        self._create_users()
        vehicles = self._create_vehicles()
        options = self._create_options()
        customers = self._create_customers()
        self._create_reservations(vehicles, customers, options)
        self._create_maintenance(vehicles)
        self._create_payments_and_invoices()
        self._create_deposits()

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _create_users(self):
        if User.objects.filter(username='employee1').exists():
            return
        admin = User.objects.get(username='admin')
        Profile.objects.get_or_create(user=admin, role='admin')

        for i in range(1, 4):
            u = User.objects.create_user(
                username=f'employee{i}',
                email=f'employee{i}@atlas.com',
                password='pass1234',
                first_name=random.choice(['Youssef', 'Fatima', 'Mohammed', 'Amina', 'Omar']),
                last_name=random.choice(['Alami', 'Benjelloun', 'Tazi', 'Idrissi', 'Chakir']),
            )
            Profile.objects.create(user=u, role='employee')
        self.stdout.write('  Created users')

    def _create_vehicles(self):
        if Vehicle.objects.exists():
            return list(Vehicle.objects.all())

        brands_models = [
            ('Renault', 'Clio', 'sedan'), ('Renault', 'Captur', 'suv'),
            ('Peugeot', '208', 'city'), ('Peugeot', '3008', 'suv'),
            ('Dacia', 'Logan', 'city'), ('Dacia', 'Duster', 'suv'),
            ('Toyota', 'Yaris', 'city'), ('Toyota', 'Corolla', 'sedan'),
            ('Hyundai', 'Tucson', 'suv'), ('Hyundai', 'i20', 'city'),
            ('Mercedes', 'Classe C', 'luxury'), ('BMW', 'Serie 3', 'luxury'),
            ('Volkswagen', 'Golf', 'sedan'), ('Ford', 'Ranger', 'utility'),
            ('Kia', 'Sportage', 'suv'), ('Nissan', 'Qashqai', 'suv'),
            ('Opel', 'Corsa', 'city'), ('Fiat', '500', 'city'),
            ('Mazda', 'CX-5', 'suv'), ('Citroen', 'C3', 'city'),
        ]
        colors = ['White', 'Black', 'Silver', 'Blue', 'Red', 'Grey', 'Grey']
        statuses = ['available'] * 14 + ['rented'] * 4 + ['maintenance'] * 2

        vehicles = []
        for i, (brand, model, cat) in enumerate(brands_models):
            v = Vehicle.objects.create(
                license_plate=f'{random.randint(1,99)}-{chr(random.randint(65,90))}{chr(random.randint(65,90))}-{random.randint(10000,99999)}',
                brand=brand,
                model=model,
                year=random.randint(2019, 2025),
                color=random.choice(colors),
                category=cat,
                transmission=random.choice(['manual', 'automatic']),
                seats=random.choice([4, 5, 7]),
                mileage=random.randint(5000, 80000),
                last_revision=date.today() - timedelta(days=random.randint(10, 300)),
                daily_price=Decimal(str(random.choice([250, 300, 350, 400, 450, 500, 600, 800, 1000, 1200]))),
                deposit=Decimal(str(random.choice([1000, 1500, 2000, 3000, 5000]))),
                status=statuses[i],
                maintenance_threshold=random.choice([10000, 15000, 20000]),
            )
            vehicles.append(v)
        self.stdout.write(f'  Created {len(vehicles)} vehicles')
        return vehicles

    def _create_options(self):
        if VehicleOption.objects.exists():
            return list(VehicleOption.objects.all())
        opts = [
            VehicleOption.objects.create(name='GPS', daily_price=Decimal('30')),
            VehicleOption.objects.create(name='Baby Seat', daily_price=Decimal('25')),
            VehicleOption.objects.create(name='Additional Driver', daily_price=Decimal('40')),
            VehicleOption.objects.create(name='WiFi Hotspot', daily_price=Decimal('20')),
            VehicleOption.objects.create(name='Full Insurance', daily_price=Decimal('50')),
        ]
        self.stdout.write(f'  Created {len(opts)} vehicle options')
        return opts

    def _create_customers(self):
        if Customer.objects.exists():
            return list(Customer.objects.all())

        first_names_m = ['Ahmed', 'Mohammed', 'Youssef', 'Omar', 'Khalid', 'Rachid', 'Hamza', 'Said', 'Nabil', 'Tarik']
        first_names_f = ['Fatima', 'Amina', 'Khadija', 'Salma', 'Nora', 'Sara', 'Hajar', 'Imane']
        last_names = ['Alami', 'Benjelloun', 'Tazi', 'Idrissi', 'Chakir', 'Bouzid', 'El Fassi', 'Mouline', 'Bennani', 'Kabbaj', 'Ait Brahim', 'Ouazzani']
        nationalities = ['Moroccan', 'French', 'Spanish', 'German', 'British', 'American', 'Italian', 'Dutch']

        customers = []
        for i in range(12):
            fn = random.choice(first_names_m + first_names_f)
            ln = random.choice(last_names)
            birth = date.today() - timedelta(days=random.randint(7000, 20000))
            c = Customer.objects.create(
                cin=f'BE{random.randint(100000, 999999)}',
                passport=f'PA{random.randint(1000000, 9999999)}' if random.random() > 0.5 else None,
                first_name=fn,
                last_name=ln,
                nationality=random.choice(nationalities),
                birth_date=birth,
                license_number=f'FR-{random.randint(100000, 999999)}',
                license_expiration=date.today() + timedelta(days=random.choice([-30, 60, 120, 200, 365, 500])),
                phone=f'06{random.randint(10000000, 99999999)}',
                email=f'{fn.lower()}.{ln.lower()}@email.com',
                address=f'{random.randint(1,200)} Rue {random.choice(["Mohammed V", "Hassan II", "Fès", "Marrakech", "Rabat"])}, Casablanca',
                customer_type=random.choice(['individual', 'individual', 'individual', 'company', 'partner_agency']),
            )
            customers.append(c)
        self.stdout.write(f'  Created {len(customers)} customers')
        return customers

    def _create_reservations(self, vehicles, customers, options):
        if Reservation.objects.exists():
            return

        available_vehicles = [v for v in vehicles if v.status in ['available', 'rented']]
        statuses = ['completed'] * 5 + ['active'] * 3 + ['confirmed'] * 2 + ['pending'] * 2 + ['cancelled'] * 1

        for i, status in enumerate(statuses):
            vehicle = random.choice(available_vehicles)
            customer = random.choice(customers)
            start = date.today() - timedelta(days=random.randint(0, 30))
            duration = random.randint(2, 14)
            end = start + timedelta(days=duration)

            if status == 'active':
                start = date.today() - timedelta(days=random.randint(1, 3))
                end = date.today() + timedelta(days=random.randint(1, 5))
            elif status == 'confirmed':
                start = date.today() + timedelta(days=random.randint(1, 7))
                end = start + timedelta(days=duration)
            elif status == 'pending':
                start = date.today() + timedelta(days=random.randint(3, 14))
                end = start + timedelta(days=duration)

            res = Reservation(
                customer=customer,
                vehicle=vehicle,
                pickup_date=start,
                return_date=end,
                pickup_location=random.choice(['agency', 'airport', 'hotel_delivery']),
                return_location=random.choice(['agency', 'airport', 'hotel_delivery']),
                status=status,
            )
            res.save()

            num_options = random.randint(0, 2)
            chosen = random.sample(options, min(num_options, len(options)))
            for opt in chosen:
                ReservationOption.objects.create(
                    reservation=res,
                    option=opt,
                    quantity=1,
                )

            res.calculate_totals()

        self.stdout.write(f'  Created {Reservation.objects.count()} reservations')

    def _create_maintenance(self, vehicles):
        if Maintenance.objects.exists():
            return
        types = ['oil_change', 'tire_change', 'brake_service', 'revision', 'engine_repair']
        garages = ['AutoGarage Casa', 'MecaPro Rabat', 'SpeedFix Marrakech', 'Garage Atlas']
        count = 0
        for v in vehicles[:8]:
            for _ in range(random.randint(1, 3)):
                d = date.today() - timedelta(days=random.randint(30, 365))
                Maintenance.objects.create(
                    vehicle=v,
                    maintenance_type=random.choice(types),
                    garage=random.choice(garages),
                    date=d,
                    mileage=v.mileage - random.randint(0, 5000),
                    cost=Decimal(str(random.randint(150, 3000))),
                    notes=random.choice(['', 'Regular service', 'Urgent repair', 'Scheduled maintenance']),
                )
                count += 1
        self.stdout.write(f'  Created {count} maintenance records')

    def _create_payments_and_invoices(self):
        if Payment.objects.exists():
            return
        completed = Reservation.objects.filter(status__in=['completed', 'active', 'confirmed'])
        for res in completed[:8]:
            Payment.objects.create(
                reservation=res,
                method=random.choice(['cash', 'bank_transfer', 'credit_card', 'cheque']),
                amount=res.total * Decimal(str(random.uniform(0.5, 1.0))).quantize(Decimal('0.01')),
                reference=f'REF-{random.randint(100000, 999999)}',
            )
        self.stdout.write(f'  Created {Payment.objects.count()} payments')

        for res in completed[:6]:
            if not Invoice.objects.filter(reservation=res).exists():
                Invoice.objects.create(
                    reservation=res,
                    subtotal=res.subtotal,
                    vat=res.vat,
                    total=res.total,
                )
        self.stdout.write(f'  Created {Invoice.objects.count()} invoices')

    def _create_deposits(self):
        if Deposit.objects.exists():
            return
        for res in Reservation.objects.filter(status__in=['completed', 'active'])[:5]:
            Deposit.objects.create(
                reservation=res,
                amount_received=res.deposit,
                amount_returned=res.deposit if res.status == 'completed' else 0,
                return_date=res.return_date if res.status == 'completed' else None,
                notes='',
            )
        self.stdout.write(f'  Created {Deposit.objects.count()} deposits')
