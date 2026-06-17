#system will save:

#news events
#economic events
#gold prices
#sentiment scores
#AI signals
#logs   
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/gold_market_system"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)