import asyncio
import uvicorn
import sys
import os
import signal
from config import LoadConfig
from core.core import start

import webbrowser


# Global exit flag
EXIT_FLAG = False

def signal_handler(signum, frame):
    """Signal handler for SIGINT (Ctrl+C)"""
    global EXIT_FLAG
    print(f"\n🚨 Signal {signum} received - FORCE EXIT!")
    EXIT_FLAG = True
    os._exit(0)

async def start_core(): 
    global EXIT_FLAG
    try:
        core = await start()
    except asyncio.CancelledError:
        print("🛑 Core task cancelled")
        EXIT_FLAG = True
        os._exit(0)

async def start_server_async(config):
    """Start FastAPI server asynchronously"""
    global EXIT_FLAG
    print(f"🌐 Starting web server on {config.server.host}:{config.server.port}")
    
    server_config = uvicorn.Config(
        "server.server:app",
        host=config.server.host,
        port=config.server.port,
        log_level="info"
    )
    
    server = uvicorn.Server(server_config)
    
    try:
        await server.serve()
    except asyncio.CancelledError:
        print("🛑 Server stopped")
        EXIT_FLAG = True
        os._exit(0)

async def exit_monitor():
    """Monitor exit flag and force exit if needed"""
    global EXIT_FLAG
    while not EXIT_FLAG:
        await asyncio.sleep(0.1)
    
    print("🔪 EXIT FLAG TRIGGERED - KILLING EVERYTHING!")
    os._exit(0)

async def main():
    """Main async function"""
    global EXIT_FLAG
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 50)
    print("🚀 Starting CRYPTO application...")
    print("=" * 50)
    
    # Load configuration
    print("📄 Loading configuration...")
    config = LoadConfig()
    print(f"🎯 App: {config.app_name} v{config.version}")
    print(f"🔧 Debug mode: {config.debug}")
    
    print("📊 Initializing CRYPTO modules...")
    await asyncio.sleep(1)
    
    if EXIT_FLAG:
        os._exit(0)
    
    print("💾 Setting up database...")
    print(f"   Database URL: {config.database.url}")
    await asyncio.sleep(0.5)
    
    if EXIT_FLAG:
        os._exit(0)
    
    print("⚡ Configuring crypto settings...")
    print(f"   Exchange: {config.crypto.exchange}")
    print(f"   Trading enabled: {config.crypto.trading_enabled}")
    await asyncio.sleep(0.5)
    
    if EXIT_FLAG:
        os._exit(0)
    
    print("✅ CRYPTO application initialized successfully!")
    print("-" * 50)
    
    # Create tasks including exit monitor
    tasks = [
        asyncio.create_task(start_server_async(config)),
        asyncio.create_task(start_core()),
        asyncio.create_task(exit_monitor()),
    ]
    
    print(f"🎯 Web server starting on {config.server.host}:{config.server.port}")
    print(f"📱 Access the application at: http://localhost:{config.server.port}")
    webbrowser.open(f"http://localhost:{config.server.port}")
    
    print("🔄 Background tasks started")
    print("⚠️  Press Ctrl+C for FORCE EXIT")
    print("-" * 50)
    print("⚡ CRYPTO application is running...")
    
    try:
        # Use wait instead of gather for better control
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\n🛑 Killing everything...")
        EXIT_FLAG = True
        
        # Cancel all tasks
        for task in tasks:
            if not task.done():
                task.cancel()
        
        # Wait a bit for cleanup
        await asyncio.sleep(0.1)
        
        # Force exit
        print("👋 Bye!")
        os._exit(0)
    except Exception as e:
        print(f"💥 Error: {e}")
        EXIT_FLAG = True
        os._exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🔪 KEYBOARD INTERRUPT - FORCE EXIT")
        EXIT_FLAG = True
        os._exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        os._exit(1)
    finally:
        # Just in case
        print("🏁 Final exit")
        os._exit(0)