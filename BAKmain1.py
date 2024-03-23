import tkinter as tk
import sys
from tkinter import Canvas, ttk, scrolledtext, Button, VERTICAL, NS, NSEW, END
import pymysql

#################################################
# 一、该函数库可以import pymysql  (全部数据查询)
# (实现查询所有)直接蒋数据库查询出来的数据转换成列表，依照字典的形式存储，然后写入但页面表中
#################################################
def get_work_tesk(agvcode) -> list:
    conn = pymysql.connect(host='172.16.12.5', user='root', password='root123', db='evo_wcs_g2p', port=3306,charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 查询主任务信息
    cur.execute('select date_format(created_date,"%Y-%m-%d %T") created_date, agv_code, robot_job_id, work_mode, state, bucket_slot_code, target_bucket_slot_code from  evo_wcs_g2p.bucket_robot_job where agv_code ="' + agvcode + '"  and state not in("ABNORMAL_CANCEL", "ABNORMAL_COMPLETED", "CANCEL", "DONE") order by created_date desc')
    # 游标对象接受元组
    return cur.fetchall()

def get_container(agvcode) -> list:
    conn = pymysql.connect(host='172.16.12.5', user='root', password='root123', db='evo_wcs_g2p', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 查询主任务信息
    cur.execute('select robot_job_id,container_code from workbin_job_extends where robot_job_id in(select robot_job_id from bucket_robot_job where agv_code ="' + agvcode + '"  and state not in("ABNORMAL_CANCEL","ABNORMAL_COMPLETED","CANCEL","DONE") )')
       # 游标对象接受元组
    return cur.fetchall()


def get_agv_band(agvcode) -> list:
    conn = pymysql.connect(host='172.16.12.5', user='root', password='root123', db='evo_wcs_g2p', port=3306,charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 查询主任务信息
    cur.execute('select a.container_code from evo_basic.basic_container a RIGHT JOIN (select bb.id from evo_basic.basic_bucket bb where bucket_code in(select v.bucket_code from  evo_rcs.basic_agv v WHERE agv_code= "' + agvcode + '")) as hh ON a.bucket_id = hh.id')
        # 游标对象接受元组
    return cur.fetchall()

def get_daoku(agvcode,containercode) -> list:
    conn = pymysql.connect(host='172.16.12.5', user='root', password='root123', db='evo_wcs_g2p', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 查询主任务信息
    cur.execute('select date_format(created_date,"%Y-%m-%d %T") created_date,container_code, start_slot_code, end_slot_code, work_mode,state from workbin_standard_move_job where  agv_code="' + agvcode + '" and  container_code= "' + containercode + '"  ORDER BY created_date desc')
    # 游标对象接受元组
    return cur.fetchall()



# 定义一个退出点击触发函数
def tool_exit():
    sys.exit()

# 定义一个点击及查询事件
def get_data():
    agvcode = en1.get()
    work_tesk = get_work_tesk(agvcode)
    for i in work_tesk:
        data1 = []
        for j in i:
            data1.append(str(i[j]))
        data2 = tuple(data1)
        tree_date.insert("","end",text="1",values=data2)

    container = get_container(agvcode)
    dc = []
    for i in container:
        data1 = []
        for j in i:
            data1.append(str(i[j]))
        data2 = tuple(data1)
        dc.append(str(data2[1]))
        tree_date2.insert("", "end", text="1", values=data2)


    banding = get_agv_band(agvcode)
    cc =[]
    for i in banding:
        data1 = []
        for j in i:
            data1.append(str(i[j]))
        data2 = tuple(data1)
        cc.append(data2[0])
        tree_date3.insert("", "end", text="1", values=data2)

    # 判断绑定到车上的料箱是否在任务组中没有
    for i in cc:
        if i in dc:
            continue
        else:
            daoku = get_daoku(agvcode,i)
            for i in daoku:
                data1 = []
                for j in i:
                    data1.append(str(i[j]))
                data2 = tuple(data1)
                tree_date4.insert("", "end", text="1", values=data2)



window = tk.Tk()
# 设置标题
window.title('故障离场助手')
# 窗口的位置和大小
sw = window.winfo_screenwidth()
# 得到屏幕宽度
sh = window.winfo_screenheight()
# 得到屏幕高度
ww = 1700
wh = 800
# 窗口宽高为500
x = (sw-ww) / 2
y = (sh-wh) / 2
window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
# 设置窗口是否可以变化长宽,默认可变
window.resizable(width=False, height=False)


canvas = Canvas(window)
# 创建表格
tree_date = ttk.Treeview(canvas, show='headings', height=10)
Label1 = ttk.Label(canvas, text="当前AGV作业中的任务信息").pack()
canvas.place(x=10, y=10)
# 定义列
tree_date["columns"] = ["created_date", "agv_code", "robot_job_id", "work_mode", "state","bucket_slot_code","target_bucket_slot_code"]
tree_date.pack()
# 设置列宽度
tree_date.column("created_date", width=140)
tree_date.column("agv_code", width=150)
tree_date.column("robot_job_id", width=150)
tree_date.column("work_mode", width=140)
tree_date.column("state", width=140)
tree_date.column("bucket_slot_code", width=140)
tree_date.column("target_bucket_slot_code", width=140)
# 添加列名
tree_date.heading("created_date", text="时间")
tree_date.heading("agv_code", text="agv编码")
tree_date.heading("robot_job_id", text="任务号")
tree_date.heading("work_mode", text="模式")
tree_date.heading("state", text="状态")
tree_date.heading("bucket_slot_code", text="开始库位")
tree_date.heading("target_bucket_slot_code", text="目标库位")
print(type(tree_date))



tree_date2 = ttk.Treeview(canvas, show='headings', height=10)
Label2 = ttk.Label(canvas, text="当前AGV作业中的任务号和容器号").pack()
canvas.place(x=10, y=20)
# 定义列
tree_date2["columns"] = ["robot_job_id", "container_code"]
tree_date2.pack()
# 设置列宽度
tree_date2.column("robot_job_id", width=350)
tree_date2.column("container_code", width=350)
# 添加列名
tree_date2.heading("robot_job_id", text="任务号")
tree_date2.heading("container_code", text="容器号")

tree_date3 = ttk.Treeview(canvas, show='headings', height=10)
Label3 = ttk.Label(canvas, text="当前绑定在AGV上的容器号").pack()
canvas.place(x=10, y=30)
# 定义列
tree_date3["columns"] = ["container_code"]
tree_date3.pack()
# 设置列宽度
tree_date3.column("container_code",width=700)
# 添加列名
tree_date3.heading("container_code", text="容器号")

canvas2 = Canvas(window)
tree_date4 = ttk.Treeview(canvas2, show='headings', height=12)
Label4 = ttk.Label(canvas2, text="当前正在倒箱的容器号").pack()
canvas2.place(x=1050, y=30)
# 定义列
tree_date4["columns"] = ["created_date","container_code","start_slot_code","end_slot_code","work_mode","state"]
tree_date4.pack()
tree_date4.column("created_date",width=100)
# 添加列名
tree_date4.heading("created_date", text="创建时间")
# 设置列宽度
tree_date4.column("container_code",width=100)
# 添加列名
tree_date4.heading("container_code", text="容器号")
tree_date4.column("start_slot_code",width=100)
# 添加列名
tree_date4.heading("start_slot_code", text="起始库位")
tree_date4.column("end_slot_code",width=100)
# 添加列名
tree_date4.heading("end_slot_code", text="目标库位")
tree_date4.column("work_mode",width=100)
# 添加列名
tree_date4.heading("work_mode", text="工作模式")
tree_date4.column("state",width=100)
# 添加列名
tree_date4.heading("state", text="状态")

Label4 = ttk.Label(canvas2, text="请先输入当前AGV编码，然后查询：",font=('微软雅黑', 14)).pack()
en1= ttk.Entry(canvas2,width=30)
en1.pack(padx=10,pady=10)



run_button = Button(window, text="查询", font=('微软雅黑', 20), width=5,command=get_data)
run_button.place(x=1200, y=400)

exit_button = Button(window, text="退出", font=('微软雅黑', 20), width=5,command=tool_exit)
exit_button.place(x=1400, y=400)

window.mainloop()