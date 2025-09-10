import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# Create FastAPI app
app = FastAPI(title="Server", version="1.0.0")

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
UI_DIR = BASE_DIR / "ui"

# Check if UI directory exists
if UI_DIR.exists():
    
    @app.get("/")
    async def read_index():
        """Serve index.html as root page"""
        index_file = UI_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "Index file not found"}
    
    @app.get("/{file_path:path}")
    async def serve_ui_files(file_path: str):
        """Serve files from ui directory"""
        file = UI_DIR / file_path
        if file.exists() and file.is_file():
            return FileResponse(str(file))
        # Fallback to index.html for SPA routing
        index_file = UI_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"error": "File not found"}
else:
    @app.get("/")
    async def read_root():
        return {"message": "CRYPTO Server is running", "ui_directory": "not found"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "ui_available": UI_DIR.exists()}

# API endpoints can be added here
@app.get("/api/status")
async def api_status():
    return {"status": "API is working", "version": "1.0.0"}

def start_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """
    Start the FastAPI server
    
    Args:
        host: Server host address
        port: Server port
        reload: Enable auto-reload for development
    """
    print(f"Starting CRYPTO server...")
    print(f"UI directory: {UI_DIR}")
    print(f"Server will be available at: http://{host}:{port}")
    
    uvicorn.run(
        "server.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    # For development - run with reload
    start_server(reload=True)