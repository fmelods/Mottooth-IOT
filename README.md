
# MOTTOOTH - IoT e Visao Computacional
### Sprint 3 - Sistema de Localizacao com Visao Computacional

---

## Integrantes
- Arthur Ramos dos Santos – RM558798
- Felipe Melo de Sousa – RM556099
- Robert Daniel da Silva Coimbra – RM555881

**Turma:** 2TDSPW  

---

## Descricao do Projeto
O desafio da Mottu e monitorar e mapear com precisao a localizacao das motos dentro de seus patios, que variam em tamanho e layout, em mais de 100 filiais no Brasil e no Mexico.  
O processo atual e manual e impreciso, o que gera atrasos, falhas de controle e aumento de custos.  

Nossa solucao consiste em um **sistema inteligente de localizacao** que combina **sensores IoT, beacons BLE** e **visao computacional simulada** para:  
- Mapear a posicao das motos em tempo real  
- Registrar historico de movimentacoes  
- Emitir alertas quando uma moto esta em local errado ou desaparecida  
- Disponibilizar um **dashboard interativo** para visualizacao e gestao

---

## Estrutura de Pastas

```
projeto/
│── mottu_vision_system.py     # Codigo principal do sistema
│── requirements.txt            # Dependencias do projeto
│── relatorio_tecnico_mottu.md  # Relatorio tecnico gerado automaticamente
│── mottu_system.db             # Banco de dados SQLite (criado apos execucao)
```

---

## Tecnologias Utilizadas
- **Python 3.8+**
- **SQLite3** (banco de dados embarcado)
- **Tkinter** (dashboard interativo)
- **Threading** (processamento paralelo)
- **NumPy e Pandas** (simulacao e manipulacao de dados)
- **Random/UUID** (geracao de IDs e dados simulados)

---

## Instalacao

1. Clone o repositorio ou copie os arquivos para sua maquina  
   ```bash
   git clone <repositorio>
   cd projeto
   ```

2. Crie e ative um ambiente virtual (opcional, recomendado):  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Instale as dependencias:  
   ```bash
   pip install -r requirements.txt
   ```

---

## Execucao

1. Execute o sistema principal:  
   ```bash
   python mottu_vision_system.py
   ```

2. O sistema ira:  
   - Criar automaticamente o banco **SQLite**  
   - Gerar dados historicos simulados  
   - Executar casos de teste (moto desaparecida, moto em lugar errado, tempo real)  
   - Abrir o **dashboard interativo** para acompanhamento em tempo real  

---

## Uso do Sistema

- **Mapa do patio**: mostra a posicao das motos e cameras  
- **Lista de motos**: exibe informacoes atualizadas sobre cada moto detectada  
- **Alertas**: lista alertas de motos em local errado ou desaparecidas  
- **Historico**: gera relatorios de movimentacao por periodo  

---

## Casos de Uso Implementados

- **Deteccao de moto desaparecida**: alerta se a moto nao e vista ha mais de 2 minutos  
- **Deteccao de moto em lugar errado**: alerta se moto esta fora da area designada  
- **Monitoramento em tempo real**: atualizacao continua das posicoes  
- **Historico de movimentacoes**: todas as movimentacoes ficam registradas no banco

---

## Metricas Simuladas

- Taxa de deteccao: ~95%  
- Precisao media: ~0.85  
- Tempo medio de resposta: ~1.2s  
- FPS: 30 por camera  

---

## Proximos Passos

- Integracao com modelo **YOLO real** para deteccao via camera  
- API REST para acesso externo aos dados  
- Dashboard web (React ou Vue)  
- Analise preditiva para manutencao preventiva  
- Escalabilidade com conteinerizacao (Docker/Kubernetes)  

---

## Status
**Versao do Sistema:** 1.0.0  
**Situacao:** Prototipo funcional com simulacao de visao computacional
