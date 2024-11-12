from datetime import datetime
import json
import numpy as np
from collections import defaultdict

def time_of_day(hour):
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'
    
def load_db(fl):
    with open(fl, "r") as file:
        data = json.load(file)
    
    return data

def write_db(fl, data):
    with open(fl, "w") as file:
        json.dump(data, file, indent=4)

def normalize_dataset(data):
    if not data:
        raise ValueError('The input data should list not empty')
    # ex: [10, 25, 15, 30]
    min_value = min(data) #30
    max_value = max(data)  #10

    if min_value == max_value: 
        raise ValueError('The input data is constant value') 

    # min-max scaling. if 25 -> (25-10) / (30-10) = 0.75
    normalized = [(point - min_value)/(max_value - min_value)  for point in data]

    return normalized 

def get_avg_wait_time(arrival_dayofweek, time_of_day, average_wait_time):
    return average_wait_time.get((arrival_dayofweek, time_of_day), None)

def average_by_obj(db, key):
    grouped_wait_times = {}

    for entry in db:
        group_key = (entry["arrival_dayofweek"], entry["time_of_day"])

        if group_key not in grouped_wait_times:
            grouped_wait_times[group_key] = []

        grouped_wait_times[group_key].append(entry[key])

    mean_wait_times = {}
    for group_key, wait_times in grouped_wait_times.items():
        mean_wait_times[group_key] = np.nanmean(wait_times)

    overall_mean = np.nanmean(list(mean_wait_times.values()))
    return overall_mean

def predict(request, model):
    # after feature selection -> ['queue_length', 'tod', 'cumulative_queue', 'avg_wait_by_day_time', 'avg_queue_by_day_time']
    desc_tod = {'night': 0, 'morning': 1, 'afternoon': 2, 'evening': 3}
    db = load_db("api_apps/queue.json")

    start_time = datetime.strptime(request.start_time, "%d-%m-%Y %H:%M")

    arrival_time = datetime.strptime(request.arrival_time, "%d-%m-%Y %H:%M")
    timeOfDay = time_of_day(arrival_time.hour)
    arrival_dayofweek = arrival_time.weekday()
    tod = desc_tod[timeOfDay]

    queue_length = request.queue_length
    queue = list([data['queue_length'] for data in db])
    queue.append(queue_length)
    
    cumulative_queue = np.cumsum(queue)

    arrival_dayofweek = arrival_time.weekday()

    grouped_wait_times = average_by_obj(db, 'wait_time')
    grouped_wait_queue = average_by_obj(db, 'queue_length')
    
    features = [queue_length, tod, cumulative_queue[len(cumulative_queue)-1], grouped_wait_times, grouped_wait_queue]
    features = normalize_dataset(features)
    # Make prediction
    predicted_wait_time = model.predict([features])[0]

    time_difference = arrival_time - start_time
    wait_time = time_difference.total_seconds() / 3600

    obj = {"arrival_dayofweek": arrival_dayofweek, "time_of_day": timeOfDay, "wait_time": wait_time, "queue_length": queue_length}
    db.append(obj)
 
    write_db("api_apps/queue.json", db)
    return round(predicted_wait_time, 2)