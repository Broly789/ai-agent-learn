import json
import os
from pathlib import Path
import pickle, base64

from typing import Sequence, Any
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, CheckpointTuple, CheckpointMetadata, Checkpoint, ChannelVersions
from app.code_agent.tools.file_tools import file_tools
from app.code_agent.model.qwen import llm_qwen

class FileSaver(BaseCheckpointSaver[str]):
    def __init__(self, base_path: str = "/Users/brolylee/2026web/ai-agent/.temp/checkpoint"):
        self.base_path = base_path

        os.makedirs(self.base_path, exist_ok=True)
    def get_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        """Fetch a checkpoint tuple using the given configuration.

             Args:
                 config: Configuration specifying which checkpoint to retrieve.

             Returns:
                 The requested checkpoint tuple, or `None` if not found.

             Raises:
                 NotImplementedError: Implement this method in your custom checkpoint saver.
             """
        thread_id = config["configurable"].get("thread_id")
        dir_path = os.path.join(self.base_path, str(thread_id))
        checkpoint_files = list(Path(dir_path).glob("*.json"))
        checkpoint_files.sort(key=lambda x: x.stem, reverse=True)
        latest_checkpoint = checkpoint_files[0]
        checkpoint_id = latest_checkpoint.stem
        checkpoint_file_path = self._get_checkpoint_path(thread_id, checkpoint_id)
        with open(checkpoint_file_path, "r", encoding="utf-8") as f:
            checkpoint_data = json.load(f)

        checkpoint = self._deserialize_checkpoint(checkpoint_data["checkpoint"])
        metadata = self._deserialize_checkpoint(checkpoint_data["metadata"])
        return CheckpointTuple(
            config={
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_id": checkpoint_id,
                },
            },
            checkpoint=checkpoint,
            metadata=metadata,
        )

    def _deserialize_checkpoint(self, data) -> Any:
        data = base64.b64decode(data.encode("utf-8"))
        return pickle.loads(data)

    def _serialize_checkpoint(self, data) -> str:
         data = pickle.dumps(data)
         return base64.b64encode(data).decode("utf-8")

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        """Store a checkpoint with its configuration and metadata.

        Args:
            config: Configuration for the checkpoint.
            checkpoint: The checkpoint to store.
            metadata: Additional metadata for the checkpoint.
            new_versions: New channel versions as of this write.

        Returns:
            RunnableConfig: Updated configuration after storing the checkpoint.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        thread_id = config["configurable"]["thread_id"]
        checkpoint_path = self._get_checkpoint_path(thread_id, checkpoint["id"])
        checkpoint_data = {
            "checkpoint": self._serialize_checkpoint(checkpoint),
            "metadata": self._serialize_checkpoint(metadata),
        }
        with open(checkpoint_path, "w") as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_id": checkpoint["id"],
            }
        }

    def _get_checkpoint_path(self, thread_id: str, checkpoint_id: str):
        dir_path = os.path.join(self.base_path, str(thread_id))
        os.makedirs(dir_path, exist_ok=True)
        return os.path.join(dir_path, checkpoint_id + ".json")

    def put_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Store intermediate writes linked to a checkpoint.

        Args:
            config: Configuration of the related checkpoint.
            writes: List of writes to store.
            task_id: Identifier for the task creating the writes.
            task_path: Path of the task creating the writes.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        print("put_writes")

if __name__ == "__main__":
    memory = FileSaver()
    agent = create_agent(
        model=llm_qwen,
        tools=file_tools,
        checkpointer=memory,
        # system_prompt="你是一个智能助手，你可以读取文件内容并根据文件内容回答问题。",
        debug=True,
    )
    config = RunnableConfig(configurable={"thread_id": 1})
    # res = agent.invoke(input={"messages": [HumanMessage(content="我叫Broly，我喜欢周杰伦")]}, config=config)
    res = agent.invoke(input={"messages": [HumanMessage(content="我叫什么，我喜欢什么")]}, config=config)
    print(res)
