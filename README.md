# cajuist
> as in "CA~MIS~JUIST"

This code can auto-fill your Cegeka CAMIS timesheets based on data provided from another, more usable, source.

## Currently available integrations:
- Toggl
- CSV-file
- API

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
- Create a file called .env and put your Cegeka AD login in there, like this:
    ```
    AD_LOGIN='firstname.lastname@cegeka.com'
    AD_PASSWORD='xxxxx' (optional)
    TOTP_SECRET='xxxxx' (optional)
    ```
- Write your own script or use an existing one if it matches your needs

### Working example 
An example of such a script is [toggl_to_camis.py](toggl_to_camis.py), which performs those three steps for a specific case:
1. Imports all entries from Toggl for today
2. Trims workorders and task descriptions to what's typical at the Ventouris team (using [Ventouris processor](model/ventouris_processor.py))
3. Fills out CAMIS for today:
    - reuses lines completely matching Workorder + Activity + Description
    - adds new lines otherwise

    IT DOESN'T SAVE AUTOMATICALLY THOUGH (that's on purpose to let you review the entries before clicking Save)



## Running the API

### Development Mode
```bash
python camis_api.py
```

### Production Mode
```bash
uvicorn camis_api:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Endpoints

### Health Check
- **GET** `/health` - Check API status

### Fill Timesheet
- **POST** `/fill-timesheet` - Fill CAMIS timesheet with entries