import json
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class ServerConfig:
    """Server configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int = 1

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = "sqlite:///crypto.db"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10

@dataclass
class CryptoConfig:
    """Crypto specific configuration"""
    api_key: str = ""
    api_secret: str = ""
    exchange: str = "binance"
    trading_enabled: bool = False
    max_trades: int = 10

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    file: str = "crypto.log"
    max_size: int = 10485760  # 10MB
    backup_count: int = 5

@dataclass
class AppConfig:
    """Main application configuration"""
    app_name: str = "CRYPTO"
    version: str = "1.0.0"
    debug: bool = False
    secret_key: str = "your-secret-key-change-me"
    
    # Sub-configurations
    server: ServerConfig = None
    database: DatabaseConfig = None
    crypto: CryptoConfig = None
    logging: LoggingConfig = None
    
    def __post_init__(self):
        """Initialize sub-configs if not provided"""
        if self.server is None:
            self.server = ServerConfig()
        if self.database is None:
            self.database = DatabaseConfig()
        if self.crypto is None:
            self.crypto = CryptoConfig()
        if self.logging is None:
            self.logging = LoggingConfig()

# Global config instance
config: Optional[AppConfig] = None

def LoadConfig(config_path: str = "config.json") -> AppConfig:
    """
    Load configuration from JSON file
    
    Args:
        config_path: Path to config file
        
    Returns:
        AppConfig: Loaded configuration object
    """
    global config
    
    config_file = Path(config_path)
    
    # Create default config if file doesn't exist
    if not config_file.exists():
        print(f"⚠️  Config file '{config_path}' not found, creating default...")
        config = AppConfig()
        SaveConfig(config, config_path)
        return config
    
    try:
        # Load JSON file
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create config object
        config = AppConfig(
            app_name=data.get("app_name", "CRYPTO"),
            version=data.get("version", "1.0.0"),
            debug=data.get("debug", False),
            secret_key=data.get("secret_key", "your-secret-key-change-me"),
            
            server=ServerConfig(**data.get("server", {})),
            database=DatabaseConfig(**data.get("database", {})),
            crypto=CryptoConfig(**data.get("crypto", {})),
            logging=LoggingConfig(**data.get("logging", {}))
        )
        
        print(f"✅ Configuration loaded from '{config_path}'")
        return config
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON config: {e}")
        print("🔄 Using default configuration...")
        config = AppConfig()
        return config
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        print("🔄 Using default configuration...")
        config = AppConfig()
        return config

def SaveConfig(cfg: AppConfig, config_path: str = "config.json") -> bool:
    """
    Save configuration to JSON file
    
    Args:
        cfg: Configuration object to save
        config_path: Path to save config file
        
    Returns:
        bool: True if saved successfully
    """
    try:
        config_file = Path(config_path)
        
        # Convert to dictionary
        config_dict = asdict(cfg)
        
        # Save to JSON with nice formatting
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
        
        print(f"💾 Configuration saved to '{config_path}'")
        return True
        
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False

def GetConfig() -> AppConfig:
    """
    Get current configuration
    
    Returns:
        AppConfig: Current configuration object
    """
    global config
    if config is None:
        config = LoadConfig()
    return config

# Example usage and testing
if __name__ == "__main__":
    # Test configuration loading
    print("🧪 Testing configuration...")
    
    # Load config
    cfg = LoadConfig("test_config.json")
    
    # Print some values
    print(f"App: {cfg.app_name} v{cfg.version}")
    print(f"Server: {cfg.server.host}:{cfg.server.port}")
    print(f"Database: {cfg.database.url}")
    print(f"Debug: {cfg.debug}")
    
    # Save config
    SaveConfig(cfg, "test_config.json")
    
    print("✅ Configuration test completed!")