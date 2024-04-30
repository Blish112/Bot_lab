import pandas as pd
import sys

def convrt(file_name:str):
    if file_name.endswith(".xlsx"):
        try:
            data = pd.read_excel(file_name)
        except FileNotFoundError:
            print(f'Файл не найден')
            return
        
        output_file = file_name.replace(".xlsx", ".json")
        data.to_json(output_file, orient="records", force_ascii=False)
        print(f"Файл успешно сконвертирован в {output_file}")
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file in sys.argv:
            convrt(file)
    else:
        print('Ошибка, вы не передали файл')
                
