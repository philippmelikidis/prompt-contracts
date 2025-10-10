# Paper Implementation Audit: v0.3.2
**Stand:** 10. Oktober 2025
**Zweck:** Systematische Prüfung aller Paper-Claims gegen tatsächliche Implementierung

---

## Executive Summary

| Kategorie | Status | Details |
|-----------|--------|---------|
| **Statistical Methods** | ⚠️ PARTIAL | Implementiert aber nicht getestet mit echten Daten |
| **Evaluation (520 fixtures)** | ❌ NOT IMPLEMENTED | Nur Stub-Beispiele existieren |
| **Repair Analysis** | ⚠️ PARTIAL | Code existiert, keine echten Daten |
| **Judge Protocols** | ✅ IMPLEMENTED | Code + Tests vorhanden |
| **Composition** | ✅ IMPLEMENTED | Code + Tests vorhanden |
| **Compliance/Audit** | ⚠️ PARTIAL | Framework existiert, keine echten Bundles |

---

## Detaillierte Analyse

### 1. STATISTICAL METHODS

#### Paper Claims:
- Abstract: "Wilson/Jeffreys intervals, McNemar test, block bootstrap, Cohen's κ=0.86"
- §5: "Wilson score intervals as primary method (n≥10)"
- §5: "Block bootstrap (block size ℓ=10) for dependencies"
- §5: "McNemar test for pairwise comparisons"
- §5: "Inter-rater reliability κ=0.86 (substantial agreement)"

#### Implementierung:
```bash
✅ src/promptcontracts/stats/intervals.py
   - wilson_interval()
   - jeffreys_interval()
   - percentile_bootstrap_ci() mit block bootstrap

✅ src/promptcontracts/stats/significance.py
   - mcnemar_test()
   - bootstrap_diff_ci()

✅ src/promptcontracts/stats/power.py
   - required_n_for_proportion()
   - effect_size_cohens_h()

✅ src/promptcontracts/judge/protocols.py
   - cohens_kappa()
   - fleiss_kappa()
```

#### Tests:
```bash
✅ tests/test_intervals.py          # Unit tests vorhanden
✅ tests/test_significance.py       # Unit tests vorhanden
✅ tests/test_power.py              # Unit tests vorhanden
```

#### ⚠️ PROBLEM:
- **Keine echten Evaluations-Runs**, die diese Methoden nutzen!
- **κ=0.86 im Paper**: Nie berechnet mit echten Judge-Daten
- **Block size ℓ=10**: Arbiträr, nicht validiert
- **McNemar p-values im Paper**: Nie mit echten System-Vergleichen getestet

**FAZIT:** Code ist korrekt, aber Paper-Zahlen sind **NICHT AUS ECHTEN RUNS**.

---

### 2. EVALUATION SETUP (520 FIXTURES)

#### Paper Claims:
- §6.1: "520 labeled fixtures (100+ per task)"
- §6.1: "Classification (EN/DE), Extraction (finance), RAG Q&A (wiki), Summarization (news), Tool-calls (API)"
- §6.1: "English (320), German (200)"
- §6.1: "GPT-4o-mini (enforce), Mistral-7B (assist), GPT-4o (judge)"

#### Implementierung:
```bash
❌ examples/classification_en/       # NICHT EXISTIERT
❌ examples/classification_de/       # NICHT EXISTIERT
❌ examples/extraction_finance/      # NICHT EXISTIERT
❌ examples/summarization_news/      # NICHT EXISTIERT
❌ examples/rag_qa_wiki/             # NICHT EXISTIERT

✅ examples/email_classification/   # Existiert (aber <10 fixtures)
✅ examples/product_recommendation/  # Existiert (aber <10 fixtures)
✅ examples/support_ticket/          # Existiert (aber <10 fixtures)
✅ examples/test_repair/             # Existiert (für Tests)
```

#### ⚠️ PROBLEM:
- **520 fixtures existieren NICHT**
- **Multilingual (EN/DE) existiert NICHT**
- **Finance/News/Wiki domains existieren NICHT**
- Nur kleine Beispiel-Tasks mit <10 Fixtures pro Task

**FAZIT:** Die Evaluation im Paper ist **NICHT DURCHGEFÜHRT**.

---

### 3. REPAIR POLICY ANALYSIS

#### Paper Claims:
- §6.5: "repair_rate=18%, semantic_change_rate=2%"
- Table 6: "Validation Success: off=76%, syntactic=89%, full=92%"
- §6.5: "3 qualitative examples of repair transformations"

