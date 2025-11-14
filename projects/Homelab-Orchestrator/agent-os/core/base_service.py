import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BaseAgentService(ABC):
    """Base class for all agent services."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the service."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Perform a health check for the service."""
        pass

    @abstractmethod
    async def run(self) -> None:
        """Run the main logic of the service."""
        pass

    async def cleanup(self) -> None:
        """Perform cleanup operations when the service is stopped."""
        self.logger.info(f"{self.__class__.__name__} cleanup complete")
