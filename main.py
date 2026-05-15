from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn
import os

from app.api.v1 import router as v1_router
from app.database import engine, Base
from app.schemas import ApiResponse

load_dotenv()

app = FastAPI(
    title="Mini API",
    description="A simple API for animal data",
    version="1.0.0",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail, "data": None},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Error: {exc}")
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": str(exc), "data": None},
    )

# 包含路由
app.include_router(v1_router, prefix="/api/v1")

# 根路由
@app.get("/", response_model=ApiResponse)
async def root():
    return ApiResponse(
        code=200,
        message="success",
        data={
            "name": "Mini API",
            "version": "1.0.0",
            "docs": "/docs",
        },
    )

# 健康检查
@app.get("/health", response_model=ApiResponse)
async def health():
    return ApiResponse(
        code=200,
        message="success",
        data={"status": "ok"},
    )

# 示例：返回布尔值
@app.get("/example/bool", response_model=ApiResponse)
async def example_bool():
    return ApiResponse(
        code=200,
        message="success",
        data=True,
    )

# 示例：返回字符串
@app.get("/example/string", response_model=ApiResponse)
async def example_string():
    return ApiResponse(
        code=200,
        message="success",
        data="hello world",
    )

# 示例：返回数字
@app.get("/example/number", response_model=ApiResponse)
async def example_number():
    return ApiResponse(
        code=200,
        message="success",
        data=42,
    )

# 示例：返回对象
@app.get("/example/object", response_model=ApiResponse)
async def example_object():
    return ApiResponse(
        code=200,
        message="success",
        data={"name": "test", "value": 123},
    )

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    uvicorn.run("main:app", host=host, port=port, reload=debug)
