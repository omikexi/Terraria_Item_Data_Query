import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter.messagebox import showerror, showwarning


# 全局样式配置
def set_global_style():
    style = ttk.Style()
    # 主色调（可根据喜好调整）
    style.theme_use("clam")
    style.configure(".", font=("微软雅黑", 10), foreground="#333333", background="#F5F5F5")

    # 标题标签样式
    style.configure("Title.TLabel", font=("微软雅黑", 12, "bold"), foreground="#2F5496", background="#F5F5F5")

    # 按钮样式
    style.configure("Primary.TButton", font=("微软雅黑", 10, "bold"), foreground="#FFFFFF", background="#409EFF",
                    relief="flat", borderwidth=0)
    style.map("Primary.TButton", background=[("active", "#66B1FF")])

    # 输入框样式
    style.configure("Entry.TEntry", fieldbackground="#FFFFFF", background="#FFFFFF", foreground="#333333",
                    borderwidth=1, relief="flat")

    # 下拉菜单样式
    style.configure("TMenubutton", background="#F5F5F5", foreground="#333333", font=("微软雅黑", 10))

    # 表格样式
    style.configure("Treeview", background="#FFFFFF", foreground="#333333", fieldbackground="#FFFFFF",
                    borderwidth=0, rowheight=26)
    style.configure("Treeview.Heading", font=("微软雅黑", 10, "bold"), background="#E6F3FF", foreground="#333333",
                    relief="flat")
    style.map("Treeview.Heading", background=[("active", "#D9ECFF")])


def load_command_file():
    global command_df
    try:
        command_df = pd.read_excel('素材/指令.xlsx')
        for item in command_tree.get_children():
            command_tree.delete(item)
        command_tree["show"] = "headings"
        command_tree["columns"] = list(command_df.columns)
        for col in command_df.columns:
            command_tree.heading(col, text=col)
            command_tree.column(col, anchor=tk.CENTER)
        for _, row in command_df.iterrows():
            command_tree.insert("", tk.END, values=list(row))
    except Exception as e:
        showerror("错误", f"加载文件失败: {str(e)}")


def search_file():
    selected_name = file_choice.get()
    selected_file = file_mapping[selected_name]
    search_term = search_entry.get().strip().lower()
    if not search_term:
        showwarning("警告", "请输入查询内容")
        return
    try:
        file_path = f'素材/{selected_file}'
        df = pd.read_excel(file_path)
        if selected_file in ['怪物id.xlsx', '物品id.xlsx', 'buff_id.xlsx', '坐骑id.xlsx']:
            if 'inner_name' in df.columns:
                df = df.drop(columns='inner_name')
        if selected_file == '物品id.xlsx' and 'id' in df.columns:
            df['id'] = pd.to_numeric(df['id'], errors='coerce').dropna().astype(int)
        if search_term in ['all', '*']:
            result_df = df
        else:
            result_df = df[
                df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)]
        for item in result_tree.get_children():
            result_tree.delete(item)
        result_tree["show"] = "headings"
        result_tree["columns"] = list(result_df.columns)
        for col in result_df.columns:
            result_tree.heading(col, text=col)
            result_tree.column(col, anchor=tk.CENTER)
        for _, row in result_df.iterrows():
            result_tree.insert("", tk.END, values=list(row))
    except Exception as e:
        showerror("错误", f"查询失败: {str(e)}")


root = tk.Tk()
root.title("国服泰拉瑞亚游戏数据查询工具")
root.geometry("1000x600")
root.configure(bg="#F5F5F5")

# 设置全局样式
set_global_style()

# 左侧框架
left_frame = tk.Frame(root, bg="#F5F5F5")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

command_label = ttk.Label(left_frame, text="指令文件内容", style="Title.TLabel")
command_label.pack(anchor=tk.W, pady=(0, 8))

left_table_frame = tk.Frame(left_frame, bg="#F5F5F5")
left_table_frame.pack(fill=tk.BOTH, expand=True)

# 左侧表格滚动条
command_vscroll = ttk.Scrollbar(left_table_frame, orient=tk.VERTICAL)
command_vscroll.pack(side=tk.RIGHT, fill=tk.Y)
command_hscroll = ttk.Scrollbar(left_table_frame, orient=tk.HORIZONTAL)
command_hscroll.pack(side=tk.BOTTOM, fill=tk.X)

command_tree = ttk.Treeview(
    left_table_frame,
    yscrollcommand=command_vscroll.set,
    xscrollcommand=command_hscroll.set,
    selectmode="extended",
    show="headings"
)
command_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

command_vscroll.config(command=command_tree.yview)
command_hscroll.config(command=command_tree.xview)

load_command_file()

# 右侧框架
right_frame = tk.Frame(root, bg="#F5F5F5")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# 右侧标题及下拉菜单
top_right_frame = tk.Frame(right_frame, bg="#F5F5F5")
top_right_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

file_choice = tk.StringVar(right_frame)
file_choice.set('物品id')
file_mapping = {
    '物品id': '物品id.xlsx',
    '怪物id': '怪物id.xlsx',
    '盔甲id': '盔甲id.xlsx',
    '前缀id': '前缀id.xlsx',
    'buff_id': 'buff_id.xlsx',
    '坐骑id': '坐骑id.xlsx',
    '事件': '事件.xlsx'
}
file_menu = ttk.OptionMenu(top_right_frame, file_choice, *file_mapping)
file_menu.pack(side=tk.LEFT, padx=(0, 10))

search_label = ttk.Label(top_right_frame, text="查询内容（输入all/*显示全部）", style="Title.TLabel")
search_label.pack(side=tk.LEFT, pady=(0, 5))

# 查询输入框和按钮
middle_right_frame = tk.Frame(right_frame, bg="#F5F5F5")
middle_right_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

search_entry = ttk.Entry(middle_right_frame, style="Entry.TEntry")
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

search_button = ttk.Button(middle_right_frame, text="查询", command=search_file, style="Primary.TButton")
search_button.pack(side=tk.LEFT)

# 查询结果区域
result_label = ttk.Label(right_frame, text="查询结果", style="Title.TLabel")
result_label.pack(anchor=tk.W, pady=(0, 8))

right_table_frame = tk.Frame(right_frame, bg="#F5F5F5")
right_table_frame.pack(fill=tk.BOTH, expand=True)

# 右侧表格滚动条
result_vscroll = ttk.Scrollbar(right_table_frame, orient=tk.VERTICAL)
result_vscroll.pack(side=tk.RIGHT, fill=tk.Y)

result_tree = ttk.Treeview(
    right_table_frame,
    yscrollcommand=result_vscroll.set,
    selectmode="extended",
    show="headings"
)
result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_vscroll.config(command=result_tree.yview)

root.mainloop()