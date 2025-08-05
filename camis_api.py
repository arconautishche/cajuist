from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
import uvicorn
import logging

import util
from model.spent_time_records import WorkedDay
from model.ventouris_processor import VentourisProcessor
from page_objects.camis.timesheet import Timesheet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CAMIS Timesheet API",
    description="API for automatically filling CAMIS timesheet entries",
    version="1.0.0"
)

# Pydantic models for request/response
class TimesheetEntry(BaseModel):
    workorder: str = Field(..., description="Work order number")
    activity: str = Field(..., description="Activity description")
    description: str = Field(..., description="Task description")
    hours: float = Field(..., gt=0, description="Hours worked (must be positive)")

class TimesheetRequest(BaseModel):
    target_date: date = Field(..., description="Date for the timesheet entries")
    entries: List[TimesheetEntry] = Field(..., description="List of timesheet entries")
    headless: bool = Field(default=False, description="Run browser in headless mode")

class TimesheetResponse(BaseModel):
    success: bool
    message: str
    total_hours: float
    entries_processed: int
    errors: List[str] = []


@app.post("/fill-timesheet", response_model=TimesheetResponse)
async def fill_timesheet(request: TimesheetRequest):
    """
    Fill CAMIS timesheet with provided entries for a specific date
    """
    try:
        logger.info(f"Processing timesheet request for date: {request.target_date}")
        logger.info(f"Number of entries: {len(request.entries)}")
        
        # Convert Pydantic entries to the format expected by WorkedDay
        entries_data = [
            {
                'workorder': entry.workorder,
                'activity': entry.activity,
                'description': entry.description,
                'hours': entry.hours
            }
            for entry in request.entries
        ]
        
        # Create WorkedDay object
        day_report = WorkedDay(entries_data, caption_processor=VentourisProcessor())
        total_hours = day_report.total_hours()
        
        logger.info(f"Total hours: {total_hours}")
        
        # Initialize timesheet
        ts = None
        try:
            ts = Timesheet(request.headless)

            ts.set_date(request.target_date);
            
            # Fill CAMIS with entries
            errors = util.fill_camis(day_report, ts, request.target_date)
            
            # Save if no errors
            if not errors:
                ts.save()
                logger.info("Timesheet saved successfully")
                message = f"Successfully processed {len(request.entries)} entries with {total_hours} total hours"
            else:
                message = f"Processed entries but found errors: {', '.join(errors)}"
            
            return TimesheetResponse(
                success=len(errors) == 0,
                message=message,
                total_hours=total_hours,
                entries_processed=len(request.entries),
                errors=errors
            )
            
        except Exception as e:
            logger.error(f"Error during timesheet processing: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Timesheet processing failed: {str(e)}")
        
        finally:
            # Always close the browser
            if ts:
                try:
                    ts.close()
                except Exception as e:
                    logger.warning(f"Error closing browser: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "CAMIS Timesheet API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 