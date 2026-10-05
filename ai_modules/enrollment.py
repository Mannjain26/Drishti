import numpy as np
from database import SessionLocal, Student, FaceEmbedding
from detector.student_store import StudentStore
from detector.protected_store import ProtectedRepresentationStore

local_student_store = StudentStore("data/students.db")
local_rep_store = ProtectedRepresentationStore("data/protected_keys/face_rep.key")

class EnrollmentService:
    @staticmethod
    def enroll_student(student_id: str, name: str, batch: str, frame_embeddings: list) -> tuple:
        """Averages multiple face embeddings and stores them in both DB and detector ProtectedRepresentationStore."""
        if not frame_embeddings:
            return False, "No facial embeddings provided."

        # Average the 128D embeddings and normalize
        avg_vector = np.mean(frame_embeddings, axis=0)
        norm = np.linalg.norm(avg_vector)
        if norm > 0:
            avg_vector = avg_vector / norm
        
        vector_to_save = [float(x) for x in avg_vector]

        # 1. Save into local detector StudentStore & ProtectedRepresentationStore (DPDP 2023 compliance)
        try:
            token = local_rep_store.protect(np.asarray(avg_vector, dtype=np.float32))
            local_student_store.upsert(
                student_id=student_id,
                name=name,
                batch=batch,
                representation=token,
                sample_count=len(frame_embeddings),
                quality_score=0.95,
                consent_confirmed=True
            )
        except Exception as e:
            print(f"[Detector StudentStore Sync Warning] {e}")

        # 2. Save into Supabase PostgreSQL / SQLite
        db = SessionLocal()
        try:
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if not student:
                student = Student(student_id=student_id, name=name, batch=batch)
                db.add(student)
                db.commit()
            else:
                student.name = name
                student.batch = batch
                db.commit()

            # Save / update embedding
            existing_emb = db.query(FaceEmbedding).filter(FaceEmbedding.student_id == student_id).first()
            if existing_emb:
                existing_emb.set_vector(vector_to_save)
            else:
                new_emb = FaceEmbedding(student_id=student_id)
                new_emb.set_vector(vector_to_save)
                db.add(new_emb)

            db.commit()
            return True, "Enrolled successfully."
        except Exception as e:
            db.rollback()
            print(f"[Enrollment Error] {e}")
            return False, str(e)
        finally:
            db.close()
