import graphene
from database import get_connection


class ZoneType(graphene.ObjectType):
    id = graphene.Int(required=True)
    name = graphene.String(required=True)
    area_code = graphene.String(required=True)
    schedules = graphene.List(lambda: CollectionScheduleType, required=True)
    complaints = graphene.List(lambda: ComplaintType, required=True)

    def resolve_schedules(self, info):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM collection_schedules WHERE zone_id = ? ORDER BY id", (self.id,)
        ).fetchall()
        conn.close()
        return [
            CollectionScheduleType(
                id=r["id"], zone_id=r["zone_id"], vehicle_id=r["vehicle_id"],
                date=r["date"], status=r["status"]
            ) for r in rows
        ]

    def resolve_complaints(self, info):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM complaints WHERE zone_id = ? ORDER BY id", (self.id,)
        ).fetchall()
        conn.close()
        return [
            ComplaintType(
                id=r["id"], zone_id=r["zone_id"], description=r["description"],
                status=r["status"], created_at=r["created_at"]
            ) for r in rows
        ]


class VehicleType(graphene.ObjectType):
    id = graphene.Int(required=True)
    registration_number = graphene.String(required=True)
    capacity = graphene.Float(required=True)
    status = graphene.String(required=True)
    disposal_logs = graphene.List(lambda: DisposalLogType, required=True)

    def resolve_disposal_logs(self, info):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM disposal_logs WHERE vehicle_id = ? ORDER BY id", (self.id,)
        ).fetchall()
        conn.close()
        return [
            DisposalLogType(
                id=r["id"], vehicle_id=r["vehicle_id"],
                waste_quantity=r["waste_quantity"], date=r["date"]
            ) for r in rows
        ]


class DriverType(graphene.ObjectType):
    id = graphene.Int(required=True)
    name = graphene.String(required=True)
    phone = graphene.String(required=True)


class CollectionScheduleType(graphene.ObjectType):
    id = graphene.Int(required=True)
    zone_id = graphene.Int(required=True)
    vehicle_id = graphene.Int(required=True)
    date = graphene.String(required=True)
    status = graphene.String(required=True)
    zone = graphene.Field(ZoneType)
    vehicle = graphene.Field(VehicleType)

    def resolve_zone(self, info):
        conn = get_connection()
        r = conn.execute("SELECT * FROM zones WHERE id = ?", (self.zone_id,)).fetchone()
        conn.close()
        if r:
            return ZoneType(id=r["id"], name=r["name"], area_code=r["area_code"])
        return None

    def resolve_vehicle(self, info):
        conn = get_connection()
        r = conn.execute("SELECT * FROM vehicles WHERE id = ?", (self.vehicle_id,)).fetchone()
        conn.close()
        if r:
            return VehicleType(
                id=r["id"], registration_number=r["registration_number"],
                capacity=r["capacity"], status=r["status"]
            )
        return None


class ComplaintType(graphene.ObjectType):
    id = graphene.Int(required=True)
    zone_id = graphene.Int(required=True)
    description = graphene.String(required=True)
    status = graphene.String(required=True)
    created_at = graphene.String()
    zone = graphene.Field(ZoneType)

    def resolve_zone(self, info):
        conn = get_connection()
        r = conn.execute("SELECT * FROM zones WHERE id = ?", (self.zone_id,)).fetchone()
        conn.close()
        if r:
            return ZoneType(id=r["id"], name=r["name"], area_code=r["area_code"])
        return None


class DisposalLogType(graphene.ObjectType):
    id = graphene.Int(required=True)
    vehicle_id = graphene.Int(required=True)
    waste_quantity = graphene.Float(required=True)
    date = graphene.String(required=True)
    vehicle = graphene.Field(VehicleType)

    def resolve_vehicle(self, info):
        conn = get_connection()
        r = conn.execute("SELECT * FROM vehicles WHERE id = ?", (self.vehicle_id,)).fetchone()
        conn.close()
        if r:
            return VehicleType(
                id=r["id"], registration_number=r["registration_number"],
                capacity=r["capacity"], status=r["status"]
            )
        return None


