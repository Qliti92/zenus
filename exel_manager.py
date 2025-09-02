import pandas as pd

class ExelReader:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.df = None


    def load_exel(self):
        self.df = pd.read_excel(self.file_path)


    def iter_rows(self):
        """Trả về từng hàng dưới dạng dict"""
        if self.df is None:
            raise ValueError("Bạn chưa load file! Hãy gọi load() trước.")
        
        for _, row in self.df.iterrows():
            yield row.to_dict()


# Cách dùng:
if __name__ == "__main__":
    reader = ExelReader("du_lieu.xlsx")  
    reader.load_exel()

    for record in reader.iter_rows():
        id_game = record["id_game"]
        name_sale = record["name_sale"]
        print(f"{id_game} - {name_sale}")


