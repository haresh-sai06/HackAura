#!/usr/bin/env python3

from sqlalchemy import create_engine, text
from config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)
with engine.connect() as conn:
    # Fix emergency services with spaces
    result = conn.execute(text('UPDATE call_records SET assigned_service = "FIRE_DEPARTMENT" WHERE assigned_service = "FIRE DEPARTMENT"'))
    print(f'Fixed "FIRE DEPARTMENT" to "FIRE_DEPARTMENT": {result.rowcount}')
    
    result = conn.execute(text('UPDATE call_records SET assigned_service = "MULTIPLE_SERVICES" WHERE assigned_service = "MULTIPLE SERVICES"'))
    print(f'Fixed "MULTIPLE SERVICES" to "MULTIPLE_SERVICES": {result.rowcount}')
    
    conn.commit()
    print('✅ Emergency services with spaces fixed')
