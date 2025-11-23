from fastapi import APIRouter
from database.core import DbSession
from entities.table import Feedback, Picture
from sqlalchemy import func, case

dashboard_route = APIRouter()


@dashboard_route.get("/dashboard")
async def get_dashboard(db: DbSession):
    """
    Get dashboard statistics including:
    - Total pictures uploaded
    - Total feedback received
    - Feedback grouped by date with correct/incorrect counts
    """

    # Get total pictures
    total_pictures = db.query(func.count(Picture.id)).scalar()

    # Get total feedback
    total_feedback = db.query(func.count(Feedback.id)).scalar()

    # Get feedback by date with correct/incorrect counts
    # A feedback is "correct" if the correct_label matches the picture's label
    feedback_by_date = (
        db.query(
            func.date(Feedback.created_at).label("date"),
            func.sum(case((Feedback.correct_label == Picture.label, 1), else_=0)).label(
                "correct"
            ),
            func.sum(case((Feedback.correct_label != Picture.label, 1), else_=0)).label(
                "incorrect"
            ),
        )
        .join(Picture, Feedback.picture_id == Picture.id)
        .group_by(func.date(Feedback.created_at))
        .order_by(func.date(Feedback.created_at))
        .all()
    )

    # Format the data for the frontend
    chart_data = [
        {
            "date": str(row.date),
            "correct": int(row.correct) if row.correct else 0,
            "incorrect": int(row.incorrect) if row.incorrect else 0,
        }
        for row in feedback_by_date
    ]

    return {
        "total_pictures": total_pictures or 0,
        "total_feedback": total_feedback or 0,
        "feedback_by_date": chart_data,
    }
