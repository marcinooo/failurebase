"""Api router module."""

from fastapi import APIRouter

from .event import router as event_router
from .test import router as test_router

router = APIRouter(prefix='/api')

router.include_router(event_router)
router.include_router(test_router)
