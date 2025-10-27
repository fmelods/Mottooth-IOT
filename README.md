# 🛵 MOTTU - IoT Dashboard Integrado

Link: https://mottooth-iot-dashboard.streamlit.app

Dashboard desenvolvido para a **Sprint 4** da disciplina **Disruptive Architectures: IoT, IOB & Generative IA (FIAP / Mottu)**.  
Este projeto integra dados de **IoT (motos e beacons)** com uma **API Java (Spring Boot + Oracle Cloud)**, exibindo métricas e visualizações em tempo real via **Streamlit**.

---

## 🚀 Funcionalidades

✅ Login autenticado via **JWT** na API Java  
✅ Integração com os endpoints `/motos`, `/beacons` e `/localizacoes`  
✅ Atualização automática de dados em tempo real  
✅ Mapa interativo do pátio dividido por áreas (A, B, C, D)  
✅ Dashboard escuro (dark mode) e responsivo  
✅ Métricas, tabelas e visualizações dinâmicas integradas à API

---

## 🧠 Arquitetura da Solução

```
ESP32 / Simulador IoT
        ↓  (HTTP POST)
API Java (Spring Boot)
        ↓  (JSON)
Oracle Cloud Database
        ↓
Dashboard Streamlit (Python)
```

---

## 🗂️ Estrutura do Projeto

```
MOTTOOTH-IOT/
│
├── .streamlit/
│   └── secrets.toml        # Variáveis seguras (opcional)
│
├── 2TDSPW_2025_IOT.py      # Dashboard principal (Streamlit)
├── mottu_api.py            # Classe de integração com a API REST
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

---

## ⚙️ Requisitos

- Python 3.10+  
- Pip atualizado (`python -m pip install --upgrade pip`)

---

## 🧩 Instalação e Execução Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/fmelods/Mottooth-IOT.git
   cd Mottooth-IOT
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o dashboard:
   ```bash
   streamlit run 2TDSPW_2025_IOT.py
   ```

4. Acesse no navegador:
   ```
   http://localhost:8501
   ```

---

## 🔐 Variáveis de Configuração (opcional)

No arquivo `.streamlit/secrets.toml`, você pode definir:

```toml
API_URL = "https://mottooth-java-1.onrender.com"
USERNAME = "admin@ex.com"
PASSWORD = "fiap25"
```

Esses valores são lidos automaticamente pelo Streamlit para autenticação na API.

---

## 🌐 Deploy no Streamlit Cloud

1. Acesse [streamlit.io](https://share.streamlit.io)  
2. Clique em **New App**
3. Configure:
   - **Repository:** `fmelods/Mottooth-IOT`
   - **Branch:** `main`
   - **Main file path:** `2TDSPW_2025_IOT.py`
4. Clique em **Deploy**

O app ficará disponível em um link como:

```
https://fmelods-mottooth-iot.streamlit.app
```

---

## 📊 Visual do Dashboard

### 🔹 Painel Principal
- Métricas em tempo real (Motos, Beacons, Localizações, Status)
- Mapa do pátio com áreas A, B, C e D
- Tabelas detalhadas sincronizadas com a API

### 🔹 Layout
Interface moderna e minimalista com modo escuro e atualização automática a cada intervalo configurável.

---

## 🧱 Tecnologias Utilizadas

| Camada | Tecnologia |
|:--|:--|
| Frontend Dashboard | Streamlit + Plotly |
| Backend API | Java Spring Boot |
| Banco de Dados | Oracle Cloud |
| Integração IoT | Python (simuladores e scripts) |

---

## 👨‍💻 Integrantes

| Nome | RM | Função |
|------|----|--------|
| **Arthur Ramos dos Santos** | RM558798 | Lógica de detecção e interface de dashboard |
| **Felipe Melo de Sousa** | RM556099 | Integração com API Java e Oracle Cloud |
| **Robert Daniel da Silva Coimbra** | RM555881 | Arquitetura IoT e simulação de dispositivos |

---

## 🏁 Status do Projeto
✅ **Finalizado e funcional** — pronto para entrega da **Sprint 4 (FIAP / Mottu)**.

---

> Projeto acadêmico desenvolvido na **FIAP** em parceria com a **Mottu**, como parte do desafio de integração entre **IoT + Backend + Cloud + Dashboard**.
