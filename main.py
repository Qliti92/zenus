import os
import time
import re
from typing import Dict, List
from collections import defaultdict
from seleniumbase import SB
from config import Config
from exel_manager import ExelReader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Zeusx_Automation:
    def __init__(self):
        self.data = None
        self.reader = ExelReader("du_lieu.xlsx")
        self.profile_name = "Test_profile"
        self.sb = None
        
        # Mapping game names to their creation functions
        self.game_creators = {
            "League of Legends": self.create_offer_lol_and_valorant,
            "Valorant": self.create_offer_lol_and_valorant,
            "Roblox": self.creater_offer_roblox_and_pubg,
            "PUBG": self.creater_offer_roblox_and_pubg,
            "Genshin Impact": self.creater_offer_genshin_impact,
            "GTA5": self.creater_offer_gta5,
        }

    def _login_zeusx(self):
        """Login to Zeusx platform"""
        print("🔐 Bắt đầu đăng nhập...")
        
        # if self.sb.wait_for_element('.header_login-btn__fRliL', timeout=10):
        #     print("🏠 Vào trang chủ thành công")
        #     self.sb.cdp.click('button.header_login-btn__fRliL')
            
        time.sleep(3)
        self.sb.cdp.type("input[placeholder='Username']", "thongbe995@gmail.com")
        self.sb.cdp.type("input[placeholder='Min 8 characters']", "Thongbe995@")
        self.sb.cdp.click("button.login-screen_login-btn__9tKfS")
        
        if self.sb.wait_for_element('div.user-dropdown_user-dropdown__HmrmT', timeout=20):
            print("✅ Đăng nhập thành công!")
            return True
        else:
            print("❌ Đăng nhập thất bại, thử lại...")
            return self._login_zeusx()

    def get_game_name_from_data(self, data: Dict) -> str:
        """Extract game name from data based on id_game"""
        id_game = str(data.get("id_game", "")).strip().lower()
        
        # Mapping id_game to game names
        game_mapping = {
            "league": "League of Legends",
            "lol": "League of Legends",
            "valorant": "Valorant",
            "roblox": "Roblox",
            "pubg": "PUBG",
            "genshin": "Genshin Impact",
            "gta": "GTA5",
            "gta5": "GTA5"
        }
        
        for key, game_name in game_mapping.items():
            if key in id_game:
                return game_name
        
        # Default fallback
        return "Unknown"

    def group_data_by_game(self, all_data: List[Dict]) -> Dict[str, List[Dict]]:
        """Group data by game type"""
        games_data = defaultdict(list)
        
        for data in all_data:
            game_name = self.get_game_name_from_data(data)
            games_data[game_name].append(data)
            
        return dict(games_data)

    def check_pagination(self) -> int:
        """Check total pages in my-listing"""
        self.sb.open('https://zeusx.com/my-listing')
        self.sb.sleep(2)
        
        try:
            # Get current page
            current = int(self.sb.get_text("button.pagination_active__iVvCL span"))
            print(f"📄 Trang hiện tại: {current}")
            
            # Get total pages
            nums = []
            for el in self.sb.find_elements("button.pagination_page-item__Ed5q0"):
                txt = (el.text or "").strip()
                if re.fullmatch(r"\d+", txt):
                    nums.append(int(txt))
            
            total = max(nums) if nums else 1
            print(f"📊 Tổng số trang: {total}")
            return total
            
        except Exception as e:
            print(f"⚠️ Lỗi khi check pagination: {e}")
            return 1

    def delete_listings_by_game_page(self, game_text: str) -> int:
        """Delete listings on current page for specific game"""
        try:
            self.sb.wait_for_element_visible(
                "div.my-profile-table_my-profile-table__X_qWk", timeout=10
            )
        except Exception as e:
            print(f"⚠️ Không tìm thấy bảng listings: {e}")
            return 0
        
        try:
            rows = self.sb.find_elements("div.my-profile-table_row__iRibv")
            rows_count = len(rows)
            print(f"📊 Tìm thấy {rows_count} rows")
            
            if rows_count == 0:
                print("⚪ Không có rows nào")
                return 0
        except Exception as e:
            print(f"⚠️ Lỗi khi tìm rows: {e}")
            return 0
        
        game_count = 0
        
        for i in range(rows_count):
            try:
                row_index = i + 1
                row_selector = f"div.my-profile-table_row__iRibv:nth-child({row_index})"
                cat_selector = f"{row_selector} .my-listing-table_category__wNaJj"
                
                if not self.sb.is_element_visible(cat_selector):
                    continue
                    
                cat = self.sb.get_text(cat_selector, timeout=2).strip()
                
                if not cat:
                    continue
                    
                if game_text.lower() in cat.lower():
                    print(f"🎯 Tìm thấy {game_text}: {cat}")
                    checkbox_selector = f"{row_selector} .checkbox_checkbox-box__2fLhD"
                    
                    if self.sb.is_element_visible(checkbox_selector):
                        self.sb.click(checkbox_selector)
                        game_count += 1
                        print(f"✅ Đã chọn item #{game_count}")
                        
            except Exception as e:
                print(f"❌ Lỗi tại row {row_index}: {e}")
                continue
                
        return game_count

    def delete_all_listings_by_game(self, game_text: str):
        """Delete all listings for a specific game across all pages"""
        print(f"🗑️ Bắt đầu xóa tất cả listings của game: {game_text}")
        
        total_pages = self.check_pagination()
        total_deleted = 0
        
        for page in range(total_pages, 0, -1):  # Đi từ trang cuối về trang đầu
            print(f"📄 Đang xử lý trang {page}/{total_pages}")
            
            self.sb.open(f'https://zeusx.com/my-listing?page={page}')
            self.sb.sleep(3)
            
            game_count = self.delete_listings_by_game_page(game_text)
            
            if game_count > 0:
                print(f"🎯 Tìm thấy {game_count} items {game_text} trên trang {page}")
                
                # Click remove button
                try:
                    self.sb.click("//div[@class='select-multiple-badge_action__hsgHX' and contains(., 'Remove Listing')]")
                    self.sb.wait_for_element("button.success-popup_btn-primary__DpGCB", timeout=10)
                    self.sb.click("button.success-popup_btn-primary__DpGCB")
                    
                    # Wait for success message
                    self.sb.wait_for_text("Your Change was updated successfully!", timeout=15)
                    print(f"✅ Xóa thành công {game_count} items trên trang {page}")
                    
                    total_deleted += game_count
                    self.sb.sleep(2)
                    
                except Exception as e:
                    print(f"❌ Lỗi khi xóa trên trang {page}: {e}")
            else:
                print(f"⚪ Không tìm thấy {game_text} trên trang {page}")
        
        print(f"🎉 Hoàn thành xóa {game_text}: Tổng cộng {total_deleted} items đã được xóa")

    # HÀM HỖ TRỢ - Chọn thẻ dropdown
    def select_dropdown_option(self, label_name: str, option_text: str):
        """Select dropdown option"""
        try:
            self.sb.cdp.click(f"//div[div[@class='select-form_label__dAwvH' and text()='{label_name}']]//div[contains(@class,'select-form_select-wrapper')]")
            self.sb.cdp.click(f"//div[contains(@class,'radio-box_label') and normalize-space()='{option_text}']")
        except Exception as e:
            print(f"⚠️ Lỗi khi chọn {label_name}: {option_text} - {e}")

    def create_offer_lol_and_valorant(self):
        """Create offer for League of Legends and Valorant"""
        print("🎮 Tạo offer cho LOL/Valorant...")
        
        self.sb.open('https://zeusx.com/create-offer')
        self.sb.cdp.type("input.co-select-game_input-search__AqNcm", self.data["id_game"])
        self.sb.cdp.click("div.co-select-game_game-item___jTq9:first-of-type")

        # Fill basic info
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input", self.data["name_sale"])
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input[type='text']", str(int(self.data["price_sale"])))
        
        # Select options
        self.select_dropdown_option("Rank", self.data.get('rank_sale', ''))
        self.select_dropdown_option("Server", self.data.get('sever_sale', ''))
        
        # Multiple quantity
        self.sb.cdp.click("//div[contains(@class,'checkbox_checkbox__') and .//div[normalize-space()='Multiple quantity?']]")
        self.sb.cdp.type('input[placeholder="Eg: 10"]', "99")
        self.sb.cdp.type("div.row-2 div.input_input__N_xjH:nth-child(2) input", "3")
        
        # Description
        self.sb.cdp.press_keys("div.ck-content[contenteditable='true']", str(self.data["description_sale"]))
        
        # Tags
        self._add_tags()

        # Upload image
        self._upload_image()
        self.sb.cdp.click("//button[.//div[text()='List Items']]")

    def creater_offer_roblox_and_pubg(self):
        """Create offer for Roblox and PUBG"""
        print("🎮 Tạo offer cho Roblox/PUBG...")
        
        self.sb.open('https://zeusx.com/create-offer')
        self.sb.cdp.type("input.co-select-game_input-search__AqNcm", self.data["id_game"])
        self.sb.cdp.click("div.co-select-game_game-item___jTq9:first-of-type")
        
        # Fill basic info
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input", self.data["name_sale"])
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input[type='text']", str(int(self.data["price_sale"])))
        
        # Multiple quantity
        self.sb.cdp.click("//div[contains(@class,'checkbox_checkbox__') and .//div[normalize-space()='Multiple quantity?']]")
        self.sb.cdp.type('input[placeholder="Eg: 10"]', "99")
        self.sb.cdp.type("div.row-2 div.input_input__N_xjH:nth-child(2) input", "3")
        
        # Description
        self.sb.cdp.press_keys("div.ck-content[contenteditable='true']", str(self.data["description_sale"]))
        
        # Tags
        self._add_tags()
        
        # Upload image
        self._upload_image()
        
        self.sb.cdp.click("//button[.//div[text()='List Items']]")

    def creater_offer_genshin_impact(self):
        """Create offer for Genshin Impact"""
        print("🎮 Tạo offer cho Genshin Impact...")
        
        self.sb.open('https://zeusx.com/create-offer')

        self.sb.cdp.type("input.co-select-game_input-search__AqNcm", self.data["id_game"])
        self.sb.cdp.click("div.co-select-game_game-item___jTq9:first-of-type")
        
        # Fill basic info
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input", self.data["name_sale"])
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input[type='text']", str(int(self.data["price_sale"])))
        
        # Multiple quantity
        self.sb.cdp.click("//div[contains(@class,'checkbox_checkbox__') and .//div[normalize-space()='Multiple quantity?']]")
        self.sb.cdp.type('input[placeholder="Eg: 10"]', "99")
        self.sb.cdp.type("div.row-2 div.input_input__N_xjH:nth-child(2) input", "3")
        
        # Select options
        self.select_dropdown_option("Player Gender", self.data.get('character_sale', ''))
        self.select_dropdown_option("Server/Region", self.data.get('sever_sale', ''))
        
        # Description
        self.sb.cdp.press_keys("div.ck-content[contenteditable='true']", str(self.data["description_sale"]))
        
        # Tags
        self._add_tags()

        # Upload image
        self._upload_image()
        self.sb.cdp.click("//button[.//div[text()='List Items']]")

    def creater_offer_gta5(self):
        """Create offer for GTA5"""
        print("🎮 Tạo offer cho GTA5...")
        
        self.sb.open('https://zeusx.com/create-offer')
        self.sb.cdp.type("input.co-select-game_input-search__AqNcm", self.data["id_game"])
        self.sb.cdp.click("div.co-select-game_game-item___jTq9:first-of-type")

        
        # Fill basic info
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input", self.data["name_sale"])
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input[type='text']", str(int(self.data["price_sale"])))
        
        # Multiple quantity
        self.sb.cdp.click("//div[contains(@class,'checkbox_checkbox__') and .//div[normalize-space()='Multiple quantity?']]")
        self.sb.cdp.type('input[placeholder="Eg: 10"]', "99")
        self.sb.cdp.type("div.row-2 div.input_input__N_xjH:nth-child(2) input", "3")
        
        # Select platform
        self.select_dropdown_option("Platform / Device", self.data.get('device_sale', ''))
        
        # Description
        self.sb.cdp.press_keys("div.ck-content[contenteditable='true']", str(self.data["description_sale"]))
        
        # Tags
        self._add_tags()

        
        # Upload image
        self._upload_image()
        


    def _add_tags(self):
        """Add tags to the offer"""
        if "tag_sale" in self.data and self.data["tag_sale"]:
            tags = str(self.data["tag_sale"]).split(",")
            for tag in tags:
                tag = tag.strip()
                if tag:
                    self.sb.cdp.type("input[placeholder='Enter to add']", tag)
                    self.sb.cdp.evaluate('''
                        document.querySelector("input[placeholder='Enter to add']")
                        .dispatchEvent(new KeyboardEvent('keydown', {
                            key: 'Enter', 
                            keyCode: 13,
                            bubbles: true
                        }));
                    ''')
                    time.sleep(0.5)

    def _upload_image(self):
        """Upload image for the offer"""
        if "linkpic_sale" in self.data and self.data["linkpic_sale"]:
            file_path = os.path.abspath(f"pic/{self.data['linkpic_sale']}")
            if os.path.exists(file_path):
                self.sb.cdp.wait_for_element_visible('.image-upload_image-upload-box__Iv_LD')
                el = self.sb.cdp.find(".image-upload_image-upload-box__Iv_LD:nth-child(1) > input")
                el.send_file(file_path)
                self.sb.cdp.click('.co-upload-photos_rules__iHACT .checkbox_checkbox-box__2fLhD')
            else:
                print(f"⚠️ Không tìm thấy file ảnh: {file_path}")

    def wait_for_success_popup(self) -> bool:
        """Wait for success popup after creating offer"""
        try:
            self.sb.cdp.wait_for_element_visible("div.success-popup_success-popup__bb900", timeout=15)
            print("✅ Đăng sản phẩm thành công!")
            return True
        except Exception as e:
            print(f"❌ Không thấy popup thành công: {str(e)}")
            return False

    def create_offer_for_game(self, game_name: str, data: dict) -> bool:
        """Create offer based on game type"""
        self.data = data
        
        try:
            if game_name in self.game_creators:
                print(f"🎯 Tạo offer cho {game_name}: {data.get('name_sale', '')}")
                self.game_creators[game_name]()
                success = self.wait_for_success_popup()
                return success
            else:
                print(f"⚠️ Không hỗ trợ game: {game_name}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khi tạo offer cho {game_name}: {e}")
            return False

    def process_game_batch(self, game_name: str, game_data: List[Dict]):
        """Process a batch of data for specific game"""
        print(f"\n🎮 BẮT ĐẦU XỬ LÝ GAME: {game_name}")
        print(f"📊 Số lượng items: {len(game_data)}")
        
        # Step 1: Check and delete existing listings for this game
        print(f"\n🗑️ BƯỚC 1: Kiểm tra và xóa listings cũ của {game_name}")
        deletion_performed = self.delete_all_listings_by_game(game_name)
        
        if deletion_performed:
            print(f"✅ Đã xóa listings cũ của {game_name}")
        else:
            print(f"✅ Không có listings cũ của {game_name}, tiến hành tạo mới")
        
        # Step 2: Create new listings
        print(f"\n➕ BƯỚC 2: Tạo listings mới cho {game_name}")
        success_count = 0
        
        for index, data in enumerate(game_data, 1):
            print(f"\n--- Item {index}/{len(game_data)} ---")
            success = self.create_offer_for_game(game_name, data)
            
            if success:
                success_count += 1
                print(f"✅ Item {index}: THÀNH CÔNG")
            else:
                print(f"❌ Item {index}: THẤT BẠI")
            
            # Delay between items
            self.sb.sleep(5)
        
        print(f"\n🎉 KẾT QUẢ {game_name}: {success_count}/{len(game_data)} thành công")

    def run_automation_cycle(self):
        """Run one complete automation cycle"""
        print("\n" + "="*60)
        print("🚀 BẮT ĐẦU CHU KỲ AUTOMATION MỚI")
        print("="*60)
        
        # Load data from Excel
        self.reader.load_exel()
        all_data = list(self.reader.iter_rows())
        
        if not all_data:
            print("⚠️ Không có dữ liệu trong file Excel")
            return
        
        # Group data by game
        games_data = self.group_data_by_game(all_data)
        
        print(f"📊 Tổng quan dữ liệu:")
        for game_name, data_list in games_data.items():
            print(f"  - {game_name}: {len(data_list)} items")
        
        # Process each game
        for game_name, game_data in games_data.items():
            if game_name == "Unknown":
                print(f"⚠️ Bỏ qua game không xác định: {len(game_data)} items")
                continue
                
            try:
                self.process_game_batch(game_name, game_data)
            except Exception as e:
                print(f"❌ Lỗi khi xử lý {game_name}: {e}")
                continue
        
        print("\n✅ HOÀN THÀNH CHU KỲ AUTOMATION")

    def run_infinite_loop(self):
        """Run automation in infinite loop"""
        # Get delay from config
        delay_minutes = Config.AUTOMATION_DELAY_MINUTES
        delay_seconds = delay_minutes * 60
        
        print(f"🔄 Khởi động automation với chu kỳ: {delay_minutes} phút")
        
        # Validate configuration before starting
        config_errors = Config.validate_config()
        if config_errors:
            print("❌ LỖI CONFIGURATION:")
            for error in config_errors:
                print(f"  - {error}")
            return
            
        # Print current configuration
        Config.print_config()
        
        profile_dir = Config.get_chrome_profile_path()
        os.makedirs(profile_dir, exist_ok=True)
        
        cycle_count = 0
        
        while True:
            try:
                cycle_count += 1
                print(f"\n🔄 CHU KỲ SỐ: {cycle_count}")
                print(f"⏰ Thời gian: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                with SB(uc=True, locale="en", user_data_dir=profile_dir) as sb:
                    self.sb = sb
                    self.sb.activate_cdp_mode("https://zeusx.com/login")
                    
                    # Handle captcha if present
                    try:
                        if sb.find_element("#FGRYW5", timeout=3):
                            print("🤖 Phát hiện captcha, đang xử lý...")
                            self.sb.sleep(10)
                            self.sb.uc_gui_click_captcha()
                    except Exception:
                        pass
                    
                    # Login
                    if not self._login_zeusx():
                        print("❌ Không thể đăng nhập, thử lại sau...")
                        continue
                    
                    # Run automation cycle
                    self.run_automation_cycle()
                
                print(f"\n⏳ Chờ {delay_minutes} phút trước chu kỳ tiếp theo...")
                print(f"💤 Nghỉ từ {time.strftime('%H:%M:%S')} đến {time.strftime('%H:%M:%S', time.localtime(time.time() + delay_seconds))}")
                
                time.sleep(delay_seconds)
                
            except KeyboardInterrupt:
                print("\n🛑 Dừng chương trình theo yêu cầu người dùng")
                break
            except Exception as e:
                print(f"❌ Lỗi trong chu kỳ {cycle_count}: {e}")
                print(f"⏳ Chờ {Config.ERROR_RETRY_DELAY} phút trước khi thử lại...")
                time.sleep(Config.ERROR_RETRY_DELAY * 60)

if __name__ == "__main__":
    print("🎮 ZEUSX AUTOMATION SYSTEM")
    print("=" * 50)
    
    automation = Zeusx_Automation()
    automation.run_infinite_loop()
    input("NHẤN PHÍM BẤT KỲ ĐỂ THÓA CHƯƠNG TRÌNH")
