import hashlib
import json

def generate_hash(index, vote_data, timestamp, previous_hash):
    """Generate SHA-256 hash of block"""
    block_string = json.dumps({
        "index": index,
        "vote_data": vote_data,
        "timestamp": timestamp,  
        "previous_hash": previous_hash
    }, sort_keys=True).encode()

    return hashlib.sha256(block_string).hexdigest()
