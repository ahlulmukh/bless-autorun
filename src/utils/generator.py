import hashlib
import os


class Generator:
    @staticmethod
    def generate_hash():
        random_data = os.urandom(32)
        hash_object = hashlib.sha512(random_data)
        return hash_object.hexdigest()
