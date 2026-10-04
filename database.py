import json
import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv

# Load .env configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Check for Supabase / PostgreSQL Database URL
DATABASE_URL = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")

if not DATABASE_URL or DATABASE_URL.startswith("sqlite"):
    # Fallback to local SQLite if no Supabase URL provided
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'attendance.db')}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    print("[Database] Connected to Local SQLite Database.")
else:
    # Ensure standard postgresql+psycopg2 scheme for SQLAlchemy
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    # Configure PostgreSQL Engine with connection pooling and pre-ping
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300
    )
    print("[Database] Connected to Supabase PostgreSQL Database.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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
        self.embedding_json = json.dumps(list(vec))

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

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
