from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api import deps
from app.models.content import Content
from app.models.user import User
from app.schemas.content import ContentCreate, Content as ContentSchema
from app.services.ai_service import ai_service

router = APIRouter()

async def process_content_background(content_id: int, db: Session):
    """
    Background task to process content with AI.
    """
    # Re-fetch content to ensure we have the latest state (though we just created it)
    # Ideally, we should use a fresh session or handle session scope carefully in background tasks.
    # For simplicity in this assignment, we'll try to use the passed session, 
    # but in production, a new session is safer for background tasks.
    
    # Let's create a new session for the background task to be safe
    from app.db.session import SessionLocal
    background_db = SessionLocal()
    try:
        content = background_db.query(Content).filter(Content.id == content_id).first()
        if content:
            result = await ai_service.analyze_text(content.body)
            content.summary = result["summary"]
            content.sentiment = result["sentiment"]
            background_db.add(content)
            background_db.commit()
    finally:
        background_db.close()

@router.post("/", response_model=ContentSchema)
async def create_content(
    *,
    db: Session = Depends(deps.get_db),
    content_in: ContentCreate,
    current_user: User = Depends(deps.get_current_user),
    background_tasks: BackgroundTasks
) -> Any:
    """
    Create new content and trigger AI processing.
    """
    content = Content(
        title=content_in.title,
        body=content_in.body,
        owner_id=current_user.id,
    )
    db.add(content)
    db.commit()
    db.refresh(content)

    # Trigger background task
    background_tasks.add_task(process_content_background, content.id, db)

    return content

@router.get("/", response_model=List[ContentSchema])
def read_contents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve contents.
    """
    contents = db.query(Content).filter(Content.owner_id == current_user.id).offset(skip).limit(limit).all()
    return contents

@router.get("/{id}", response_model=ContentSchema)
def read_content(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get content by ID.
    """
    content = db.query(Content).filter(Content.id == id, Content.owner_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.delete("/{id}", response_model=ContentSchema)
def delete_content(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete content.
    """
    content = db.query(Content).filter(Content.id == id, Content.owner_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(content)
    db.commit()
    return content
