from typing import List
import numpy as np

from chromadb.api import API
from chromadb.api.models.Collection import Collection


def test_high_collections(api: API) -> None:
    """Test that we can create a large number of collections and that the system
    # remains responsive."""
    api.reset()

    N = 10
    D = 10

    metadata = None
    # TODO: done
    if api.get_settings().is_persistent:
        metadata = {"hnsw:batch_size": 3, "hnsw:sync_threshold": 3}
    else:
        return  # FOR NOW

    num_collections = 10000
    collections: List[Collection] = []
    for i in range(num_collections):
        new_collection = api.create_collection(
            f"test_collection_{i}",
            metadata=metadata,
        )
        collections.append(new_collection)

    # Add a few embeddings to each collection
    data = np.random.rand(N, D).tolist()
    ids = [f"test_id_{i}" for i in range(N)]
    for i in range(num_collections):
        collections[i].add(ids, data)