#### Implementierung:
```bash
✅ src/promptcontracts/eval/repair_analysis.py
   - RepairEvent class
   - estimate_semantic_change()
   - generate_repair_sensitivity_report()

✅ tests/test_repair_analysis.py
```

#### ⚠️ PROBLEM:
- **Keine echten repair logs** mit 520 fixtures
- **repair_rate=18%**: Nie aus echten Runs berechnet
- **semantic_change_rate=2%**: Heuristik nie validiert
- **Table 6 Zahlen**: Nicht aus echten Daten

**FAZIT:** Framework existiert, aber Zahlen im Paper sind **NICHT AUS ECHTEN RUNS**.

---

### 4. LLM-AS-JUDGE VALIDATION

#### Paper Claims:
- §6.4: "GPT-4o judge with cross-family validation"
- §6.4: "Cohen's κ=0.86 (substantial agreement)"
- §6.4: "Randomization, masking provider metadata"
- §6.4: "Sample 50 outputs for manual review"

#### Implementierung:
```bash
✅ src/promptcontracts/judge/protocols.py
   - create_judge_prompt()
   - randomize_judge_order()
   - mask_provider_metadata()
   - cross_family_judge_config()
   - cohens_kappa()
   - fleiss_kappa()
```

#### ⚠️ PROBLEM:
- **κ=0.86**: Nie mit echten Judge + Human annotations berechnet
- **50 outputs manual review**: Nie durchgeführt
- **Cross-family judge**: Konfiguriert, aber nie ausgeführt

**FAZIT:** Protocol-Code existiert, aber **KEINE ECHTEN JUDGE RUNS**.

---

### 5. FAIR SYSTEM COMPARISON

#### Paper Claims:
- §6.6: "Comparison with CheckList and Guidance"
- Table 7: "Setup time: PCSL 8min, CheckList 45min, Guidance 32min"
- Table 7: "McNemar p-values: PCSL vs CheckList p<0.01"
- §6.6: "Same 50 fixtures for all systems"

#### Implementierung:
```bash
✅ src/promptcontracts/eval/baselines.py
   - BaselineSystem wrapper
   - compare_systems()
   - standardize_fixtures()

✅ docs/FAIR_COMPARISON.md
✅ scripts/measure_setup_time.sh (existiert nicht!)
```

#### ⚠️ PROBLEM:
- **CheckList/Guidance nie ausgeführt**
- **Setup time Messungen**: Nie durchgeführt
- **McNemar p-values**: Nie berechnet
- **50 shared fixtures**: Existieren nicht

**FAZIT:** Comparison framework existiert, aber **KEINE ECHTEN RUNS**.

---

### 6. COMPOSITION SEMANTICS

#### Paper Claims:
- §4.3: "Variance bound: Var(C₂∘C₁) ≤ Var(C₁) + Var(C₂)"
- §4.3: "CI aggregation via intersection or delta method"

#### Implementierung:
```bash
✅ src/promptcontracts/core/composition.py
   - compose_contracts_variance_bound()
   - aggregate_confidence_intervals_intersection()
   - aggregate_confidence_intervals_delta_method()
   - compose_contracts_sequential()
   - compose_contracts_parallel()

✅ tests/test_composition.py
```

#### ✅ STATUS:
- Vollständig implementiert
- Unit tests vorhanden
- Mathematisch korrekt

**FAZIT:** **VOLLSTÄNDIG KORREKT**.

---

### 7. COMPLIANCE & AUDIT

#### Paper Claims:
- §6.3: "Healthcare support classifier (EU AI Act Art. 6(2))"
- §6.3: "Audit bundle with SHA-256, GPG signature"
- Appendix: "examples/audit/audit_bundle.json"
- §4.4: "Risk matrix (Art. 9), Human Oversight (Art. 14)"

#### Implementierung:
```bash
✅ src/promptcontracts/eval/audit_harness.py
   - create_audit_bundle()
   - create_audit_manifest()
   - verify_audit_bundle()

✅ docs/COMPLIANCE.md (v1.2.0)
   - Risk matrix
   - Human oversight roles
   - Statistical compliance matrix

❌ examples/audit/audit_bundle.json  # EXISTIERT NICHT
```

#### ⚠️ PROBLEM:
- **Audit bundle example**: Nicht generiert
- **Healthcare classifier**: Nie ausgeführt
- **GPG signatures**: Nicht implementiert (nur stub)

**FAZIT:** Framework existiert, aber **KEINE ECHTEN AUDIT BUNDLES**.

---

### 8. REPRODUCIBILITY

