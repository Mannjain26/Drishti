import numpy as np
from database import SessionLocal, Student, FaceEmbedding

class EnrollmentService:
    @staticmethod
    def enroll_student(student_id: str, name: str, batch: str, frame_embeddings: list) -> bool:
        """Averages multiple face embeddings and stores them safely in DB."""
        if not frame_embeddings:
            return False

        # Average the 128D embeddings and normalize
        avg_vector = np.mean(frame_embeddings, axis=0)
        norm = np.linalg.norm(avg_vector)
        if norm > 0:
            avg_vector = avg_vector / norm

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
                existing_emb.set_vector(avg_vector)
            else:
                new_emb = FaceEmbedding(student_id=student_id)
                new_emb.set_vector(avg_vector)
                db.add(new_emb)

            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"[Enrollment Error] {e}")
            return False
        finally:
            db.close()
