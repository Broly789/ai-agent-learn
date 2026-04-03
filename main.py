from langchain_ollama import ChatOllama

def main():
    llm = ChatOllama(model="qwen3:latest")
    result = llm.stream("一句话介绍下周杰伦 是周杰伦")
    for chunk in result:
        print(chunk.content, end="")


if __name__ == "__main__":
    main()
