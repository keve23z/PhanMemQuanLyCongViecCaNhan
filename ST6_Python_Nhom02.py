import datetime
import sys
import json
import pandas as pd
import tkinter as tk
from tkinter import messagebox, scrolledtext
from bs4 import BeautifulSoup
import requests
import hashlib
import re

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
class CongViec:
    def __init__(self, maCV, tieuDe, moTa, hanChot, chiSoUuTien):
        self.MaCV = maCV
        self.TieuDe = tieuDe
        self.MoTa = moTa
        self.HanChot = hanChot
        self.ChiSoUuTien = int(chiSoUuTien)  

    def ConvertToJson(self):
        return {
            "MaCV": self.MaCV,
            "TieuDe": self.TieuDe,
            "MoTa": self.MoTa,
            "HanChot": self.HanChot,
            "ChiSoUuTien": self.ChiSoUuTien
        }

class DanhSachCongViec:
    def __init__(self):
        self.DS = []

    def Loadfile(self, fileName):
        try:
            with open(fileName, 'r', encoding='utf-8') as file:
                self.DS = json.load(file)
        except FileNotFoundError:
            print("Không tìm thấy file!!!")
            self.DS = []
        except json.JSONDecodeError:
            print("File Json đang rỗng")
            self.DS = []

    def SaveFile(self, fileName):
        try:
            with open(fileName, 'w', encoding='utf-8') as file:
                json.dump(self.DS, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Lỗi đọc file: {e}")

    def KiemTraMaCV(self, NewMaCV, OldMaCV=None):
        for cv in self.DS:
            if cv['MaCV'] == NewMaCV and NewMaCV != OldMaCV:
                return False
        return True

    def ThemCongViec(self, MaCV, TieuDe, MoTa, HanChot, ChiSoUuTien):
        if self.KiemTraMaCV(MaCV):
            cv = CongViec(MaCV, TieuDe, MoTa, HanChot, ChiSoUuTien)
            self.DS.append(cv.ConvertToJson())
            self.DS.sort(key=lambda ChiSo: int(ChiSo["ChiSoUuTien"])) 
            return True
        else:
            messagebox.showerror("Lỗi", "Mã công việc đã tồn tại. Vui lòng điền mã khác!!")
            return False

    def ChinhSuaCongViec(self, MaCV, TieuDe, MoTa, HanChot, ChiSoUuTien, CVChinhSua, fileName):
        if not all((MaCV, TieuDe)):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
            return
        try:
            datetime.datetime.strptime(HanChot, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Lỗi", "Sai định dạng Ngày/Tháng/Năm!!")
            return
        try:
            ChiSoUuTien = int(ChiSoUuTien)
        except ValueError:
            messagebox.showerror("Lỗi", "Chỉ số ưu tiên phải thuộc kiểu int")
            return

        oldMaCV = CVChinhSua['MaCV']
        if self.KiemTraMaCV(MaCV, oldMaCV):
            CVChinhSua['MaCV'] = MaCV
            CVChinhSua['TieuDe'] = TieuDe
            CVChinhSua['MoTa'] = MoTa
            CVChinhSua['HanChot'] = HanChot
            CVChinhSua['ChiSoUuTien'] = ChiSoUuTien

            self.DS.sort(key=lambda ChiSo: int(ChiSo["ChiSoUuTien"]))  # Ensure sorting as integers
            self.SaveFile(fileName)
            messagebox.showinfo("Thông báo", "Chỉnh sửa thành công!!")
        else:
            messagebox.showerror("Lỗi", "Mã công việc đã tồn tại. Vui lòng điền mã khác!!")

    def ChinhSuaCongViec_hienthi(self, ChinhSuaCongViec, MaCV, TieuDe, MoTa, HanChot, ChiSoUuTien, CVChinhSua, fileName):
        self.ChinhSuaCongViec(MaCV, TieuDe, MoTa, HanChot, ChiSoUuTien, CVChinhSua, fileName)
        ChinhSuaCongViec.destroy()
    def TimCongViec(self, MaCV):
        for CV in self.DS:
            if CV['MaCV'] == MaCV:
                return CV
        return None
""" ============================================================================================================ """

""" Cửa sổ chính khi đăng nhập thành công """
def CuaSoChucNang(loai):
    clear_window()
    root.geometry("1000x650+300+50")
    root.title("Chức năng")
    root.configure(bg="#63cdda")
    label_MoTaChucNang = tk.Label(root,text="Các chức năng quản lý công việc",font=("Sriracha",30,"bold"),bg="#63cdda",fg="#f7f1e3")
    label_MoTaChucNang.pack(pady=10)
    """ MENU chức năng """
    frame_Them = tk.Frame(root,bg="#aaa69d",bd=5)
    button_Them = tk.Button(frame_Them,text="Thêm một công việc vào danh sách",width=50,font=("Lexend Deca",18),relief="flat",command=lambda:CuaSoThem(loai))
    frame_Them.pack(pady=10)
    button_Them.pack()

    frame_HienThi = tk.Frame(root,bg="#aaa69d",bd=5)
    button_HienThi = tk.Button(frame_HienThi,text="Hiển thị danh sách công việc hiện có",width=50,font=("Lexend Deca",18),relief="flat",command=lambda:CuaSoHienThi(loai))
    frame_HienThi.pack(pady=15)
    button_HienThi.pack()
        
    frame_Sua = tk.Frame(root,bg="#aaa69d",bd=5)
    button_Sua = tk.Button(frame_Sua,text="Chỉnh sửa thông tin công việc",width=50,font=("Lexend Deca",18),relief="flat",command=lambda:CuaSoChinhSua(loai))
    frame_Sua.pack(pady=20)
    button_Sua.pack()
    if loai==1:
        root.geometry("1000x450+300+50")
    else:
        frame_Xoa = tk.Frame(root,bg="#aaa69d",bd=5)
        button_Xoa = tk.Button(frame_Xoa,text="Xoá một hoặc nhiều công việc",width=50,font=("Lexend Deca",18),relief="flat",command=lambda:CuaSoXoa(loai))
        frame_Xoa.pack(pady=15)
        button_Xoa.pack()
        
        frame_ThemTuWeb =tk.Frame(root,bg="#aaa69d",bd=5) 
        button_ThemTuWeb=tk.Button(frame_ThemTuWeb,text="Thêm Từ Web vào danh sách",width=50,font=("Lexend Deca",18),relief="flat",command=lambda:CuaSoCrawlWeb(loai))  
        frame_ThemTuWeb.pack(pady=20)
        button_ThemTuWeb.pack()
    
    frame_Dangxuat =tk.Frame(root,bg="#aaa69d",bd=5) 
    button_Dangxuat=tk.Button(frame_Dangxuat,text="Đăng Xuất",width=20,font=("Lexend Deca",18),relief="flat",command=exporting)  
    frame_Dangxuat.pack(pady=20)
    button_Dangxuat.pack()
    
""" Kết thúc cửa sổ menu chức năng """
""" ============================================================================================================ """
"""Các hàm phụ"""
#Hàm xoá nàm hình cũ
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()  
# Hàm khởi tạo thanh tiến trình
def create_progress_bar(parent, width=300, height=30):
    global progress_bar, progress_text, progress
    progress = 0  # Phần trăm hoàn thành (0-100)
    progress_bar = tk.Canvas(parent, width=width, height=height, bg="white")
    progress_bar.pack(pady=20)
    progress_bar.create_rectangle(0, 0, 0, height, fill="blue", tags="bar")
    progress_bar.create_text(width // 2, height // 2, text="0%", fill="black", tags="text")

# Hàm cập nhật tiến trình
def set_progress(value):
    global progress
    progress = value
    update_progress()

# Hàm để cập nhật hiển thị thanh tiến trình và văn bản
def update_progress():
    fill_width = (progress / 100) * progress_bar.winfo_width()
    progress_bar.coords("bar", 0, 0, fill_width, progress_bar.winfo_height())
    progress_bar.itemconfig("text", text=f"{progress}%")

# Hàm hiển thị thông báo hoàn thành
def show_completion_message():
    messagebox.showinfo("Thông báo", "Thành công đăng ký!!!")
    root_temp.destroy()
    login()

# Hàm giả lập tiến trình
def simulate_progress(current_value=0):
    if current_value <= 100:
        set_progress(current_value)
        root_temp.after(50, simulate_progress, current_value + 1)
    else:
        show_completion_message()

def loading():
    global root_temp
    root_temp = tk.Toplevel(root)
    root_temp.title("Đang Tải")
    root_temp.geometry("350x100+550+300")
    create_progress_bar(root_temp, width=300, height=30)
    simulate_progress(0)
# Hàm check mức độ của Password
def check_password_strength(event=None):
    password = password_entry.get()
    strength = calculate_strength(password)
    display_strength(strength)

def calculate_strength(password):
    length_criteria = len(password) >= 8
    digit_criteria = re.search(r'\d', password) is not None
    uppercase_criteria = re.search(r'[A-Z]', password) is not None
    lowercase_criteria = re.search(r'[a-z]', password) is not None
    special_char_criteria = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None
    
    score = sum([length_criteria, digit_criteria, uppercase_criteria, lowercase_criteria, special_char_criteria])
    
    if score <= 1:
        return "Yếu", "red"
    elif score == 2:
        return "Trung bình", "dimgray"
    elif score == 3:
        return "Khá", "maroon"
    elif score == 4:
        return "Mạnh", "green"
    elif score == 5:
        return "Rất mạnh", "blue"

def display_strength(strength_info):
    strength_text, strength_color = strength_info
    strength_label.config(text=f"Độ mạnh của mật khẩu: {strength_text}", fg=strength_color) 
# Hàm chia độ rộng của 2 lựa chọn
def radio(label, options, x, y):
    var = tk.StringVar(value=options[0])
    for i, option in enumerate(options):
        radio_button = tk.Radiobutton(root, text=option, bg="azure", variable=var, value=option, font=("Times New Roman", 11))
        radio_button.place(x=x + i * 100, y=y)
    return var
# Hàm thoát màn hình

def exit(x,y):
    frame_Exit = tk.Frame(root, bd=2, bg="#2d3436")
    frame_Exit.place(x=x, y=y)
    button_Exit = tk.Button(frame_Exit, relief="flat", bg="#dfe6e9", text="Thoát", width=10, font=("Times New Roman", 10, "bold"), command=root.destroy)
    button_Exit.pack()
    
#Hàm xuất và quay lại 
def CuaSoVe(title,loai):
    clear_window()
    root.title(title)
    root.geometry("600x700+500+50")
    root.configure(bg="#f7f1e3")
    frame_Back = tk.Frame(root, bd=2, bg="#2d3436")
    frame_Back.place(x=10, y=10)
    button_Back = tk.Button(frame_Back, relief="flat", bg="#dfe6e9", text=f"Quay lại", width=10, font=("Times New Roman", 10, "bold"),command=lambda:CuaSoChucNang(loai))
    button_Back.pack()
""" Các hàm chức năng """
'''hiển thị'''
def CapNhatListBox(listBox, DSCV):
    listBox.delete(0, tk.END)
    for idx, task in enumerate(DSCV, start=1):
        listBox.insert(tk.END, f"{idx}. {task['MaCV']} - {task['TieuDe']}")

def HienThi(CuaSoHienThiChiTietCV, task_PhanTuDuocChon):
    frame_HienThi = tk.Frame(CuaSoHienThiChiTietCV, bd=2, bg="#2d3436")
    frame_HienThi.pack(pady=7, padx=7)
    label_HienThiMaCV = tk.Label(frame_HienThi, text=f"{task_PhanTuDuocChon['TieuDe']}", width=35, font=("Times New Roman", 20, "bold"))
    label_HienThiMaCV.pack()

    frame_HienThi.pack(pady=10, padx=5)
    label_HienThiMaCV = tk.Label(frame_HienThi, text=f"Mã : {task_PhanTuDuocChon['MaCV']}", width=35, font=("Times New Roman", 15, "bold"))
    label_HienThiMaCV.pack()
    label_HienThiMoTa = tk.Label(frame_HienThi, text="Chi tiết ", width=35, font=("Times New Roman", 15, "bold"))
    label_HienThiMoTa.pack()
    text_MoTa = scrolledtext.ScrolledText(frame_HienThi, wrap=tk.WORD, width=45, height=10, font=("Times New Roman", 13))
    text_MoTa.insert(tk.END, task_PhanTuDuocChon['MoTa'])
    text_MoTa.config(state=tk.DISABLED)
    text_MoTa.pack()
    label_HienThiHanChot = tk.Label(frame_HienThi, text=f"Hạn chót : {task_PhanTuDuocChon['HanChot']}", width=39, font=("Times New Roman", 15, "bold"))
    label_HienThiHanChot.pack()
    label_HienThiChiSoUuTien = tk.Label(frame_HienThi, text=f"Độ ưu tiên : {task_PhanTuDuocChon['ChiSoUuTien']}", width=39, font=("Times New Roman", 15, "bold"))
    label_HienThiChiSoUuTien.pack()
def HienThiChiTietCV(loai,listBox, dscv):
    index_PhanTuDuocChon = listBox.curselection()
    if index_PhanTuDuocChon:
        task_PhanTuDuocChon = dscv.DS[index_PhanTuDuocChon[0]]
        CuaSoHienThiChiTietCV = tk.Toplevel()
        CuaSoHienThiChiTietCV.geometry("400x500+100+150")
        CuaSoHienThiChiTietCV.title("Chi tiết công việc")
        CuaSoHienThiChiTietCV.configure(bg="#b2bec3")

        HienThi(CuaSoHienThiChiTietCV, task_PhanTuDuocChon)
        if loai==0:
            frame_Button_ChinhSua = tk.Frame(CuaSoHienThiChiTietCV, bg="#2d3436", bd=2)
            frame_Button_ChinhSua.pack(pady=10)

            frame_Button_Xoa = tk.Frame(CuaSoHienThiChiTietCV, bg="#2d3436", bd=2)
            frame_Button_Xoa.pack(pady=10)

            button_ChinhSua = tk.Button(frame_Button_ChinhSua,text=f"Chỉnh sửa",width=10,font=("Times New Roman",15,"bold"),relief="flat",command=lambda : CuaSoChinhSuaCongViec_hienthi(CuaSoHienThiChiTietCV,listBox,dscv,fileName))
            button_ChinhSua.pack()

            button_Xoa = tk.Button(frame_Button_Xoa,text=f"Xoá",width=10,font=("Times New Roman",15,"bold"),bg="#d63031",fg="#dfe6e9",relief="flat",command=lambda : XoaCongViec_hienthi(CuaSoHienThiChiTietCV,listBox,dscv,fileName))
            button_Xoa.pack()

def HienThiDanhSachCV(listBox, DSCV):
    if not DSCV:
        messagebox.showinfo("Thông báo", "Hiện chưa có công việc nào trong danh sách!!")
    else:
        CapNhatListBox(listBox, DSCV)
''' thêm'''
def ThemCongViec(entry_MaCV,entry_TieuDe,text_MoTa,entry_HanChot,entry_ChiSoUuTien,dscv,fileName):  
        MaCV = entry_MaCV.get()
        TieuDe = entry_TieuDe.get()
        MoTa = text_MoTa.get("1.0", tk.END)
        HanChot = entry_HanChot.get()
        ChiSoUuTien = entry_ChiSoUuTien.get()
        if not all((MaCV,TieuDe)):
            messagebox.showerror("Lỗi","Vui lòng điền đầy đủ thông tin")
            return
        try:
            datetime.datetime.strptime(HanChot,'%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Lỗi","Sai định dạng Ngày/Tháng/Năm!!")
            return
        try :
            int(ChiSoUuTien)
        except ValueError:
            messagebox.showerror("Lỗi","Thông tin thêm vào phải thuộc kiểu int")
            return
        if dscv.ThemCongViec(MaCV,TieuDe,MoTa,HanChot,ChiSoUuTien):      
            dscv.SaveFile(fileName)
            entry_MaCV.delete(0, tk.END)
            entry_TieuDe.delete(0, tk.END)
            text_MoTa.delete("1.0", tk.END)
            entry_HanChot.delete(0, tk.END)
            entry_ChiSoUuTien.delete(0,tk.END)
            messagebox.showinfo("Thông báo","Thêm thành công!")
'''xoá'''
def XoaCongViec_hienthi(CuaSoHienThiChiTietCV,listBox,dscv,fileName):
    XoaCongViec(listBox,dscv,fileName)
    CuaSoHienThiChiTietCV.destroy()
def XoaCongViec(listBox,dscv,fileName):
        index_CongViecCanXoa = listBox.curselection()
        if index_CongViecCanXoa:
            XacNhan = messagebox.askyesno("Xác nhận","Bạn có muốn xoá công việc này ?")
            if XacNhan:
                for idx in index_CongViecCanXoa[::-1]:  
                    cong_viec = dscv.DS[idx]
                    dscv.DS.remove(cong_viec)
                dscv.SaveFile(fileName)
                CapNhatListBox(listBox,dscv.DS)
                messagebox.showinfo("Thông báo", "Xoá thành công!!")        
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn công việc cần xóa!")        
def XoaTatCaCongViec(listBox,dscv,fileName):
        XacNhan = messagebox.askyesno("Xác nhận","Bạn có chắc muốn xoá toàn bộ công việc ?")
        if XacNhan:
            dscv.DS.clear()
            dscv.SaveFile(fileName)
            listBox.delete(0,tk.END)
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn công việc cần xóa!")
'''chinh sua'''
def CuaSoChinhSuaCongViec_hienthi(CuaSoHienThiChiTietCV,listBox,dscv,fileName):
    CuaSoHienThiChiTietCV.destroy()
    CuaSoChinhSuaCongViec(listBox,dscv,fileName)
def CuaSoChinhSuaCongViec(listBox,dscv,fileName):
    CuaSoChinhSua_temp = tk.Toplevel()
    CuaSoChinhSua_temp.geometry("550x400+525+50")
    CuaSoChinhSua_temp.configure(bg="#82ccdd")
    CuaSoChinhSua_temp.columnconfigure(0, weight=1)
    CuaSoChinhSua_temp.columnconfigure(1, weight=2)
     
    index_ChonMucCanChinh = listBox.curselection()
    if index_ChonMucCanChinh:
        MaCV = dscv.DS[index_ChonMucCanChinh[0]]['MaCV']
        TieuDe = dscv.DS[index_ChonMucCanChinh[0]]['TieuDe']
        MoTa = dscv.DS[index_ChonMucCanChinh[0]]['MoTa']
        HanChot = dscv.DS[index_ChonMucCanChinh[0]]['HanChot']
        ChiSoUuTien = dscv.DS[index_ChonMucCanChinh[0]]['ChiSoUuTien']
                    
        label_MaCV = tk.Label(CuaSoChinhSua_temp, text="Mã công việc :",font=("Times New Roman",15),bg="#82ccdd")
        label_MaCV.grid(row=1, column=0,padx=10, pady=5)
        entry_MaCV = tk.Entry(CuaSoChinhSua_temp,width=50)
        entry_MaCV_temp = entry_MaCV.get()
        entry_MaCV.insert(0,f"{MaCV}")
        if (entry_MaCV_temp != MaCV):
            entry_MaCV.insert(0,f"{entry_MaCV_temp}") 
        entry_MaCV.grid(row=1, column=1, padx=5, pady=5)
            
        label_TieuDe = tk.Label(CuaSoChinhSua_temp, text="Tiêu đề :",font=("Times New Roman",15),bg="#82ccdd")
        label_TieuDe.grid(row=2, column=0,padx=10, pady=5)
        entry_TieuDe = tk.Entry(CuaSoChinhSua_temp,width=50)
        entry_TieuDe_temp = entry_TieuDe.get()
        entry_TieuDe.insert(0,f"{TieuDe}")
        if (entry_TieuDe_temp != TieuDe):
            entry_TieuDe.insert(0,f"{entry_TieuDe_temp}") 
        entry_TieuDe.grid(row=2, column=1, padx=5, pady=5)
                
        label_MoTa = tk.Label(CuaSoChinhSua_temp, text="Chi tiết :",font=("Times New Roman",15),bg="#82ccdd")
        label_MoTa.grid(row=3, column=0,padx=10, pady=5)
        text_MoTa = tk.Text(CuaSoChinhSua_temp,width=37,height=10,wrap=tk.WORD)
        text_MoTa_temp = text_MoTa.get("1.0",tk.END)
        text_MoTa.insert("1.0",f"{MoTa}")
        if (text_MoTa_temp != MoTa):
            text_MoTa.insert("1.0",f"{text_MoTa_temp}") 
        text_MoTa.grid(row=3, column=1, padx=5, pady=5)
                
        label_HanChot = tk.Label(CuaSoChinhSua_temp, text="Hạn chót (DD/MM/YYYY) :",font=("Times New Roman",15),bg="#82ccdd")
        label_HanChot.grid(row=4, column=0,padx=10, pady=5)
        entry_HanChot = tk.Entry(CuaSoChinhSua_temp,width=50)
        entry_HanChot_temp = entry_HanChot.get()
        entry_HanChot.insert(0,f"{HanChot}")
        if (entry_HanChot_temp != HanChot):
            entry_HanChot.insert(0,f"{entry_HanChot_temp}") 
        entry_HanChot.grid(row=4, column=1, padx=5, pady=5)
            
        label_ChiSoUuTien = tk.Label(CuaSoChinhSua_temp, text="Độ ưu tiên :",font=("Times New Roman",15),bg="#82ccdd")
        label_ChiSoUuTien.grid(row=5, column=0,padx=10, pady=5)
        entry_ChiSoUuTien = tk.Entry(CuaSoChinhSua_temp,width=50)
        entry_ChiSoUuTien_temp = entry_ChiSoUuTien.get()
        entry_ChiSoUuTien.insert(0,f"{ChiSoUuTien}")
        if (entry_ChiSoUuTien_temp != ChiSoUuTien):
            entry_ChiSoUuTien.insert(0,f"{entry_ChiSoUuTien_temp}") 
        entry_ChiSoUuTien.grid(row=5, column=1, padx=5, pady=5)
            
        frame_HoanThanh = tk.Frame(CuaSoChinhSua_temp,bd=2,bg="#2d3436")
        frame_HoanThanh.grid(row=6, columnspan=2,padx=10, pady=10)
        button_HoanThanh = tk.Button(frame_HoanThanh,text="Hoàn thành",font=("Times New Roman",15),width=15,relief="flat",bg="#ffda79",command=lambda : (dscv.ChinhSuaCongViec_hienthi(CuaSoChinhSua_temp,entry_MaCV.get(),entry_TieuDe.get(),text_MoTa.get("1.0",tk.END),entry_HanChot.get(),entry_ChiSoUuTien.get(),dscv.DS[index_ChonMucCanChinh[0]],fileName),CapNhatListBox(listBox,dscv.DS)))
        button_HoanThanh.pack()
    else:
        messagebox.showerror("Lỗi", "Vui lòng chọn công việc cần chỉnh!")  
'''======================Crawl data=============================='''
def CrawlDaTa(dscv, fileName, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích nội dung HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('td')
            
            # In các kết quả tìm được để kiểm tra
            for row in results:
                tmp = {}
                macv=row.find_all('h4')
                macv_data = [column.get_text(strip=True) for column in macv]
                for i in macv_data:
                    tmp['MaCV'] = i
                tieude = row.find_all('b', class_="b_Ten")
                tieude_data = [column.get_text(strip=True) for column in tieude]
                for i in tieude_data:
                    tmp['Ten'] = i
                mota=row.find_all('p', class_="p_nd")
                mota_data = [column.get_text(strip=True) for column in mota]
                for i in mota_data:
                    tmp['MoTa'] = i
                hanchot = row.find_all('p')
                hanchot_data = [column.get_text(strip=True) for column in hanchot]
                for i in hanchot_data:
                    tmp['HanChot'] = i
                dut = row.find_all('h5')
                dut_data = [column.get_text(strip=True) for column in dut]
                for i in dut_data:
                    tmp['DUT'] = i
                for cv in [tmp]:
                    dscv.ThemCongViec(cv['MaCV'], cv['Ten'], cv['MoTa'], cv['HanChot'], cv['DUT']) 
            dscv.SaveFile(fileName)
        messagebox.showinfo("Thông báo", "Thêm thành công!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối đến URL: {e}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


""" ============================================================================================================ """              

       
""" Cửa sổ thêm """    
def CuaSoThem(loai):            
    clear_window()
    root.title("Thêm công việc")
    root.geometry("600x700+500+50")
    root.configure(bg="#f7f1e3")
    
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=2)
    
    frame_Back = tk.Frame(root,bd=2,bg="#2d3436")
    frame_Back.grid(row=0,column=0,pady=5,padx=0)
    button_Back = tk.Button(frame_Back,relief="flat",bg="#dfe6e9",text=f"Quay lại",width=10,font=("Times New Roman",10,"bold"),command=lambda:CuaSoChucNang(loai))
    button_Back.pack()
    
    label_MaCV = tk.Label(root, text="Mã công việc :",font=("Times New Roman",15),bg="#f7f1e3")
    label_MaCV.grid(row=1, column=0,padx=10, pady=5)
    entry_MaCV = tk.Entry(root,width=50)
    entry_MaCV.grid(row=1, column=1, padx=5, pady=5)
    
    label_TieuDe = tk.Label(root, text="Tiêu đề :",font=("Times New Roman",15),bg="#f7f1e3")
    label_TieuDe.grid(row=2, column=0,padx=10, pady=5)
    entry_TieuDe = tk.Entry(root,width=50)
    entry_TieuDe.grid(row=2, column=1, padx=5, pady=5)
    
    label_MoTa = tk.Label(root, text="Chi tiết :",font=("Times New Roman",15),bg="#f7f1e3")
    label_MoTa.grid(row=3, column=0,padx=10, pady=5)
    text_MoTa = tk.Text(root,width=37,height=10,wrap=tk.WORD)
    text_MoTa.grid(row=3, column=1, padx=5, pady=5)
    
    label_HanChot = tk.Label(root, text="Hạn chót (DD/MM/YYYY) :",font=("Times New Roman",15),bg="#f7f1e3")
    label_HanChot.grid(row=4, column=0,padx=10, pady=5)
    entry_HanChot = tk.Entry(root,width=50)
    entry_HanChot.grid(row=4, column=1, padx=5, pady=5)
    
    label_ChiSoUuTien = tk.Label(root, text="Độ ưu tiên :",font=("Times New Roman",15),bg="#f7f1e3")
    label_ChiSoUuTien.grid(row=5, column=0,padx=10, pady=5)
    entry_ChiSoUuTien = tk.Entry(root,width=50)
    entry_ChiSoUuTien.grid(row=5, column=1, padx=5, pady=5)
    
    button_ThemCongViec = tk.Button(root,text="Thêm công việc",font=("Times New Roman",13),relief="raised",width=20,bg="#ffda79",fg="black",command=lambda: ThemCongViec(entry_MaCV,entry_TieuDe,text_MoTa,entry_HanChot,entry_ChiSoUuTien,dscv,fileName))
    button_ThemCongViec.grid(row=6,column=0,pady=5)
    button_ThemCongViec = tk.Button(root,text="Hiển thị danh sách công việc",font=("Times New Roman",13),relief="raised",width=25,bg="#ffda79",fg="black",command=lambda: HienThiDanhSachCV(ListBox,dscv.DS))
    button_ThemCongViec.grid(row=6,column=1,pady=5)
    
    label_ListBox = tk.Label(text="Danh sách các công việc",font=("Times New Roman",15),bg="#ffda79",height=1,width=200)
    label_ListBox.grid(row=7,columnspan=2,pady=10)  
    ListBox = tk.Listbox(root,width=80,height=11,selectmode=tk.MULTIPLE,font=("Times New Roman",15))
    ListBox.grid(row=9,columnspan=2,pady=5)
    button_ThemCongViec = tk.Button(root,text="Chi tiết công việc",font=("Times New Roman",11),relief="raised",width=20,bg="#dfe6e9",fg="black",command=lambda: HienThiChiTietCV(loai,ListBox,dscv))
    button_ThemCongViec.grid(row=8,columnspan=2,pady=5) 

    def kiem_tra_gia_tri(event=None):
        current_value = entry_ChiSoUuTien.get()
        if not current_value.isdigit():
            entry_ChiSoUuTien.config(bg="red")
        else:
            entry_ChiSoUuTien.config(bg="white")
    entry_ChiSoUuTien.bind("<KeyRelease>", kiem_tra_gia_tri)
""" Kết thúc cửa sổ thêm """
""" ============================================================================================================ """  
""" Cửa sổ CrawlWeb """        
def CuaSoCrawlWeb(loai):
    CuaSoVe("Crawl từ web",loai)
    frame_ChonMucXoa = tk.Frame(root, bd=2, bg="#dfe6e9")
    frame_ChonMucXoa.pack(pady=50)
    label_ChonMucXoa = tk.Label(frame_ChonMucXoa, text="Crawl web", font=("Sriracha", 30), width=25, bg="#f7f1e3", fg="#1B1464")
    label_ChonMucXoa.pack()

    label_ListBox = tk.Label(root, text="Nhập nguồn web", font=("Times New Roman", 15), bg="#ffda79", height=1, width=200)
    label_ListBox.pack(pady=5)

    entry_url = tk.Entry(root, width=90)
    entry_url.place(x=20, y=250)
    
    def add_from_web():
        url = entry_url.get()
        CrawlDaTa(dscv, fileName, url)
    
    frame_url = tk.Frame(root, bd=2, bg="#2d3436")
    frame_url.place(x=420, y=465)
    button_url = tk.Button(frame_url, width=10, relief="flat", bg="#dfe6e9", text="Thêm vào", font=("Times New Roman", 13), command=add_from_web)
    button_url.pack()
""" Kết thúc cửa sổ CrawlWeb """
""" ============================================================================================================ """  

def CuaSoXoa(loai):
    if dscv.DS == []:
        messagebox.showinfo("Thông báo","Danh sách công việc hiện đang rỗng!!")
        return
    CuaSoVe("Xoá công việc",loai)
    
    frame_ChonMucXoa = tk.Frame(root,bd=2,bg="#dfe6e9")
    frame_ChonMucXoa.pack(pady=50)
    label_ChonMucXoa = tk.Label(frame_ChonMucXoa,text="Chọn các mục cần xoá",font=("Sriracha",30),width=25,bg="#f7f1e3",fg="#1B1464")
    label_ChonMucXoa.pack()
    
    label_ListBox = tk.Label(text="Danh sách các công việc",font=("Times New Roman",15),bg="#ffda79",height=1,width=200)
    label_ListBox.pack(pady=5)
    ListBox = tk.Listbox(root,width=80,height=11,selectmode=tk.MULTIPLE,font=("Times New Roman",15))
    ListBox.pack(pady=5)
    HienThiDanhSachCV(ListBox,dscv.DS)
    
    frame_XemChiTiet = tk.Frame(root,bd=2,bg="#2d3436")
    frame_XemChiTiet.pack(pady=10)
    button_XemChiTiet = tk.Button(frame_XemChiTiet,text="Xem thông tin mục đã chọn",font=("Times New Roman",15),width=30,relief="flat",command=lambda: HienThiChiTietCV(loai,ListBox,dscv))
    button_XemChiTiet.pack()
    
    frame_XoaMucDaChon = tk.Frame(root,bd=2,bg="#2d3436")
    frame_XoaMucDaChon.pack(pady=10)
    button_XoaMucDaChon = tk.Button(frame_XoaMucDaChon,text="Xoá các mục đã chọn",font=("Times New Roman",15),width=23,relief="flat",command=lambda: XoaCongViec(ListBox,dscv,fileName))
    button_XoaMucDaChon.pack()
    
    frame_XoaTatCa = tk.Frame(root,bd=2,bg="#2d3436")
    frame_XoaTatCa.pack(pady=10)
    button_XoaTatCa = tk.Button(frame_XoaTatCa,text="Xoá tất cả công việc có trong danh sách",font=("Times New Roman",15),width=30,relief="flat",background="#ff7675",command=lambda: XoaTatCaCongViec(ListBox,dscv,fileName))
    button_XoaTatCa.pack()
""" Kết thúc cửa sổ xoá """
""" ============================================================================================================ """      
""" Cửa sổ chỉnh sửa """
def CuaSoChinhSua(loai):
    if dscv.DS == []:
        messagebox.showinfo("Thông báo","Danh sách công việc hiện đang rỗng!!")
        return
    
    CuaSoVe("Chỉnh sửa công việc",loai)
    
    frame_ChonMucChinhSua = tk.Frame(root,bd=2,bg="#dfe6e9")
    frame_ChonMucChinhSua.pack(pady=50)
    label_ChonMucChinhSua = tk.Label(frame_ChonMucChinhSua,text="Chọn mục cần chỉnh sửa",font=("Sriracha",30),width=22,bg="#f7f1e3",fg="#1B1464")
    label_ChonMucChinhSua.pack()
    
    label_ListBox = tk.Label(text="Danh sách các công việc",font=("Times New Roman",15),bg="#ffda79",height=1,width=200)
    label_ListBox.pack(pady=5)
    ListBox = tk.Listbox(root,width=80,height=11,selectmode=tk.SINGLE,font=("Times New Roman",15))
    ListBox.pack(pady=5)
    HienThiDanhSachCV(ListBox,dscv.DS)
    
    frame_XemChiTiet = tk.Frame(root,bd=2,bg="#2d3436")
    frame_XemChiTiet.pack(pady=10)
    button_XemChiTiet = tk.Button(frame_XemChiTiet,text="Xem thông tin mục đã chọn",font=("Times New Roman",15),width=30,relief="flat",command=lambda: HienThiChiTietCV(loai,ListBox,dscv))
    button_XemChiTiet.pack()
    
    frame_ChinhSuaCongViec = tk.Frame(root,bd=2,bg="#2d3436")
    frame_ChinhSuaCongViec.pack(pady=10)
    button_ChinhSuaCongViec = tk.Button(frame_ChinhSuaCongViec,text="Chỉnh sửa",font=("Times New Roman",15),width=20,relief="flat",bg="#82ccdd",command=lambda : CuaSoChinhSuaCongViec(ListBox,dscv,fileName))
    button_ChinhSuaCongViec.pack()
    
""" Kết thúc cửa sổ chỉnh sửa """
""" ============================================================================================================ """
""" Cửa sổ Hiển Thị """
def CuaSoHienThi(loai):
    if not dscv.DS:
        messagebox.showinfo("Thông báo", "Danh sách công việc hiện đang rỗng!!")
        return
    
    CuaSoVe("Hiển thị công việc",loai)
    
    ListBox = tk.Listbox(root, width=80, height=17, selectmode=tk.SINGLE, font=("Times New Roman", 15))
    ListBox.pack(pady=60)
    HienThiDanhSachCV(ListBox, dscv.DS)
    
    frame_XemChiTiet = tk.Frame(root, bd=2, bg="#2d3436")
    frame_XemChiTiet.pack()
    button_XemChiTiet = tk.Button(frame_XemChiTiet, text="Xem thông tin mục đã chọn", font=("Times New Roman", 15), width=30, relief="flat", bg="#dfe6e9", command=lambda: HienThiChiTietCV(loai,ListBox, dscv))
    button_XemChiTiet.pack()
         
    label_Tim = tk.Label(root, text="Nhập mã công việc để tìm : ", bg="#f7f1e3", font=("Times New Roman", 15))
    label_Tim.place(x=30, y=470)
    entry_Tim = tk.Entry(font=("Times New Roman", 15), width=15)
    entry_Tim.place(x=260, y=470)
    
    def XoaCV(cv):
        dscv.DS.remove(cv)
        dscv.SaveFile(fileName)
        CapNhatListBox(ListBox,dscv.DS)
        messagebox.showinfo("Thông báo", "Xoá thành công!!")
        CuaSoHienThiChiTietCV.destroy()
    
    def ChinhSuaCV(cv):
        CuaSoChinhSua_temp = tk.Toplevel()
        CuaSoChinhSua_temp.geometry("550x400+525+50")
        CuaSoChinhSua_temp.configure(bg="#82ccdd")
        CuaSoChinhSua_temp.columnconfigure(0, weight=1)
        CuaSoChinhSua_temp.columnconfigure(1, weight=2)
        
        MaCV = cv['MaCV']
        TieuDe = cv['TieuDe']
        MoTa = cv['MoTa']
        HanChot = cv['HanChot']
        ChiSoUuTien = cv['ChiSoUuTien']
                    
        label_MaCV = tk.Label(CuaSoChinhSua_temp, text="Mã công việc :",font=("Times New Roman",15),bg="#82ccdd")
        label_MaCV.grid(row=1, column=0,padx=10, pady=5)
        entry_MaCV = tk.Entry(CuaSoChinhSua_temp,width=50)
        entry_MaCV_temp = entry_MaCV.get()
        entry_MaCV.insert(0,f"{MaCV}")
        if (entry_MaCV_temp != MaCV):
            entry_MaCV.insert(0,f"{entry_MaCV_temp}") 
        entry_MaCV.grid(row=1, column=1, padx=5, pady=5)
            
        label_TieuDe = tk.Label(CuaSoChinhSua_temp, text="Tiêu đề :",font=("Times New Roman",15),bg="#82ccdd")
        label_TieuDe.grid(row=2, column=0,padx=10, pady=5)
        entry_TieuDe = tk.Entry(CuaSoChinhSua_temp,width=50)
        entry_TieuDe_temp = entry_TieuDe.get()
        entry_TieuDe.insert(0,f"{TieuDe}")
        if (entry_TieuDe_temp != TieuDe):
            entry_TieuDe.insert(0,f"{entry_TieuDe_temp}") 
        entry_TieuDe.grid(row=2, column=1, padx=5, pady=5)
                
        label_MoTa = tk.Label(CuaSoChinhSua_temp, text="Chi tiết :",font=("Times New Roman",15),bg="#82ccdd")
        label_MoTa.grid(row=3, column=0,padx=10, pady=5)
        text_MoTa = tk.Text(CuaSoChinhSua_temp,width=37,height=10,wrap=tk.WORD)
        text_MoTa_temp = text_MoTa.get("1.0",tk.END)
        text_MoTa.insert("1.0",f"{MoTa}")
        if (text_MoTa_temp != MoTa):
            text_MoTa.insert("1.0",f"{text_MoTa_temp}") 
        text_MoTa.grid(row=3, column=1, padx=5, pady=5)
                
        label_HanChot = tk.Label(CuaSoChinhSua_temp, text="Hạn chót (DD/MM/YYYY) :",font=("Times New Roman",15),bg="#82ccdd")
        label_HanChot.grid(row=4, column=0,padx=10, pady=5)
        entry_HanChot = tk.Entry(CuaSoChinhSua_temp,width=50)
        entry_HanChot_temp = entry_HanChot.get()
        entry_HanChot.insert(0,f"{HanChot}")
        if (entry_HanChot_temp != HanChot):
            entry_HanChot.insert(0,f"{entry_HanChot_temp}") 
        entry_HanChot.grid(row=4, column=1, padx=5, pady=5)
            
        label_ChiSoUuTien = tk.Label(CuaSoChinhSua_temp, text="Độ ưu tiên :",font=("Times New Roman",15),bg="#82ccdd")
        label_ChiSoUuTien.grid(row=5, column=0,padx=10, pady=5)
        entry_ChiSoUuTien = tk.Entry(CuaSoChinhSua_temp,width=50)
        entry_ChiSoUuTien_temp = entry_ChiSoUuTien.get()
        entry_ChiSoUuTien.insert(0,f"{ChiSoUuTien}")
        if (entry_ChiSoUuTien_temp != ChiSoUuTien):
            entry_ChiSoUuTien.insert(0,f"{entry_ChiSoUuTien_temp}") 
        entry_ChiSoUuTien.grid(row=5, column=1, padx=5, pady=5)
            
        frame_HoanThanh = tk.Frame(CuaSoChinhSua_temp,bd=2,bg="#2d3436")
        frame_HoanThanh.grid(row=6, columnspan=2,padx=10, pady=10)
        button_HoanThanh = tk.Button(frame_HoanThanh,text="Hoàn thành",font=("Times New Roman",15),width=15,relief="flat",bg="#ffda79",command=lambda : (dscv.ChinhSuaCongViec_hienthi(CuaSoChinhSua_temp,entry_MaCV.get(),entry_TieuDe.get(),text_MoTa.get("1.0",tk.END),entry_HanChot.get(),entry_ChiSoUuTien.get(),cv,fileName),CapNhatListBox(ListBox,dscv.DS)))
        button_HoanThanh.pack()
    
    def TimCongViec():
        CapNhatListBox(ListBox, dscv.DS)
        MaCVCanTim = entry_Tim.get()
        CV = dscv.TimCongViec(MaCVCanTim)
        if CV:
            messagebox.showinfo("Thông báo", "Đã tìm thấy!!")                
            global CuaSoHienThiChiTietCV
            CuaSoHienThiChiTietCV = tk.Toplevel()
            CuaSoHienThiChiTietCV.geometry("400x500+100+150")
            CuaSoHienThiChiTietCV.title("Chi tiết công việc")
            CuaSoHienThiChiTietCV.configure(bg="#b2bec3")
            

            HienThi(CuaSoHienThiChiTietCV, CV)
            if loai==0:
                frame_Button_ChinhSua = tk.Frame(CuaSoHienThiChiTietCV, bg="#2d3436", bd=2)
                frame_Button_ChinhSua.pack(pady=10)

                frame_Button_Xoa = tk.Frame(CuaSoHienThiChiTietCV, bg="#2d3436", bd=2)
                frame_Button_Xoa.pack(pady=10)

                button_ChinhSua = tk.Button(frame_Button_ChinhSua,text=f"Chỉnh sửa",width=10,font=("Times New Roman",15,"bold"),relief="flat",command=lambda : ChinhSuaCV(CV))
                button_ChinhSua.pack()

                button_Xoa = tk.Button(frame_Button_Xoa,text=f"Xoá",width=10,font=("Times New Roman",15,"bold"),bg="#d63031",fg="#dfe6e9",relief="flat",command=lambda : XoaCV(CV))
                button_Xoa.pack()

        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy")
             
    frame_Tim = tk.Frame(root, bd=2, bg="#2d3436")
    frame_Tim.place(x=420, y=465)
    button_Tim = tk.Button(frame_Tim, width=10, relief="flat", bg="#dfe6e9", text="Tìm kiếm", font=("Times New Roman", 13), command=TimCongViec)
    button_Tim.pack()
""" Kết thúc cửa sổ hiển thị """
""" ============================================================================================================ """
'''Main'''
def main_screen():
    clear_window()
    root.geometry("1000x600+300+100")
    root.configure(bg ='#f7d794')
    root.title("QUẢN LÝ CÔNG VIỆC CÁ NHÂN")
    label_LoiChao1 = tk.Label(root, text="Chào mừng bạn đến với phần mềm quản lý danh sách công việc cá nhân", font=("Sriracha", 20, "bold"), bg="#e15f41", fg="white")
    label_LoiChao2 = tk.Label(root, text="Chọn tiếp tục để bắt đầu...", font=("Times New Roman", 17, "italic"), bg="#f7d794")
    label_LoiChao1.pack(pady=20)
    label_LoiChao2.pack()

    frame_ButtonCuaSoChinh = tk.Frame(root, bg='#4b7bec', bd=3)
    frame_ButtonCuaSoChinh.pack(pady=100)
    button_DenCuaSoChinh = tk.Button(frame_ButtonCuaSoChinh, text="Tiếp tục", width=10, height=1, font=("Times New Roman", 15), relief="flat", bg="#f1f2f6", command=login)
    button_DenCuaSoChinh.pack()
'''Đăng nhập'''
def login_user():
    username = entry_User.get()
    password = entry_password.get()
    

    if not (username and password):
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
        return

    # Đọc thông tin từ file user.json
    try:
        with open("user.json", 'r', encoding='utf-8') as file:
            users = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "File user.json không tồn tại.")
        return
    
    # Kiểm tra thông tin đăng nhập
    for user in users:
        if user["User_login"] == username:
            # Mã hóa password nhập vào để so sánh với password trong file JSON
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user["password"] == hashed_password:
                messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
                if user["account_type"] == "ADMIN":
                    loai = 0
                    CuaSoChucNang(loai)
                else:
                    loai = 1
                    CuaSoChucNang(loai)
                return
            else:
                messagebox.showerror("Lỗi", "Sai mật khẩu. Đăng nhập thất bại.")
                return

    messagebox.showerror("Lỗi", "Tên đăng nhập không tồn tại trong hệ thống.")


def login():
    clear_window()
    root.title("Đăng nhập")
    root.geometry("400x300+600+200")
    root.configure(bg="azure")
    
    frame_Back = tk.Frame(root, bd=2, bg="#2d3436")
    frame_Back.place(x=10, y=10)
    button_Back = tk.Button(frame_Back, relief="flat", bg="#dfe6e9", text="Quay lại", width=10, font=("Times New Roman", 10, "bold"), command=main_screen)
    button_Back.pack()
    
    exit(300,10)
    
    label_LoiChao3 = tk.Label(root, text="Đăng nhập tài khoản", font=("Times New Roman", 20, "bold"), bg="azure", fg="blue")
    label_LoiChao3.place(x=80, y=50)
    
    global entry_User, entry_password
    
    label_User = tk.Label(root, text="Tên đăng nhập: ", font=("Times New Roman", 12), bg="azure")  
    label_User.place(x=30, y=100)
    entry_User = tk.Entry(root, width=25, font=("Times New Roman", 12))
    entry_User.place(x=150, y=100)
    
    label_password = tk.Label(root, text="Mật khẩu: ", font=("Times New Roman", 12), bg="azure")
    label_password.place(x=30, y=150)
    entry_password = tk.Entry(root, width=25, font=("Times New Roman", 12), show="*")
    entry_password.place(x=150, y=150)
    
    button_login = tk.Button(root, text="Đăng nhập", width=19, font=("Times New Roman", 11, "bold"), bg="orangered", fg="white", command=login_user)
    button_login.place(x=200, y=200)
    
    button_Register = tk.Button(root, text="Đăng ký", width=15, font=("Times New Roman", 8, "bold"), bg="slategrey", fg="white", command=register) 
    button_Register.place(x=240, y=250)
'''Đăng ký'''
def register_user():
    full_name = entry_HoTen.get()
    dob = entry_NgaySinh.get()
    gender = gender_var.get()
    account_type = account_type_var.get()
    User_login = entry_Users.get()
    password = password_entry.get()
    confirm_password = entry_confirm_pass.get()

    if not (full_name and dob and User_login and password and confirm_password and gender and account_type):
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
        return

    try:
        datetime.datetime.strptime(dob, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Lỗi", "Ngày sinh không hợp lệ. Vui lòng nhập theo định dạng dd/mm/yyyy.")
        return

    if password != confirm_password:
        messagebox.showerror("Lỗi", "Password và nhập lại password không khớp.")
        return

    birth_date = datetime.datetime.strptime(dob, "%d/%m/%Y")
    today = datetime.datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        messagebox.showerror("Lỗi", "Bạn phải từ 18 tuổi trở lên để đăng ký tài khoản.")
        return

    try:
        with open("user.json", 'r', encoding='utf-8') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    for user in users:
        if user["User_login"] == User_login:
            messagebox.showerror("Lỗi", "Tài khoản đã tồn tại trong hệ thống.")
            return

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_user = {
        "full_name": full_name,
        "dob": dob,
        "gender": gender,
        "account_type": account_type,
        "User_login": User_login,
        "password": hashed_password
    }
    users.append(new_user)

    with open("user.json", 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)
    loading()


def register():
    global entry_HoTen, entry_NgaySinh, entry_Users, password_entry, entry_confirm_pass, gender_var, account_type_var, strength_label

    clear_window()
    root.title("Đăng ký")
    root.geometry("400x620+500+50")
    root.configure(bg="azure")

    frame_Back = tk.Frame(root, bd=2, bg="#2d3436")
    frame_Back.place(x=10, y=10)
    button_Back = tk.Button(frame_Back, relief="flat", bg="#dfe6e9", text="Quay lại", width=10, font=("Times New Roman", 10, "bold"), command=login)
    button_Back.pack()

    exit(300,10)

    label_LoiChao3 = tk.Label(root, text="Đăng ký tài khoản", font=("Times New Roman", 20, "bold"), bg="azure", fg="blue")
    label_LoiChao3.place(x=85, y=50)

    label_HoTen = tk.Label(root, text="Họ và tên: ", font=("Times New Roman", 12), bg="azure")
    label_HoTen.place(x=25, y=130)
    entry_HoTen = tk.Entry(root, width=25, font=("Times New Roman", 12))
    entry_HoTen.place(x=170, y=130)

    label_NgaySinh = tk.Label(root, text="Ngày sinh:", font=("Times New Roman", 12), bg="azure")
    label_NgaySinh.place(x=25, y=180)
    entry_NgaySinh = tk.Entry(root, width=25, font=("Times New Roman", 12))
    entry_NgaySinh.place(x=170, y=180)

    label_GioiTinh = tk.Label(root, text="Giới tính: ", font=("Times New Roman", 12), bg="azure")
    label_GioiTinh.place(x=25, y=230)
    gender_var = radio("Giới tính", ["Nam", "Nữ"], 170, 230)

    label_user = tk.Label(root, text="CHỌN TÀI KHOẢN", font=("Times New Roman", 12), bg="azure")
    label_user.place(x=25, y=280)
    account_type_var = radio("CHỌN TÀI KHOẢN", ["USER", "ADMIN"], 170, 320)

    label_Users = tk.Label(root, text="Tên đăng nhập: ", font=("Times New Roman", 12), bg="azure")
    label_Users.place(x=25, y=380)
    entry_Users = tk.Entry(root, width=25, font=("Times New Roman", 12))
    entry_Users.place(x=170, y=380)

    label_pass = tk.Label(root, text="Mật khẩu: ", font=("Times New Roman", 12), bg="azure")
    label_pass.place(x=25, y=430)
    password_entry = tk.Entry(root, width=25, font=("Times New Roman", 12), show="*")
    password_entry.place(x=170, y=430)
    password_entry.bind("<KeyRelease>", check_password_strength)

    strength_label = tk.Label(root, text="Độ mạnh của mật khẩu: Yếu", fg="red", bg="azure")
    strength_label.place(x=25, y=460)

    label_confirm_pass = tk.Label(root, text="Nhập lại mật khẩu: ", font=("Times New Roman", 12), bg="azure")
    label_confirm_pass.place(x=25, y=495)
    entry_confirm_pass = tk.Entry(root, width=25, font=("Times New Roman", 12), show="*")
    entry_confirm_pass.place(x=170, y=495)

    button_register = tk.Button(root, text="ĐĂNG KÝ", width=15, font=("Times New Roman", 11, "bold"), bg="orangered", fg="white", command=register_user)
    button_register.place(x=200, y=550) 
""" ============================================================================================================ """
''' đăng xuất''' 
def exporting():
    XacNhan = messagebox.askyesno("Xác nhận","Bạn có muốn đăng xuất ?")
    if XacNhan:
        login()
        return
""" ============================================================================================================ """


""" *********************** Hàm main *********************** """
""" Cửa sổ gốc """
fileName = r"Tasks.json"
'''Lưu trữ đăng nhập và password'''
root = tk.Tk()
dscv = DanhSachCongViec()
dscv.Loadfile(fileName)
loai=None
'''Lưu trữ biến cho dữ liệu của user và password'''
entry_HoTen = None
entry_NgaySinh = None
entry_Users = None
entry_pass = None
entry_confirm_pass = None
gender_var = tk.StringVar()
account_type_var = tk.StringVar()
main_screen()
root.mainloop()

