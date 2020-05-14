# Registered time providers

## Toggl
https://toggl.com/ is a start-stop timer. The free version allows more than enough to track your time.

1. Put your API token on a separate line in the .env file: `TOGGL_TOKEN='your_token_goes_here'`
   > You can probably find your token on the Profile page - https://toggl.com/app/profile
2. Use the following conventions to nicely match attributes of Toggl entries to those of CAMIS:
    | CAMIS	| Toggl	|
    |---|---|
    |Workorder|Project name|
    |Activity|Tags (use one tag per task)|
    |Description|Description|