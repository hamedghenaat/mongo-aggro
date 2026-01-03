# Pipeline

The `Pipeline` class is the core component of Mongo Aggro. It acts as a container for aggregation stages and can be passed directly to MongoDB's `aggregate()` method.

## Creating a Pipeline

### From a List of Stages

```python
from mongo_aggro import Pipeline, Match, Sort, Limit

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Sort(fields={"created_at": -1}),
    Limit(count=10),
])
```

### Empty Pipeline with Method Chaining

```python
pipeline = (
    Pipeline()
    .add_stage(Match(query={"status": "active"}))
    .add_stage(Sort(fields={"created_at": -1}))
    .add_stage(Limit(count=10))
)
```

## Pipeline Methods

### `add_stage(stage)`

Adds a stage to the end of the pipeline. Returns `self` for chaining.

```python
pipeline = Pipeline()
pipeline.add_stage(Match(query={"x": 1}))
pipeline.add_stage(Limit(count=5))
```

### `to_list()`

Returns the pipeline as a list of dictionaries.

```python
stages = pipeline.to_list()
# [{"$match": {"x": 1}}, {"$limit": 5}]
```

### `__len__()`

Returns the number of stages.

```python
print(len(pipeline))  # 2
```

### `__iter__()`

Makes the pipeline iterable. This is what allows direct use with PyMongo.

```python
for stage in pipeline:
    print(stage)
```

## Direct MongoDB Integration

The Pipeline class implements `__iter__`, which means MongoDB's `aggregate()` method can iterate over it directly:

```python
from pymongo import MongoClient
from mongo_aggro import Pipeline, Match, Limit

client = MongoClient()
collection = client.mydb.mycollection

pipeline = Pipeline([
    Match(query={"active": True}),
    Limit(count=100),
])

# No need to call .to_list() - pipeline is directly iterable
results = collection.aggregate(pipeline)
```

## Pipeline Reusability

Pipelines can be iterated multiple times:

```python
pipeline = Pipeline([Match(query={"x": 1})])

# First iteration
first_run = list(collection.aggregate(pipeline))

# Second iteration - works fine
second_run = list(collection.aggregate(pipeline))
```

## Combining Pipelines

You can combine stages from multiple sources:

```python
base_stages = [
    Match(query={"active": True}),
    Sort(fields={"date": -1}),
]

pagination_stages = [
    Skip(count=20),
    Limit(count=10),
]

pipeline = Pipeline(base_stages + pagination_stages)
```
