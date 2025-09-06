import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration management class"""
    
    # ===== LOGIN CREDENTIALS =====
    ZEUSX_USERNAME = os.getenv('ZEUSX_USERNAME', 'thongbe995@gmail.com')
    ZEUSX_PASSWORD = os.getenv('ZEUSX_PASSWORD', 'Thongbe995@')
    
    # ===== AUTOMATION SETTINGS =====
    AUTOMATION_DELAY_MINUTES = int(os.getenv('AUTOMATION_DELAY_MINUTES', 60))
    ITEM_CREATION_DELAY = int(os.getenv('ITEM_CREATION_DELAY', 5))
    
    # ===== FILE PATHS =====
    EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH', 'du_lieu.xlsx')
    IMAGES_FOLDER = os.getenv('IMAGES_FOLDER', 'pic')
    CHROME_PROFILE_NAME = os.getenv('CHROME_PROFILE_NAME', 'Test_profile')
    
    # ===== BROWSER SETTINGS =====
    LOGIN_TIMEOUT = int(os.getenv('LOGIN_TIMEOUT', 20))
    ELEMENT_TIMEOUT = int(os.getenv('ELEMENT_TIMEOUT', 10))
    SUCCESS_POPUP_TIMEOUT = int(os.getenv('SUCCESS_POPUP_TIMEOUT', 15))
    
    # ===== ADVANCED SETTINGS =====
    MAX_RETRY_ATTEMPTS = int(os.getenv('MAX_RETRY_ATTEMPTS', 3))
    ERROR_RETRY_DELAY = int(os.getenv('ERROR_RETRY_DELAY', 5))
    
    # ===== GAME MAPPING =====
    GAME_MAPPING = {
        "league": "League of Legends",
        "lol": "League of Legends", 
        "valorant": "Valorant",
        "roblox": "Roblox",
        "pubg": "PUBG",
        "genshin": "Genshin Impact",
        "gta": "GTA5",
        "gta5": "GTA5"
    }
    
    @classmethod
    def get_chrome_profile_path(cls):
        """Get full path to Chrome profile directory"""
        return os.path.abspath(os.path.join("chrome_profiles", cls.CHROME_PROFILE_NAME))
    
    @classmethod
    def get_image_path(cls, filename):
        """Get full path to image file"""
        return os.path.abspath(os.path.join(cls.IMAGES_FOLDER, filename))
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []
        
        # Check required files
        if not os.path.exists(cls.EXCEL_FILE_PATH):
            errors.append(f"Excel file not found: {cls.EXCEL_FILE_PATH}")
            
        if not os.path.exists(cls.IMAGES_FOLDER):
            errors.append(f"Images folder not found: {cls.IMAGES_FOLDER}")
            
        # Check credentials
        if not cls.ZEUSX_USERNAME or not cls.ZEUSX_PASSWORD:
            errors.append("Login credentials not configured")
            
        # Check numeric values
        if cls.AUTOMATION_DELAY_MINUTES <= 0:
            errors.append("AUTOMATION_DELAY_MINUTES must be positive")
            
        return errors
    
    @classmethod
    def print_config(cls):
        """Print current configuration (hide sensitive data)"""
        print("\n📋 CURRENT CONFIGURATION:")
        print("=" * 50)
        print(f"📧 Username: {cls.ZEUSX_USERNAME}")
        print(f"🔐 Password: {'*' * len(cls.ZEUSX_PASSWORD)}")
        print(f"⏰ Automation Delay: {cls.AUTOMATION_DELAY_MINUTES} minutes")
        print(f"⚡ Item Creation Delay: {cls.ITEM_CREATION_DELAY} seconds")
        print(f"📁 Excel File: {cls.EXCEL_FILE_PATH}")
        print(f"🖼️ Images Folder: {cls.IMAGES_FOLDER}")
        print(f"🌐 Chrome Profile: {cls.CHROME_PROFILE_NAME}")
        print("=" * 50)
