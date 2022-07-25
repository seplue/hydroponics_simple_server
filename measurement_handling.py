import json

file_name = 'MEASUREMENTS.py'

measurement_example = {
    'time_utc': 0,
    'temperature': 23.1,
    'humidity': 60.0,
    'light': 0.7,
}


def read_json():
    # Opening JSON file
    with open(file_name, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    print(json_object)
    print(type(json_object))
    print(json_object[0]['temperature'])
    # json_object is of type list which contains dictionaries
    return json_object


def write_json(x):
    # Serializing json
    json_object = json.dumps(x)

    # Writing to sample.json
    with open(file_name, 'w') as outfile:
        outfile.write(json_object)


def add_measurement(x):
    measurements = read_json()
    print(measurements)
    measurements.append(x)
    print(measurements)
    write_json(measurements)


def send_json(x):
    pass


if __name__ == "__main__":
    read_json()
    # write_json(measurement_example)
    add_measurement(measurement_example)
