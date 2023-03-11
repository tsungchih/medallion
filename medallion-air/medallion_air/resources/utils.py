from typing import Any

from dagster import DagsterEventType, OutputContext


def get_output_metadata_entries(self, entry_keys: list[str], ctx: OutputContext) -> dict[str, Any]:
    all_handled_output_logs = ctx.step_context.instance.all_logs(
        ctx.step_context.run_id, of_type=DagsterEventType.HANDLED_OUTPUT
    )
    step_handled_output_log = [
        log for log in all_handled_output_logs if log.step_key == ctx.step_key
    ][0]
    metadata = step_handled_output_log.dagster_event.event_specific_data.metadata_entries
    results = {}
    target_entries = [entry for entry in metadata if entry.label in entry_keys]
    for entry in target_entries:
        results[entry.label] = entry.entry_data.value
    return results
