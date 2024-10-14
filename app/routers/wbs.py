# app/routers/wbs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.wbs import Wbs
from app.models.activity import Activity
from app.schemas.wbs import WbsCreate, WbsResponse
from app.schemas.activity import ActivityResponse

router = APIRouter()

def filter_activity(activities):
    activity_map = {activity.activityID: ActivityResponse.from_orm(activity) for activity in activities}
    root_activities = []

    for activity in activities:
        if activity.parentActivityId is 0 or None:
            root_activities.append(activity_map[activity.activityID])

    return root_activities

@router.get("/wbs", response_model=List[WbsResponse])
def get_wbs_list(db: Session = Depends(get_db)):
    return db.query(Wbs).all()

@router.get("/wbs/{wbs_id}", response_model=WbsResponse)
def get_wbs(wbs_id: int, db: Session = Depends(get_db)):
    wbs = db.query(Wbs).filter(Wbs.wbsId == wbs_id).first()
    if wbs is None:
        raise HTTPException(status_code=404, detail="WBS not found")
    wbs_response = WbsResponse.from_orm(wbs)
    wbs_response.activities = filter_activity(wbs.activities)
    return wbs_response

@router.get("/wbs/{wbs_id}/activities", response_model=List[ActivityResponse])
def get_wbs_activities(wbs_id: int, db: Session = Depends(get_db)):
    activities = db.query(Activity).filter(Activity.wbsId == wbs_id).all()
    return filter_activity(activities)

@router.post("/wbs", response_model=WbsResponse)
def create_wbs(wbs: WbsCreate, db: Session = Depends(get_db)):
    db_wbs = Wbs(**wbs.dict(by_alias=True))
    db.add(db_wbs)
    db.commit()
    db.refresh(db_wbs)
    return db_wbs

@router.put("/wbs/{wbs_id}", response_model=WbsResponse)
def update_wbs(wbs_id: int, wbs: WbsCreate, db: Session = Depends(get_db)):
    db_wbs = db.query(Wbs).filter(Wbs.wbsId == wbs_id).first()
    if db_wbs is None:
        raise HTTPException(status_code=404, detail="WBS not found")
    for key, value in wbs.dict(by_alias=True).items():
        setattr(db_wbs, key, value)
    db.commit()
    db.refresh(db_wbs)
    return db_wbs

@router.delete("/wbs/{wbs_id}", status_code=204)
def delete_wbs(wbs_id: int, db: Session = Depends(get_db)):
    wbs = db.query(Wbs).filter(Wbs.wbsId == wbs_id).first()
    if wbs is None:
        raise HTTPException(status_code=404, detail="WBS not found")
    db.delete(wbs)
    db.commit()
    return {"ok": True}