class CreateScheduleInput(graphene.InputObjectType):
    zone_id = graphene.Int(required=True)
    vehicle_id = graphene.Int(required=True)
    date = graphene.String(required=True)


class CreateComplaintInput(graphene.InputObjectType):
    zone_id = graphene.Int(required=True)
    description = graphene.String(required=True)


class CreateDisposalLogInput(graphene.InputObjectType):
    vehicle_id = graphene.Int(required=True)
    waste_quantity = graphene.Float(required=True)
    date = graphene.String(required=True)


class Query(graphene.ObjectType):
    zones = graphene.List(ZoneType)
    zone = graphene.Field(ZoneType, id=graphene.Int(required=True))
    vehicles = graphene.List(VehicleType)
    vehicle = graphene.Field(VehicleType, id=graphene.Int(required=True))
    drivers = graphene.List(DriverType)
    driver = graphene.Field(DriverType, id=graphene.Int(required=True))
    schedules = graphene.List(CollectionScheduleType, status=graphene.String())
    schedule = graphene.Field(CollectionScheduleType, id=graphene.Int(required=True))
    complaints = graphene.List(ComplaintType, status=graphene.String())
    complaint = graphene.Field(ComplaintType, id=graphene.Int(required=True))
    disposal_logs = graphene.List(DisposalLogType, vehicle_id=graphene.Int())

    def resolve_zones(self, info):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM zones ORDER BY id").fetchall()
        conn.close()
        return [ZoneType(id=r["id"], name=r["name"], area_code=r["area_code"]) for r in rows]

    def resolve_zone(self, info, id):
        conn = get_connection()
        r = conn.execute("SELECT * FROM zones WHERE id = ?", (id,)).fetchone()
        conn.close()
        if r:
            return ZoneType(id=r["id"], name=r["name"], area_code=r["area_code"])
        return None

    def resolve_vehicles(self, info):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM vehicles ORDER BY id").fetchall()
        conn.close()
        return [
            VehicleType(
                id=r["id"], registration_number=r["registration_number"],
                capacity=r["capacity"], status=r["status"]
            ) for r in rows
        ]

    def resolve_vehicle(self, info, id):
        conn = get_connection()
        r = conn.execute("SELECT * FROM vehicles WHERE id = ?", (id,)).fetchone()
        conn.close()
        if r:
            return VehicleType(
                id=r["id"], registration_number=r["registration_number"],
                capacity=r["capacity"], status=r["status"]
            )
        return None

    def resolve_drivers(self, info):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM drivers ORDER BY id").fetchall()
        conn.close()
        return [DriverType(id=r["id"], name=r["name"], phone=r["phone"]) for r in rows]

    def resolve_driver(self, info, id):
        conn = get_connection()
        r = conn.execute("SELECT * FROM drivers WHERE id = ?", (id,)).fetchone()
        conn.close()
        if r:
            return DriverType(id=r["id"], name=r["name"], phone=r["phone"])
        return None

    def resolve_schedules(self, info, status=None):
        conn = get_connection()
        if status:
            rows = conn.execute(
                "SELECT * FROM collection_schedules WHERE status = ? ORDER BY id", (status,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM collection_schedules ORDER BY id").fetchall()
        conn.close()
        return [
            CollectionScheduleType(
                id=r["id"], zone_id=r["zone_id"], vehicle_id=r["vehicle_id"],
                date=r["date"], status=r["status"]
            ) for r in rows
        ]

    def resolve_schedule(self, info, id):
        conn = get_connection()
        r = conn.execute("SELECT * FROM collection_schedules WHERE id = ?", (id,)).fetchone()
        conn.close()
        if r:
            return CollectionScheduleType(
                id=r["id"], zone_id=r["zone_id"], vehicle_id=r["vehicle_id"],
                date=r["date"], status=r["status"]
            )
        return None

    def resolve_complaints(self, info, status=None):
        conn = get_connection()
        if status:
            rows = conn.execute(
                "SELECT * FROM complaints WHERE status = ? ORDER BY id", (status,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM complaints ORDER BY id").fetchall()
        conn.close()
        return [
            ComplaintType(
                id=r["id"], zone_id=r["zone_id"], description=r["description"],
                status=r["status"], created_at=r["created_at"]
            ) for r in rows
        ]

    def resolve_complaint(self, info, id):
        conn = get_connection()
        r = conn.execute("SELECT * FROM complaints WHERE id = ?", (id,)).fetchone()
        conn.close()
        if r:
            return ComplaintType(
                id=r["id"], zone_id=r["zone_id"], description=r["description"],
                status=r["status"], created_at=r["created_at"]
            )
        return None

    def resolve_disposal_logs(self, info, vehicle_id=None):
        conn = get_connection()
        if vehicle_id:
            rows = conn.execute(
                "SELECT * FROM disposal_logs WHERE vehicle_id = ? ORDER BY id", (vehicle_id,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM disposal_logs ORDER BY id").fetchall()
        conn.close()
        return [
            DisposalLogType(
                id=r["id"], vehicle_id=r["vehicle_id"],
                waste_quantity=r["waste_quantity"], date=r["date"]
            ) for r in rows
        ]


class CreateSchedule(graphene.Mutation):
    class Arguments:
        input = CreateScheduleInput(required=True)

    collection_schedule = graphene.Field(CollectionScheduleType)

    def mutate(self, info, input):
        conn = get_connection()

        zone = conn.execute("SELECT * FROM zones WHERE id = ?", (input.zone_id,)).fetchone()
        if not zone:
            conn.close()
            raise Exception("Zone not found")

        vehicle = conn.execute("SELECT * FROM vehicles WHERE id = ?", (input.vehicle_id,)).fetchone()
        if not vehicle:
            conn.close()
            raise Exception("Vehicle not found")
        if vehicle["status"] != "available":
            conn.close()
            raise Exception(f"Vehicle is not available (current status: {vehicle['status']})")

        cursor = conn.execute(
            "INSERT INTO collection_schedules (zone_id, vehicle_id, date, status) VALUES (?, ?, ?, 'planned')",
            (input.zone_id, input.vehicle_id, input.date)
        )
        schedule_id = cursor.lastrowid

        conn.execute("UPDATE vehicles SET status = 'assigned' WHERE id = ?", (input.vehicle_id,))
        conn.commit()

        r = conn.execute("SELECT * FROM collection_schedules WHERE id = ?", (schedule_id,)).fetchone()
        conn.close()

        return CreateSchedule(
            collection_schedule=CollectionScheduleType(
                id=r["id"], zone_id=r["zone_id"], vehicle_id=r["vehicle_id"],
                date=r["date"], status=r["status"]
            )
        )


class UpdateScheduleStatus(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        status = graphene.String(required=True)

    collection_schedule = graphene.Field(CollectionScheduleType)

    def mutate(self, info, id, status):
        valid_statuses = ["planned", "completed"]
        if status not in valid_statuses:
            raise Exception(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        conn = get_connection()
        schedule = conn.execute("SELECT * FROM collection_schedules WHERE id = ?", (id,)).fetchone()
        if not schedule:
            conn.close()
            raise Exception("Schedule not found")

        conn.execute("UPDATE collection_schedules SET status = ? WHERE id = ?", (status, id))

        if status == "completed":
            conn.execute("UPDATE vehicles SET status = 'available' WHERE id = ?", (schedule["vehicle_id"],))

        conn.commit()

        r = conn.execute("SELECT * FROM collection_schedules WHERE id = ?", (id,)).fetchone()
        conn.close()

        return UpdateScheduleStatus(
            collection_schedule=CollectionScheduleType(
                id=r["id"], zone_id=r["zone_id"], vehicle_id=r["vehicle_id"],
                date=r["date"], status=r["status"]
            )
        )


class CreateComplaint(graphene.Mutation):
    class Arguments:
        input = CreateComplaintInput(required=True)

    complaint = graphene.Field(ComplaintType)

    def mutate(self, info, input):
        conn = get_connection()

        zone = conn.execute("SELECT * FROM zones WHERE id = ?", (input.zone_id,)).fetchone()
        if not zone:
            conn.close()
            raise Exception("Zone not found")

        cursor = conn.execute(
            "INSERT INTO complaints (zone_id, description) VALUES (?, ?)",
            (input.zone_id, input.description)
        )
        conn.commit()

        r = conn.execute("SELECT * FROM complaints WHERE id = ?", (cursor.lastrowid,)).fetchone()
        conn.close()

        return CreateComplaint(
            complaint=ComplaintType(
                id=r["id"], zone_id=r["zone_id"], description=r["description"],
                status=r["status"], created_at=r["created_at"]
            )
        )


class ResolveComplaint(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    complaint = graphene.Field(ComplaintType)

    def mutate(self, info, id):
        conn = get_connection()

        complaint = conn.execute("SELECT * FROM complaints WHERE id = ?", (id,)).fetchone()
        if not complaint:
            conn.close()
            raise Exception("Complaint not found")
        if complaint["status"] == "resolved":
            conn.close()
            raise Exception("Complaint is already resolved")

        conn.execute("UPDATE complaints SET status = 'resolved' WHERE id = ?", (id,))
        conn.commit()

        r = conn.execute("SELECT * FROM complaints WHERE id = ?", (id,)).fetchone()
        conn.close()

        return ResolveComplaint(
            complaint=ComplaintType(
                id=r["id"], zone_id=r["zone_id"], description=r["description"],
                status=r["status"], created_at=r["created_at"]
            )
        )


class CreateDisposalLog(graphene.Mutation):
    class Arguments:
        input = CreateDisposalLogInput(required=True)

    disposal_log = graphene.Field(DisposalLogType)

    def mutate(self, info, input):
        conn = get_connection()

        vehicle = conn.execute("SELECT * FROM vehicles WHERE id = ?", (input.vehicle_id,)).fetchone()
        if not vehicle:
            conn.close()
            raise Exception("Vehicle not found")

        if input.waste_quantity <= 0:
            conn.close()
            raise Exception("Waste quantity must be greater than 0")

        if input.waste_quantity > vehicle["capacity"]:
            conn.close()
            raise Exception(
                f"Waste quantity ({input.waste_quantity}) exceeds vehicle capacity ({vehicle['capacity']})"
            )

        cursor = conn.execute(
            "INSERT INTO disposal_logs (vehicle_id, waste_quantity, date) VALUES (?, ?, ?)",
            (input.vehicle_id, input.waste_quantity, input.date)
        )
        conn.commit()

        r = conn.execute("SELECT * FROM disposal_logs WHERE id = ?", (cursor.lastrowid,)).fetchone()
        conn.close()

        return CreateDisposalLog(
            disposal_log=DisposalLogType(
                id=r["id"], vehicle_id=r["vehicle_id"],
                waste_quantity=r["waste_quantity"], date=r["date"]
            )
        )


class UpdateVehicleStatus(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        status = graphene.String(required=True)

    vehicle = graphene.Field(VehicleType)

    def mutate(self, info, id, status):
        valid_statuses = ["available", "assigned", "maintenance"]
        if status not in valid_statuses:
            raise Exception(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        conn = get_connection()
        vehicle = conn.execute("SELECT * FROM vehicles WHERE id = ?", (id,)).fetchone()
        if not vehicle:
            conn.close()
            raise Exception("Vehicle not found")

        conn.execute("UPDATE vehicles SET status = ? WHERE id = ?", (status, id))
        conn.commit()

        r = conn.execute("SELECT * FROM vehicles WHERE id = ?", (id,)).fetchone()
        conn.close()

        return UpdateVehicleStatus(
            vehicle=VehicleType(
                id=r["id"], registration_number=r["registration_number"],
                capacity=r["capacity"], status=r["status"]
            )
        )


class Mutation(graphene.ObjectType):
    create_schedule = CreateSchedule.Field()
    update_schedule_status = UpdateScheduleStatus.Field()
    create_complaint = CreateComplaint.Field()
    resolve_complaint = ResolveComplaint.Field()
    create_disposal_log = CreateDisposalLog.Field()
    update_vehicle_status = UpdateVehicleStatus.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
