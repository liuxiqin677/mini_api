from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models import Tool, UserTool
from app.schemas import ToolResponse, ToolDetail, UserToolResponse, UserToolWithDetail, UserToolCollectionResponse


class ToolService:
    @staticmethod
    def get_all_tools(db: Session, user_id: int) -> List[ToolResponse]:
        tools = db.query(Tool).all()
        user_collected_ids = {ut.tool_id for ut in db.query(UserTool.tool_id).filter(UserTool.user_id == user_id).all()}

        result = []
        for tool in tools:
            result.append(ToolResponse(
                id=tool.id,
                name=tool.name,
                emoji=tool.emoji,
                description=tool.description,
                rarity=tool.rarity,
                is_collected=tool.id in user_collected_ids,
                world_ids=tool.world_ids,
                target_ids=tool.target_ids,
                created_at=tool.created_at,
                updated_at=tool.updated_at
            ))
        return result

    @staticmethod
    def get_tool_by_id(db: Session, tool_id: int, user_id: int) -> Optional[ToolDetail]:
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            return None

        user_collected = db.query(UserTool).filter(
            UserTool.user_id == user_id,
            UserTool.tool_id == tool_id
        ).first()

        return ToolDetail(
            id=tool.id,
            name=tool.name,
            emoji=tool.emoji,
            description=tool.description,
            rarity=tool.rarity,
            is_collected=user_collected is not None,
            world_ids=tool.world_ids,
            target_ids=tool.target_ids,
            created_at=tool.created_at,
            updated_at=tool.updated_at
        )

    @staticmethod
    def collect_tool(db: Session, user_id: int, tool_id: int) -> Optional[UserTool]:
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            return None

        # 检查用户是否已经收集过这个工具
        user_tool = db.query(UserTool).filter(
            UserTool.user_id == user_id,
            UserTool.tool_id == tool_id
        ).first()

        if user_tool:
            # 如果已经收集过，数量+1
            user_tool.count += 1
            db.commit()
            db.refresh(user_tool)
            return user_tool
        else:
            # 如果没有收集过，创建新记录
            user_tool = UserTool(
                user_id=user_id,
                tool_id=tool_id,
                name=tool.name,
                description=tool.description,
                rarity=tool.rarity,
                count=1
            )
            db.add(user_tool)
            db.commit()
            db.refresh(user_tool)
            return user_tool

    @staticmethod
    def get_user_tools(db: Session, user_id: int) -> List[UserToolResponse]:
        user_tools = db.query(UserTool).filter(UserTool.user_id == user_id).all()
        tool_ids = [ut.tool_id for ut in user_tools]
        tools = db.query(Tool).filter(Tool.id.in_(tool_ids)).all()
        tool_map = {t.id: t for t in tools}

        result = []
        for ut in user_tools:
            tool = tool_map.get(ut.tool_id)
            emoji = tool.emoji if tool else ""
            result.append(UserToolResponse(
                id=ut.id,
                user_id=ut.user_id,
                tool_id=ut.tool_id,
                name=ut.name,
                emoji=emoji,
                description=ut.description,
                rarity=ut.rarity,
                count=ut.count,
                created_at=ut.created_at,
                updated_at=ut.updated_at
            ))
        return result

    @staticmethod
    def get_user_tools_with_detail(db: Session, user_id: int) -> Tuple[List[UserToolWithDetail], int]:
        """获取用户收集的工具列表，包含工具详情和数量"""
        user_tools = db.query(UserTool).filter(UserTool.user_id == user_id).all()
        tool_ids = [ut.tool_id for ut in user_tools]
        tools = db.query(Tool).filter(Tool.id.in_(tool_ids)).all()
        tool_map = {t.id: t for t in tools}

        result = []
        for ut in user_tools:
            tool = tool_map.get(ut.tool_id)
            if tool:
                tool_response = ToolResponse(
                    id=tool.id,
                    name=tool.name,
                    emoji=tool.emoji,
                    description=tool.description,
                    rarity=tool.rarity,
                    is_collected=True,
                    world_ids=tool.world_ids,
                    target_ids=tool.target_ids,
                    created_at=tool.created_at,
                    updated_at=tool.updated_at
                )
                result.append(UserToolWithDetail(
                    id=ut.id,
                    user_id=ut.user_id,
                    tool_id=ut.tool_id,
                    name=ut.name,
                    emoji=tool.emoji,
                    description=ut.description,
                    rarity=ut.rarity,
                    count=ut.count,
                    tool_detail=tool_response,
                    created_at=ut.created_at,
                    updated_at=ut.updated_at
                ))

        return result, len(result)

    @staticmethod
    def edit_tool_name(db: Session, user_tool_id: int, user_id: int, name: str) -> Optional[UserTool]:
        user_tool = db.query(UserTool).filter(
            UserTool.id == user_tool_id,
            UserTool.user_id == user_id
        ).first()
        if not user_tool:
            return None

        user_tool.name = name
        db.commit()
        db.refresh(user_tool)
        return user_tool

    @staticmethod
    def delete_tool(db: Session, user_tool_id: int, user_id: int) -> bool:
        user_tool = db.query(UserTool).filter(
            UserTool.id == user_tool_id,
            UserTool.user_id == user_id
        ).first()
        if not user_tool:
            return False

        db.delete(user_tool)
        db.commit()
        return True
