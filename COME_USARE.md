# 🚀 COME USARE IL BLOG GENERATOR

## File Importanti (solo questi!)

- `blog_generator.py` - Script principale (QUESTO È QUELLO DA USARE)
- `input_manager.py` - Gestione input (non toccare)
- `config.yaml` - Configurazioni (puoi modificare)
- `prompts.yaml` - Prompt ottimizzati (puoi modificare)
- `requirements.txt` - Dipendenze Python

## 🎯 COME TESTARE SUBITO

### 1. Test Veloce con Template
```bash
# Genera un template di esempio
py blog_generator.py --generate-template

# Modifica il file input_template.yaml che viene creato
# Poi usalo:
py blog_generator.py --input-file input_template.yaml
```

### 2. Test Interattivo (CONSIGLIATO)
```bash
py blog_generator.py --interactive
```
Ti farà delle domande e genererà l'articolo.

### 3. Test con Parametri Diretti
```bash
py blog_generator.py --topic "Case Vacanza Costiera Amalfitana" --intent commerciale --website "https://miosito.it" --business "Affitti turistici"
```

## ✅ COSA È STATO MIGLIORATO

1. **Input Completi**: Ora puoi specificare:
   - Topic dell'articolo
   - Intento (informativo/commerciale/educativo)
   - Sito web di destinazione
   - Attività da sponsorizzare
   - Pubblico target
   - Tono di voce

2. **Step Intermedio**: Aggiunto agente di analisi strategica

3. **Modelli Economici**: Usa GPT-4o-mini per ricerca e analisi (più economico)

4. **Prompt Italiani**: Ottimizzati per il mercato italiano

## 🔧 CONFIGURAZIONE

### File .env (OBBLIGATORIO)
```
OPENROUTER_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### config.yaml (opzionale)
Puoi cambiare i modelli usati:
```yaml
models:
  research: "gpt-4o-mini"    # Economico
  analysis: "gpt-4o-mini"    # Economico  
  outline: "gpt-4o"          # Avanzato
  drafting: "gpt-4o"         # Avanzato
  optimization: "gpt-4o"     # Avanzato
```

## 🎯 ESEMPIO PRATICO

1. Esegui: `py blog_generator.py --interactive`
2. Inserisci:
   - Topic: "Migliori Ristoranti Roma 2025"
   - Intento: commerciale
   - Website: "https://ristorantiroma.it"
   - Business: "Prenotazioni ristoranti"
   - Audience: "turisti e romani"
   - Tono: professionale

3. Aspetta che generi l'articolo!

## 📁 OUTPUT

Il sistema creerà:
- `blog_[topic]_[timestamp].md` - Articolo finale
- `blog_generator.log` - Log delle operazioni

## ❗ PROBLEMI COMUNI

1. **"python non riconosciuto"** → Usa `py` invece di `python`
2. **Errore API keys** → Controlla il file `.env`
3. **Errore modelli** → Verifica le API keys OpenRouter

## 🚀 PRONTO!

Il sistema è ora pulito e semplificato. Usa solo `blog_generator.py` e segui questa guida!
