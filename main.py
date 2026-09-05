"""
Kempromed Core, Entropy & Multi-Platform Vault Ecosystem
Copyright (c) 2026 Dr. Mauro Ernesto Falcón Muñoz. All rights reserved.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import logging

app = FastAPI(title="Kempromed Sovereign Engine", version="4.2.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kempromed_ecosystem")

INTERNAL_TOKEN = os.getenv("INTERNAL_TOKEN", "kempromed_zero_trust_secure_key")
ALEX_CLABE = os.getenv("ALEX_CLABE", "012345678901234567")

class MultiPlatformEvent(BaseModel):
    event_id: str
    source_type: str  # "crypto_volatility" o "online_gaming"
    platform_name: str
    capital_base: float
    current_valuation: float
    entropy_index: float

class SpeiInbound(BaseModel):
    clave_rastreo: str
    monto: float
    banco_emisor: str
    concepto: str

class VaultTransfer(BaseModel):
    tx_id: str
    monto: float
    origen: str

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "system": "Kempromed Sovereign Engine",
        "modules": ["SPEI Rail", "Crypto/Gaming Entropy", "Blind Vault (Alex)"],
        "security": "Zero Trust / Proprietary"
    }

@app.post("/api/v1/entropy/evaluate")
async def evaluate_cross_platform_event(payload: MultiPlatformEvent, request: Request):
    token = request.headers.get("X-Kempromed-Token")
    if token != INTERNAL_TOKEN:
        logger.error("Intento de acceso no autorizado al motor de entropía.")
        raise HTTPException(status_code=403, detail="Unauthorized access")

    delta_gain = payload.current_valuation - payload.capital_base
    roi_percentage = (delta_gain / payload.capital_base) if payload.capital_base > 0 else 0.0

    logger.info(f"EVALUACIÓN | Fuente: {payload.source_type} ({payload.platform_name}) | ROI: {roi_percentage:.2f}% | Entropía: {payload.entropy_index}")

    take_profit_threshold = 0.80
    execute_secure_vault = False

    if roi_percentage >= take_profit_threshold:
        logger.info(f"¡UMBRAL DE TAKE PROFIT ALCANZADO ({roi_percentage*100:.1f}%)! Asegurando capital hacia la bóveda.")
        execute_secure_vault = True
    elif payload.entropy_index > 0.85:
        logger.warning(f"Alta entropía detectada ({payload.entropy_index}). Aplicando protocolo de mitigación de riesgo.")
        execute_secure_vault = True

    secured_amount = delta_gain if execute_secure_vault and delta_gain > 0 else 0.0

    return {
        "status": "evaluated",
        "source": payload.platform_name,
        "roi_captured": roi_percentage,
        "vault_transfer_triggered": execute_secure_vault,
        "secured_to_alex_clabe": ALEX_CLABE if execute_secure_vault else None,
        "secured_amount": secured_amount
    }

@app.post("/api/v1/spei/inbound")
async def process_spei_and_route(payload: SpeiInbound, request: Request):
    token = request.headers.get("X-Kempromed-Token")
    if token != INTERNAL_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    logger.info(f"SPEI RECIBIDO | Rastreo: {payload.clave_rastreo} | Monto: ${payload.monto} MXN")
    return {
        "status": "processed_and_secured",
        "clave_rastreo": payload.clave_rastreo,
        "monto": payload.monto,
        "vault_destination": ALEX_CLABE
    }

@app.post("/api/v1/vault/deposit")
async def vault_blind_deposit(payload: VaultTransfer, request: Request):
    token = request.headers.get("X-Kempromed-Token")
    if token != INTERNAL_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized vault access")

    logger.info(f"DEPÓSITO EN BÓVEDA [Alex] | ID: {payload.tx_id} | Monto: ${payload.monto}")
    return {
        "status": "vault_credited",
        "beneficiary": "Alex",
        "secured_clabe": ALEX_CLABE,
        "amount": payload.monto
    }
