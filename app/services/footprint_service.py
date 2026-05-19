from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Footprint, UserAnimal, UserPlant
from app.schemas import FootprintResponse


class FootprintService:
    @staticmethod
    def get_user_footprints(
        db: Session,
        user_id: int,
        target_type: Optional[str] = None,
        action_type: Optional[str] = None,
        limit: Optional[int] = 50,
        offset: Optional[int] = 0
    ) -> List[FootprintResponse]:
        """获取用户足迹"""
        query = db.query(Footprint).filter(Footprint.user_id == user_id)

        if target_type:
            query = query.filter(Footprint.target_type == target_type)

        if action_type:
            query = query.filter(Footprint.action_type == action_type)

        footprints = query.order_by(Footprint.created_at.desc()).offset(offset).limit(limit).all()

        result = []
        for fp in footprints:
            result.append(FootprintResponse(
                id=fp.id,
                user_id=fp.user_id,
                action_type=fp.action_type,
                target_type=fp.target_type,
                target_id=fp.target_id,
                target_name=fp.target_name,
                detail=fp.detail,
                change_value=fp.change_value,
                created_at=fp.created_at
            ))
        return result
