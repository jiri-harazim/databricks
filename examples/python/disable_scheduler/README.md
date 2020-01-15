# About

Databricks (v 3.9) does not support temporarily disabling job schedules. This means that your jobs run on bank holidays or during maintenance windows unless you delete the schedule or the whole job.

This example shows how to automate 'disabling' schedules using Databricks Jobs REST API. It deletes a schedule from a given job (in the UI it says Schedule: None). The example can be extended to persist the existing schedules (to a file/database/..) so they can be restored eventually.

The benefit of this approach instead of deleting a job is that it still explicitly exists in the UI but simply disables (=deletes) the schedule.

Available as-is.

https://github.com/jiri-harazim/databricks-public