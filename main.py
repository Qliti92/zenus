import os
from sre_parse import SUCCESS
import time
from seleniumbase import SB

from exel_manager import ExelReader


class Zeusx_Automation:
    def __init__(self):
        self.data = None
        self.reader = ExelReader("du_lieu.xlsx") 
        self.profile_name= "Test_profile"
        pass

    def _login_Zeusx(self):
        print("Bắt đâu đăng nhập ")
        time.sleep(3)
        self.sb.cdp.type("input[placeholder='Username']", "thongbe995@gmail.com")  
        self.sb.cdp.type("input[placeholder='Min 8 characters']", "Thongbe995@")
        self.sb.cdp.click("button.login-screen_login-btn__9tKfS")
        self.sb.cdp.sleep(10)
        if self.sb.find_elements('div.user-dropdown_user-dropdown__HmrmT'):
            print("Đăng nhập thành công  ")
            return True
        else:
            return self._login_Zeusx()
            print("Vào Trang Chủ Thành công")

    # --------------------------------------------------
    # PHẦN XÓA SALE PRODUCT
    #----------------------------------------------------
    def del_product_of_type(self):
        self.sb.cdp.open("https://zeusx.com/my-listing")
        self.sb.cdp.click("button.my-purchases-route_filter-btn__888IG")
        self.sb.cdp.sleep(2)
        # Modal body
        modal = ".my-purchases-filter-modal_modal-body__G8u_z"
        # Lấy các label con trong All Games
        labels_css = f"{modal} .expandable_expandable__aY1Yx:nth-of-type(2) .expandable_expand-body__0T609 .checkbox_label__hcNDr"
        self.sb.cdp.wait_for_element_visible(labels_css, timeout=6)
        els = self.sb.cdp.find_elements(labels_css)
        games = [e.text.strip() for e in els]
        print(games)  # ['Genshin Impact', 'League of Legends', 'Roblo1', 'GT5']
        target = "Genshin Impact" 
        for e in els:
            if e.text.strip() == target:
                # click vào label để tick
                e.click()
                break
        self.sb.cdp.click("button.my-purchases-filter-modal_apply-btn__Db0BN")
        self.sb.cdp.click("div.my-purchases-table_checkbox__3Hfh3 div.checkbox_checkbox-box__2fLhD")
        self.sb.cdp.sleep(2)
        
           # 1) Khoanh vùng theo label có chữ "Select all"
        label_xpath = ("/html/body/div[1]/div[4]/div/div[1]/div/div[1]")
        # 2) Ô vuông checkbox là anh/em đứng TRƯỚC label
        box_xpath = label_xpath + "/preceding-sibling::div[contains(@class,'checkbox_checkbox-box__')]"

        # Đợi label xuất hiện
        self.sb.cdp.wait_for_element_visible(label_xpath, timeout=5)
        self.sb.cdp.click(label_xpath)
        self.sb.cdp.click(".select-multiple-badge_action__hsgHX u")
        self.sb.cdp.click("//div[contains(@class,'more-actions-button_action-row__')][.//span[normalize-space()='Remove Listing']]")
        self.sb.cdp.click("//button[.//div[normalize-space()='Remove multiple listing']]")


        


        self.sb.cdp.sleep(100)


    # HÀM HỖ TRỢ - Chọn thẻ drop select 
    def select_dropdown_option(self, label_name: str, option_text: str):
        self.sb.cdp.click(f"//div[div[@class='select-form_label__dAwvH' and text()='{label_name}']]//div[contains(@class,'select-form_select-wrapper')]")
        self.sb.cdp.click(f"//div[contains(@class,'radio-box_label') and normalize-space()='{option_text}']")

    # --------------------------------------------------
    # CREATER SALE GAME LOL
    #----------------------------------------------------
    def create_offer_lol_and_Valorant(self):
        self.sb.open('https://zeusx.com/create-offer')
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút next
        self.sb.cdp.type("input.co-select-game_input-search__AqNcm", self.data["id_game"]) # Điền id_game
        self.sb.cdp.click("div.co-select-game_game-item___jTq9:first-of-type") # Chọn sản phẩm đầu tiên
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút next
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input", self.data["name_sale"]) # điền tên sale
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input[type='text']", str(int(self.data["price_sale"]))) # giá tiền
        self.select_dropdown_option("Rank", self.data['rank_sale'])        # Chọn rank
        self.select_dropdown_option("Server", self.data['sever_sale'])        # Chọn rank
        self.sb.cdp.click("//div[contains(@class,'checkbox_checkbox__') and .//div[normalize-space()='Multiple quantity?']]") #Check check book Multiple quantity?
        self.sb.cdp.type('input[placeholder="Eg: 10"]', "99") # Điền số lượng sản phẩm dư
        self.sb.cdp.type("div.row-2 div.input_input__N_xjH:nth-child(2) input", "3")
        self.sb.cdp.press_keys("div.ck-content[contenteditable='true']", str(self.data["description_sale"])) # Điền mô tả sản phẩm
        # Điền tags ---------
        tags = str(self.data["tag_sale"]).split(",")
        for tag in tags:
            self.sb.cdp.type("input[placeholder='Enter to add']", tag) # Điền tags
            self.sb.cdp.evaluate('''document.querySelector("input[placeholder='Enter to add']").dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13,bubbles: true}));''') # nhấn enter
            time.sleep(0.5)
        # Điền tags ---------
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút nexĐườngt
        file_path = os.path.abspath(f"pic/{self.data['linkpic_sale']}") #  dẫn tới ảnh
        self.sb.cdp.wait_for_element_visible('.image-upload_image-upload-box__Iv_LD') # Chờ phần tử up ảnh xuất hiên
        el = self.sb.cdp.find(".image-upload_image-upload-box__Iv_LD:nth-child(1) > input").send_file(file_path) # up ảnh lên

        self.sb.cdp.click('.co-upload-photos_rules__iHACT .checkbox_checkbox-box__2fLhD') # Checkbox 
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH")#Click nút list item

    # --------------------------------------------------
    # CREATER SALE GAME LOL
    #----------------------------------------------------
    def creater_offer_roblox_and_pubg(self):
        self.sb.open('https://zeusx.com/create-offer')
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút next
        self.sb.cdp.type("input.co-select-game_input-search__AqNcm", self.data["id_game"]) # Điền id_game
        self.sb.cdp.click("div.co-select-game_game-item___jTq9:first-of-type") # Chọn sản phẩm đầu tiên
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút next
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input", self.data["name_sale"]) # điền tên sale
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input[type='text']", str(int(self.data["price_sale"]))) # giá tiền
        self.sb.cdp.click("//div[contains(@class,'checkbox_checkbox__') and .//div[normalize-space()='Multiple quantity?']]") #Check check book Multiple quantity?
        self.sb.cdp.type('input[placeholder="Eg: 10"]', "99") # Điền số lượng sản phẩm dư
        self.sb.cdp.type("div.row-2 div.input_input__N_xjH:nth-child(2) input", "3") # Điền giờ
        self.sb.cdp.press_keys("div.ck-content[contenteditable='true']", str(self.data["description_sale"])) # Điền mô tả sản phẩm
        # Điền tags ---------
        tags = str(self.data["tag_sale"]).split(",")
        for tag in tags:
            self.sb.cdp.type("input[placeholder='Enter to add']", tag) # Điền tags
            self.sb.cdp.evaluate('''document.querySelector("input[placeholder='Enter to add']").dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13,bubbles: true}));''') # nhấn enter
            time.sleep(0.5)
        # Điền tags ---------
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút nexĐườngt
        file_path = os.path.abspath(f"pic/{self.data['linkpic_sale']}") #  dẫn tới ảnh
        self.sb.cdp.wait_for_element_visible('.image-upload_image-upload-box__Iv_LD') # Chờ phần tử up ảnh xuất hiên
        el = self.sb.cdp.find(".image-upload_image-upload-box__Iv_LD:nth-child(1) > input").send_file(file_path) # up ảnh lên

        self.sb.cdp.click('.co-upload-photos_rules__iHACT .checkbox_checkbox-box__2fLhD') # Checkbox 
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH")#Click nút list item

    # --------------------------------------------------
    # CREATER SALE GAME GENHSHIN IMPACT
    #----------------------------------------------------
    def creater_offer_genshin_impact(self):
        self.sb.open('https://zeusx.com/create-offer')
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút next
        self.sb.cdp.type("input.co-select-game_input-search__AqNcm", self.data["id_game"]) # Điền id_game
        self.sb.cdp.click("div.co-select-game_game-item___jTq9:first-of-type") # Chọn sản phẩm đầu tiên
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút next
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input", self.data["name_sale"]) # điền tên sale
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input[type='text']", str(int(self.data["price_sale"]))) # giá tiền
        self.sb.cdp.click("//div[contains(@class,'checkbox_checkbox__') and .//div[normalize-space()='Multiple quantity?']]") #Check check book Multiple quantity?
        self.sb.cdp.type('input[placeholder="Eg: 10"]', "99") # Điền số lượng sản phẩm dư
        self.sb.cdp.type("div.row-2 div.input_input__N_xjH:nth-child(2) input", "3") # Điền giờ
        self.select_dropdown_option("Player Gender", self.data['character_sale'])  # Chon giới tính
        self.select_dropdown_option("Server/Region", self.data['sever_sale'])        # Chọn sever
    
        self.sb.cdp.press_keys("div.ck-content[contenteditable='true']", str(self.data["description_sale"])) # Điền mô tả sản phẩm
        # Điền tags ---------
        tags = str(self.data["tag_sale"]).split(",")
        for tag in tags:
            self.sb.cdp.type("input[placeholder='Enter to add']", tag) # Điền tags
            self.sb.cdp.evaluate('''document.querySelector("input[placeholder='Enter to add']").dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13,bubbles: true}));''') # nhấn enter
            time.sleep(0.5)
        # Điền tags ---------
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút nexĐườngt
        file_path = os.path.abspath(f"pic/{self.data['linkpic_sale']}") #  dẫn tới ảnh
        self.sb.cdp.wait_for_element_visible('.image-upload_image-upload-box__Iv_LD') # Chờ phần tử up ảnh xuất hiên
        el = self.sb.cdp.find(".image-upload_image-upload-box__Iv_LD:nth-child(1) > input").send_file(file_path) # up ảnh lên

        self.sb.cdp.click('.co-upload-photos_rules__iHACT .checkbox_checkbox-box__2fLhD') # Checkbox 
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH")#Click nút list item

    # --------------------------------------------------
    # CREATER SALE GAME GTA5
    #----------------------------------------------------
    def creater_offer_gta5(self):
        self.sb.open('https://zeusx.com/create-offer')
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút next
        self.sb.cdp.type("input.co-select-game_input-search__AqNcm", self.data["id_game"]) # Điền id_game
        self.sb.cdp.click("div.co-select-game_game-item___jTq9:first-of-type") # Chọn sản phẩm đầu tiên
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút next
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input", self.data["name_sale"]) # điền tên sale
        self.sb.cdp.type("div.input_input-wrapper__jq4iS > input[type='text']", str(int(self.data["price_sale"]))) # giá tiền
        self.sb.cdp.click("//div[contains(@class,'checkbox_checkbox__') and .//div[normalize-space()='Multiple quantity?']]") #Check check book Multiple quantity?
        self.sb.cdp.type('input[placeholder="Eg: 10"]', "99") # Điền số lượng sản phẩm dư
        self.sb.cdp.type("div.row-2 div.input_input__N_xjH:nth-child(2) input", "3") # Điền giờ
        self.select_dropdown_option("Platform / Device", self.data['device_sale'])  # Chon thiết bị
    
        self.sb.cdp.press_keys("div.ck-content[contenteditable='true']", str(self.data["description_sale"])) # Điền mô tả sản phẩm
        # Điền tags ---------
        tags = str(self.data["tag_sale"]).split(",")
        for tag in tags:
            self.sb.cdp.type("input[placeholder='Enter to add']", tag) # Điền tags
            self.sb.cdp.evaluate('''document.querySelector("input[placeholder='Enter to add']").dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13,bubbles: true}));''') # nhấn enter
            time.sleep(0.5)
        # Điền tags ---------
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH") # Nhấn nút nexĐườngt
        file_path = os.path.abspath(f"pic/{self.data['linkpic_sale']}") #  dẫn tới ảnh
        self.sb.cdp.wait_for_element_visible('.image-upload_image-upload-box__Iv_LD') # Chờ phần tử up ảnh xuất hiên
        el = self.sb.cdp.find(".image-upload_image-upload-box__Iv_LD:nth-child(1) > input").send_file(file_path) # up ảnh lên

        self.sb.cdp.click('.co-upload-photos_rules__iHACT .checkbox_checkbox-box__2fLhD') # Checkbox 
        self.sb.cdp.click("button.wo-step-control_btn-next__cotoH")#Click nút list item


    def wait_for_success_popup(self) -> bool:
        try:
            self.sb.cdp.wait_for_element_visible("div.success-popup_success-popup__bb900", timeout=15)
            print("✓ Đăng sản phẩm thành công!")
            return True
        except Exception as e:
            print(f"✗ Không thấy popup thành công: {str(e)}")
            return False
    
    def create_all_sale(self, data: dict) -> bool:
        self.data = data
        id_game = str(data.get("id_game", "")).strip()
        name_sale = str(data.get("name_sale", "")).strip()
        print(id_game, name_sale)
        self.creater_offer_roblox_and_pubg()
        success = self.wait_for_success_popup()


    def run_sele(self, ) -> bool:
        

        profile_dir = os.path.abspath(os.path.join("chrome_profiles", self.profile_name))
        os.makedirs(profile_dir, exist_ok=True)

        print(f"Bắt đầu khởi tạo driver")
        with SB(uc=True,locale="en",window_size="300,850", user_data_dir=profile_dir, ) as sb:
            self.sb = sb
            self.sb.activate_cdp_mode("https://zeusx.com/login")
            try:
                if sb.find_element("#FGRYW5"):
                    print("_Bắt Đầu Vượt captcha")
                    self.sb.sleep(10)
                    self.sb.uc_gui_click_captcha()
            except Exception:
                pass
            
            self._login_Zeusx()
            # self.del_product_of_type()
          

            # Phần automation - tạo sale 
            self.reader.load_exel()
            for index, row in enumerate(self.reader.iter_rows(), start=1 ):
                success = self.create_all_sale(row)

            print(f"Hàng: {index} : {'SUCCESS' if success else 'FAIL'}")
            



            
            self.sb.sleep(10)





if __name__=="__main__":
    runner = Zeusx_Automation()
    runner.run_sele()