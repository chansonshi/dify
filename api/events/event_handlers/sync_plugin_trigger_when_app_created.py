import logging

from events.app_event import app_draft_workflow_was_synced
from models.model import App, AppMode
from models.workflow import Workflow
from services.workflow_plugin_trigger_service import WorkflowPluginTriggerService

logger = logging.getLogger(__name__)


@app_draft_workflow_was_synced.connect
def handle(sender, synced_draft_workflow: Workflow, **kwargs):
    """
    While creating a workflow or updating a workflow, we may need to sync
    its plugin trigger relationships in DB.
    """
    app: App = sender
    if app.mode != AppMode.WORKFLOW.value:
        # only handle workflow app, chatflow is not supported yet
        return

    WorkflowPluginTriggerService.sync_plugin_trigger_relationships(app, synced_draft_workflow)
