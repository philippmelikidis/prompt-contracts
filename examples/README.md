# Prompt-Contracts Examples

Dieses Verzeichnis enthält vollständige Beispiel-Contracts, die verschiedene Use Cases und Execution Modes demonstrieren.

## 📁 Verfügbare Beispiele

### 1. Support Ticket Classification
**Verzeichnis:** [`support_ticket/`](./support_ticket/)
**Use Case:** Klassifizierung von Support-Anfragen
**Execution Mode:** `assist`
**Provider:** Ollama (Mistral)

Klassifiziert Support-Tickets in Kategorien mit Priorität und Begründung.

**Dateien:**
- `pd.json` - Prompt Definition
- `es.json` - Expectation Suite (6 Checks)
- `ep.json` - Evaluation Profile (2 Fixtures)

**Ausführen:**
```bash
prompt-contracts run \
  --pd examples/support_ticket/pd.json \
  --es examples/support_ticket/es.json \
  --ep examples/support_ticket/ep.json \
  --report cli
```

---

### 2. Email Classification
**Verzeichnis:** [`email_classification/`](./email_classification/)
**Use Case:** E-Mail-Kategorisierung mit Sentiment-Analyse
**Execution Modes:** Alle vier Modi (observe, assist, enforce, auto)
**Provider:** Ollama / OpenAI

Analysiert E-Mails und klassifiziert sie nach Kategorie, Dringlichkeit und Sentiment.

**Dateien:**
- `pd.json` - Prompt Definition
- `es.json` - Expectation Suite (8 Checks)
- `ep_observe.json` - Observe Mode (Nur Validierung)
- `ep_assist.json` - Assist Mode (Prompt-Augmentation)
- `ep_enforce.json` - Enforce Mode (Schema-guided JSON, OpenAI)
- `ep_auto.json` - Auto Mode (Adaptive)

**Ausführen:**
```bash
# Observe Mode - Nur Validierung
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_observe.json

# Assist Mode - Mit Prompt-Augmentation
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_assist.json

# Enforce Mode - Schema-guided (benötigt OpenAI)
export OPENAI_API_KEY="sk-..."
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_enforce.json

# Auto Mode - Adaptiv
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_auto.json
```

---

### 3. Product Recommendation
**Verzeichnis:** [`product_recommendation/`](./product_recommendation/)
**Use Case:** Personalisierte Produktempfehlungen
**Execution Mode:** `assist`
**Provider:** Ollama (Mistral)

Generiert Produktempfehlungen basierend auf Benutzerpräferenzen.

**Dateien:**
- `pd.json` - Prompt Definition
- `es.json` - Expectation Suite (7 Checks)
- `ep.json` - Evaluation Profile (3 Fixtures)

**Ausführen:**
```bash
prompt-contracts run \
  --pd examples/product_recommendation/pd.json \
  --es examples/product_recommendation/es.json \
  --ep examples/product_recommendation/ep.json \
  --save-io artifacts/product_recs/
```

---

### 4. Simple YAML Example
**Verzeichnis:** [`simple_yaml/`](./simple_yaml/)
**Use Case:** Minimales Beispiel in YAML-Format
**Format:** YAML

Einfaches Beispiel, das zeigt, wie YAML-Contracts verwendet werden können.

**Ausführen:**
```bash
# YAML wird automatisch zu JSON konvertiert
prompt-contracts validate pd examples/simple_yaml/contract.yaml
```

---

## 🚀 Quick Start

### 1. Installation
```bash
pip install prompt-contracts
```

### 2. Setup Ollama (für lokale Modelle)
```bash
# Install Ollama
brew install ollama

# Start Server
ollama serve

# Pull Mistral
ollama pull mistral
```

### 3. Erstes Beispiel ausführen
```bash
prompt-contracts run \
  --pd examples/support_ticket/pd.json \
  --es examples/support_ticket/es.json \
  --ep examples/support_ticket/ep.json \
  --report cli
```

---

## 📊 Execution Modes Vergleich

| Example | observe | assist | enforce | auto |
|---------|---------|--------|---------|------|
| support_ticket | - | ✅ | - | - |
| email_classification | ✅ | ✅ | ✅ | ✅ |
| product_recommendation | - | ✅ | - | - |
| simple_yaml | - | - | - | - |

### Mode Eigenschaften

| Mode | Prompt-Änderungen | Auto-Repair | Retry | Schema Enforcement |
|------|-------------------|-------------|-------|-------------------|
| **observe** | ❌ Keine | ❌ Nein | ❌ Nein | ❌ Nein |
| **assist** | ✅ Constraints | ✅ Ja | ✅ Ja | ❌ Nein |
| **enforce** | ✅ Schema | ✅ Ja | ✅ Ja | ✅ Ja (wenn unterstützt) |
| **auto** | 🔄 Adaptiv | ✅ Ja | ✅ Ja | 🔄 Wenn verfügbar |

---

## 🔧 Artifact Saving

Speichern Sie alle Input/Output-Artefakte für detaillierte Analyse:

```bash
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_assist.json \
  --save-io artifacts/ \
  --report json \
  --out results.json
```

**Artifact-Struktur:**
```
artifacts/
  <target-id>/
    <fixture-id>/
      input_final.txt      # Finaler Prompt (mit Constraints falls assist)
      output_raw.txt       # Raw Model Response
      output_norm.txt      # Normalisierter Output (nach Auto-Repair)
      run.json            # Vollständige Execution Metadata
```

---

## 📝 Eigenen Contract erstellen

### 1. Prompt Definition (pd.json)
```json
{
  "pcsl": "0.1.0",
  "id": "my.contract.v1",
  "io": {
    "channel": "text",
    "expects": "structured/json"
  },
  "prompt": "Your prompt here..."
}
```

### 2. Expectation Suite (es.json)
```json
{
  "pcsl": "0.1.0",
  "checks": [
    { "type": "pc.check.json_valid" },
    { "type": "pc.check.json_required", "fields": ["field1", "field2"] },
    { "type": "pc.check.enum", "field": "$.field1", "allowed": ["val1", "val2"] }
  ]
}
```

### 3. Evaluation Profile (ep.json)
```json
{
  "pcsl": "0.1.0",
  "targets": [
    { "type": "ollama", "model": "mistral", "params": { "temperature": 0 } }
  ],
  "fixtures": [
    { "id": "test1", "input": "Test input 1" },
    { "id": "test2", "input": "Test input 2" }
  ],
  "execution": {
    "mode": "assist",
    "max_retries": 1,
    "auto_repair": {
      "lowercase_fields": ["$.field1"],
      "strip_markdown_fences": true
    }
  }
}
```

---

## 📚 Weitere Ressourcen

- **Vollständige Dokumentation:** [README.md](../README.md)
- **Getting Started Guide:** [QUICKSTART.md](../QUICKSTART.md)
- **PCSL Specification:** [pcsl-v0.1.md](../src/promptcontracts/spec/pcsl-v0.1.md)
- **GitHub Repository:** https://github.com/philippmelikidis/prompt-contracts

---

## 🤝 Contributing

Haben Sie ein interessantes Beispiel? Wir freuen uns über Pull Requests!

1. Fork das Repository
2. Erstellen Sie Ihr Beispiel in `examples/your-example/`
3. Fügen Sie eine Beschreibung zu dieser README hinzu
4. Öffnen Sie einen Pull Request

---

## 📄 License

MIT License - siehe [LICENSE](../LICENSE) für Details
