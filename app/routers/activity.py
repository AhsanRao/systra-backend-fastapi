# app/routers/activity.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityResponse

router = APIRouter()

@router.get("/activities", response_model=List[ActivityResponse])
def get_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()

@router.get("/activities/suggestions", response_model=List[str])
def get_activity_name_suggestions(db: Session = Depends(get_db)):
    return db.query(Activity.activityName).filter(Activity.parentActivityId == None).distinct().all()

@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.activityID == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.post("/activities", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = Activity(**activity.dict(by_alias=True))
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.put("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = db.query(Activity).filter(Activity.activityID == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    for key, value in activity.dict(by_alias=True).items():
        setattr(db_activity, key, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.delete("/activities/{activity_id}", status_code=204)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.activityID == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(activity)
    db.commit()
    return {"ok": True}