# Smart Waste Management System - GraphQL API

A GraphQL API to manage waste collection zones, vehicles, schedules, and complaints built with Flask, Graphene, and SQLite.

## Tech Stack

- **Python 3** with **Flask** (web framework)
- **Graphene** (GraphQL library)
- **SQLite** (database)
- **GraphiQL** (interactive query interface)

## Database Models

| Model | Fields |
|-------|--------|
| **Zone** | id, name, area_code |
| **Vehicle** | id, registration_number, capacity, status |
| **Driver** | id, name, phone |
| **CollectionSchedule** | id, zone_id, vehicle_id, date, status |
| **Complaint** | id, zone_id, description, status, created_at |
| **DisposalLog** | id, vehicle_id, waste_quantity, date |

## Setup & Run

```bash
pip install -r requirements.txt
python seed.py
python app.py
```

Open **http://localhost:4000/graphql** in your browser to access GraphiQL.

## Sample Queries

### Get all zones
```graphql
{
  zones {
    id
    name
    areaCode
  }
}
```

### Get all vehicles
```graphql
{
  vehicles {
    id
    registrationNumber
    capacity
    status
  }
}
```

### Get open complaints
```graphql
{
  complaints(status: "open") {
    id
    description
    zone { name }
    createdAt
  }
}
```

## Sample Mutations

### Create a collection schedule
```graphql
mutation {
  createSchedule(input: {
    zoneId: 1
    vehicleId: 2
    date: "2026-08-01"
  }) {
    collectionSchedule { id status }
  }
}
```

### File a complaint
```graphql
mutation {
  createComplaint(input: {
    zoneId: 2
    description: "Bins not emptied since Monday"
  }) {
    complaint { id status createdAt }
  }
}
```

### Resolve a complaint
```graphql
mutation {
  resolveComplaint(id: 1) {
    complaint { id status }
  }
}
```

### Log waste disposal
```graphql
mutation {
  createDisposalLog(input: {
    vehicleId: 1
    wasteQuantity: 3000.0
    date: "2026-08-01"
  }) {
    disposalLog { id wasteQuantity }
  }
}
```

## Business Rules

- **Vehicle status**: available, assigned, maintenance
- **Schedule status**: planned, completed
- **Complaint status**: open, resolved
- Cannot assign a vehicle that is not `available`
- Waste quantity in disposal logs cannot exceed vehicle capacity
- Completing a schedule automatically releases the vehicle