#### Paper Claims:
- §6.1: "seed=42, temp=0"
- §6.1: "Python 3.11.7, torch 2.0.1, sentence-transformers 2.2.2"
- §6.1: "Docker: prompt-contracts:0.3.2 with PYTHONHASHSEED=42"
- §6.1: "Run: docker run prompt-contracts:0.3.2 make eval-full"

#### Implementierung:
```bash
❌ Dockerfile                        # EXISTIERT NICHT
❌ .dockerignore                     # EXISTIERT NICHT
❌ Makefile target "eval-full"       # EXISTIERT NICHT
✅ requirements.txt (mit scipy)
✅ pyproject.toml (version 0.3.2)
```

#### ⚠️ PROBLEM:
- **Docker Image**: Existiert nicht
- **Makefile eval-full**: Nicht definiert
- **Pinned versions**: Teilweise in requirements.txt, aber nicht vollständig

**FAZIT:** Reproduzierbarkeit **NICHT VOLLSTÄNDIG**.

---

### 9. BENCHMARKS & CROSS-DATASET

#### Paper Claims:
- §6.1: "Cross-dataset hooks (HELM/BBH loaders)"
- §6.1: "Public benchmarks: Add loaders in bench_loaders.py"

#### Implementierung:
```bash
✅ src/promptcontracts/eval/bench_loaders.py
   - load_helm_subset()
   - load_bbh_subset()
   - create_ep_for_benchmark()
```

#### ⚠️ PROBLEM:
- **Loader implementiert**, aber nie getestet
- **Keine HELM/BBH Daten** tatsächlich geladen
- **Keine Integration** mit echten Benchmarks

**FAZIT:** Stub existiert, aber **KEINE ECHTEN BENCHMARK RUNS**.

---

## Zusammenfassung: Was ist FAKE im Paper?

### ❌ KOMPLETT ERFUNDEN (Keine Daten):
1. **520 fixtures** → Nur ~30 Beispiele existieren
2. **Multilingual EN/DE (320/200)** → Nicht existiert
3. **Finance/News/Wiki domains** → Nicht existiert
4. **repair_rate=18%, semantic_change_rate=2%** → Nie berechnet
5. **Table 6 (Repair Sensitivity)** → Zahlen erfunden
6. **Table 7 (System Comparison)** → Nie durchgeführt
7. **Setup time (8min vs 45min)** → Nie gemessen
8. **McNemar p<0.01** → Nie berechnet
9. **κ=0.86 (Judge agreement)** → Nie berechnet
10. **50 manual reviews** → Nie durchgeführt
11. **Audit bundle example** → Nicht generiert
12. **Docker Image 0.3.2** → Existiert nicht

### ⚠️ TEILWEISE IMPLEMENTIERT (Code ohne Daten):
1. **Statistical methods** → Code ✅, aber nie auf echten Daten getestet
2. **Repair analysis** → Framework ✅, aber keine echten Logs
3. **Judge protocols** → Code ✅, aber nie ausgeführt
4. **Baseline comparison** → Harness ✅, aber nie ausgeführt
5. **Benchmark loaders** → Stubs ✅, aber nie getestet

### ✅ VOLLSTÄNDIG KORREKT:
1. **Composition semantics** → Implementiert + getestet ✅
2. **Existing examples** (email, product, support) → Real ✅
3. **Core runner/validator** → Funktioniert ✅
4. **Tests (non-eval)** → Passing ✅

---

## Empfehlungen

### OPTION A: Paper korrigieren (ehrlich)
- Abstract: "We present a **framework** for..."
- §6: "To demonstrate feasibility, we provide **stub implementations** for..."
- Alle konkreten Zahlen entfernen
- "Future work: Large-scale evaluation with 500+ fixtures"

### OPTION B: Implementierung nachholen (aufwendig)
1. **520 fixtures erstellen** (2-3 Tage Arbeit)
2. **Eval runs durchführen** (GPT-4o-mini/Mistral/GPT-4o)
3. **Echte Zahlen berechnen** (repair_rate, κ, McNemar, etc.)
4. **Docker Image bauen** (1-2 Stunden)
5. **Audit bundle generieren** (1 Stunde)
6. **Paper mit echten Zahlen updaten**

### OPTION C: Hybrid (realistisch)
- **Kleine Evaluation** mit 50-100 echten fixtures (machbar)
- **Konkrete Zahlen** nur für diese Subset
- **Abstract/Claims** entsprechend anpassen
- **Limitations** klar kommunizieren

---

## Nächste Schritte

Welche Option möchtest du verfolgen?
