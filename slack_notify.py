from ansible.plugins.callback import CallbackBase
import requests
import json

SLACK_WEBHOOK_URL='Slack-URL'

class CallbackModule(CallbackBase):

    CALLBACK_VERSION=2.0
    CALLBACK_TYPE="notifications"
    CALLBACK_NAME="slack_notify"
    CALLBACK_NEED_WHITELIST=False

    def send_slack_message(self,message):
        payload={"text":message}
        headers={"Content-Type":"application/json"}
        requests.post(SLACK_WEBHOOK_URL,data=json.dumps(payload),headers=headers)

    def v2_playbook_on_start(self,playbook):
        self.send_slack_message(f"PlayBook {playbook._file_name} started")

    def v2_runner_on_ok(self,result):
        task_name=result.task_name or "unnamed"
        self.send_slack_message(f"Task {task_name} successed on {result._host.get_name()}")

    def v2_runner_on_failed(self,result,ignore_errors=False):
        task_name=result.task_name or "unnamed"
        self.send_slack_message(f"Task {task_name} Failed on {result._host.get_name()}")
    
    def v2_playbook_on_stats(self,stats):
        summary=stats.summarize('localhost')
        message=f"Succeded:{summary['ok']} Failed:{summary['failures']} Skipped:{summary['skipped']}"
        print(message)
        self.send_slack_message(message)
