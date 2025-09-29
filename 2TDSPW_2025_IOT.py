import os
import numpy as np
import sqlite3
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
import queue
from dataclasses import dataclass
from typing import List, Dict, Tuple
import random
import uuid
from datetime import datetime, timedelta

# ======================================================
# Estruturas de dados
# ======================================================

@dataclass
class Moto:
    id: str
    placa: str
    modelo: str
    pos_x: float
    pos_y: float
    area: str
    status: str
    timestamp: str
    camera_id: str
    confianca: float

@dataclass
class Camera:
    id: str
    nome: str
    pos_x: float
    pos_y: float
    area_cobertura: float
    status: str
    fps: int

@dataclass
class Alerta:
    id: str
    tipo: str
    moto_id: str
    descricao: str
    timestamp: str
    resolvido: bool

class Config:
    PATIO_WIDTH = 100
    PATIO_HEIGHT = 80

    AREAS = {
        "A": {"x_min": 0, "x_max": 50, "y_min": 0, "y_max": 40, "cor": "lightblue"},
        "B": {"x_min": 50, "x_max": 100, "y_min": 0, "y_max": 40, "cor": "lightgreen"},
        "C": {"x_min": 0, "x_max": 50, "y_min": 40, "y_max": 80, "cor": "lightyellow"},
        "D": {"x_min": 50, "x_max": 100, "y_min": 40, "y_max": 80, "cor": "lightcoral"}
    }

# ======================================================
# Simulador YOLO
# ======================================================

class YOLOSimulador:
    def __init__(self):
        self.limiar_confianca = 0.3

    def detectar_motos(self, camera_pos: Tuple[float, float]) -> List[Dict]:
        detections = []
        num = random.randint(2, 5)
        for _ in range(num):
            x = random.uniform(0.1, 0.9)
            y = random.uniform(0.1, 0.9)
            w = random.uniform(0.1, 0.15)
            h = random.uniform(0.1, 0.2)
            conf = random.uniform(0.5, 0.95)
            if conf > self.limiar_confianca:
                world_x = camera_pos[0] + (x - 0.5) * 30
                world_y = camera_pos[1] + (y - 0.5) * 25
                world_x = max(0, min(Config.PATIO_WIDTH, world_x))
                world_y = max(0, min(Config.PATIO_HEIGHT, world_y))
                detections.append({
                    "bbox": [x, y, w, h],
                    "conf": conf,
                    "id": f"MOTO_{random.randint(1000,9999)}",
                    "world_pos": (world_x, world_y)
                })
        return detections

# ======================================================
# Banco de dados
# ======================================================

