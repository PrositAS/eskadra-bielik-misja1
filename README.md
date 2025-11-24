# Eskadra Bielik - Misja 1 - ADK + Cloud Run + Bielik
Przykładowy kod źródłowy pozwalający na:

* Skonfigurowanie własnej instancji modelu [Bielik](https://ollama.com/SpeakLeash/bielik-4.5b-v3.0-instruct) w oparciu o [Ollama](https://ollama.com/)

* Skonfigurowanie prostych systemów agentowych przy wykorzystaniu [Agent Development Kit](https://google.github.io/adk-docs/)

* Uruchomienie obu powyższych serwisów na [Cloud Run](https://cloud.google.com/run?hl=en)

  

## 1. Przygotowanie projektu Google Cloud

1. Uzyskaj kredyt Cloud **OnRamp**, lub skonfiguruj płatności w projekcie Google Cloud

2. Przejdź do **Google Cloud Console**: [console.cloud.google.com](https://console.cloud.google.com)

3. Stwórz nowy projekt Google Cloud i wybierz go aby był aktywny
>[!TIP]
>Możesz sprawdzić dostępność kredytów OnRamp wybierając z menu po lewej stronie: Billing / Credits

4. Otwórz Cloud Shell ([dokumentacja](https://cloud.google.com/shell/docs))

5. Sklonuj repozytorium z przykładowym kodem i przejdź do nowoutworzonego katalogu
   ```bash
   git clone https://github.com/PrositAS/eskadra-bielik-misja1.git
   cd eskadra-bielik-misja1
   ```

6. Zmień nazwę pliku `.env.sample` na `.env`
   ```bash
   mv .env.sample .env
   ```

7. Zaktualizuj odpowiednie na tym etapie zmienne środowiskowe w pliku `.env`     
      * `BIELIK_EVENT_ID`- Identyfikator warsztatów zgodny z kodem użytym w OnRamp Credits
      * `GOOGLE_CLOUD_LOCATION`- zmienną definiującą region Google Cloud
      * `BIELIK_SERVICE_NAME` - domyślną nazwę dla usługi gdzie uruchomimy Bielika
      * `BIELIK_MODEL_NAME` - wersję Bielika z której będziemy korzystać 

>[!TIP]
>W terminalu `Cloud Shell` dostępny jest edytor po wybraniu opcji *Open Editor*

   ```bash
   BIELIK_EVENT_ID="<IDENTYFIKATOR>"
   GOOGLE_CLOUD_LOCATION="europe-west1"  # Europe (Belgium)
   BIELIK_SERVICE_NAME="ollama-bielik-v3"
   BIELIK_MODEL_NAME="SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0"
   ```
>[!IMPORTANT]
>Jeżeli zmieniasz w `BIELIK_MODEL_NAME` domyślny model Bielika na inną wersję, to zaktualizuj tę informację również w pliku `ollama-bielik/Dockerfile`

   ```dockerfile
   ENV MODEL SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0
   ```

8. Wczytaj zmienne środowiskowe korzystając z podręcznego skryptu

   ```bash
   source reload-env.sh
   ```



## 2. Własna instancja Bielika

1. Ustal domyślne konto serwisowe dla wybranego projektu `default service account`
   ```bash
   gcloud builds get-default-service-account
   ```

2. Poniższa komenda stworzy nową usługę w Cloud Run o nazwie takiej jak wartość zmiennej `$BIELIK_SERVICE_NAME`. Na podstawie definicji w `ollama-bielik/Dockerfile` nardzędzie `gcloud` stworzy odpowiedni kontener, skonfiguruje usługę Ollama oraz wczyta odpowiednią wersję modelu Bielik.

   ```bash
   gcloud run deploy $BIELIK_SERVICE_NAME --source ollama-bielik/ --region $GOOGLE_CLOUD_LOCATION --concurrency 7 --cpu 8 --set-env-vars OLLAMA_NUM_PARALLEL=4 --gpu 1 --gpu-type nvidia-l4 --max-instances 1 --memory 16Gi --allow-unauthenticated --no-cpu-throttling --no-gpu-zonal-redundancy --timeout 600 --labels dev-tutorial=codelab-dos-$BIELIK_EVENT_ID
   ```

>[!CAUTION]
>Flaga `--allow-unauthenticated` udostępnia usługę publicznie w internecie i każdy kto zna URL, może zaczać z niej korzystać. W środowisku produkcyjnym zazwyczaj trzeba tę flagę usunąć i odpowiednio skonfigurować reguły dostępu.

>[!TIP]
>Alternatywnie, możesz uruchomić powyższą komendę korzystając ze skryptu `deploy-bielik.sh`
   ```bash
   deploy-bielik.sh
   ```

3. Uruchom poniższą komendę, aby sprawdzić pod jakim URL jest dostępny Bielik

   ```bash
   gcloud run services describe $BIELIK_SERVICE_NAME --region=$GOOGLE_CLOUD_LOCATION --format='value(status.url)'
   ```
>[!TIP]
>Odpowiedz twierdząco, jeżeli system spyta o włączenie odpowiednich API oraz stworzenie rejestru artefaktów

4. Przypisz powyższy URL do zmiennej środowiskowej `OLLAMA_API_BASE` w pliku `.env` i następnie wczytaj zmienne środowiskowe ponownie:
   ```bash
   source reload-env.sh
   ```



### Jak sprawdzić, czy nasz Bielik jest gotowy?

* Sprawdź w Google Cloud console czy nowy serwis jest już dostępny
* Sprawdź czy otwierając URL w przeglądarce zobaczysz informację: `Ollama is running`
* Sprawdź przez API jakie modele są dostępne lokalnie na serwerze Ollama
   ```bash
   curl "${OLLAMA_API_BASE}/api/tags"
   ```
* Wyślij zapytanie przez API
   ```bash
   curl "${OLLAMA_API_BASE}/api/generate" -d "{
      \"model\": \"$BIELIK_MODEL_NAME\",
      \"prompt\": \"Kto zabił smoka wawelskiego?\",
      \"stream\": false
   }"
   ```



## 3. Konfiguracja systemów agentowych ADK

1. Skonfiguruj swój własny klucz Gemini API
   *   Stwórz lub skopiuj istniejący Gemini API key z [Google AI Studio](https://ai.dev).
   *   Dodaj wartość klucza ze swojego Gemini API key jako wartość zmiennej `GOOGLE_API_KEY` w pliku `.env`
   ```bash
   GOOGLE_API_KEY=TWÓJ_KLUCZ
   ```
2. Wczytaj zmienne środowiskowe ponownie
   ```bash
   source reload-env.sh
   ```
3. Przejdź do katalogu z agentami

   ```bash
   cd adk-agents
   ```
   
4. Stwórz i aktywuj wirtualne środowisko Python

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   
5. Zainstaluj wymagane komponenty

   ```bash
   pip install -r requirements.txt
   ```



## 4. Przykładowe systemy agentowe

### 4.1 System agentowy - Twórca treści (`content_creator`)

Ten prosty system agentowy, działający jedynie w oparciu o model Bielik, jest prostym przykładem wykorzystania [LLM Agents](https://google.github.io/adk-docs/agents/llm-agents/) oraz [Workflow Agents](https://google.github.io/adk-docs/agents/workflow-agents/) dostępnych w ADK. System ma na celu generowanie artykułów dla różnych grup docelowych (dzieci, kadra zarządzająca) w oparciu o temat zasugerowany przez użytkownika.

- `content_creator_agent` - Główny, sekwencyjny agent, uruchamia pod-agentów jeden po drugim
- `topic_identifier_agent` - Agent LLM odpowiedzialny za zidentyfikowanie tematu którym interesuje się użytkownik.
- `topic_expander_agent` - Agent LLM odpowiedzialny za rozwinięcie tematu. Generuje listę ciekawych faktów związanych z tematem.
- `authoring_agent` - Agent równoległy - uruchamia pod-agentów równolegle. Zawiera dwóch pod-agentów, po jednym na każdą grupę docelową
- `children_audience_agent` - Agent LLM odpowiedzialny za tworzenie treści skierowanych do dzieci.
- `executive_audience_agent` - Agent LLM odpowiedzialny za tworzenie treści skierowanych do kadry zarządzającej.
- `silesian_audience_agent` - Agent LLM odpowiedzialny za tworzenie treści po śląsku.

```mermaid
graph TD
    subgraph content_creator_agent [content_creator_agent:SequentialAgent]
        direction LR
        topic_identifier_agent("topic_identifier_agent:Agent") --> topic_expander_agent("topic_expander_agent:Agent");
        topic_expander_agent --> authoring_agent;
    end

    subgraph authoring_agent [authoring_agent:ParallelAgent]
        direction TB
        children_audience_agent("children_audience_agent:Agent");
        executive_audience_agent("executive_audience_agent:Agent");
        silesian_audience_agent("silesian_audience_agent:Agent");
    end
```


1. Upewnij się, że jesteś w katalogu `adk_agents` oraz że wszystkie zmienne środowiskowe są załadowane
2. Uruchom agenta w konsoli **Cloud Shell** i rozpocznij interakcję

   ```bash
    adk run content_creator/
   ```



### 4.2 System agentowy - Przewodnik kulinarny (`culinary_guide`)

Ten hybrydowy system agentowy, działający w oparciu o modele Gemini i Bielik, jest przykładem wykorzystania Agentów LLM ([LLM Agents](https://google.github.io/adk-docs/agents/llm-agents/)), funkcji-jako-narzędzi ([Function Tools](https://google.github.io/adk-docs/tools/function-tools/#function-tool)) oraz agentów-jako-narzędzi ([Agent-as-a-tTool](https://google.github.io/adk-docs/tools/function-tools/#agent-tool)) dostępnych w ADK.

System ma na celu pełnienie roli międzynarodowego przewodnika kulinarnego, który deleguje zadania do wyspecjalizowanych pod-agentów lub narzędzi w zależności od kraju, o który pyta użytkownik.

- `culinary_guide_agent` - Główny agent, który komunikuje się z użytkownikiem w języku angielskim. Jego zadaniem jest zrozumienie prośby o rekomendacje kulinarne, identyfikacja kraju i preferencji dietetycznych, a następnie delegowanie zadania do odpowiednich narzędzi.
- `polish_expert_tool` - Narzędzie typu AgentTool, które opakowuje agenta polish_culinary_expert_agent, umożliwiając głównemu agentowi korzystanie z jego wyspecjalizowanych zdolności.
- `polish_culinary_expert_agent` - Wyspecjalizowany Agent LLM oparty na modelu Bielik, ekspert w dziedzinie kuchni polskiej. Przyjmuje zapytania i odpowiada wyłącznie w języku polskim.
- `german_food_tool` - Proste narzędzie oparte na funkcji Pythona, które dostarcza rekomendacji kulinarnych dla Niemiec w oparciu o zdefiniowaną logikę.

```mermaid
graph TD
    subgraph Culinary Recommendation System
        direction TB

        %% Define the Root Agent
        A[fa:fa-robot culinary_guide_agent]

        %% Define the Tools
        subgraph polish_expert_tool
            direction TB
            B[fa:fa-wrench AgentTool] --> C[fa:fa-robot polish_culinary_agent]
        end

        D[fa:fa-wrench german_food_tool]

        %% Define the relationships
        A --> B
        A --> D
    end
```
1. Upewnij się, że jesteś w katalogu `adk_agents` oraz że wszystkie zmienne środowiskowe są załadowane
2. Uruchom agenta w konsoli **Cloud Shell** i rozpocznij interakcję

   ```bash
    adk run culinary_guide_agent/
   ```



### 4.3 System agentowy - Planista Podróży po Polsce (`polish_travel_planner`)

Ten kompleksowy system agentowy, działający w oparciu o model Bielik, demonstruje zaawansowane możliwości planowania i orkiestracji workflow w ADK. System wykorzystuje zarówno [Sequential Agents](https://google.github.io/adk-docs/agents/workflow-agents/#sequential-agent) jak i [Parallel Agents](https://google.github.io/adk-docs/agents/workflow-agents/#parallel-agent) do tworzenia szczegółowych, spersonalizowanych planów podróży po Polsce.

System ma na celu stworzenie kompletnego, gotowego do użycia planu wycieczki na podstawie preferencji użytkownika. Showcaseuje możliwości Bielika w dziedzinie lokalnej wiedzy o Polsce, kulturze i praktycznych aspektach turystyki.

Architektura systemu:

- `polish_travel_planner_agent` - Główny agent sekwencyjny, który orchestruje cały proces planowania podróży
- `destination_analyzer_agent` - Agent LLM analizujący preferencje użytkownika (góry vs morze, historia vs przyroda, itp.) i sugerujący odpowiednie destynacje w Polsce
- `research_team` - Agent równoległy koordynujący pracę trzech wyspecjalizowanych ekspertów, którzy działają jednocześnie:
  - `history_expert_agent` - Ekspert od polskiej historii i zabytków, dostarczający informacji o najważniejszych miejscach historycznych
  - `practical_guide_agent` - Praktyczny przewodnik zajmujący się logistyką: transport, noclegi, gastronomia i koszty
  - `cultural_activities_agent` - Znawca kultury lokalnej, festiwali, tradycji i aktywności na świeżym powietrzu
- `itinerary_creator_agent` - Agent syntetyzujący wszystkie zebrane informacje w szczegółowy, dzień-po-dniu plan podróży z budżetem i praktycznymi wskazówkami

```mermaid
graph TD
    subgraph polish_travel_planner_agent [polish_travel_planner_agent:SequentialAgent]
        direction LR
        A[destination_analyzer_agent:Agent] --> B[research_team:ParallelAgent]
        B --> C[itinerary_creator_agent:Agent]
    end

    subgraph research_team [research_team:ParallelAgent]
        direction TB
        D[history_expert_agent:Agent]
        E[practical_guide_agent:Agent]
        F[cultural_activities_agent:Agent]
    end

    B -.-> D
    B -.-> E
    B -.-> F
```


**Przykładowe zapytania do przetestowania:**
- "Chcę pojechać w góry na weekend, interesuje mnie historia i dobre jedzenie"
- "Planuję rodzinną wycieczkę do Krakowa na 3 dni"
- "Szukam spokojnego miejsca nad morzem, lubię przyrodę i długie spacery"
- "Chciałbym zwiedzić Wrocław, interesuję się architekturą i życiem nocnym"

1. Upewnij się, że jesteś w katalogu `adk_agents` oraz że wszystkie zmienne środowiskowe są załadowane
2. Uruchom agenta w konsoli **Cloud Shell** i rozpocznij interakcję

   ```bash
    adk run polish_travel_planner/
   ```



### 4.4 System agentowy - Ekspert Prawa Konsumenckiego (`order_compliant_agent`)

Ten hybrydowy system agentowy, działający w oparciu o modele Gemini i Bielik, jest przykładem zastosowania [Agent-as-Tool](https://google.github.io/adk-docs/tools/function-tools/#agent-tool) oraz [Function Tools](https://google.github.io/adk-docs/tools/function-tools/#function-tool) w kontekście prawno-biznesowym. System demonstruje inteligentny routing zapytań i specjalizację agentów w polskim prawie konsumenckim.

System ma na celu pomoc konsumentom w nawigacji przez proces reklamacji i zwrotów zamówień, dostarczając precyzyjnych instrukcji zgodnych z polskim prawem konsumenckim. Główny agent (Gemini) klasyfikuje intencję użytkownika i deleguje zadanie do odpowiedniego eksperta (Bielik).

Architektura systemu:

- `polish_consumer_law_agent` - Główny agent (Gemini) odpowiedzialny za wstępną analizę zapytania użytkownika, klasyfikację intencji (reklamacja vs zwrot vs inne) i delegowanie do odpowiedniego eksperta
- `polish_complaints_law_expert_agent` - Wyspecjalizowany agent (Bielik) będący ekspertem od polskiego prawa reklamacyjnego. Dostarcza szczegółowych instrukcji krok po kroku dla procesu reklamacji uszkodzonych lub wadliwych produktów
- `polish_complaints_law_expert_tool` - Narzędzie AgentTool opakowujące agenta eksperta od reklamacji
- `polish_return_policies_expert_agent` - Wyspecjalizowany agent (Bielik) będący ekspertem od polskich przepisów dotyczących zwrotów. Wyjaśnia prawa konsumenta związane z 14-dniowym terminem odstąpienia od umowy
- `polish_return_policies_expert_tool` - Narzędzie AgentTool opakowujące agenta eksperta od zwrotów
- `no_return_complain_possible_response` - Prosta funkcja Pythona jako Function Tool, która informuje użytkownika, gdy reklamacja lub zwrot nie jest możliwy

```mermaid
graph TD
    subgraph Consumer Law System
        direction TB
        
        A[fa:fa-robot polish_consumer_law_agent<br/>Gemini - Router]
        
        subgraph Tools
            direction TB
            B[fa:fa-wrench polish_complaints_law_expert_tool<br/>AgentTool]
            C[fa:fa-wrench polish_return_policies_expert_tool<br/>AgentTool]
            D[fa:fa-wrench no_return_complain_possible_response<br/>Function Tool]
        end
        
        E[fa:fa-robot polish_complaints_law_expert_agent<br/>Bielik - Reklamacje]
        F[fa:fa-robot polish_return_policies_expert_agent<br/>Bielik - Zwroty]
        
        A --> B
        A --> C
        A --> D
        B --> E
        C --> F
    end
```

**Co demonstruje ten system:**
- ✅ Hybrydowa architektura (Gemini jako router, Bielik jako ekspert domeny)
- ✅ Agent-as-Tool pattern (2 wyspecjalizowane agenty jako narzędzia)
- ✅ Function Tools (prosta funkcja Pythona jako narzędzie)
- ✅ Inteligentny routing zapytań na podstawie intencji użytkownika
- ✅ Specjalizacja agentów (każdy ekspert zna swoją domenę prawa)
- ✅ Lokalna wiedza Bielika (polskie prawo konsumenckie)
- ✅ Praktyczne zastosowanie biznesowe (customer support)

**Przykładowe zapytania do przetestowania:**
- "Otrzymałem uszkodzony produkt. Jak złożyć reklamację?"
- "Chcę zwrócić zamówienie, które nie spełnia moich oczekiwań"
- "Produkt działa, ale nie pasuje. Czy mogę go zwrócić?"
- "W jakim terminie muszę zgłosić reklamację?"

**Scenariusze użycia:**
- E-commerce customer support
- Automatyzacja obsługi reklamacji i zwrotów
- Edukacja konsumentów o ich prawach
- First-line support przed eskalacją do specjalisty

1. Upewnij się, że jesteś w katalogu `adk_agents` oraz że wszystkie zmienne środowiskowe są załadowane
2. Uruchom agenta w konsoli **Cloud Shell** i rozpocznij interakcję

   ```bash
    adk run order_compliant_agent/
   ```



## 5. Przetestuj systemy agentowe w środowisku Cloud Shell + Web

1. Upewnij się, że jesteś w katalogu `adk_agents` oraz że wszystkie zmienne środowiskowe są załadowane
2. Uruchom środowisko ADK Web
    ```bash
    adk web
    ```
3. Zmień port w **Web View** (jeżeli potrzeba, zazwyczaj jest to port 8000)
4. Zaakceptuj zmiany poprzez: *Change and Preview*
5. Z rozwijanego menu po lewej stronie ekranu wybierz system z którym chcesz pracować



## 6. Uruchom systemy agentowe w Cloud Run

1. Upewnij się, że jesteś w katalogu `adk_agents` oraz że wszystkie zmienne środowiskowe są załadowane
    ```bash
    gcloud run deploy adk-agents --source . --region $GOOGLE_CLOUD_LOCATION --allow-unauthenticated --set-env-vars GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION --set-env-vars OLLAMA_API_BASE=$OLLAMA_API_BASE --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY --labels dev-tutorial=codelab-dos-$BIELIK_EVENT_ID
    ```
>[!CAUTION]
>Flaga `--allow-unauthenticated` udostępnia usługę publicznie w internecie i każdy kto zna URL, może zaczać z niej korzystać. W środowisku produkcyjnym zazwyczaj trzeba tę flagę usunąć i odpowiednio skonfigurować reguły dostępu.

>[!TIP]
>Alternatywnie, możesz uruchomić powyższą komendę korzystając ze skryptu `deploy-adk-agents.sh`

   ```bash
   deploy-adk-agents.sh
   ```

2. Narzędzie `gcloud` stworzy kontener na podstawie konfiguracji zawartej w `adk-agents/Dockerfile` i uruchomi usługę w Cloud Run, podając URL pod którym serwis będzie dostępny
3. Wywołaj otrzymany URL w przeglądarce WWW aby mieć dostęp do środowiska ADK Web