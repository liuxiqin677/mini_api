from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import (
    ToolResponse, ToolDetail, UserToolResponse, ApiResponse,
    CollectToolRequest, UseToolRequest, EditToolNameRequest, DeleteToolRequest,
    UserToolCollectionResponse
)
from app.services.tool_service import ToolService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/tools/list", response_model=ApiResponse[List[ToolResponse]])
async def get_tools_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tools = ToolService.get_all_tools(db, current_user.id)
    return ApiResponse(code=200, message="success", data=tools)


@router.get("/tools/detail", response_model=ApiResponse[ToolDetail])
async def get_tool_detail(
    tool_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tool = ToolService.get_tool_by_id(db, tool_id, current_user.id)
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    return ApiResponse(code=200, message="success", data=tool)


@router.post("/user/collect/tool", response_model=ApiResponse)
async def collect_tool(
    request: CollectToolRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_tool = ToolService.collect_tool(db, current_user.id, request.tool_id)
    if not user_tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    return ApiResponse(code=200, message="收集成功", data=True)


@router.post("/user/collect/tool/use", response_model=ApiResponse)
async def use_tool(
    request: UseToolRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """使用一个工具"""
    ToolService.use_tool(db, current_user.id, request.tool_id)
    return ApiResponse(code=200, message="使用成功", data=True)


@router.get("/user/collect/tool/list", response_model=ApiResponse[List[UserToolResponse]])
async def get_user_tools(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tools = ToolService.get_user_tools(db, current_user.id)
    return ApiResponse(code=200, message="success", data=tools)


@router.get("/user/collect/tool/list-with-detail", response_model=ApiResponse[UserToolCollectionResponse])
async def get_user_tools_with_detail(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户收集的工具列表，包含工具详情和数量"""
    items, total_count = ToolService.get_user_tools_with_detail(db, current_user.id)
    return ApiResponse(code=200, message="success", data={
        "items": items,
        "total_count": total_count
    })


@router.post("/user/collect/tool/edit", response_model=ApiResponse)
async def edit_tool_name(
    request: EditToolNameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_tool = ToolService.edit_tool_name(db, request.tool_id, current_user.id, request.name)
    if not user_tool:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="编辑成功", data=True)


@router.delete("/user/collect/tool/delete", response_model=ApiResponse)
async def delete_tool(
    request: DeleteToolRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = ToolService.delete_tool(db, request.tool_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return ApiResponse(code=200, message="删除成功", data=True)
