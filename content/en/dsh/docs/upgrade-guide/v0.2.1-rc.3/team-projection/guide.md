---
title: "Team projection retains tasks and mode"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-rc.3/team-projection/guide.md
fetched: 2026-11-03
---
# Team projection retains tasks and mode

English | [中文](guide.zh.md)

## Change

The `agentTeam` projection no longer restores `members`, `messages`, or `delivered` from historical `team/member` and `team/message/*` events. It ignores their payloads, so historical roster or mailbox validation failures no longer block task reads or writes. Historical teammates are not restored and queued mail is not delivered.

Task revisions, task owners, deleted-task records, and the saved Team mode remain supported. Ordinary subagent discovery and messaging are unchanged. The Session format and committed log files do not change; projection checkpoint version 7 rebuilds older cached state from the log.

## Migration

1. No data conversion or configuration change is required. Open the Session normally to rebuild incompatible projection checkpoints.
2. Use `list_agents` and `send_message` for current teammates. Read historical roster or mailbox events from the original Session log if you need an archive; the Team projection no longer supplies these collections.
3. Confirm that the task board and saved Team mode are restored. Historical roster and mailbox records do not grant task-assignment authority.
