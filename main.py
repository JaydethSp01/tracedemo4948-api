from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
import uvicorn
import uuid

app = FastAPI(title="GymManager API", version="1.0.0")

# CRUD generico server-side (persistencia multi-dispositivo)
try:
    from app.routers import data as _data_router
    app.include_router(_data_router.router)
except Exception as _e:
    import logging; logging.getLogger('uvicorn').warning('data router: %s', _e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── MODELS ────────────────────────────────────────────────────────────────────

class Plan(BaseModel):
    id: str
    nombre: str
    descripcion: str
    precio_mensual: float
    duracion_meses: int
    clases_incluidas: int
    activo: bool = True
    creado_en: str

class PlanCreate(BaseModel):
    nombre: str
    descripcion: str
    precio_mensual: float
    duracion_meses: int
    clases_incluidas: int
    activo: bool = True

class PlanUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_mensual: Optional[float] = None
    duracion_meses: Optional[int] = None
    clases_incluidas: Optional[int] = None
    activo: Optional[bool] = None

class Socio(BaseModel):
    id: str
    nombre: str
    apellido: str
    email: str
    telefono: str
    fecha_nacimiento: str
    fecha_alta: str
    activo: bool = True
    foto_url: Optional[str] = None

class SocioCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    fecha_nacimiento: str
    activo: bool = True
    foto_url: Optional[str] = None

class SocioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    activo: Optional[bool] = None
    foto_url: Optional[str] = None

class Membresia(BaseModel):
    id: str
    socio_id: str
    plan_id: str
    fecha_inicio: str
    fecha_fin: str
    estado: str
    monto_pagado: float
    metodo_pago: str
    creado_en: str

class MembresiaCreate(BaseModel):
    socio_id: str
    plan_id: str
    fecha_inicio: str
    fecha_fin: str
    estado: str
    monto_pagado: float
    metodo_pago: str

class MembresiaUpdate(BaseModel):
    socio_id: Optional[str] = None
    plan_id: Optional[str] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    estado: Optional[str] = None
    monto_pagado: Optional[float] = None
    metodo_pago: Optional[str] = None

class Clase(BaseModel):
    id: str
    nombre: str
    descripcion: str
    instructor: str
    capacidad_maxima: int
    inscritos: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str
    sala: str
    activa: bool = True
    creado_en: str

class ClaseCreate(BaseModel):
    nombre: str
    descripcion: str
    instructor: str
    capacidad_maxima: int
    inscritos: int = 0
    dia_semana: str
    hora_inicio: str
    hora_fin: str
    sala: str
    activa: bool = True

class ClaseUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    instructor: Optional[str] = None
    capacidad_maxima: Optional[int] = None
    inscritos: Optional[int] = None
    dia_semana: Optional[str] = None
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    sala: Optional[str] = None
    activa: Optional[bool] = None

# ─── SEED DATA ─────────────────────────────────────────────────────────────────

planes_db: List[dict] = [
    {
        "id": "plan-001",
        "nombre": "Básico",
        "descripcion": "Acceso a sala de musculación en horario estándar",
        "precio_mensual": 29.99,
        "duracion_meses": 1,
        "clases_incluidas": 0,
        "activo": True,
        "creado_en": "2024-01-01T00:00:00",
    },
    {
        "id": "plan-002",
        "nombre": "Premium",
        "descripcion": "Acceso ilimitado + 8 clases grupales al mes",
        "precio_mensual": 49.99,
        "duracion_meses": 1,
        "clases_incluidas": 8,
        "activo": True,
        "creado_en": "2024-01-01T00:00:00",
    },
    {
        "id": "plan-003",
        "nombre": "Elite Anual",
        "descripcion": "Acceso ilimitado + clases ilimitadas + nutricionista",
        "precio_mensual": 39.99,
        "duracion_meses": 12,
        "clases_incluidas": 999,
        "activo": True,
        "creado_en": "2024-01-01T00:00:00",
    },
    {
        "id": "plan-004",
        "nombre": "Familiar",
        "descripcion": "Hasta 4 miembros del hogar con acceso completo",
        "precio_mensual": 89.99,
        "duracion_meses": 1,
        "clases_incluidas": 16,
        "activo": True,
        "creado_en": "2024-02-15T00:00:00",
    },
    {
        "id": "plan-005",
        "nombre": "Estudiante",
        "descripcion": "Plan reducido con acreditación universitaria vigente",
        "precio_mensual": 19.99,
        "duracion_meses": 1,
        "clases_incluidas": 4,
        "activo": True,
        "creado_en": "2024-03-01T00:00:00",
    },
]

socios_db: List[dict] = [
    {
        "id": "soc-001",
        "nombre": "Carlos",
        "apellido": "Mendoza",
        "email": "carlos.mendoza@email.com",
        "telefono": "+34 612 345 678",
        "fecha_nacimiento": "1990-05-12",
        "fecha_alta": "2024-01-10",
        "activo": True,
        "foto_url": None,
    },
    {
        "id": "soc-002",
        "nombre": "Laura",
        "apellido": "Fernández",
        "email": "laura.fernandez@email.com",
        "telefono": "+34 698 234 567",
        "fecha_nacimiento": "1995-08-23",
        "fecha_alta": "2024-02-05",
        "activo": True,
        "foto_url": None,
    },
    {
        "id": "soc-003",
        "nombre": "Miguel",
        "apellido": "Torres",
        "email": "miguel.torres@email.com",
        "telefono": "+34 677 890 123",
        "fecha_nacimiento": "1988-11-30",
        "fecha_alta": "2024-01-22",
        "activo": True,
        "foto_url": None,
    },
    {
        "id": "soc-004",
        "nombre": "Ana",
        "apellido": "García",
        "email": "ana.garcia@email.com",
        "telefono": "+34 654 321 098",
        "fecha_nacimiento": "2001-03-17",
        "fecha_alta": "2024-03-14",
        "activo": True,
        "foto_url": None,
    },
    {
        "id": "soc-005",
        "nombre": "Javier",
        "apellido": "López",
        "email": "javier.lopez@email.com",
        "telefono": "+34 623 456 789",
        "fecha_nacimiento": "1983-07-04",
        "fecha_alta": "2023-11-01",
        "activo": False,
        "foto_url": None,
    },
    {
        "id": "soc-006",
        "nombre": "Sofía",
        "apellido": "Martínez",
        "email": "sofia.martinez@email.com",
        "telefono": "+34 689 012 345",
        "fecha_nacimiento": "1998-12-09",
        "fecha_alta": "2024-04-01",
        "activo": True,
        "foto_url": None,
    },
]

membresias_db: List[dict] = [
    {
        "id": "mem-001",
        "socio_id": "soc-001",
        "plan_id": "plan-002",
        "fecha_inicio": "2024-05-01",
        "fecha_fin": "2024-06-01",
        "estado": "activa",
        "monto_pagado": 49.99,
        "metodo_pago": "tarjeta",
        "creado_en": "2024-05-01T09:30:00",
    },
    {
        "id": "mem-002",
        "socio_id": "soc-002",
        "plan_id": "plan-003",
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2024-12-31",
        "estado": "activa",
        "monto_pagado": 479.88,
        "metodo_pago": "transferencia",
        "creado_en": "2024-01-01T10:00:00",
    },
    {
        "id": "mem-003",
        "socio_id": "soc-003",
        "plan_id": "plan-001",
        "fecha_inicio": "2024-04-01",
        "fecha_fin": "2024-05-01",
        "estado": "vencida",
        "monto_pagado": 29.99,
        "metodo_pago": "efectivo",
        "creado_en": "2024-04-01T11:15:00",
    },
    {
        "id": "mem-004",
        "socio_id": "soc-004",
        "plan_id": "plan-005",
        "fecha_inicio": "2024-03-14",
        "fecha_fin": "2024-04-14",
        "estado": "activa",
        "monto_pagado": 19.99,
        "metodo_pago": "tarjeta",
        "creado_en": "2024-03-14T16:00:00",
    },
    {
        "id": "mem-005",
        "socio_id": "soc-005",
        "plan_id": "plan-002",
        "fecha_inicio": "2023-11-01",
        "fecha_fin": "2023-12-01",
        "estado": "cancelada",
        "monto_pagado": 49.99,
        "metodo_pago": "tarjeta",
        "creado_en": "2023-11-01T08:45:00",
    },
    {
        "id": "mem-006",
        "socio_id": "soc-006",
        "plan_id": "plan-004",
        "fecha_inicio": "2024-04-01",
        "fecha_fin": "2024-05-01",
        "estado": "activa",
        "monto_pagado": 89.99,
        "metodo_pago": "domiciliacion",
        "creado_en": "2024-04-01T12:30:00",
    },
]

clases_db: List[dict] = [
    {
        "id": "cls-001",
        "nombre": "Spinning Intensivo",
        "descripcion": "Cardio en bicicleta estática con música y alta intensidad",
        "instructor": "Marta Ruiz",
        "capacidad_maxima": 20,
        "inscritos": 17,
        "dia_semana": "Lunes",
        "hora_inicio": "07:00",
        "hora_fin": "08:00",
        "sala": "Sala A",
        "activa": True,
        "creado_en": "2024-01-15T00:00:00",
    },
    {
        "id": "cls-002",
        "nombre": "Yoga Flow",
        "descripcion": "Secuencia de posturas enlazadas con respiración consciente",
        "instructor": "Elena Soler",
        "capacidad_maxima": 15,
        "inscritos": 12,
        "dia_semana": "Martes",
        "hora_inicio": "09:30",
        "hora_fin": "10:30",
        "sala": "Sala B",
        "activa": True,
        "creado_en": "2024-01-15T00:00:00",
    },
    {
        "id": "cls-003",
        "nombre": "CrossFit Funcional",
        "descripcion": "Entrenamiento de alta intensidad con movimientos funcionales",
        "instructor": "Raúl Jiménez",
        "capacidad_maxima": 12,
        "inscritos": 12,
        "dia_semana": "Miércoles",
        "hora_inicio": "18:00",
        "hora_fin": "19:00",
        "sala": "Sala C",
        "activa": True,
        "creado_en": "2024-02-01T00:00:00",
    },
    {
        "id": "cls-004",
        "nombre": "Pilates Mat",
        "descripcion": "Fortalecimiento del core y mejora postural en colchoneta",
        "instructor": "Carmen Vidal",
        "capacidad_maxima": 18,
        "inscritos": 9,
        "dia_semana": "Jueves",
        "hora_inicio": "11:00",
        "hora_fin": "12:00",
        "sala": "Sala B",
        "activa": True,
        "creado_en": "2024-02-10T00:00:00",
    },
    {
        "id": "cls-005",
        "nombre": "Zumba Fitness",
        "descripcion": "Baile aeróbico con ritmos latinos y caribeños",
        "instructor": "Paola Herrera",
        "capacidad_maxima": 25,
        "inscritos": 21,
        "dia_semana": "Viernes",
        "hora_inicio": "19:30",
        "hora_fin": "20:30",
        "sala": "Sala A",
        "activa": True,
        "creado_en": "2024-03-01T00:00:00",
    },
    {
        "id": "cls-006",
        "nombre": "Box Fitness",
        "descripcion": "Técnicas de boxeo adaptadas para acondicionamiento físico",
        "instructor": "David Mora",
        "capacidad_maxima": 14,
        "inscritos": 6,
        "dia_semana": "Sábado",
        "hora_inicio": "10:00",
        "hora_fin": "11:00",
        "sala": "Sala C",
        "activa": False,
        "creado_en": "2024-03-20T00:00:00",
    },
]

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def now_iso() -> str:
    return datetime.utcnow().isoformat()

# ─── PLANS ENDPOINTS ───────────────────────────────────────────────────────────

@app.get("/planes", response_model=List[Plan])
def get_planes():
    return planes_db

@app.get("/planes/{plan_id}", response_model=Plan)
def get_plan(plan_id: str):
    plan = next((p for p in planes_db if p["id"] == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return plan

@app.post("/planes", response_model=Plan, status_code=201)
def create_plan(data: PlanCreate):
    nuevo = {
        "id": new_id("plan"),
        **data.dict(),
        "creado_en": now_iso(),
    }
    planes_db.append(nuevo)
    return nuevo

@app.put("/planes/{plan_id}", response_model=Plan)
def update_plan(plan_id: str, data: PlanUpdate):
    plan = next((p for p in planes_db if p["id"] == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    for key, value in data.dict(exclude_none=True).items():
        plan[key] = value
    return plan

@app.delete("/planes/{plan_id}", status_code=204)
def delete_plan(plan_id: str):
    global planes_db
    plan = next((p for p in planes_db if p["id"] == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    planes_db = [p for p in planes_db if p["id"] != plan_id]

# ─── SOCIOS ENDPOINTS ──────────────────────────────────────────────────────────

@app.get("/socios", response_model=List[Socio])
def get_socios():
    return socios_db

@app.get("/socios/{socio_id}", response_model=Socio)
def get_socio(socio_id: str):
    socio = next((s for s in socios_db if s["id"] == socio_id), None)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio

@app.post("/socios", response_model=Socio, status_code=201)
def create_socio(data: SocioCreate):
    existing = next((s for s in socios_db if s["email"] == data.email), None)
    if existing:
        raise HTTPException(status_code=409, detail="Ya existe un socio con ese email")
    nuevo = {
        "id": new_id("soc"),
        **data.dict(),
        "fecha_alta": date.today().isoformat(),
    }
    socios_db.append(nuevo)
    return nuevo

@app.put("/socios/{socio_id}", response_model=Socio)
def update_socio(socio_id: str, data: SocioUpdate):
    socio = next((s for s in socios_db if s["id"] == socio_id), None)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    for key, value in data.dict(exclude_none=True).items():
        socio[key] = value
    return socio

@app.delete("/socios/{socio_id}", status_code=204)
def delete_socio(socio_id: str):
    global socios_db
    socio = next((s for s in socios_db if s["id"] == socio_id), None)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    socios_db = [s for s in socios_db if s["id"] != socio_id]

# ─── MEMBRESIAS ENDPOINTS ──────────────────────────────────────────────────────

@app.get("/membresias", response_model=List[Membresia])
def get_membresias():
    return membresias_db

@app.get("/membresias/{mem_id}", response_model=Membresia)
def get_membresia(mem_id: str):
    mem = next((m for m in membresias_db if m["id"] == mem_id), None)
    if not mem:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    return mem

@app.get("/socios/{socio_id}/membresias", response_model=List[Membresia])
def get_membresias_by_socio(socio_id: str):
    socio = next((s for s in socios_db if s["id"] == socio_id), None)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return [m for m in membresias_db if m["socio_id"] == socio_id]

@app.post("/membresias", response_model=Membresia, status_code=201)
def create_membresia(data: MembresiaCreate):
    socio = next((s for s in socios_db if s["id"] == data.socio_id), None)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    plan = next((p for p in planes_db if p["id"] == data.plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    nuevo = {
        "id": new_id("mem"),
        **data.dict(),
        "creado_en": now_iso(),
    }
    membresias_db.append(nuevo)
    return nuevo

@app.put("/membresias/{mem_id}", response_model=Membresia)
def update_membresia(mem_id: str, data: MembresiaUpdate):
    mem = next((m for m in membresias_db if m["id"] == mem_id), None)
    if not mem:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    for key, value in data.dict(exclude_none=True).items():
        mem[key] = value
    return mem

@app.delete("/membresias/{mem_id}", status_code=204)
def delete_membresia(mem_id: str):
    global membresias_db
    mem = next((m for m in membresias_db if m["id"] == mem_id), None)
    if not mem:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    membresias_db = [m for m in membresias_db if m["id"] != mem_id]

# ─── CLASES ENDPOINTS ──────────────────────────────────────────────────────────

@app.get("/clases", response_model=List[Clase])
def get_clases():
    return clases_db

@app.get("/clases/{clase_id}", response_model=Clase)
def get_clase(clase_id: str):
    clase = next((c for c in clases_db if c["id"] == clase_id), None)
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    return clase

@app.post("/clases", response_model=Clase, status_code=201)
def create_clase(data: ClaseCreate):
    nuevo = {
        "id": new_id("cls"),
        **data.dict(),
        "creado_en": now_iso(),
    }
    clases_db.append(nuevo)
    return nuevo

@app.put("/clases/{clase_id}", response_model=Clase)
def update_clase(clase_id: str, data: ClaseUpdate):
    clase = next((c for c in clases_db if c["id"] == clase_id), None)
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    for key, value in data.dict(exclude_none=True).items():
        clase[key] = value
    return clase

@app.delete("/clases/{clase_id}", status_code=204)
def delete_clase(clase_id: str):
    global clases_db
    clase = next((c for c in clases_db if c["id"] == clase_id), None)
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    clases_db = [c for c in clases_db if c["id"] != clase_id]

# ─── STATS ENDPOINT ────────────────────────────────────────────────────────────

@app.get("/stats")
def get_stats():
    total_socios = len(socios_db)
    socios_activos = sum(1 for s in socios_db if s["activo"])
    membresias_activas = sum(1 for m in membresias_db if m["estado"] == "activa")
    ingresos_mes = sum(m["monto_pagado"] for m in membresias_db if m["estado"] == "activa")
    clases_activas = sum(1 for c in clases_db if c["activa"])
    ocupacion_media = (
        round(
            sum(c["inscritos"] / c["capacidad_maxima"] for c in clases_db if c["activa"]) / clases_activas * 100,
            1,
        )
        if clases_activas > 0
        else 0
    )
    return {
        "total_socios": total_socios,
        "socios_activos": socios_activos,
        "membresias_activas": membresias_activas,
        "ingresos_mes": round(ingresos_mes, 2),
        "clases_activas": clases_activas,
        "ocupacion_media_pct": ocupacion_media,
        "planes_disponibles": len([p for p in planes_db if p["activo"]]),
    }

# ─── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)