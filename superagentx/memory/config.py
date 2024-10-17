import os
from pathlib import Path

from pydantic import BaseModel, Field

from superagentx.vector_stores.base import BaseVectorStore
from superagentx.vector_stores.chroma import ChromaDB


def _db_path():
    _db_dir = os.environ.get('AGENTX_MEMORY_DIR')
    if not _db_dir:
        _db_dir = Path().home()
    else:
        _db_dir = Path(_db_dir)
    return _db_dir / 'history.db'


def _chroma():
    return ChromaDB(collection_name="test")


class MemoryConfig(BaseModel):
    vector_store: BaseVectorStore = Field(
        description="Configuration for the vector store",
        default=None,
    )

    db_path: str = Field(
        description="Path to the history database",
        default=_db_path(),
    )

    class Config:
        arbitrary_types_allowed = True
