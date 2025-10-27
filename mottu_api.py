import requests
import streamlit as st

class MottoAPI:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.token = None

    # =========================================================
    # LOGIN - Obtém o token JWT
    # =========================================================
    def login(self, username, password):
        url = f"{self.base_url}/api/auth/login"
        payload = {"username": username, "password": password}

        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                st.session_state["token"] = self.token
                return True
            else:
                st.error(f"Erro ao autenticar ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            st.error(f"Falha na conexão: {e}")
            return False

    # =========================================================
    # HEADERS com token JWT
    # =========================================================
    def _headers(self):
        if not self.token:
            self.token = st.session_state.get("token")
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    # =========================================================
    # GET genérico (com tratamento do formato da resposta)
    # =========================================================
    def get_data(self, endpoint):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.get(url, headers=self._headers(), timeout=10)
            if response.status_code == 200:
                data = response.json()

                # Corrige formato (casos: dict, list, dict com "content")
                if isinstance(data, dict):
                    if "content" in data and isinstance(data["content"], list):
                        return data["content"]
                    else:
                        return [data]
                elif isinstance(data, list):
                    return data
                else:
                    st.warning(f"Formato inesperado em {endpoint}: {type(data)}")
                    return []

            elif response.status_code == 403:
                st.error("Acesso negado. Token expirado ou inválido.")
            else:
                st.warning(f"Erro {response.status_code} ao buscar {endpoint}")
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")
        return []

    # =========================================================
    # ENDPOINTS específicos
    # =========================================================
    def get_motos(self):
        return self.get_data("/api/motos")

    def get_beacons(self):
        return self.get_data("/api/beacons")

    def get_localizacoes(self):
        return self.get_data("/api/localizacoes")
