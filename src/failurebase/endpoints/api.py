"""Api router module."""

from fastapi import APIRouter

from .auth import router as auth_router
from .event import router as event_router
from .test import router as test_router
from .client import router as client_router


router = APIRouter(prefix='/api')

router.include_router(auth_router)
router.include_router(event_router)
router.include_router(test_router)
router.include_router(client_router)
