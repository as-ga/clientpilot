# ClientPilot Demo Script

## 0:00-0:20: Problem

Client teams lose time moving between project context, issue trackers, internal chat, and email. A status dashboard can show those systems, but it cannot decide what the blocker means or execute the follow-up.

## 0:20-0:35: Prompt

Open the Agent screen and submit:

> Check Acme Corp and handle anything blocking their project.

## 0:35-1:40: Agent workflow

Point out the live event stream:

1. ClientPilot understands the request and finds Acme Corp in Notion.
2. It checks Jira and finds ACME-102 blocked.
3. Because Jira alone does not explain the blocker, the graph conditionally searches Slack.
4. Slack reveals that payment API credentials are missing.
5. The agent decides that the client must provide an input and that engineering needs context.

## 1:40-2:00: Actions

Show the completed action events:

- Jira issue updated.
- Engineering notified in Slack.
- Client contacted through Gmail.
- Final result reports the blocker and each action outcome.

For a read-only contrast, run: `Give me the current status of Acme Corp.` The graph gathers context but performs no mutations.

## 2:00-2:30: Value proposition

ClientPilot does not just tell you what is happening. It understands the client's operational state, identifies what needs attention, decides which tools to use, and executes the workflow across the business stack.
