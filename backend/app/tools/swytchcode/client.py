from typing import Any, Protocol


class ToolExecutor(Protocol):
    def execute(self, canonical_id: str,
                args: dict[str, Any]) -> dict[str, Any]: ...


class SwytchcodeExecutor:
    """Calls only enabled Swytchcode tools; it never constructs provider HTTP requests."""

    def __init__(self, demo_mode: bool = True) -> None:
        self.demo_mode = demo_mode

    def execute(self, canonical_id: str, args: dict[str, Any]) -> dict[str, Any]:
        if self.demo_mode:
            from app.tools.swytchcode.demo import demo_execute

            return demo_execute(canonical_id, args)

        try:
            from swytchcode_runtime import exec as swytchcode_exec
        except ImportError as error:
            raise RuntimeError(
                "Install swytchcode-runtime and configure the Swytchcode CLI before disabling DEMO_MODE."
            ) from error

        result = swytchcode_exec(canonical_id, args)
        if not isinstance(result, dict):
            raise RuntimeError(
                f"Unexpected Swytchcode response for {canonical_id}")
        return result
