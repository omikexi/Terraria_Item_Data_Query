import os
import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONFIG, EXCEL_CONFIG, FILE_TABLE_MAPPING


def excel_to_mysql():
    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        for excel_file, table_name in FILE_TABLE_MAPPING.items():
            file_path = os.path.join(EXCEL_CONFIG['folder_path'], excel_file)
            df = pd.read_excel(file_path)
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists='replace',
                index=False
            )
            print(f"数据已成功从 {excel_file} 导入到表 {table_name}！")
    except Exception as e:
        print(f"导入失败：{str(e)}")
    finally:
        if 'engine' in locals():
            engine.dispose()
if __name__ == "__main__":
    excel_to_mysql()