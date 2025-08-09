# 🎮 泰拉瑞亚游戏数据查询系统（MySQL 版）

## 📋 项目简介

本系统为泰拉瑞亚玩家提供了一套完整的游戏数据管理工具，通过 MySQL 数据库存储游戏内核心数据（物品、Buff、怪物、指令等），并支持通过 SQL 查询快速检索信息。系统包含数据库设计、查询存储过程及 Excel 数据导入功能，适用于各类泰拉瑞亚相关工具开发或玩家数据查询需求。

**数据来源**：所有游戏数据均参考自[泰拉瑞亚维基（中文）](https://terraria.wiki.gg/zh/)

## 🛠️ 系统组成



```mermaid
graph TD
    A[数据库结构] --> A1[8张核心数据表]
    A --> A2[8个查询存储过程]
    B[数据导入工具] --> B1[Excel数据解析]
    B --> B2[MySQL批量导入]
    C[查询功能] --> C1[直接SQL查询]
    C --> C2[存储过程调用]
```

## 🔧 数据库搭建步骤

### 1. 创建数据库



```
CREATE DATABASE IF NOT EXISTS terraria

CHARACTER SET utf8mb4

COLLATE utf8mb4\_unicode\_ci;
```

### 2. 切换数据库



```
USE terraria;
```

### 3. 创建数据表结构



| 表名           | 用途           | 核心字段                                |
| ------------ | ------------ | ----------------------------------- |
| `armor_id`   | 存储盔甲数据       | `id, head, body, leg`               |
| `buff_id`    | 存储 Buff 效果数据 | `id, name, inner_name, type`        |
| `command`    | 存储游戏指令数据     | `id, command, notes`                |
| `event`      | 存储游戏事件数据     | `id, name, inner_name`              |
| `monster_id` | 存储怪物数据       | `id, name, inner_name, description` |
| `mount_id`   | 存储坐骑数据       | `id, name, inner_name`              |
| `object_id`  | 存储物品数据       | `id, name, inner_name`              |
| `prefix_id`  | 存储前缀数据       | `id, name`                          |



```
\-- 盔甲数据表

CREATE TABLE armor\_id (

&#x20; id double,

&#x20; head varchar(255),

&#x20; body varchar(255),

&#x20; leg varchar(255)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

\-- Buff数据表

CREATE TABLE buff\_id (

&#x20; id double,

&#x20; name varchar(255),

&#x20; inner\_name varchar(255),

&#x20; type char(2)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

\-- 指令数据表

CREATE TABLE command (

&#x20; id double,

&#x20; command varchar(255),

&#x20; notes varchar(255)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

\-- 事件数据表

CREATE TABLE event (

&#x20; id double,

&#x20; name varchar(255),

&#x20; inner\_name varchar(255)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

\-- 怪物数据表

CREATE TABLE monster\_id (

&#x20; id double,

&#x20; name varchar(255),

&#x20; inner\_name varchar(255),

&#x20; description varchar(255) DEFAULT ''

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

\-- 坐骑数据表

CREATE TABLE mount\_id (

&#x20; id double,

&#x20; name varchar(255),

&#x20; inner\_name varchar(255)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

\-- 物品数据表

CREATE TABLE object\_id (

&#x20; id double,

&#x20; name varchar(255),

&#x20; inner\_name varchar(255)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

\-- 前缀数据表

CREATE TABLE prefix\_id (

&#x20; id double,

&#x20; name varchar(255)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 4. 创建查询存储过程

存储过程提供了便捷的模糊查询功能，支持按关键词快速检索各类数据：



```
DELIMITER //

\-- 查询Buff（按名称）

CREATE PROCEDURE SearchBuff(IN keyword VARCHAR(255))

BEGIN

&#x20;   SELECT \* FROM buff\_id WHERE name LIKE CONCAT('%', keyword, '%');

END //

\-- 查询事件（按名称）

CREATE PROCEDURE SearchEvent(IN keyword VARCHAR(255))

BEGIN

&#x20;   SELECT \* FROM event WHERE name LIKE CONCAT('%', keyword, '%');

END //

\-- 查询怪物（按名称）

CREATE PROCEDURE SearchMonster(IN keyword VARCHAR(255))

BEGIN

&#x20;   SELECT \* FROM monster\_id WHERE name LIKE CONCAT('%', keyword, '%');

END //

\-- 查询坐骑（按名称）

CREATE PROCEDURE SearchMount(IN keyword VARCHAR(255))

BEGIN

&#x20;   SELECT \* FROM mount\_id WHERE name LIKE CONCAT('%', keyword, '%');

END //

\-- 查询物品（按名称）

CREATE PROCEDURE SearchObject(IN keyword VARCHAR(255))

BEGIN

&#x20;   SELECT \* FROM object\_id WHERE name LIKE CONCAT('%', keyword, '%');

END //

\-- 查询前缀（按名称）

CREATE PROCEDURE SearchPrefix(IN keyword VARCHAR(255))

BEGIN

&#x20;   SELECT \* FROM prefix\_id WHERE name LIKE CONCAT('%', keyword, '%');

END //

\-- 查询指令（按备注）

CREATE PROCEDURE SearchCommand(IN keyword VARCHAR(255))

BEGIN

&#x20;   SELECT \* FROM command WHERE notes LIKE CONCAT('%', keyword, '%');

END //

\-- 查询盔甲（按头部/身体/腿部）

CREATE PROCEDURE SearchArmor(IN keyword VARCHAR(255))

BEGIN

&#x20;   SELECT \* FROM armor\_id&#x20;

&#x20;   WHERE head LIKE CONCAT('%', keyword, '%')

&#x20;   OR body LIKE CONCAT('%', keyword, '%')

&#x20;   OR leg LIKE CONCAT('%', keyword, '%');

END //

DELIMITER ;
```

## 📊 数据导入工具使用说明

### 工具功能

通过 Python 脚本将 Excel 格式的游戏数据批量导入到 MySQL 数据库，支持灵活配置导入参数，适用于初始化数据库或更新数据。

### 文件结构



```
excel\_to\_mysql/  \<!-- 项目根目录 -->

├── main.py               # 数据导入主程序

├── config.py             # 配置文件（数据库连接、Excel路径等）

├── requirements.txt      # 项目依赖清单

└── 素材/                 # Excel数据文件存放目录

&#x20;   ├── buff\_id.xlsx      # Buff数据Excel文件

&#x20;   ├── 怪物id.xlsx       # 怪物数据Excel文件

&#x20;   ├── 盔甲id.xlsx       # 盔甲数据Excel文件

&#x20;   ├── 前缀id.xlsx       # 前缀数据Excel文件

&#x20;   ├── 物品id.xlsx       # 物品数据Excel文件

&#x20;   ├── 坐骑id.xlsx       # 坐骑数据Excel文件

&#x20;   ├── 事件.xlsx         # 事件数据Excel文件

&#x20;   └── 指令.xlsx         # 指令数据Excel文件
```

### 配置说明（config.py）



```
\# 数据库配置 - 根据实际环境修改

DB\_CONFIG = {

&#x20;   'host': 'localhost',    # 数据库主机地址

&#x20;   'user': 'root',         # 数据库用户名

&#x20;   'password': '',         # 数据库密码

&#x20;   'database': 'terraria', # 数据库名称

&#x20;   'port': '3306'          # 数据库端口

}

\# Excel文件配置 - 素材文件夹路径（无需修改，已适配项目结构）

EXCEL\_CONFIG = {

&#x20;   'folder\_path': '素材'   # 素材文件夹相对路径（位于项目根目录下）

}

\# 文件与表名映射关系 - 自动匹配Excel文件与数据库表

FILE\_TABLE\_MAPPING = {

&#x20;   'buff\_id.xlsx': 'buff\_id',

&#x20;   '怪物id.xlsx':'monster\_id',

&#x20;   '盔甲id.xlsx': 'armor\_id',

&#x20;   '前缀id.xlsx': 'prefix\_id',

&#x20;   '物品id.xlsx': 'object\_id',

&#x20;   '坐骑id.xlsx':'mount\_id',

&#x20;   '事件.xlsx': 'event',

&#x20;   '指令.xlsx': 'command',

}
```

### 使用步骤



1.  **准备数据**：确保所有 Excel 文件已放入`素材`文件夹，且文件格式与数据表结构匹配（列名一致）

2.  **安装依赖**：



```
pip install -r requirements.txt
```



1.  **配置参数**：编辑`config.py`，填写数据库连接信息（重点修改`user`和`password`）

2.  **运行脚本**：在项目根目录（`excel_to_mysql`文件夹）中执行



```
python main.py
```



1.  **查看结果**：脚本会输出各文件的导入结果，成功时显示 “数据已成功从 XX 导入到表 XX”，失败时显示具体错误信息

## 🔍 数据查询方法

### 直接 SQL 查询示例



```
\-- 查询所有Buff

SELECT \* FROM buff\_id WHERE name LIKE '%%';

\-- 查询所有事件

SELECT \* FROM event WHERE name LIKE '%%';

\-- 查询所有怪物

SELECT \* FROM monster\_id WHERE name LIKE '%%';

\-- 查询所有坐骑

SELECT \* FROM mount\_id WHERE name LIKE '%%';

\-- 查询所有物品

SELECT \* FROM object\_id WHERE name LIKE '%%';

\-- 查询所有前缀

SELECT \* FROM prefix\_id WHERE name LIKE '%%';

\-- 查询所有指令

SELECT \* FROM command WHERE notes LIKE '%%';

\-- 查询包含"铁"的盔甲

SELECT \* FROM armor\_id WHERE CONCAT\_WS(',', head, body, leg) LIKE CONCAT('%', '铁', '%');
```

### 存储过程调用示例



```
\-- 查询包含"生命"的Buff

CALL SearchBuff('生命');

\-- 查询包含"雨"的事件

CALL SearchEvent('雨');

\-- 查询包含"史莱姆"的怪物

CALL SearchMonster('史莱姆');

\-- 查询包含"猪龙鱼"的坐骑

CALL SearchMount('猪龙鱼');

\-- 查询包含"剑"的物品

CALL SearchObject('剑');

\-- 查询包含"时间"的指令

CALL SearchCommand('时间');

\-- 查询包含"铜"的盔甲

CALL SearchArmor('铜');
```

## ⚠️ 注意事项



*   首次使用需先执行「数据库搭建步骤」创建表结构和存储过程

*   Excel 导入时，确保表头与数据库表字段完全一致（大小写不敏感）

*   脚本默认使用`if_exists='replace'`参数，会覆盖目标表原有数据，首次导入后建议备份数据

*   数据库采用`utf8mb4`字符集，完美支持中文查询和特殊符号显示

*   数据版本可能与游戏最新版本存在差异，创建项目时版本为1.4.49565,建议结合[泰拉瑞亚维基（中文）](https://terraria.wiki.gg/zh/)查阅最新信息



***