import json
import datetime
import os
import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv

# Load .env configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASE_URL = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")
SQLITE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'attendance.db')}"

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    batch = Column(String(50), default="Batch-2026-A")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    embeddings = relationship("FaceEmbedding", back_populates="student", cascade="all, delete-orphan")
    attendance = relationship("AttendanceRecord", back_populates="student", cascade="all, delete-orphan")

class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(50), ForeignKey("students.student_id"), nullable=False)
    embedding_json = Column(Text, nullable=False)  # Serialized 128-D vector
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="embeddings")

    def get_vector(self):
        return json.loads(self.embedding_json)

    def set_vector(self, vec):
        if hasattr(vec, "tolist"):
            self.embedding_json = json.dumps(vec.tolist())
        else:
            self.embedding_json = json.dumps([float(x) for x in vec])

class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    session_id = Column(String(50), primary_key=True, index=True)
    classroom = Column(String(100), default="Main-Hall")
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    records = relationship("AttendanceRecord", back_populates="session", cascade="all, delete-orphan")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(50), ForeignKey("attendance_sessions.session_id"), nullable=False)
    student_id = Column(String(50), ForeignKey("students.student_id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(20), default="Present")

    session = relationship("AttendanceSession", back_populates="records")
    student = relationship("Student", back_populates="attendance")

# Initialize Primary and Fallback Engines
primary_engine = None
fallback_engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
FallbackSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=fallback_engine)

if DATABASE_URL and not DATABASE_URL.startswith("sqlite"):
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    try:
        primary_engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={"connect_timeout": 8}
        )
        PrimarySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)
        print(f"[Database] Primary PostgreSQL engine initialized ({primary_engine.url.host}).")
    except Exception as e:
        print(f"[Database Warning] PostgreSQL engine init failed: {e}")
        PrimarySessionLocal = None
else:
    PrimarySessionLocal = None

def init_db():
    if primary_engine:
        try:
            Base.metadata.create_all(bind=primary_engine)
            print("[Database] Supabase schema synchronized successfully.")
        except Exception as e:
            print(f"[Database Warning] Primary DB sync failed: {e}. Syncing fallback SQLite...")
            Base.metadata.create_all(bind=fallback_engine)
    else:
        Base.metadata.create_all(bind=fallback_engine)
        print("[Database] SQLite schema synchronized successfully.")

from sqlalchemy import text

def get_session():
    """Returns an active database session with automatic fallback to SQLite if remote fails."""
    if PrimarySessionLocal:
        try:
            session = PrimarySessionLocal()
            session.execute(text("SELECT 1"))
            return session
        except Exception as e:
            print(f"[Database Fallback] Switching to local DB due to remote error: {e}")
            Base.metadata.create_all(bind=fallback_engine)
            return FallbackSessionLocal()
    else:
        Base.metadata.create_all(bind=fallback_engine)
        return FallbackSessionLocal()

def SessionLocal():
    return get_session()

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
