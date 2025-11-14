#!/usr/bin/env python3
"""
AdGuard API Routes
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from src.services.adguard import AdGuardService

router = APIRouter()
adguard_service = AdGuardService()


@router.get("/status")
async def get_status() -> dict[str, Any]:
    """Get AdGuard status"""
    try:
        await adguard_service.initialize()
        return await adguard_service.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/stats")
async def get_stats() -> dict[str, Any]:
    """Get DNS statistics"""
    try:
        await adguard_service.initialize()
        return await adguard_service.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/querylog")
async def get_querylog(limit: int = 100) -> list[dict[str, Any]]:
    """Get DNS query log"""
    try:
        await adguard_service.initialize()
        return await adguard_service.get_querylog(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/filters/add")
async def add_filter(name: str, url: str):
    """Add DNS filter"""
    try:
        await adguard_service.initialize()
        await adguard_service.add_filter(name, url)
        return {"message": f"Filter {name} added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/filters/{filter_id}")
async def remove_filter(filter_id: int):
    """Remove DNS filter"""
    try:
        await adguard_service.initialize()
        await adguard_service.remove_filter(filter_id)
        return {"message": f"Filter {filter_id} removed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/filters/{filter_id}/enable")
async def enable_filter(filter_id: int):
    """Enable DNS filter"""
    try:
        await adguard_service.initialize()
        await adguard_service.enable_filter(filter_id)
        return {"message": f"Filter {filter_id} enabled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/filters/{filter_id}/disable")
async def disable_filter(filter_id: int):
    """Disable DNS filter"""
    try:
        await adguard_service.initialize()
        await adguard_service.disable_filter(filter_id)
        return {"message": f"Filter {filter_id} disabled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/whitelist/add")
async def add_whitelist_rule(domain: str):
    """Add domain to whitelist"""
    try:
        await adguard_service.initialize()
        await adguard_service.add_whitelist_rule(domain)
        return {"message": f"Domain {domain} added to whitelist"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/whitelist/{domain}")
async def remove_whitelist_rule(domain: str):
    """Remove domain from whitelist"""
    try:
        await adguard_service.initialize()
        await adguard_service.remove_whitelist_rule(domain)
        return {"message": f"Domain {domain} removed from whitelist"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/rewrite/add")
async def add_rewrite_rule(domain: str, answer: str):
    """Add DNS rewrite rule"""
    try:
        await adguard_service.initialize()
        await adguard_service.rewrite_dns(domain, answer)
        return {"message": f"Rewrite rule for {domain} added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/protection/enable")
async def enable_protection():
    """Enable DNS protection"""
    try:
        await adguard_service.initialize()
        await adguard_service.set_protection(True)
        return {"message": "DNS protection enabled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/protection/disable")
async def disable_protection():
    """Disable DNS protection"""
    try:
        await adguard_service.initialize()
        await adguard_service.set_protection(False)
        return {"message": "DNS protection disabled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
