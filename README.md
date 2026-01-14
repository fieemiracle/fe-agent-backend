## Fe Agent Backend

### Install

```bash
# 安装单个依赖
pip install xxx
# or
pip install xxx=xx.xx.xx

# 升级依赖
pip install --upgrade xxxx
# or
pip install -U xxxx
# or
pip install --upgrade -r requirements.txt

# 查看可升级的包
pip list --outdated
```

### Run

```bash
uvicorn app:main:app --reload
```

### Router

例如创建路由为: `/api/asst/stream`

#### 创建新的路由分组(推荐)

(1)创建 endpoint 文件: app/api/asst/endpoints/stream.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/stream")
async def create_stream():
    return {
        "message": "Stream created"
    }
```

(2)创建 asst 路由器：app/api/asst/router.py

```python
from fastapi import APIRouter
from app.api.asst.endpoints import stream

asst_router = APIRouter()
asst_router.include_router(stream.router, tags=["assistant"])
```

(3)在`main.py`中注册

```python
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.api.asst.router import asst_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
    )

    app.include_router(api_router, prefix="/api/v1")
    app.include_router(asst_router, prefix="/api/asst")  # 新增

    return app


app = create_app()
```

#### 直接在v1路由中添加

(1)创建：app/api/v1/endpoints/assistant.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/asst/stream")
async def create_stream():
    return {
        "message": "Stream created"
    }
```

(2)在`app/api/v1/router.py`引入

```python
from fastapi import APIRouter
from app.api.v1.endpoints import health, assistant

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(assistant.router, tags=["assistant"])
```

#### 完全自定义路由(不推荐)

直接在 `main.py` 中定义：

```python
@app.post("/api/asst/stream")
async def create_stream():
    return {"message": "Stream created"}
```

### Common Command

```bash
# 1. 安装新包
pip install openai

# 2. 安装指定版本
pip install openai==1.12.0

# 3. 升级包
pip install --upgrade openai

# 4. 卸载包
pip uninstall openai

# 5. 查看已安装的包
pip list

# 6. 查看某个包的详细信息
pip show openai

# 7. 查看过时的包
pip list --outdated

# 8. 从 requirements.txt 安装所有依赖
pip install -r requirements.txt

# 9. 导出当前环境的所有包
pip freeze > requirements.txt

# 10. 升级 pip 本身
pip install --upgrade pip
```

### Format

```bash
black app/
```
