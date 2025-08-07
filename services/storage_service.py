"""
Storage service for managing candidate data persistence
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from config.settings import settings
from models.candidate import CandidateDatabase, InterviewSummary, CandidateInfo
from utils.logger import logger, log_error
from utils.helpers import generate_session_id, sanitize_filename

class StorageService:
    """Service for handling data storage and retrieval"""

    def __init__(self):
        self.data_dir = Path(settings.DATA_DIR)
        self.candidates_file = Path(settings.CANDIDATES_FILE)
        self.session_id = generate_session_id()
        self._ensure_data_directory()

    def _ensure_data_directory(self) -> None:
        """Ensure data directory exists"""
        try:
            self.data_dir.mkdir(exist_ok=True)
            logger.info("Data directory ensured", path=str(self.data_dir))
        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "ensure_data_directory"})

    def save_candidate_data(self, candidate_data: Dict[str, Any], session_id: str) -> bool:
        """Save candidate data to storage"""
        try:
            # Load existing database
            database = self._load_database()

            # Create candidate info
            candidate_info = CandidateInfo(
                name=candidate_data["name"],
                email=candidate_data["email"],
                phone=candidate_data["phone"],
                experience_years=candidate_data["experience_years"],
                tech_stack=candidate_data["tech_stack"]
            )

            # Calculate interview metrics
            responses = candidate_data.get("responses", [])
            questions = candidate_data.get("technical_questions", [])

            # Create interview summary
            summary = InterviewSummary(
                session_id=session_id,
                candidate_info=candidate_info,
                interview_date=datetime.now(),
                technical_questions_count=len(questions),
                responses_count=len(responses),
                completion_percentage=self._calculate_completion_percentage(candidate_data),
                notes=self._generate_interview_notes(candidate_data)
            )

            # Check if candidate already exists (by email)
            existing_candidate = database.get_candidate_by_email(candidate_info.email)
            if existing_candidate:
                # Update existing candidate
                existing_candidate.interview_date = datetime.now()
                existing_candidate.technical_questions_count = len(questions)
                existing_candidate.responses_count = len(responses)
                existing_candidate.completion_percentage = summary.completion_percentage
                existing_candidate.notes = summary.notes
                logger.info("Updated existing candidate", email=candidate_info.email)
            else:
                # Add new candidate
                database.add_candidate(summary)
                logger.info("Added new candidate", email=candidate_info.email)

            # Save database
            self._save_database(database)

            # Save detailed session data
            self._save_session_data(candidate_data, session_id)

            return True

        except Exception as e:
            log_error(logger, e, self.session_id, {
                "action": "save_candidate_data",
                "session_id": session_id
            })
            return False

    def _load_database(self) -> CandidateDatabase:
        """Load candidate database from file"""
        try:
            if self.candidates_file.exists():
                with open(self.candidates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return CandidateDatabase(**data)
            else:
                return CandidateDatabase()
        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "load_database"})
            return CandidateDatabase()

    def _save_database(self, database: CandidateDatabase) -> None:
        """Save candidate database to file"""
        try:
            with open(self.candidates_file, 'w', encoding='utf-8') as f:
                json.dump(database.dict(), f, indent=2, default=str, ensure_ascii=False)
            logger.info("Database saved successfully", candidate_count=database.total_candidates)
        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "save_database"})

    def _save_session_data(self, candidate_data: Dict[str, Any], session_id: str) -> None:
        """Save detailed session data"""
        try:
            session_file = self.data_dir / f"session_{session_id}.json"

            session_data = {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "candidate_data": candidate_data,
                "completion_percentage": self._calculate_completion_percentage(candidate_data)
            }

            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, default=str, ensure_ascii=False)

            logger.info("Session data saved", session_id=session_id)

        except Exception as e:
            log_error(logger, e, self.session_id, {
                "action": "save_session_data",
                "session_id": session_id
            })

    def get_candidate_by_email(self, email: str) -> Optional[InterviewSummary]:
        """Get candidate by email"""
        try:
            database = self._load_database()
            return database.get_candidate_by_email(email)
        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "get_candidate_by_email"})
            return None

    def get_all_candidates(self) -> List[InterviewSummary]:
        """Get all candidates"""
        try:
            database = self._load_database()
            return database.candidates
        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "get_all_candidates"})
            return []

    def get_candidates_by_tech_stack(self, tech: str) -> List[InterviewSummary]:
        """Get candidates by technology"""
        try:
            database = self._load_database()
            return database.get_candidates_by_tech_stack(tech)
        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "get_candidates_by_tech_stack"})
            return []

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            database = self._load_database()
            candidates = database.candidates

            if not candidates:
                return {
                    "total_candidates": 0,
                    "completed_interviews": 0,
                    "average_completion": 0,
                    "top_technologies": [],
                    "experience_distribution": {}
                }

            # Calculate statistics
            completed_count = sum(1 for c in candidates if c.completion_percentage >= 100)
            avg_completion = sum(c.completion_percentage for c in candidates) / len(candidates)

            # Technology analysis
            tech_counts = {}
            experience_dist = {"junior": 0, "mid": 0, "senior": 0}

            for candidate in candidates:
                # Count technologies
                tech_stack = candidate.candidate_info.tech_stack.lower()
                for tech in tech_stack.split():
                    tech_clean = tech.strip('.,')
                    if len(tech_clean) > 2:
                        tech_counts[tech_clean] = tech_counts.get(tech_clean, 0) + 1

                # Count experience levels
                years = candidate.candidate_info.experience_years
                if years <= 2:
                    experience_dist["junior"] += 1
                elif years <= 5:
                    experience_dist["mid"] += 1
                else:
                    experience_dist["senior"] += 1

            # Get top technologies
            top_tech = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:10]

            return {
                "total_candidates": len(candidates),
                "completed_interviews": completed_count,
                "average_completion": round(avg_completion, 2),
                "top_technologies": top_tech,
                "experience_distribution": experience_dist,
                "last_updated": database.last_updated.isoformat() if database.last_updated else None
            }

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "get_database_stats"})
            return {"error": str(e)}

    def export_candidates_csv(self) -> Optional[str]:
        """Export candidates to CSV format"""
        try:
            import pandas as pd

            candidates = self.get_all_candidates()
            if not candidates:
                return None

            # Prepare data for CSV
            csv_data = []
            for candidate in candidates:
                info = candidate.candidate_info
                csv_data.append({
                    "Name": info.name,
                    "Email": info.email,
                    "Phone": info.phone,
                    "Experience_Years": info.experience_years,
                    "Tech_Stack": info.tech_stack,
                    "Interview_Date": candidate.interview_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "Questions_Count": candidate.technical_questions_count,
                    "Responses_Count": candidate.responses_count,
                    "Completion_Percentage": candidate.completion_percentage,
                    "Status": candidate.status,
                    "Session_ID": candidate.session_id
                })

            # Create DataFrame and CSV
            df = pd.DataFrame(csv_data)
            csv_filename = f"candidates_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            csv_path = self.data_dir / csv_filename

            df.to_csv(csv_path, index=False, encoding='utf-8')

            logger.info("Candidates exported to CSV", filename=csv_filename, count=len(csv_data))
            return str(csv_path)

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "export_candidates_csv"})
            return None

    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        """Clean up old session files"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 3600)
            cleaned_count = 0

            for session_file in self.data_dir.glob("session_*.json"):
                if session_file.stat().st_mtime < cutoff_date:
                    session_file.unlink()
                    cleaned_count += 1

            logger.info("Cleaned up old sessions", count=cleaned_count, days_old=days_old)
            return cleaned_count

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "cleanup_old_sessions"})
            return 0

    def backup_database(self) -> Optional[str]:
        """Create backup of the database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"candidates_backup_{timestamp}.json"
            backup_path = self.data_dir / backup_filename

            # Copy current database to backup
            if self.candidates_file.exists():
                import shutil
                shutil.copy2(self.candidates_file, backup_path)

                logger.info("Database backup created", filename=backup_filename)
                return str(backup_path)
            else:
                logger.warning("No database file to backup")
                return None

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "backup_database"})
            return None

    def _calculate_completion_percentage(self, candidate_data: Dict[str, Any]) -> float:
        """Calculate completion percentage"""
        required_fields = ["name", "email", "phone", "experience_years", "tech_stack"]
        completed_fields = sum(1 for field in required_fields if candidate_data.get(field))

        base_percentage = (completed_fields / len(required_fields)) * 80  # 80% for basic info

        # Add percentage for technical questions
        questions = candidate_data.get("technical_questions", [])
        responses = candidate_data.get("responses", [])

        if questions:
            question_percentage = (len(responses) / len(questions)) * 20  # 20% for questions
            return min(base_percentage + question_percentage, 100.0)

        return base_percentage

    def _generate_interview_notes(self, candidate_data: Dict[str, Any]) -> str:
        """Generate interview notes"""
        notes = []

        # Basic info notes
        experience = candidate_data.get("experience_years", 0)
        tech_stack = candidate_data.get("tech_stack", "")

        if experience == 0:
            notes.append("New to technology field")
        elif experience <= 2:
            notes.append("Junior level candidate")
        elif experience <= 5:
            notes.append("Mid-level candidate")
        else:
            notes.append("Senior level candidate")

        # Tech stack analysis
        if "python" in tech_stack.lower():
            notes.append("Python experience")
        if "javascript" in tech_stack.lower():
            notes.append("JavaScript experience")
        if "react" in tech_stack.lower():
            notes.append("React experience")
        if "aws" in tech_stack.lower() or "azure" in tech_stack.lower() or "cloud" in tech_stack.lower():
            notes.append("Cloud experience")

        # Question completion
        questions = candidate_data.get("technical_questions", [])
        responses = candidate_data.get("responses", [])

        if questions and responses:
            completion_rate = len(responses) / len(questions)
            if completion_rate >= 1.0:
                notes.append("Completed all technical questions")
            elif completion_rate >= 0.5:
                notes.append("Completed most technical questions")
            else:
                notes.append("Partially completed technical questions")

        return "; ".join(notes) if notes else "Standard screening completed"

# Global storage service instance
storage_service = StorageService()
