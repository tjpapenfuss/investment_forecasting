from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import tempfile
import os

# Import your simulation function
from main_sim import run_investment_simulation

# Create FastAPI app
app = FastAPI(
    title="Investment Simulation API",
    description="API for running investment simulations",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define request model for JSON config
class SimulationRequest(BaseModel):
    config: Dict[str, Any]
    simulation_type: str = "top_n"

@app.get("/")
async def root():
    return {"message": "Investment Simulation API is running"}

@app.post("/run-simulation")
async def api_run_simulation(
    request: Optional[SimulationRequest] = None,
    config_file: Optional[UploadFile] = File(None)
):
    """
    Run an investment simulation with either an uploaded configuration file
    or a configuration dictionary provided in the request body.
    
    Request can be made in two ways:
    1. As JSON with a 'config' object and optional 'simulation_type'
    2. As a form with a 'config_file' (JSON file upload) and optional 'simulation_type'
    """
    try:
        if config_file is not None:
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp:
                temp_path = temp.name
                content = await config_file.read()
                temp.write(content)
            
            # Run simulation with the temporary file
            try:
                simulation_type = request.simulation_type if request else "top_n"
                results = run_investment_simulation(config_file=temp_path, simulation=simulation_type)
            finally:
                # Clean up the temporary file
                os.unlink(temp_path)
                
        elif request is not None:
            # Run simulation with the provided config dictionary
            results = run_investment_simulation(
                config_dict=request.config, 
                simulation=request.simulation_type
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Either a configuration file or a configuration dictionary must be provided"
            )
            
        # Return the results directly
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)