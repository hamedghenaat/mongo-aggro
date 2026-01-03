# Real-World Use Cases

This page demonstrates real-world aggregation pipelines for common business scenarios.

## E-Commerce Analytics

### Sales Dashboard

```python
from mongo_aggro import (
    Pipeline, Match, Unwind, Group, Sort, Limit, Project,
    Sum, Avg, Max, Min, Count_, merge_accumulators
)

def get_sales_dashboard(start_date: str, end_date: str):
    """Get sales metrics for a date range."""
    return Pipeline([
        Match(query={
            "orderDate": {"$gte": start_date, "$lte": end_date},
            "status": {"$in": ["completed", "shipped"]},
        }),
        Unwind(path="items"),
        Group(
            id="$items.productId",
            accumulators=merge_accumulators(
                Sum(name="totalRevenue", field="items.subtotal"),
                Sum(name="unitsSold", field="items.quantity"),
                Avg(name="avgPrice", field="items.price"),
                Count_(name="orderCount"),
            )
        ),
        Sort(fields={"totalRevenue": -1}),
        Limit(count=20),
        Project(fields={
            "_id": 0,
            "productId": "$_id",
            "totalRevenue": {"$round": ["$totalRevenue", 2]},
            "unitsSold": 1,
            "avgPrice": {"$round": ["$avgPrice", 2]},
            "orderCount": 1,
        }),
    ])
```

### Customer Lifetime Value

```python
from mongo_aggro import Pipeline, Match, Group, Sort, Project, Sum, Avg

def calculate_customer_ltv():
    """Calculate customer lifetime value."""
    return Pipeline([
        Match(query={"status": "completed"}),
        Group(
            id="$customerId",
            accumulators={
                "totalSpent": {"$sum": "$total"},
                "orderCount": {"$sum": 1},
                "avgOrderValue": {"$avg": "$total"},
                "firstOrder": {"$min": "$orderDate"},
                "lastOrder": {"$max": "$orderDate"},
            }
        ),
        Project(fields={
            "_id": 0,
            "customerId": "$_id",
            "totalSpent": {"$round": ["$totalSpent", 2]},
            "orderCount": 1,
            "avgOrderValue": {"$round": ["$avgOrderValue", 2]},
            "customerSince": "$firstOrder",
            "lastActive": "$lastOrder",
            "daysSinceFirstOrder": {
                "$divide": [
                    {"$subtract": ["$$NOW", "$firstOrder"]},
                    86400000  # ms per day
                ]
            },
        }),
        Sort(fields={"totalSpent": -1}),
    ])
```

### Cart Abandonment Analysis

```python
from mongo_aggro import Pipeline, Match, Lookup, Group, Project

def analyze_cart_abandonment():
    """Analyze abandoned carts."""
    return Pipeline([
        Match(query={
            "status": "abandoned",
            "createdAt": {"$gte": "2024-01-01"},
        }),
        Lookup(
            from_collection="users",
            local_field="userId",
            foreign_field="_id",
            as_field="user"
        ),
        Unwind(path="user"),
        Group(
            id={
                "reason": "$abandonmentReason",
                "userType": "$user.type",
            },
            accumulators={
                "count": {"$sum": 1},
                "avgCartValue": {"$avg": "$cartTotal"},
                "totalLostRevenue": {"$sum": "$cartTotal"},
            }
        ),
        Project(fields={
            "_id": 0,
            "reason": "$_id.reason",
            "userType": "$_id.userType",
            "count": 1,
            "avgCartValue": {"$round": ["$avgCartValue", 2]},
            "totalLostRevenue": {"$round": ["$totalLostRevenue", 2]},
        }),
        Sort(fields={"totalLostRevenue": -1}),
    ])
```

## User Analytics

### User Engagement Metrics

```python
from mongo_aggro import (
    Pipeline, Match, Group, Sort, Project, Facet, Count
)

def get_user_engagement(date: str):
    """Get daily user engagement metrics."""
    return Pipeline([
        Match(query={"date": date}),
        Facet(pipelines={
            "byActivity": Pipeline([
                Group(
                    id="$activityType",
                    accumulators={
                        "count": {"$sum": 1},
                        "uniqueUsers": {"$addToSet": "$userId"},
                    }
                ),
                Project(fields={
                    "activity": "$_id",
                    "count": 1,
                    "uniqueUsers": {"$size": "$uniqueUsers"},
                }),
            ]),
            "byHour": Pipeline([
                Group(
                    id={"$hour": "$timestamp"},
                    accumulators={"count": {"$sum": 1}}
                ),
                Sort(fields={"_id": 1}),
            ]),
            "topUsers": Pipeline([
                Group(
                    id="$userId",
                    accumulators={"activityCount": {"$sum": 1}}
                ),
                Sort(fields={"activityCount": -1}),
                Limit(count=10),
            ]),
        }),
    ])
```

### Cohort Retention Analysis

