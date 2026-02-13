#!/usr/bin/env python3

from sqlalchemy import create_engine, text
from config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)
with engine.connect() as conn:
    # Fix severity levels - add back underscores
    result = conn.execute(text('UPDATE call_records SET severity_level = "LEVEL_1" WHERE severity_level = "LEVEL1"'))
    print(f'Fixed LEVEL1 to LEVEL_1: {result.rowcount}')
    
    result = conn.execute(text('UPDATE call_records SET severity_level = "LEVEL_2" WHERE severity_level = "LEVEL2"'))
    print(f'Fixed LEVEL2 to LEVEL_2: {result.rowcount}')
    
    result = conn.execute(text('UPDATE call_records SET severity_level = "LEVEL_3" WHERE severity_level = "LEVEL3"'))
    print(f'Fixed LEVEL3 to LEVEL_3: {result.rowcount}')
    
    result = conn.execute(text('UPDATE call_records SET severity_level = "LEVEL_4" WHERE severity_level = "LEVEL4"'))
    print(f'Fixed LEVEL4 to LEVEL_4: {result.rowcount}')
    
    conn.commit()
    print('✅ Severity levels fixed')
