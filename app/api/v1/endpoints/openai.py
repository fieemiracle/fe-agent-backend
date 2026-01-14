from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from openai import APIError, OpenAI, RateLimitError
from pydantic import BaseModel, Field

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

print(settings.OPENAI_API_KEY)

router = APIRouter()


class ChatMessage(BaseModel):
    role: str = Field(..., description="消息角色：system, user, assistant")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    model: str = Field(default="gpt-3.5-turbo", description="使用的模型")
    messages: List[ChatMessage] = Field(..., description="对话消息列表")
    stream: bool = Field(default=False, description="是否使用流式输出")
    temperature: Optional[float] = Field(default=1.0, ge=0, le=2, description="温度参数")
    max_tokens: Optional[int] = Field(default=None, description="最大 token 数")


@router.post("/openai/chat")
def chat(request: ChatRequest):
    try:
        # 将 Pydantic 模型转换为字典
        messages = [msg.model_dump() for msg in request.messages]

        response = client.chat.completions.create(
            model=request.model,
            messages=messages,
            stream=request.stream,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        # 如果是流式输出
        if request.stream:

            def generate():
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            return StreamingResponse(generate(), media_type="text/event-stream")

        # 非流式输出
        return {
            "message": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        }
    except RateLimitError as e:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "OpenAI API 配额不足",
                "message": "请检查 OpenAI 账户余额和账单设置",
                "solution": "访问https://platform.openai.com/account/billing/overview充值",
                "original_error": str(e),
            },
        )
    except APIError as e:
        raise HTTPException(status_code=500, detail={"error": "OpenAI API 错误", "message": str(e)})
