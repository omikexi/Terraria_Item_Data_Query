# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'terraria',
    'port': '3306'
}


EXCEL_CONFIG = {
    'folder_path': '素材'
}

# 文件与表名映射配置
FILE_TABLE_MAPPING = {
    'buff_id.xlsx': 'buff_id',
    '怪物id.xlsx':'monster_id',
    '盔甲id.xlsx': 'armor_id',
    '前缀id.xlsx': 'prefix_id',
    '物品id.xlsx': 'object_id',
    '坐骑id.xlsx':'mount_id',
    '事件.xlsx': 'event',
    '指令.xlsx': 'command',
}