"""
We have a file that works as key-value storage, each line is represented as key and value
separated by = symbol, example:

name=kek
last_name=top
song_name=shadilay
power=9001

Values can be strings or integer numbers. If a value can be treated both as a number and a string,
it is treated as number.

Write a wrapper class for this key value storage that works like this:

storage = KeyValueStorage('path_to_file.txt')
that has its keys and values accessible as collection items and as attributes.
Example:
storage['name']  # will be string 'kek'
storage.song_name  # will be 'shadilay'
storage.power  # will be integer 9001

In case of attribute clash existing built-in attributes take precedence.
In case when value cannot be assigned to an attribute (for example when there's a line `1=something`)
ValueError should be raised.
File size is expected to be small, you are permitted to read it entirely into memory.
"""


class KeyValueStorage:
    def __init__(self, file_path: str):
        self._storage = {}
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                if not key.isidentifier():
                    raise ValueError(f"Key '{key}' is not a valid identifier.")

                # If value can be treated both as a number and a string, treat as number
                if value.isdigit():
                    value = int(value)

                self._storage[key] = value

    def __getitem__(self, key: str):
        return self._storage[key]

    def __getattr__(self, key: str):
        return self._storage[key]

# Test output
if __name__ == "__main__":
    storage = KeyValueStorage('task1.txt')
storage_data = {
    'name': storage['name'],
    'song_name': storage.song_name,
    'power': storage.power
}
print(storage_data)
