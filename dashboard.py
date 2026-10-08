import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import pymysql, database

CATEGORIES=["Health","Study","Fitness","Personal","Other"]
FREQUENCIES=("Daily","Weekly")

class DashboardWindow:
    def __init__(self,login_root,user_data):
        self.login_root=login_root; self.user_data=user_data
        self.user_id=user_data["user_id"]; self.user_name=user_data["name"]
        self.window=tk.Toplevel(login_root); self.window.title("Daily Habit Monitoring System - "+self.user_name)
        self.window.geometry("1000x700"); self.window.configure(bg="#F4F6F9")
        self.window.protocol("WM_DELETE_WINDOW",self.exit_app)
        self.header(); self.form(); self.searchbar(); self.table(); self.buttons(); self.load_habits()

    def db(self,sql,params=(),fetch=False):
        conn=None
        try:
            conn=database.get_connection(); cur=conn.cursor(); cur.execute(sql,params)
            data=cur.fetchall() if fetch else True; cur.close(); return data
        except pymysql.MySQLError as e:
            database.log_action("ERROR",str(e)); messagebox.showerror("Database Error",str(e)); return None
        finally:
            if conn: conn.close()

    def header(self):
        f=tk.Frame(self.window,bg="#2C3E50",height=60); f.pack(fill="x")
        tk.Label(f,text="DAILY HABIT MONITORING SYSTEM",font=("Arial",16,"bold"),bg="#2C3E50",fg="white").pack(side="left",padx=20,pady=12)
        tk.Label(f,text="User: "+self.user_name,font=("Arial",11,"bold"),bg="#2C3E50",fg="#F1C40F").pack(side="right",padx=20)

    def form(self):
        f=tk.LabelFrame(self.window,text=" Add New Habit ",font=("Arial",11,"bold"),bg="#F4F6F9",padx=10,pady=8); f.pack(fill="x",padx=20,pady=10)
        tk.Label(f,text="Habit Name:",bg="#F4F6F9").grid(row=0,column=0); self.name=tk.Entry(f,width=17); self.name.grid(row=1,column=0,padx=4)
        tk.Label(f,text="Category:",bg="#F4F6F9").grid(row=0,column=1); self.cat=ttk.Combobox(f,values=sorted(set(CATEGORIES)),state="readonly",width=13); self.cat.set("Study"); self.cat.grid(row=1,column=1,padx=4)
        tk.Label(f,text="Frequency:",bg="#F4F6F9").grid(row=0,column=2); self.freq=tk.StringVar(value="Daily")
        for x in FREQUENCIES: tk.Radiobutton(f,text=x,variable=self.freq,value=x,bg="#F4F6F9").grid(row=1,column=2+FREQUENCIES.index(x),sticky="w")
        tk.Label(f,text="Target:",bg="#F4F6F9").grid(row=0,column=4); self.target=tk.Entry(f,width=14); self.target.grid(row=1,column=4,padx=4)
        self.imp=tk.BooleanVar(); tk.Checkbutton(f,text="Important",variable=self.imp,bg="#F4F6F9").grid(row=1,column=5)
        tk.Button(f,text="+ Add Habit",command=self.add_habit,bg="#27AE60",fg="white").grid(row=1,column=6,padx=6)

    def searchbar(self):
        f=tk.Frame(self.window,bg="#F4F6F9"); f.pack(fill="x",padx=20,pady=4)
        tk.Label(f,text="Search:",bg="#F4F6F9").pack(side="left"); self.search=tk.Entry(f,width=25); self.search.pack(side="left",padx=7)
        tk.Button(f,text="Search",command=self.search_habits,bg="#2980B9",fg="white").pack(side="left",padx=3)
        tk.Button(f,text="Show All",command=self.load_habits,bg="#7F8C8D",fg="white").pack(side="left",padx=3)

    def table(self):
        f=tk.Frame(self.window,bg="#F4F6F9"); f.pack(fill="both",expand=True,padx=20)
        cols=("ID","Habit Name","Category","Frequency","Target","Important"); self.tree=ttk.Treeview(f,columns=cols,show="headings")
        widths=(65,220,130,110,150,100)
        for c,w in zip(cols,widths): self.tree.heading(c,text=c); self.tree.column(c,width=w,anchor="center")
        sb=ttk.Scrollbar(f,command=self.tree.yview); self.tree.configure(yscrollcommand=sb.set); self.tree.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")

    def buttons(self):
        f=tk.Frame(self.window,bg="#F4F6F9"); f.pack(fill="x",padx=20,pady=12)
        for text,cmd,color in [("Mark Complete",self.mark_complete,"#27AE60"),("Update Habit",self.update_habit,"#F39C12"),("Delete Habit",self.delete_habit,"#C0392B"),("Daily Progress",self.progress,"#8E44AD"),("Statistics",self.statistics,"#16A085"),("Logout",self.logout,"#7F8C8D")]:
            tk.Button(f,text=text,command=cmd,bg=color,fg="white",padx=7).pack(side="left",padx=3)

    def clear(self):
        for x in self.tree.get_children(): self.tree.delete(x)

    def load_habits(self):
        self.search.delete(0,tk.END); self.clear()
        sql="SELECT habit_id,habit_name,category,frequency,target,is_important FROM habits WHERE user_id=%s ORDER BY habit_id DESC"
        rows=self.db(sql,(self.user_id,),True)
        if rows:
            for r in rows: self.tree.insert("",tk.END,values=r)

    def add_habit(self):
        n,c,f,t=self.name.get().strip(),self.cat.get(),self.freq.get(),self.target.get().strip()
        if not n or not c or not t: messagebox.showwarning("Warning","Fill Habit Name, Category and Target."); return
        sql="INSERT INTO habits(user_id,habit_name,category,frequency,target,is_important) VALUES(%s,%s,%s,%s,%s,%s)"
        if self.db(sql,(self.user_id,n,c,f,t,"Yes" if self.imp.get() else "No")):
            database.log_action("HABIT_ADDED",n); messagebox.showinfo("Success","Habit added successfully!")
            self.name.delete(0,tk.END); self.target.delete(0,tk.END); self.cat.set("Study"); self.freq.set("Daily"); self.imp.set(False); self.load_habits()

    def search_habits(self):
        key=self.search.get().strip()
        if not key: self.load_habits(); return
        self.clear()
        sql="SELECT habit_id,habit_name,category,frequency,target,is_important FROM habits WHERE user_id=%s AND habit_name LIKE %s ORDER BY habit_id DESC"
        rows=self.db(sql,(self.user_id,"%"+key+"%"),True)
        if rows:
            for r in rows: self.tree.insert("",tk.END,values=r)
        else: messagebox.showinfo("Search","No matching habit found.")

    def selected(self):
        s=self.tree.selection()
        if not s: messagebox.showwarning("Selection","Please select a habit."); return None
        return self.tree.item(s[0])["values"]

    def mark_complete(self):
        r=self.selected()
        if not r:return
        hid,name=r[0],r[1]; today=date.today()
        if self.db("SELECT record_id FROM habit_records WHERE habit_id=%s AND record_date=%s",(hid,today),True):
            messagebox.showinfo("Notice","This habit is already completed today."); return
        if self.db("INSERT INTO habit_records(habit_id,record_date,status) VALUES(%s,%s,%s)",(hid,today,"Completed")):
            database.log_action("HABIT_COMPLETED",name); messagebox.showinfo("Success",name+" completed today!")

    def update_habit(self):
        r=self.selected()
        if not r:return
        hid,oldn,oldc,oldf,oldt=r[:5]; win=tk.Toplevel(self.window); win.title("Update Habit"); win.geometry("400x300"); win.configure(bg="#F4F6F9")
        tk.Label(win,text="UPDATE HABIT",font=("Arial",14,"bold"),bg="#F4F6F9").pack(pady=10)
        f=tk.Frame(win,bg="#F4F6F9"); f.pack()
        tk.Label(f,text="Name:",bg="#F4F6F9").grid(row=0,column=0,pady=6); n=tk.Entry(f,width=25); n.insert(0,oldn); n.grid(row=0,column=1)
        tk.Label(f,text="Category:",bg="#F4F6F9").grid(row=1,column=0); c=ttk.Combobox(f,values=CATEGORIES,state="readonly",width=22); c.set(oldc); c.grid(row=1,column=1)
        tk.Label(f,text="Frequency:",bg="#F4F6F9").grid(row=2,column=0,pady=6); fv=tk.StringVar(value=oldf)
        for i,x in enumerate(FREQUENCIES): tk.Radiobutton(f,text=x,variable=fv,value=x,bg="#F4F6F9").grid(row=2,column=i+1)
        tk.Label(f,text="Target:",bg="#F4F6F9").grid(row=3,column=0); t=tk.Entry(f,width=25); t.insert(0,oldt); t.grid(row=3,column=1)
        def save():
            if not n.get().strip() or not c.get() or not t.get().strip(): messagebox.showwarning("Warning","All fields are required."); return
            sql="UPDATE habits SET habit_name=%s,category=%s,frequency=%s,target=%s WHERE habit_id=%s AND user_id=%s"
            if self.db(sql,(n.get().strip(),c.get(),fv.get(),t.get().strip(),hid,self.user_id)):
                messagebox.showinfo("Success","Habit updated."); win.destroy(); self.load_habits()
        tk.Button(win,text="Save Changes",command=save,bg="#27AE60",fg="white",width=16).pack(pady=18)

    def delete_habit(self):
        r=self.selected()
        if not r:return
        hid,name=r[0],r[1]
        if not messagebox.askyesno("Confirm","Delete '"+name+"'?"):return
        self.db("DELETE FROM habit_records WHERE habit_id=%s",(hid,)); self.db("DELETE FROM habits WHERE habit_id=%s AND user_id=%s",(hid,self.user_id))
        database.log_action("HABIT_DELETED",name); messagebox.showinfo("Success","Habit deleted."); self.load_habits()

    def progress(self):
        total=self.db("SELECT COUNT(*) FROM habits WHERE user_id=%s",(self.user_id,),True)[0][0]
        done=self.db("SELECT COUNT(DISTINCT h.habit_id) FROM habits h JOIN habit_records r ON h.habit_id=r.habit_id WHERE h.user_id=%s AND r.record_date=%s AND r.status='Completed'",(self.user_id,date.today()),True)[0][0]
        p=done/total*100 if total else 0
        messagebox.showinfo("Daily Progress",f"Total Habits: {total}\nCompleted Today: {done}\nPending: {max(0,total-done)}\nProgress: {p:.1f}%")

    def statistics(self):
        win=tk.Toplevel(self.window); win.title("Habit Statistics"); win.geometry("550x400")
        cols=("Habit Name","Category","Completed Days"); tr=ttk.Treeview(win,columns=cols,show="headings")
        for c in cols: tr.heading(c,text=c)
        tr.column("Habit Name",width=220); tr.column("Category",width=130); tr.column("Completed Days",width=150); tr.pack(fill="both",expand=True,padx=15,pady=15)
        sql="SELECT h.habit_name,h.category,COUNT(r.record_id) FROM habits h LEFT JOIN habit_records r ON h.habit_id=r.habit_id AND r.status='Completed' WHERE h.user_id=%s GROUP BY h.habit_id,h.habit_name,h.category ORDER BY COUNT(r.record_id) DESC"
        rows=self.db(sql,(self.user_id,),True)
        if rows:
            for r in rows: tr.insert("",tk.END,values=r)
        tk.Button(win,text="Close",command=win.destroy).pack(pady=5)

    def logout(self):
        database.log_action("LOGOUT",self.user_name); self.window.destroy(); self.login_root.deiconify()

    def exit_app(self):
        database.log_action("SYSTEM",self.user_name+" closed application"); self.window.destroy(); self.login_root.destroy()
