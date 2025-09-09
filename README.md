# Blog Generator Enhanced 🚀

Sistema avanzato per la generazione automatica di articoli SEO ottimizzati in italiano utilizzando CrewAI e modelli LLM.

## ✨ Caratteristiche Principali

- **Input Completi**: Sistema di configurazione avanzato con intento, target website, business activity
- **Prompt Ottimizzati**: Prompt specializzati per il mercato italiano e SEO
- **Step Intermedi**: Agente di analisi strategica per ottimizzare la qualità
- **Modelli Economici**: Uso intelligente di modelli GPT-4o-mini per step meno critici
- **Modalità Multiple**: Interattiva, da file, da parametri CLI
- **Analytics**: Report dettagliati di esecuzione e metriche
- **Risultati Intermedi**: Salvataggio opzionale di tutti gli step

## 🏗️ Architettura

### Agenti Specializzati
1. **Research Agent** (GPT-4o-mini) - Ricerca web con Tavily
2. **Analysis Agent** (GPT-4o-mini) - Analisi strategica intermedia
3. **Outline Agent** (GPT-4o) - Strutturazione SEO
4. **Drafting Agent** (GPT-4o) - Scrittura contenuto
5. **Optimization Agent** (GPT-4o) - Ottimizzazione finale

### Flusso di Lavoro
```
Input → Research → Analysis → Outline → Drafting → Optimization → Output
```

## 📦 Installazione

1. **Clona il repository**
```bash
git clone <repository-url>
cd blog-generator
```

2. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```

3. **Configura le API Keys**
Crea un file `.env` con:
```env
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
```

## 🚀 Utilizzo

### 1. Modalità Interattiva (Consigliata)
```bash
python blog_generator_enhanced.py --interactive
```

### 2. Parametri Specifici
```bash
python blog_generator_enhanced.py \
  --topic "Case Vacanza Costiera Amalfitana" \
  --intent commerciale \
  --website "https://miosito.it" \
  --business "Affitti turistici" \
  --audience "turisti italiani" \
  --tone professionale \
  --words 2000
```

### 3. Da File di Configurazione
```bash
# Genera template
python blog_generator_enhanced.py --generate-template

# Modifica input_template.yaml e usa
python blog_generator_enhanced.py --input-file input_template.yaml
```

### 4. Configurazione Avanzata
Modifica `config.yaml` per:
- Cambiare modelli LLM
- Configurare parametri SEO
- Impostare output options

## 📁 Struttura File

```
blog-generator/
├── blog_generator_enhanced.py    # Script principale migliorato
├── input_manager.py             # Gestione input e configurazioni
├── config.yaml                  # Configurazioni sistema
├── prompts_enhanced.yaml        # Prompt ottimizzati
├── requirements.txt             # Dipendenze Python
├── .env                        # API Keys (da creare)
└── README.md                   # Documentazione
```

## ⚙️ Configurazione

### config.yaml
```yaml
models:
  research: "gpt-4o-mini"      # Economico per ricerca
  analysis: "gpt-4o-mini"     # Economico per analisi
  outline: "gpt-4o"           # Avanzato per struttura
  drafting: "gpt-4o"          # Avanzato per scrittura
  optimization: "gpt-4o"      # Avanzato per ottimizzazione

seo_config:
  keyword_density:
    primary: 1.5              # Densità keyword primarie (%)
    secondary: 0.8            # Densità keyword secondarie (%)
  readability_target: 65      # Punteggio Flesch target
  internal_links_min: 3       # Link interni minimi
  external_links_min: 5       # Link esterni minimi
```

### Input Template
```yaml
topic: "Il tuo topic qui"
intent: "commerciale"                    # informativo, commerciale, educativo
target_website: "https://tuosito.it"
business_activity: "Descrivi la tua attività"
target_audience: "Pubblico target specifico"
tone: "professionale"                    # professionale, casual, tecnico
word_count: 2000
include_cta: true
seo_focus: true
```

## 📊 Output

### File Generati
- `blog_[topic]_[timestamp].md` - Articolo finale
- `blog_[topic]_[timestamp]_analytics.json` - Report analytics
- `intermediate_[step]_[topic]_[timestamp].json` - Risultati intermedi (opzionale)

### Metriche Analytics
- Tempo di esecuzione
- Modelli utilizzati
- Configurazioni SEO applicate
- Input utilizzati

## 🎯 Esempi di Utilizzo

### Caso 1: Articolo Commerciale
```bash
python blog_generator_enhanced.py \
  --topic "Migliori Hotel Costiera Amalfitana 2025" \
  --intent commerciale \
  --website "https://hotelcostiera.it" \
  --business "Hotel di lusso" \
  --audience "turisti benestanti" \
  --tone professionale
```

### Caso 2: Contenuto Educativo
```bash
python blog_generator_enhanced.py \
  --topic "Come Investire in Immobili 2025" \
  --intent educativo \
  --website "https://consulenzaimmobiliare.it" \
  --business "Consulenza immobiliare" \
  --audience "investitori principianti" \
  --tone tecnico
```

## 🔧 Personalizzazione

### Modificare i Prompt
Edita `prompts_enhanced.yaml` per:
- Cambiare stile di scrittura
- Aggiungere requisiti specifici
- Modificare struttura output

### Aggiungere Nuovi Agenti
1. Definisci nuovo agente in `setup_agents()`
2. Crea task corrispondente in `setup_tasks()`
3. Aggiungi prompt in `prompts_enhanced.yaml`

## 🐛 Troubleshooting

### Errori Comuni
1. **API Key mancanti**: Verifica file `.env`
2. **Modelli non disponibili**: Controlla OpenRouter
3. **Errori Tavily**: Verifica quota API Tavily

### Log e Debug
- Log salvati in `blog_generator.log`
- Usa `--verbose` per output dettagliato
- Controlla risultati intermedi se abilitati

## 📈 Roadmap

- [ ] Integrazione con CMS (WordPress, etc.)
- [ ] Supporto immagini automatiche
- [ ] Analisi competitor automatica
- [ ] Template per nicchie specifiche
- [ ] API REST per integrazione

## 🤝 Contributi

1. Fork del repository
2. Crea feature branch
3. Commit delle modifiche
4. Push e Pull Request

## 📄 Licenza

MIT License - vedi file LICENSE per dettagli.

## 📞 Supporto

Per supporto e domande:
- Apri un Issue su GitHub
- Consulta la documentazione
- Controlla i log per errori specifici

---

**Nota**: Questo sistema è ottimizzato per il mercato italiano e richiede API keys valide per OpenRouter e Tavily.
