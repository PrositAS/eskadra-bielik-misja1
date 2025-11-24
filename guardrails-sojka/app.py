"""
Bielik Guard - System analizy bezpieczeństwa tekstu w języku polskim
Model klasyfikuje tekst pod kątem potencjalnie niebezpiecznych treści
"""

# Importy z biblioteki transformers (Hugging Face) do obsługi modeli NLP
from transformers import pipeline  # Pipeline upraszcza interfejs do modeli
from huggingface_hub import login  # Autoryzacja w Hugging Face Hub

# Logowanie do Hugging Face Hub (wykorzystuje token z cache jeśli istnieje)
# Potrzebne do pobrania modelu z repozytorium HF
login(new_session=False)

# Ścieżka do modelu Bielik Guard - polskiego modelu klasyfikacji bezpieczeństwa tekstu
# Model jest hosowany na Hugging Face i zostanie automatycznie pobrany przy pierwszym użyciu
model_path = "speakleash/Bielik-Guard-0.1B-v1.0" 

# Inicjalizacja pipeline dla klasyfikacji tekstu
# return_all_scores=True -> zwraca prawdopodobieństwa dla WSZYSTKICH kategorii, nie tylko najwyższej
# Pipeline automatycznie obsługuje: tokenizację, inference, dekodowanie wyników
classifier = pipeline("text-classification", model=model_path, return_all_scores=True)

def analyze_text(text):
    """Analizuje tekst i zwraca wyniki bezpieczeństwa"""
    
    # Wywołanie modelu - tekst przechodzi przez:
    # 1. Tokenizację (tekst -> tokeny zrozumiałe dla modelu)
    # 2. Forward pass przez sieć neuronową
    # 3. Softmax -> prawdopodobieństwa dla każdej kategorii
    results = classifier(text)
    
    # Pipeline zwraca listę wyników (nawet dla pojedynczego tekstu), bierzemy pierwszy element
    results = results[0]
    print(f"\n🔍 Analizowany tekst: {text}")
    print("📊 Oceny bezpieczeństwa:")
    
    # Iteracja przez wszystkie kategorie klasyfikacji
    # Model zwraca score (0-1) dla każdej z kategorii: self-harm, hate, vulgar, sex, crime
    for result in results:
        label = result['label']  # Nazwa kategorii z modelu
        score = result['score']   # Prawdopodobieństwo (confidence) dla danej kategorii

        # Mapowanie kategorii na emoji dla wizualizacji
        if 'self-harm' in label.lower():
            emoji = "🩸"
        elif 'hate' in label.lower():
            emoji = "🤐"
        elif 'vulgar' in label.lower():
            emoji = "🤬"
        elif 'sex' in label.lower():
            emoji = "💔"
        elif 'crime' in label.lower():
            emoji = "🚔"
        else:
            emoji = "📋"
        
        print(f"  {emoji} {label}: {score:.3f}")
    
    # Wyznaczanie dominującej kategorii (z najwyższym score)
    # To kategoria, do której model ma największą pewność (confidence)
    max_score = max(result['score'] for result in results)
    max_label = max(results, key=lambda x: x['score'])['label']
    
    print(f"\n🎯 Główna kategoria: {max_label}")
    print(f"📈 Ogólne ryzyko bezpieczeństwa: {max_score:.3f}")
    
    # Interpretacja wyniku na podstawie progów pewności modelu
    # Progi są arbitralne i można je dostosować do konkretnego use case
    if max_score > 0.7:
        print("🚨 WYSOKIE RYZYKO - tekst może zawierać niebezpieczne treści")
    elif max_score > 0.4:
        print("🔔 ŚREDNIE RYZYKO - tekst wymaga uwagi")
    else:
        print("✅ NISKIE RYZYKO - tekst wydaje się bezpieczny")
    print("=" * 60)

def run_sample_tests():
    """Uruchamia testy na przykładowych tekstach"""
    print("🧪 Uruchamianie testów na przykładowych tekstach...")
    
    # Zbiór testowy reprezentujący różne kategorie treści niebezpiecznych
    # Każdy tekst powinien aktywować inną kategorię modelu
    sample_texts = [
        "To jest normalna wiadomość bez problemów.",  # Neutralny baseline
        "Chcę się zabić i skończyć z tym wszystkim.",  # Self-harm
        "Dlaczego hipisi są tacy brudni i głupi",      # Hate speech
        "K*rwa, to jest ch*jowe rozwiązanie.",         # Vulgar language
        "Opowiem ci o seksie i intymności.",           # Sexual content
        "Jak ukraść samochód i nie zostać złapanym."   # Crime-related
    ]
    
    for text in sample_texts:
        analyze_text(text)
        print("-" * 60)

def interactive_mode():
    """
    Tryb interaktywny do analizy tekstu w czasie rzeczywistym
    Każde wprowadzone zdanie przechodzi przez pełny pipeline klasyfikacji
    """
    print("Wprowadź tekst do analizy (wpisz 'quit' aby wyjść, 'test' dla przykładów)")
    
    while True:
        try:
            user_input = input("\n📝 Wprowadź tekst: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'wyjście', 'q']:
                print("👋 Dziękuję za korzystanie z Bielik Guard!")
                break
            elif user_input.lower() in ['test', 'testy', 'przykłady']:
                run_sample_tests()
                continue
            elif not user_input:
                print("⚠️ Proszę wprowadzić jakiś tekst.")
                continue
            
            analyze_text(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Dziękuję za korzystanie z Bielik Guard!")
            break
        except Exception as e:
            print(f"❌ Wystąpił błąd: {e}")

if __name__ == "__main__":
    # Punkt wejścia aplikacji - wykonuje się tylko przy bezpośrednim uruchomieniu skryptu
    print("🐦 Sójka - System analizy bezpieczeństwa tekstu")
    print("🛡️ Model: speakleash/Bielik-Guard-0.1B-v1.0")
    print("=" * 60)
    
    # Uruchomienie trybu interaktywnego - użytkownik może wprowadzać własne teksty do analizy
    # Model jest już załadowany w pamięci (zainicjalizowany na początku skryptu)
    # Kolejne wywołania wykorzystują ten sam model bez ponownego ładowania
    interactive_mode()