```python
from mongo_aggro import Pipeline, Match, AddFields, Group, Sort

def cohort_retention(cohort_month: str):
    """Analyze retention for a signup cohort."""
    return Pipeline([
        Match(query={
            "signupMonth": cohort_month,
        }),
        Lookup(
            from_collection="activities",
            local_field="_id",
            foreign_field="userId",
            as_field="activities"
        ),
        Unwind(path="activities", preserve_null_and_empty=True),
        AddFields(fields={
            "monthsSinceSignup": {
                "$dateDiff": {
                    "startDate": "$signupDate",
                    "endDate": "$activities.date",
                    "unit": "month"
                }
            }
        }),
        Group(
            id="$monthsSinceSignup",
            accumulators={
                "activeUsers": {"$addToSet": "$_id"},
            }
        ),
        Project(fields={
            "month": "$_id",
            "activeCount": {"$size": "$activeUsers"},
        }),
        Sort(fields={"month": 1}),
    ])
```

## Financial Reporting

### Monthly Revenue Report

```python
from mongo_aggro import Pipeline, Match, Group, Sort, Project

def monthly_revenue_report(year: int):
    """Generate monthly revenue report."""
    return Pipeline([
        Match(query={
            "status": "completed",
            "orderDate": {
                "$gte": f"{year}-01-01",
                "$lt": f"{year + 1}-01-01",
            },
        }),
        Group(
            id={
                "year": {"$year": "$orderDate"},
                "month": {"$month": "$orderDate"},
            },
            accumulators={
                "revenue": {"$sum": "$total"},
                "orders": {"$sum": 1},
                "avgOrderValue": {"$avg": "$total"},
            }
        ),
        Sort(fields={"_id.year": 1, "_id.month": 1}),
        Project(fields={
            "_id": 0,
            "year": "$_id.year",
            "month": "$_id.month",
            "revenue": {"$round": ["$revenue", 2]},
            "orders": 1,
            "avgOrderValue": {"$round": ["$avgOrderValue", 2]},
        }),
    ])
```

### Expense Categorization

```python
from mongo_aggro import Pipeline, Match, Group, Sort, Bucket

def expense_report(department: str, year: int):
    """Categorize expenses by amount ranges."""
    return Pipeline([
        Match(query={
            "department": department,
            "year": year,
            "status": "approved",
        }),
        Bucket(
            group_by="$amount",
            boundaries=[0, 100, 500, 1000, 5000, 10000],
            default="Large",
            output={
                "count": {"$sum": 1},
                "total": {"$sum": "$amount"},
                "expenses": {
                    "$push": {
                        "description": "$description",
                        "amount": "$amount",
                    }
                },
            }
        ),
    ])
```

## Inventory Management

### Low Stock Alert

```python
from mongo_aggro import Pipeline, Match, Lookup, Project, Sort

def get_low_stock_products(threshold: int = 10):
    """Find products with low stock."""
    return Pipeline([
        Match(query={
            "quantity": {"$lte": threshold},
            "status": "active",
        }),
        Lookup(
            from_collection="orders",
            let={"productId": "$_id"},
            pipeline=Pipeline([
                Match(query={
                    "$expr": {"$eq": ["$productId", "$$productId"]},
                    "status": "pending",
                }),
                Group(
                    id=None,
                    accumulators={"pendingQty": {"$sum": "$quantity"}}
                ),
            ]),
            as_field="pendingOrders"
        ),
        Project(fields={
            "name": 1,
            "sku": 1,
            "currentStock": "$quantity",
            "pendingOrders": {
                "$ifNull": [
                    {"$arrayElemAt": ["$pendingOrders.pendingQty", 0]},
                    0
                ]
            },
            "reorderPoint": "$minQuantity",
        }),
        AddFields(fields={
            "availableStock": {
                "$subtract": ["$currentStock", "$pendingOrders"]
            },
            "needsReorder": {
                "$lte": [
                    {"$subtract": ["$currentStock", "$pendingOrders"]},
                    "$reorderPoint"
                ]
            },
        }),
        Match(query={"needsReorder": True}),
        Sort(fields={"availableStock": 1}),
    ])
```

## Log Analysis

### Error Rate by Endpoint

```python
from mongo_aggro import Pipeline, Match, Group, Sort, Project

def error_rate_by_endpoint(start_time: str, end_time: str):
    """Calculate error rates by API endpoint."""
    return Pipeline([
        Match(query={
            "timestamp": {"$gte": start_time, "$lte": end_time},
        }),
        Group(
            id="$endpoint",
            accumulators={
                "totalRequests": {"$sum": 1},
                "errors": {
                    "$sum": {
                        "$cond": [{"$gte": ["$statusCode", 400]}, 1, 0]
                    }
                },
                "avgResponseTime": {"$avg": "$responseTime"},
            }
        ),
        Project(fields={
            "_id": 0,
            "endpoint": "$_id",
            "totalRequests": 1,
            "errors": 1,
            "errorRate": {
                "$round": [
                    {"$multiply": [
                        {"$divide": ["$errors", "$totalRequests"]},
                        100
                    ]},
                    2
                ]
            },
            "avgResponseTime": {"$round": ["$avgResponseTime", 2]},
        }),
        Sort(fields={"errorRate": -1}),
    ])
```
