from openai import OpenAI
import os
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key="sk-e8b093d306e94a45a3b95c3f390104d8",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
messages = [{"role": "user", "content": "周杰伦是谁一句话告诉我"}]
completion = client.chat.completions.create(
    model="qwen3-1.7b",
    messages=messages,
    extra_body={
        "enable_thinking": True
    },
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    if chunk.choices:
        delta = chunk.choices[0].delta
        # 只收集思考内容
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
            if not is_answering:
                print(delta.reasoning_content, end="", flush=True)
        # 收到content，开始进行回复
        if hasattr(delta, "content") and delta.content:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(delta.content, end="", flush=True)