class Database:
    def __init__(self, path="mottu.db"):
        self.path = path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS motos (
            id TEXT PRIMARY KEY,
            placa TEXT,
            modelo TEXT,
            pos_x REAL,
            pos_y REAL,
            area TEXT,
            status TEXT,
            timestamp TEXT,
            camera_id TEXT,
            confianca REAL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id TEXT PRIMARY KEY,
            tipo TEXT,
            moto_id TEXT,
            descricao TEXT,
            timestamp TEXT,
            resolvido BOOLEAN
        )
        """)
        conn.commit()
        conn.close()

    def salvar_moto(self, moto: Moto):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO motos VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (moto.id, moto.placa, moto.modelo, moto.pos_x, moto.pos_y,
              moto.area, moto.status, moto.timestamp, moto.camera_id, moto.confianca))
        conn.commit()
        conn.close()

    def listar_motos(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM motos ORDER BY timestamp DESC")
        rows = cur.fetchall()
        conn.close()
        colunas = ["id","placa","modelo","pos_x","pos_y","area","status","timestamp","camera_id","confianca"]
        return [dict(zip(colunas,row)) for row in rows]

    def salvar_alerta(self, alerta: Alerta):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO alertas VALUES (?,?,?,?,?,?)",
                    (alerta.id, alerta.tipo, alerta.moto_id, alerta.descricao,
                     alerta.timestamp, alerta.resolvido))
        conn.commit()
        conn.close()

    def listar_alertas(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM alertas ORDER BY timestamp DESC")
        rows = cur.fetchall()
        conn.close()
        colunas = ["id","tipo","moto_id","descricao","timestamp","resolvido"]
        return [dict(zip(colunas,row)) for row in rows]

# ======================================================
# Sistema de visao
# ======================================================

class MottuVision:
    def __init__(self):
        self.db = Database()
        self.yolo = YOLOSimulador()
        self.cameras = [
            Camera("CAM1","Entrada",25,20,30,"online",30),
            Camera("CAM2","Area A",75,20,30,"online",30),
            Camera("CAM3","Area B",25,60,30,"online",30),
            Camera("CAM4","Area C",75,60,30,"online",30),
        ]
        self.motos = {}
        self.alertas_queue = queue.Queue()
        self.rodando = False

    def _area(self, x,y):
        for nome, bounds in Config.AREAS.items():
            if bounds["x_min"] <= x <= bounds["x_max"] and bounds["y_min"] <= y <= bounds["y_max"]:
                return nome
        return "FORA"

    def processar_camera(self, camera: Camera):
        dets = self.yolo.detectar_motos((camera.pos_x,camera.pos_y))
        result = []
        for d in dets:
            x,y = d["world_pos"]
            area = self._area(x,y)
            moto = Moto(
                id=d["id"],
                placa=f"ABC-{random.randint(1000,9999)}",
                modelo=random.choice(["Honda CG","Yamaha","Suzuki"]),
                pos_x=x,
                pos_y=y,
                area=area,
                status="ativa",
                timestamp=datetime.now().isoformat(),
                camera_id=camera.id,
                confianca=d["conf"]
            )
            self.motos[moto.id] = moto
            self.db.salvar_moto(moto)
            result.append(moto)
        return result

    def verificar_alertas(self):
        agora = datetime.now()
        for mid, moto in self.motos.items():
            t = datetime.fromisoformat(moto.timestamp)
            if (agora - t).total_seconds() > 120:
                alerta = Alerta(str(uuid.uuid4()),"desaparecida",mid,
                                f"Moto {moto.placa} sumiu ha 2 minutos",
                                agora.isoformat(),False)
                self.db.salvar_alerta(alerta)
                self.alertas_queue.put(alerta)
                del self.motos[mid]
        if random.random() < 0.05 and self.motos:
            m = random.choice(list(self.motos.values()))
            alerta = Alerta(str(uuid.uuid4()),"lugar_errado",m.id,
                            f"Moto {m.placa} pode estar em lugar errado",
                            agora.isoformat(),False)
            self.db.salvar_alerta(alerta)
            self.alertas_queue.put(alerta)

    def loop(self):
        self.rodando = True
        while self.rodando:
            for c in self.cameras:
                if c.status == "online":
                    motos = self.processar_camera(c)
                    print(f"[{c.nome}] {len(motos)} motos detectadas")
            self.verificar_alertas()
            time.sleep(1)

    def stop(self):
        self.rodando = False

# ======================================================
# Dashboard
# ======================================================

class Dashboard:
    def __init__(self, system: MottuVision):
        self.sys = system
        self.root = tk.Tk()
        self.root.title("MOTTU - Sistema de Localizacao")
        self.root.geometry("1200x800")
        self._setup()
        self._update()

    def _setup(self):
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)

        stats = ttk.LabelFrame(main, text="Estatisticas em tempo real")
        stats.pack(fill=tk.X, pady=5)

        self.labels = {}
        for k in ["total","ativas","alertas","cameras"]:
            frame = ttk.Frame(stats)
            frame.pack(side=tk.LEFT,expand=True,fill=tk.X,padx=10)
            ttk.Label(frame,text=k.upper()).pack()
            self.labels[k] = ttk.Label(frame,text="0",font=("Arial",14,"bold"))
            self.labels[k].pack()

        self.tabs = ttk.Notebook(main)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self._map_tab()
        self._motos_tab()
        self._alertas_tab()

    def _map_tab(self):
        f = ttk.Frame(self.tabs)
        self.tabs.add(f,text="Mapa Patio")
        self.canvas = tk.Canvas(f,bg="white",width=800,height=600)
        self.canvas.pack(fill=tk.BOTH,expand=True)

    def _motos_tab(self):
        f = ttk.Frame(self.tabs)
        self.tabs.add(f,text="Motos")
        cols = ("id","placa","modelo","pos","area","status","conf")
        self.tree = ttk.Treeview(f,columns=cols,show="headings")
        for c in cols:
            self.tree.heading(c,text=c)
        self.tree.pack(fill=tk.BOTH,expand=True)

    def _alertas_tab(self):
        f = ttk.Frame(self.tabs)
        self.tabs.add(f,text="Alertas")
        cols = ("tipo","moto","descricao","hora","status")
        self.alerts_tree = ttk.Treeview(f,columns=cols,show="headings")
        for c in cols:
            self.alerts_tree.heading(c,text=c)
        self.alerts_tree.pack(fill=tk.BOTH,expand=True)
        ttk.Button(f,text="Atualizar",command=self._update_alertas).pack()

    def _update(self):
        motos = self.sys.db.listar_motos()
        self.labels["total"].config(text=str(len(motos)))
        self.labels["ativas"].config(text=str(len(self.sys.motos)))
        self.labels["alertas"].config(text=str(self.sys.alertas_queue.qsize()))
        self.labels["cameras"].config(text=str(len(self.sys.cameras)))

        # Atualizar mapa
        self.canvas.delete("all")
        scale_x = 800/Config.PATIO_WIDTH
        scale_y = 600/Config.PATIO_HEIGHT
        for nome,b in Config.AREAS.items():
            self.canvas.create_rectangle(b["x_min"]*scale_x,b["y_min"]*scale_y,
                                         b["x_max"]*scale_x,b["y_max"]*scale_y,
                                         fill=b["cor"],outline="black")
            cx = (b["x_min"]+b["x_max"])/2*scale_x
            cy = (b["y_min"]+b["y_max"])/2*scale_y
            self.canvas.create_text(cx,cy,text=f"Area {nome}")

        for m in motos[-30:]:
            x = m["pos_x"]*scale_x
            y = m["pos_y"]*scale_y
            self.canvas.create_oval(x-5,y-5,x+5,y+5,fill="blue")

        # Atualizar lista de motos
        for i in self.tree.get_children():
            self.tree.delete(i)
        for m in motos[-50:]:
            self.tree.insert("",tk.END,values=(
                m["id"][:6],m["placa"],m["modelo"],
                f"({m['pos_x']:.1f},{m['pos_y']:.1f})",
                m["area"],m["status"],f"{m['confianca']:.2f}"
            ))

        self._update_alertas()

        self.root.after(2000,self._update)

    def _update_alertas(self):
        for i in self.alerts_tree.get_children():
            self.alerts_tree.delete(i)
        alertas = self.sys.db.listar_alertas()
        for a in alertas[-20:]:
            self.alerts_tree.insert("",tk.END,values=(
                a["tipo"],a["moto_id"],a["descricao"],
                a["timestamp"][:19],"OK" if a["resolvido"] else "Pendente"
            ))

    def run(self):
        self.root.mainloop()

# ======================================================
# Main
# ======================================================

def main():
    print("INICIANDO SISTEMA MOTTU - VISAO COMPUTACIONAL")
    sys = MottuVision()
    t = threading.Thread(target=sys.loop,daemon=True)
    t.start()
    dash = Dashboard(sys)
    dash.run()
    sys.stop()

if __name__ == "__main__":
    main()
