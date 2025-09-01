"""
Main API router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, companies, scan_targets, vulnerabilities, scans

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(scan_targets.router, prefix="/scan-targets", tags=["scan-targets"])
api_router.include_router(vulnerabilities.router, prefix="/vulnerabilities", tags=["vulnerabilities"])
api_router.include_router(scans.router, prefix="/scans", tags=["scans"])