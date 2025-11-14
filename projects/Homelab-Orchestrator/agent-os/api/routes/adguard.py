from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from ...services.adguard import AdGuardService

adguard_router = APIRouter(prefix="/adguard", tags=["AdGuard"])

# Initialize service instance (will be managed by agent_manager later)
adguard_service = AdGuardService(config={})

class AdGuardStatusResponse(BaseModel):
    version: str
    dns_addresses: List[str]
    protection_enabled: bool
    filtering_enabled: bool
    safebrowsing_enabled: bool
    parental_control_enabled: bool
    safesearch_enabled: bool
    blocked_domains: int
    dns_queries: int
    rules_count: int
    time_start: str

class AdGuardStatsResponse(BaseModel):
    dns_queries: int
    blocked_filtering: int
    replaced_safebrowsing: int
    replaced_parental: int
    replaced_safesearch: int
    top_queried_domains: List[Dict[str, Any]]
    top_blocked_domains: List[Dict[str, Any]]
    top_clients: List[Dict[str, Any]]
    top_upstreams: List[Dict[str, Any]]

class AdGuardQueryLogResponse(BaseModel):
    data: List[Dict[str, Any]]

class AdGuardAddFilterRequest(BaseModel):
    url: str
    name: Optional[str] = None

class AdGuardRemoveFilterRequest(BaseModel):
    id: int

class AdGuardEnableFilterRequest(BaseModel):
    id: int
    enabled: bool = True

class AdGuardDisableFilterRequest(BaseModel):
    id: int
    enabled: bool = False

class AdGuardWhitelistRuleRequest(BaseModel):
    rule: str

class AdGuardRewriteDnsRequest(BaseModel):
    domain: str
    answer: str

class AdGuardSetProtectionRequest(BaseModel):
    protection_enabled: bool

@adguard_router.get("/status", response_model=AdGuardStatusResponse)
async def get_adguard_status():
    """Get AdGuard Home status"""
    try:
        return await adguard_service.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.get("/stats", response_model=AdGuardStatsResponse)
async def get_adguard_stats():
    """Get AdGuard Home DNS statistics"""
    try:
        return await adguard_service.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.get("/querylog", response_model=AdGuardQueryLogResponse)
async def get_adguard_querylog(limit: int = 100):
    """Get AdGuard Home DNS query log"""
    try:
        data = await adguard_service.get_querylog(limit)
        return AdGuardQueryLogResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.post("/filter/add", response_model=bool)
async def add_adguard_filter(request: AdGuardAddFilterRequest):
    """Add a filter to AdGuard Home"""
    try:
        return await adguard_service.add_filter(request.url, request.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.post("/filter/remove", response_model=bool)
async def remove_adguard_filter(request: AdGuardRemoveFilterRequest):
    """Remove a filter from AdGuard Home"""
    try:
        return await adguard_service.remove_filter(request.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.post("/filter/enable", response_model=bool)
async def enable_adguard_filter(request: AdGuardEnableFilterRequest):
    """Enable a filter in AdGuard Home"""
    try:
        return await adguard_service.enable_filter(request.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.post("/filter/disable", response_model=bool)
async def disable_adguard_filter(request: AdGuardDisableFilterRequest):
    """Disable a filter in AdGuard Home"""
    try:
        return await adguard_service.disable_filter(request.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.post("/whitelist/add", response_model=bool)
async def add_adguard_whitelist_rule(request: AdGuardWhitelistRuleRequest):
    """Add a whitelist rule to AdGuard Home"""
    try:
        return await adguard_service.add_whitelist_rule(request.rule)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.post("/whitelist/remove", response_model=bool)
async def remove_adguard_whitelist_rule(request: AdGuardWhitelistRuleRequest):
    """Remove a whitelist rule from AdGuard Home"""
    try:
        return await adguard_service.remove_whitelist_rule(request.rule)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.post("/rewrite/dns", response_model=bool)
async def rewrite_adguard_dns(request: AdGuardRewriteDnsRequest):
    """Add a DNS rewrite rule to AdGuard Home"""
    try:
        return await adguard_service.rewrite_dns(request.domain, request.answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adguard_router.post("/protection", response_model=bool)
async def set_adguard_protection(request: AdGuardSetProtectionRequest):
    """Enable/disable AdGuard Home DNS protection"""
    try:
        return await adguard_service.set_protection(request.protection_enabled)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
