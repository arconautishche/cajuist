# cajuist
> as in "CA~MIS~JUIST"

This code can auto-fill your Cegeka CAMIS timesheets based on data provided from another, more usable, source.

## Currently available integration:
- Toggl

[See more details on usage](data_providers/README.md)

## How it works
You can use an existing script or write your own that will perform the simple 3 steps:
1. Import registered tasks from a source (e.g. Toggl)
    - [Data providers](/data_providers) are used for this
2. Normalize the data - round to 15 min chunks, trim descriptions, etc
    - [Model](/model) is where this happens
3. Fill out CAMIS by interacting with its UI
    - [Selenium interface](page_objects/camis) is written for this

### How to use
- Have Python 3.8+ installed
- Clone this project locally
- Switch to the .venv virtual environment. Run:
    ``` shell
    > .venv/Scripts/Activate.ps1
    ```
- Import the modules from requirements.txt. Run:
    ``` shell
    > pip install -r requirements.txt
    ```
- Create a file called .env and put your CAMIS credentials in there, like this:
    ```
    CAMIS_LOGIN='your_cegeka_AD_login'
    CAMIS_PASSWORD='your_very_secret_password'
    ```
- Write your own script or use 

### Working example 
An example of such a script is [toggl_to_camis.py](toggl_to_camis.py), which performs those three steps for a specific case:
1. Imports all entries from Toggl for today
2. Workorders and task descriptions are trimmed to what's typical at the Ventouris team
3. Fill out CAMIS by 
    - reuses lines completely matching Workorder + Activity + Description
    - adds new lines otherwise


