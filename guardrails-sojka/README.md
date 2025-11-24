# 🦅 Bielik Guard (Sójka) — szybki start (Google Cloud Shell)

(source: https://github.com/shivihs/bielik-guard-demo/tree/main)

**Sójka (Bielik Guard v0.1)** — polski model klasyfikacji bezpieczeństwa treści (multilabel), oparty na polskiej RoBercie.  
Wykrywa ryzykowne treści: przemoc, autodestrukcja, toksyczność, NSFW i inne.  

📦 **Model**: https://huggingface.co/speakleash/Bielik-Guard-0.1B-v1.0  
🔗 **Demo**: https://guard.bielik.ai

---

## Instalacja w Google Cloud Shell

### 1. Utwórz środowisko wirtualne
Linux/macOS
```bash
python -m venv .sojka_env
source .sojka_env/bin/activate
```
Windows
```
python -m venv .sojka_env
.sojka_env\Scripts\activate
```
### 2. Zainstaluj PyTorch (wersja CPU)
```bash
pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
```

### 3. Zainstaluj Transformers
```bash
pip install --no-cache-dir transformers
```

### 4. Uruchom aplikację
```bash
python app.py
```

**Aplikacja zapyta o token Hugging Face** — wpisz token typu Read.

> 💡 **Przy pierwszym uruchomieniu** model (~450MB) zostanie automatycznie pobrany z Hugging Face Hub.  
> Kolejne uruchomienia będą natychmiastowe (model zapisany lokalnie w cache).

---

## 🎯 Jak używać

Po uruchomieniu wpisz dowolny tekst do analizy, aplikacja zwróci wyniki dla pięciu kategorii:
- 🩸 **Self-harm** — treści związane z samookaleczeniem
- 🤐 **Hate** — mowa nienawiści, dyskryminacja
- 🤬 **Vulgar** — wulgaryzmy, obsceniczny język
- 💔 **Sex** — treści seksualne (NSFW)
- 🚔 **Crime** — treści związane z przestępczością

**Dostępne komendy:**
- `test` — uruchom przykładowe testy
- `quit` lub `q` — wyjście z aplikacji

---

## 📊 Przykładowy wynik analizy

```
🔍 Analizowany tekst: To jest normalna wiadomość bez problemów.
📊 Oceny bezpieczeństwa:
  🤐 hate: 0.023
  🩸 self-harm: 0.012
  💔 sex: 0.008
  🤬 vulgar: 0.015
  🚔 crime: 0.019

🎯 Główna kategoria: hate
📈 Ogólne ryzyko bezpieczeństwa: 0.023
✅ NISKIE RYZYKO - tekst wydaje się bezpieczny
```

---

## 🔧 Rozwiązywanie problemów w Google Cloud Shell

Jeśli występują błędy instalacji, sprawdź miejsce na dysku i wyczyść cache:
```bash
# Sprawdź wolne miejsce
df -h | grep home

# Wyczyść cache
rm -rf ~/.cache/pip
rm -rf ~/.cache/*
```

---

## 🧹 Usunięcie środowiska
```bash
deactivate
rm -rf .sojka_env
```