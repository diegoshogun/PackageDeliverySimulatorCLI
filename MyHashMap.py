# Class that allows me to implement my own Chaining Hash Map.
# O(N)
class MyHashMap:
    # Method initializes class.
    # O(N)
    def __init__(self):
        # Sets size of list, and assigns each bucket an empty list
        self.map = []
        self.map_size = 10
        for i in range(self.map_size):
            self.map.append([])

    # Generates hash value for key and returns it.
    def _get_hash(self, key):
        if isinstance(key, int):
            return int(key) % self.map_size
        else:
            return False

    # Inserts new key/value pair into list.
    # Also updates existing key with new value, if key already exists.
    # Space - O(N)       Time - O(N)
    def insert(self, key, value):
        # Gets the bucket list where item will go.
        bucket = self._get_hash(key)
        bucket_list = self.map[bucket]

        # Key/Value pair.
        key_value = [key, value]

        if not bucket_list:  # Checks if bucket list is empty
            bucket_list.append(key_value)  # Inserts new key value pair.
            return True
        else:  # Bucket list was not empty, which means key/value pair already exists.
            for kv in bucket_list:  # Updating key with new value.
                if kv[0] == key:
                    kv[1] = value
                    return True
            bucket_list.append(key_value)

    # Returns value that matches key (if exists) from specific bucket list.
    # Space - O(N)       Time - O(N)
    def lookup(self, key):
        # Gets the bucket list where the key would be.
        bucket = self._get_hash(key)
        bucket_list = self.map[bucket]

        if bucket_list:  # If bucket list is not empty.
            for kv in bucket_list:  # Looping through key/value pair in bucket list.
                if kv[0] == key:
                    return kv[1]  # Returning value of key.
        else:  # If bucket list is empty.
            return None

    # Deletes key/value pair from bucket list.
    # Space - O(N)       Time - O(N)
    def delete(self, key):
        # Gets the bucket list where the key would be.
        bucket = self._get_hash(key)
        bucket_list = self.map[bucket]

        if bucket_list:  # If bucket list is not empty.
            for i in range(0, len(bucket_list)):
                if bucket_list[i][0] == key:
                    bucket_list.pop(i)
                    return True
        else:  # If bucket list is empty.
            return False
