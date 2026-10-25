# 📺 GamaTV EPG

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![XMLTV](https://img.shields.io/badge/Format-XMLTV-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

Um script automatizado em Python para consolidação, limpeza e otimização de grades de programação (EPG - Electronic Program Guide) voltadas para o Brasil.

</div>

---

## 🚀 O que o GamaTV EPG faz?

O **GamaTV EPG** resolve um problema comum em listas IPTV e players multimídia: a escassez ou fragmentação de guias de programação confiáveis para canais brasileiros. 

O script executa as seguintes tarefas em lote:
1. **📥 Baixa de Múltiplas Fontes:** Coleta dados atualizados de grandes provedores abertos de EPG (`FreeEPG` e múltiplos feeds do `EPGShare01`).
2. **🗜️ Descompressão Automática:** Processa arquivos compactados via `gzip` (`.xml.gz`) em tempo de execução.
3. **🔄 Mesclagem e Deduplicação Inteligente:** Une os dados de programação, eliminando duplicatas exatas e preservando programas com horários coincidentes mas metadados complementares.
4. **🛡️ Validação de Integridade:** Testa a estrutura do XML gerado antes de sobrescrever o arquivo de destino, evitando corrupção de dados no seu player ou servidor.

---

## 🛠️ Fontes Utilizadas

Atualmente, o agregador consome e unifica os seguintes feeds:
* **FreeEPG** (`br.xml.gz`)
* **EPGShare01 - BR1** (`epg_ripper_BR1.xml.gz`)
* **EPGShare01 - BR2** (`epg_ripper_BR2.xml.gz`)

---

## ⚙️ Como Usar

### Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina. O script utiliza apenas bibliotecas nativas, com exceção da biblioteca `requests`.

```bash
pip install requests

Depois na pasta do py, execute py gerar.py.
