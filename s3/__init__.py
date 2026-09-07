"""S3-compatible object-storage integration.

The package is deliberately independent from :mod:`message`: Kafka/message
transport code must not know which object-storage provider is used.
"""

from .storage import S3CompatibleStorage

__all__ = ["S3CompatibleStorage"]
