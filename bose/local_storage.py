import os
import json

from bose.utils import relative_path


class localStoragePyStorageException(Exception):
    pass


class BasicStorageBackend:
    def raise_dummy_exception(self):
        raise localStoragePyStorageException("Called dummy backend!")

    def get_item(self, item: str, default:any = None) -> str:
        self.raise_dummy_exception()

    def set_item(self, item: str, value: any) -> None:
        self.raise_dummy_exception()

    def remove_item(self, item: str) -> None:
        self.raise_dummy_exception()

    def clear(self) -> None:
        self.raise_dummy_exception()

class JSONStorageBackend(BasicStorageBackend):
    def __init__(self) -> None:
        self.json_path = relative_path( "local_storage.json", 0)
        self.json_data = {}

        if not os.path.isfile(self.json_path):
            self.commit_to_disk()

        with open(self.json_path, "r") as json_file:
            self.json_data = json.load(json_file)
        
    def commit_to_disk(self):
        with open(self.json_path, "w") as json_file:
            json.dump(self.json_data, json_file)

    def get_item(self, key: str, default = None) -> str:
        if key in self.json_data:
            return self.json_data[key]
        return default

    def set_item(self, key: str, value: any) -> None:
        self.json_data[key] = value
        self.commit_to_disk()

    def remove_item(self, key: str) -> None: 
        if key in self.json_data:
            self.json_data.pop(key)
            self.commit_to_disk()

    def clear(self) -> None:
        if os.path.isfile(self.json_path):
            os.remove(self.json_path)
        self.json_data = {}
        self.commit_to_disk()
    
class _LocalStorage:
    def __init__(self) -> None:
        self.storage_backend_instance = JSONStorageBackend()

    def get_item(self, item: str, default = None) -> any:
        return self.storage_backend_instance.get_item(item, default)

    def set_item(self, item: str, value: any) -> None:
        self.storage_backend_instance.set_item(item, value)

    def remove_item(self, item: str) -> None:
        self.storage_backend_instance.remove_item(item)

    def clear(self):
        self.storage_backend_instance.clear()

LocalStorage = _LocalStorage()

if __name__ == "__main__":
    t = _LocalStorage()
    
    print(t.get_item("a"))
    print(t.set_item("a" ,"ss"))
    print(t.remove_item("a"))
