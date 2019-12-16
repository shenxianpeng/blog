---
title: Fix flask errors
date: 2017-11-14 13:34:46
tags: 
- Flask
- Python
categories: 
- Python
---

#### TypeError: object of type 'filter' has no len()

Change below code

```python
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
```

To

```python
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
```

Add `list()`, refer to [stackoverflow](https://stackoverflow.com/questions/19182188/how-to-find-the-length-of-a-filter-object-in-python).
