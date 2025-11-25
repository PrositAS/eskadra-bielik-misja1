# Eskadra Bielik - Misja 1 - ADK + Cloud Run + Bielik
Przykładowy kod źródłowy pozwalający na:

* Skonfigurowanie własnej instancji modelu [Bielik](https://ollama.com/SpeakLeash/bielik-4.5b-v3.0-instruct) w oparciu o [Ollama](https://ollama.com/)

* Skonfigurowanie prostych systemów agentowych przy wykorzystaniu [Agent Development Kit](https://google.github.io/adk-docs/)

* Uruchomienie obu powyższych serwisów na [Cloud Run](https://cloud.google.com/run?hl=en)

## Architektura rozwiązania

Poniższy diagram przedstawia architekturę rozwiązania, które będziemy budować podczas warsztatów. 

> [!NOTE]
> Warto zaznaczyć, że komponenty takie jak **ADK**, **Ollama** oraz model **Bielik** mogą być z powodzeniem uruchamiane lokalnie na Twoim komputerze (Local Environment). Jednak na potrzeby warsztatu, aby zapewnić wszystkim uczestnikom dostęp do odpowiedniej mocy obliczeniowej (GPU), wykorzystamy środowisko chmurowe **Google Cloud Platform** i usługę **Cloud Run**.

```mermaid
graph TD
    subgraph Local_Environment ["💻 Local Environment (Twój komputer)"]
        style Local_Environment fill:#e6f3ff,stroke:#333,stroke-width:2px
        User[("👤 Użytkownik")]
        Browser["🌐 Przeglądarka WWW"]
        Terminal["⌨️ Terminal"]
    end

    subgraph GCP_Workshop ["☁️ Google Cloud Platform (Warsztat)"]
        style GCP_Workshop fill:#fff0e6,stroke:#333,stroke-width:2px
        
        subgraph Cloud_Run ["🚀 Cloud Run (Serverless)"]
            style Cloud_Run fill:#e6ffe6,stroke:#333,stroke-width:2px
            
            ADK_Service["🤖 ADK Service<br/>(Agent Development Kit)"]
            Ollama_Service["🦙 Ollama Service<br/>(Inference Engine)"]
            
            subgraph GPU_Acceleration ["⚡ GPU Acceleration"]
                style GPU_Acceleration fill:#f9f9f9,stroke:#666,stroke-dasharray: 5 5
                Bielik_Model["🦅 Model Bielik<br/>(LLM)"]
            end
        end
        
        Artifact_Registry["📦 Artifact Registry<br/>(Docker Images)"]
        Gemini_Model["✨ Gemini 2.5 Flash<br/>(Multimodal LLM)"]
    end

    User --> Browser
    User --> Terminal
    
    Browser -- "HTTPS" --> ADK_Service
    Terminal -- "gcloud CLI" --> Cloud_Run
    
    ADK_Service -- "API Call" --> Ollama_Service
    ADK_Service -- "API Call" --> Gemini_Model
    Ollama_Service -- "Load & Run" --> Bielik_Model
    
    Cloud_Run -. "Pull Images" .-> Artifact_Registry

    linkStyle 3 stroke:#0066cc,stroke-width:2px;
    linkStyle 4 stroke:#0066cc,stroke-width:2px;
    linkStyle 5 stroke:#0066cc,stroke-width:2px;
```

## 1. Przygotowanie projektu Google Cloud Platform

### Uzyskaj kredyt Cloud **OnRamp** i skonfiguruj płatności w projekcie Google Cloud Platform

  > [!NOTE]
  > Nie potrzebujesz karty kredytowej ani płatności — otrzymasz 10 dolarów darmowych środków. Zajmie Ci to mniej niż 2 minuty, wystarczy wpisać swoje imię i nazwisko oraz zaakceptować środki.
   
  <details>
  
  <summary>Krok 1: Włącz konto billingowe, dzięki uzyskanym środkom</summary>
      
  1. Załóż konto rozliczeniowe z 10 dolarami kredytu, który będzie potrzebny do wdrożenia. Upewnij się, że masz konto Gmail.
  
  - Kliknij w przycisk: <ins>Zaloguj się jako...</ins>

    ![Krok 1-1](/assets/eskadra-bielik-misja1_01_krok_01.png)

  2 Wybierz konto z domeny @gmail.com i naciśnij przycisk: <ins>Dalej</ins>

   ![Krok 1-2](/assets/eskadra-bielik-misja1_02_krok_01.png)

  3 Po poprawnym zalogowaniu pojawi się Twoje konto z domeny @gmail.com, naciśnij przycisk: <ins>Click here to access your credits</ins>

   ![Krok 1-3](/assets/eskadra-bielik-misja1_03_krok_01.png)

  4 Otworzy się nowa zakładka w przeglądarce

  - Zweryfikuj uzupełnione pola: Imię, Nazwisko
    
  - W polu: _Adres e-mail konta_ pojawi się adres Twojego konta w domenie @gmail.com
    
  - Pole: **Kod kuponu - PROSZĘ NIE EDYTOWAĆ !** 
    
  - Naciśnij przycisk: <ins>Zaakceptuj i kontynuuj</ins>

    ![Krok 1-4](/assets/eskadra-bielik-misja1_04_krok_01.png)

  5 W polu **Konto rozliczeniowe** pojawi się informacja o treści **Google Cloud Platform Trial Billing...** oznacza to, że środki zostały aktywowane na Twoim koncie @gmail.com oraz konto bilingowe zostało poprawnie aktywowane bez konieczności podawania karty kredytowej - masz środki na dalszą część warsztatu.

   ![Krok 1-5](/assets/eskadra-bielik-misja1_05_krok_01.png)

  6 Zmieńmy nazwę na bardziej przyjazną, wybierz pozycję: _Zarządzanie kontem_

   ![Krok 1-6](/assets/eskadra-bielik-misja1_06_krok_01.png)

  7 Kliknij w ikonkę: _Edycji_ ![Ikona Edycji](/assets/eskadra-bielik-misja1_06_krok_01_ikona_edycji.png) pojawi się okno z informacją: _Zmień nazwę konta rozliczeniowego_ w polu *Nazwa* podaj:

  ```bash
  eskadra-bielik-misja1
  ```
  
  - Naciśnij przycisk: <ins>Zmień nazwę</ins>

    ![Krok 1-7](/assets/eskadra-bielik-misja1_07_krok_01.png)

  8 W polu *Konto rozliczeniowe* nowa nazwa została poprawnie zmieniona. 

   ![Krok 1-8](/assets/eskadra-bielik-misja1_08_krok_01.png)

  9 W celu weryfikacji przyznanych środków wybierz pozycje: _Środki_ i zobacz w tabeli przyznane środki kolumnę o tytule **Stan**, która wskazuje na **Dostępny**. 

   ![Krok 1-9](/assets/eskadra-bielik-misja1_09_krok_01.png)

  10 Gratulacje, możesz przejść do następnego kroku warsztatu.

  </details>

  <details>
  
  <summary>Krok 2: Stwórz nowy projekt Google Cloud Platform i powiąż z utworzonym kontem biligowym</summary>

  1 Powróć na główny ekran Google Cloud Platform.
  
  - Kliknij w logo: <ins>Google Cloud</ins>
  
  - Kliknij w pozycję z napisem: <ins>Wybierz projekt</ins>

      ![Krok 2-1](/assets/eskadra-bielik-misja1_01_krok_02.png)

  2 Po wybraniu pojawi się okienko z informacją o projektach

  - Kliknij w przycisk: <ins>Nowy projekt</ins>
  
    ![Krok 2-2](/assets/eskadra-bielik-misja1_02_krok_02.png)

  3 Pojawi się formularz z informacją o nowym projekcie, gdzie nadamy własną nazwę projektu

   ![Krok 2-3](/assets/eskadra-bielik-misja1_03_krok_02.png)

  4 W pozycji: _Nazwa projektu_ podajemy naszą własną nazwę:
  
  ```bash
  eskadra-bielik
  ```

  - Klikamy przycisk: <ins>Utwórz</ins>

    ![Krok 2-4](/assets/eskadra-bielik-misja1_04_krok_02.png)

  5 Pojawi się informacja o utworzeniu projektu

   ![Krok 2-5](/assets/eskadra-bielik-misja1_05_krok_02.png)

  6 W celu weryfikacji czy utworzone konto zostało powiązane z kontem bilinowym, na którym mamy uzyskane środki kredytowe
    
  - Z lewego menu wybierz pozycję: <ins>Płatności</ins>

    ![Krok 2-6](/assets/eskadra-bielik-misja1_06_krok_02.png)

  7 Pojawiła się informacja o Twoich kontach rozliczeniowych
  
  - Kilknij w zakładkę: <ins>Twoje projekty</ins>

    ![Krok 2-7](/assets/eskadra-bielik-misja1_07_krok_02.png)

  8 Jeżeli w pozycji *Konto rozliczeniowe* widzisz nazwę **eskadra-bielik-misja1**, to oznacza, że wszystkie kroki wcześniejsze zostały wykonane poprawnie

   ![Krok 2-8](/assets/eskadra-bielik-misja1_08_krok_02.png)

  9 Powróć na główny ekran Google Cloud Platform.
  
  - Kliknij w logo: <ins>Google Cloud</ins>
  - Kliknij w pozycję z napisem: <ins>Wybierz projekt</ins>

    ![Krok 2-9](/assets/eskadra-bielik-misja1_09_krok_02.png)

  10 Wybierz z listy projekt o nazwie: <ins>eskadra-bielik</ins>

   ![Krok 2-10](/assets/eskadra-bielik-misja1_10_krok_02.png)

  11 Wracamy na główną stronę tym razem mamy już uzupełnione informacje na jakim projekcie pracujemy
  
  - Zobacz w opisie: _Pracujesz w:_ jest informacja, że pracujemy na projkcie: <ins>eskadra-bielik</ins>
  
  - W _Numer projektu_ i _Identyfiaktor projektu_ znajdują się Twoje uniklane dane, gdzie pomoc Google Cloud Platform w tej sposób identyfikuje Twój projekt

    ![Krok 2-11](/assets/eskadra-bielik-misja1_11_krok_02.png)

  12 Gratulacje, możesz przejść do następnego kroku warsztatu.

  </details>

  <details>
  
  <summary>Krok 3: Otwórz terminal Cloud Shell ([dokumentacja](https://cloud.google.com/shell/docs))</summary>

  1 Na górnym pasku Google Cloud Platform.
  
  - Kliknij w ikonkę terminala CLI: ![Ikona terminala CLI](/assets/eskadra-bielik-misja1_01_krok_03_ikona_terminala.png)

      ![Krok 3-1](/assets/eskadra-bielik-misja1_01_krok_03.png)

  2 Po uruchomieniu terminala:
  
  - Kliknij w przycisk: <ins>Autoryzuj</ins>

    ![Krok 3-2](/assets/eskadra-bielik-misja1_02_krok_03.png)

  3 Terminal CLI poprawnie uruchomiony

  ![Krok 3-3](/assets/eskadra-bielik-misja1_03_krok_03.png)

  </details>

  <details>
  
  <summary>Krok 4: Sklonuj repozytorium z przykładowym kodem i przejdź do nowo utworzonego katalogu</summary>

  1 Skopiuj przygotowane komendy do terminala CLI i naciśnij na klawaiturze klawisz ENTER

  ```bash
   git clone https://github.com/Legard777/eskadra-bielik-misja1
   cd eskadra-bielik-misja1
  ```

  - Wynik poprawnie wykonanego kroku (repozytorium cały czas żyje, więc wartości mogą być prezentowane inne):
    ```bash
    ......@cloudshell:~/test (eskadra-bielik-......)$  git clone https://github.com/Legard777/eskadra-bielik-misja1
     cd eskadra-bielik-misja1
    Cloning into 'eskadra-bielik-misja1'...
    remote: Enumerating objects: 337, done.
    remote: Counting objects: 100% (85/85), done.
    remote: Compressing objects: 100% (58/58), done.
    remote: Total 337 (delta 75), reused 27 (delta 27), pack-reused 252 (from 2)
    Receiving objects: 100% (337/337), 7.23 MiB | 28.68 MiB/s, done.
    Resolving deltas: 100% (173/173), done.
    ......@cloudshell:~/test/eskadra-bielik-misja1 (eskadra-bielik-......)$
    ```

  </details>
  
  <details>
  
  <summary>Krok 5: Zmień nazwę pliku `.env.sample` na `.env`</summary>

  1 Skopiuj przygotowane komendy do terminala CLI i naciśnij na klawaiturze klawisz ENTER

   ```bash
   mv .env.sample .env
   ls -la .env
   ```

  - Wynik poprawnie wykonanego kroku:
    ![Krok 5-1](/assets/eskadra-bielik-misja1_01_krok_05.png)
    
  </details>

  <details>
  
  <summary>Krok 6: Skonfiguruj zmienne środowiskowe</summary>

  **W tym kroku uzupełnisz identyfikator warsztatów. Pozostałe parametry są już wstępnie skonfigurowane.**

  1. Otwórz plik `.env` w edytorze Cloud Shell, kopiując w terminalu poniższe polecenie:
     
   ```bash
   cloudshell open-workspace . | cloudshell edit-file .env
   ```

  - Wynik poprawnie wykonanego kroku:
    ![Krok 6-1](/assets/eskadra-bielik-misja1_01_krok_06.png)

  2. W otwartym edytorze znajdź zmienną `BIELIK_EVENT_ID`:

  - Usuń znak **#**, aby zmienna była widoczna

    ![Krok 6-2](/assets/eskadra-bielik-misja1_02_krok_06.png)
  
  - Wpisz swój kod (zgodny z OnRamp Credits) podany przez trenera podczas warsztatów.
    - Zamień tekst **<IDENTYFIKATOR>** na podany przez trenera
    - Przykład prawidłowej zmiany dla fikcyjnego kodu przedstawiony jest poniżej
    
    ![Krok 6-3](/assets/eskadra-bielik-misja1_03_krok_06.png)
    
  - Twój plik powinien wyglądać następująco:
    
    ```bash
    BIELIK_EVENT_ID="<IDENTYFIKATOR>"
    GOOGLE_CLOUD_LOCATION="europe-west1"
    BIELIK_SERVICE_NAME="ollama-bielik-v3"
    BIELIK_MODEL_NAME="SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0"
    ```

  3. Zapisz plik (File > Save lub skrót `Ctrl+S`).
  
  > **Opis zmiennych (informacyjnie):**
  > *   `BIELIK_EVENT_ID` – **(Do edycji)** Unikalny identyfikator warsztatów podany przez trenera podczas warsztatów.
  > *   `GOOGLE_CLOUD_LOCATION` – Region Google Cloud (domyślnie: `europe-west1`, Belgia).
  > *   `BIELIK_SERVICE_NAME` – Nazwa usługi w Cloud Run.
  > *   `BIELIK_MODEL_NAME` – Wersja modelu Bielik (domyślnie: `v3.0-instruct:Q8_0`).

  </details>

  > [!IMPORTANT]
  > **Zmiana wersji modelu**
  > Jeżeli zdecydujesz się zmienić `BIELIK_MODEL_NAME` na inną wersję niż domyślna, pamiętaj, aby zaktualizować tę informację również w pliku `ollama-bielik/Dockerfile`:
  
  ```dockerfile
  ENV MODEL SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0
  ```

  <details>
  
  <summary>Krok 7: Wczytaj zmienne środowiskowe korzystając z podręcznego skryptu</summary>

  1 Kliknij w przycisk z napisem: <ins>Otwórz terminal</ins>, aby powrócić do linii komend

  ![Krok 7-1](/assets/eskadra-bielik-misja1_01_krok_07.png)

  ![Krok 7-2](/assets/eskadra-bielik-misja1_02_krok_07.png)

  2 Skopiuj przygotowane komendy do terminala CLI i naciśnij na klawiaturze klawisz ENTER

   ```bash
   source reload-env.sh
   ```

  - Wynik poprawnie wykonanego kroku:

    ![Krok 7-3](/assets/eskadra-bielik-misja1_03_krok_07.png)

  </details>

## 2. Własna instancja Bielika na Google Cloud Platform

1. Ustal domyślne konto serwisowe dla wybranego projektu `default service account`
   
   ```bash
   gcloud builds get-default-service-account
   ```

2. Poniższa komenda stworzy nową usługę w Cloud Run o nazwie takiej jak wartość zmiennej `$BIELIK_SERVICE_NAME`. Na podstawie definicji w `ollama-bielik/Dockerfile` nardzędzie `gcloud` stworzy odpowiedni kontener, skonfiguruje usługę Ollama oraz wczyta odpowiednią wersję modelu Bielik.

> [!CAUTION]
> Tworzenie modelu może potrwać od 8-10 min.

> [!WARNING]
> Twoja sesja terminala musi być aktywna !

> [!TIP]
> Odpowiedz twierdząco, jeżeli system spyta o włączenie odpowiednich API oraz stworzenie rejestru artefaktów.

- Skopiuj przygotowane komendy do terminala CLI i naciśnij na klawiaturze klawisz ENTER.

   ```bash
   gcloud run deploy $BIELIK_SERVICE_NAME --source ollama-bielik/ --region $GOOGLE_CLOUD_LOCATION --concurrency 7 --cpu 8 --set-env-vars OLLAMA_NUM_PARALLEL=4 --gpu 1 --gpu-type nvidia-l4 --max-instances 1 --memory 16Gi --allow-unauthenticated --no-cpu-throttling --no-gpu-zonal-redundancy --timeout 600 --labels dev-tutorial=codelab-dos-$BIELIK_EVENT_ID
   ```

- Na zadane pytanie, odpowiedz **Y**.
  ```bash
  The following APIs are not enabled on project [eskadra-bielik-.....]:
        artifactregistry.googleapis.com
        cloudbuild.googleapis.com
        run.googleapis.com

  Do you want enable these APIs to continue (this will take a few minutes)? (Y/n)?  
  ```

- Na kolejne zadane pytanie, odpowiedz **Y**.
  ```bash
  Enabling APIs on project [eskadra-bielik-.....]...
  Operation "operations/............." finished successfully.
  Deploying from source requires an Artifact Registry Docker repository to store built containers. A repository named [cloud-run-source-deploy] in region
   [europe-west1] will be created.
  
  Do you want to continue (Y/n)? 
  ```

- Poprawne wykonanie zakończy się poniższym komunikatem:

  ```bash
  Building using Dockerfile and deploying container to Cloud Run service [ollama-bielik-v3] in project [eskadra-bielik-.....] region [europe-west1]
  Building and deploying new service...                                                                                                                 
    Validating Service...done                                                                                                                           
    Uploading sources...done                                                                                                                            
    Building Container... Logs are available at [https://console.cloud.google.com/cloud-build/builds;region=europe-west1/3....]....done                                                                                                                 
    Setting IAM Policy...done                                                                                                                           
    Creating Revision...done                                                                                                                            
    Routing traffic...done                                                                                                                              
  Done.                                                                                                                                                 
  Service [ollama-bielik-v3] revision [ollama-bielik-v3-.....] has been deployed and is serving 100 percent of traffic.
  Service URL: https://ollama-bielik-v3-......europe-west1.run.app
  ```

- Jeżeli pojawił się błąd z poniższą informacją:
  
  ```bash
  Building using Dockerfile and deploying container to Cloud Run service [ollama-bielik-v3] in project [eskadra-bielik-.....] region [europe-west1] ERROR: (gcloud.run.deploy) spec.template.metadata.annotations[autoscaling.knative.dev/maxScale]: You do not have quota for using GPUs without zonal redundancy. Learn more about GPU zonal redundancy: g.co/cloudrun/gpu-redundancy-help

  To request quota: g.co/cloudrun/gpu-quota
  ```

>[!TIP]
>Uruchom poniższą komendę bez GPU (będzie wolniej)...
  ```bash
  gcloud run deploy $BIELIK_SERVICE_NAME --source ollama-bielik/ --region $GOOGLE_CLOUD_LOCATION --concurrency 7 --cpu 8 --set-env-vars OLLAMA_NUM_PARALLEL=4 --max-instances 1 --memory 16Gi --allow-unauthenticated --no-cpu-throttling --timeout 600 --labels dev-tutorial=xyz-$BIELIK_EVENT_ID
  ```

>[!CAUTION]
>Flaga `--allow-unauthenticated` udostępnia usługę publicznie w internecie i każdy kto zna URL, może zaczać z niej korzystać. W środowisku produkcyjnym zazwyczaj trzeba tę flagę usunąć i odpowiednio skonfigurować reguły dostępu.

3. Uruchom poniższą komendę, aby sprawdzić pod jakim URL jest dostępny Bielik

   ```bash
   gcloud run services describe $BIELIK_SERVICE_NAME --region=$GOOGLE_CLOUD_LOCATION --format='value(status.url)'
   ```

- Skopiuj uzyskany adres do "schowka"

- Wykonaj te same czynności co w **Kroku 6**
  - Możesz też kliknąć bezpośrednio w przycisk: <ins>Otwórz edytor</ins>
  - Odnajdź pozycję **# OLLAMA_API_BASE=** (linia nr 27)
  - Usuń znak **#**
  - Po znaku **=** wklej skopiowany adres usługi Cloud Run ollama-bielik-v3....

4. Przypisz powyższy URL do zmiennej środowiskowej `OLLAMA_API_BASE` w pliku `.env` i następnie wczytaj zmienne środowiskowe ponownie:
   ```bash
   source reload-env.sh
   ```

> [!TIP]
> Czy to faktycznie działa?

### Jak sprawdzić, czy nasz Bielik jest gotowy?

* Sprawdź w Google Cloud console czy nowy serwis jest już dostępny
* Sprawdź czy otwierając URL w przeglądarce zobaczysz informację: `Ollama is running`
* Sprawdź przez API jakie modele są dostępne lokalnie na serwerze Ollama
   ```bash
   curl "${OLLAMA_API_BASE}/api/tags" | jq .
   ```
   - odpowiedź powinna wyglądać jak poniżej:
    ```json
    {
      "models": [
        {
          "name": "SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0",
          "model": "SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0",
          "modified_at": ".........",
          "size": 5061216212,
          "digest": "..............",
          "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "llama",
            "families": [
              "llama"
            ],
            "parameter_size": "4.8B",
            "quantization_level": "Q8_0"
          }
        }
      ]
    }
    ```
   - Jak to rozumieć...:
    #### 🦅 SpeakLeash / Bielik 4.5B v3.0 Instruct
  
    > **Wersja:** `Q8_0` (High Quality) &nbsp;|&nbsp; **Rodzina:** `Llama` &nbsp;|&nbsp; **Parametry:** `4.8B`
    
    *   📦 **Format:** `GGUF`
    *   💾 **Rozmiar:** 4.71 GB
    *   📅 **Data:** .....
    
    **Digest:**
    `........`

* Wyślij zapytanie przez API

   ```bash
   curl "${OLLAMA_API_BASE}/api/generate" -d "{
      \"model\": \"$BIELIK_MODEL_NAME\",
      \"prompt\": \"Kto zabił smoka wawelskiego?\",
      \"stream\": false
   }" | jq .response
   ```

   - Uruchom 2-3 razy i zobacz jaką uzyskasz odpowiedź

   - Poniżej przykładowa odpowiedź (Ty możesz mieć inną...):

    ```json
    {
      "model": "SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0",
      "created_at": "......",
      "response": "Smok wawelski został zabity przez szewca Skubę, który podrzucił mu barana wypchanego siarką i prochem. Gdy smok połknął baranka, wybuchł i zabił potwora.",
      "done": true,
      "done_reason": "stop",
      "context": [
        1, 31981, 31957, 11308, 102, 25726, 336, 102, 2910, 31957, 31977, 6583,
        31894, 31981, 31957, 6788, 102, 25726, 336, 102, 2910, 31957, 31977, 20,
        17, 20, 17, 31037, 17218, 6871, 298, 787, 18058, 632, 31956, 31981,
        31957, 27399, 31897, 102, 2910, 31957, 31977, 31981, 31957, 11308, 102,
        25726, 336, 102, 2910, 31957, 31977, 14550, 23924, 507, 31981, 31957,
        6788, 102, 25726, 336, 102, 2910, 31957, 31977, 20, 17, 20, 17, 31926,
        434, 31900, 787, 18058, 423, 1109, 3332, 339, 481, 937, 16243, 10170,
        1279, 31909, 493, 392, 13198, 555, 17494, 268, 3585, 6193, 365, 27062,
        704, 285, 884, 23257, 31917, 1645, 6871, 31900, 3174, 3479, 17494,
        2652, 31909, 6320, 31907, 285, 17218, 19153, 31888, 31917
      ],
      "total_duration": 10994891361,
      "load_duration": 64652723,
      "prompt_eval_count": 71,
      "prompt_eval_duration": 231194690,
      "eval_count": 54,
      "eval_duration": 10674966594
    }
    ```

  - Wyjaśnienie...

    **Model:** `SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0`
    **Status:** ✅ Zakończono pomyślnie (Reason: `stop`)
    
    ### 📝 Odpowiedź modelu:
    > Smok wawelski został zabity przez szewca Skubę, który podrzucił mu barana wypchanego siarką i prochem. Gdy smok połknął baranka, wybuchł i zabił potwora.
    
    ### ⚡ Statystyki wydajności
    
    Poniższa tabela przedstawia szczegółowe czasy i prędkość generowania odpowiedzi (przeliczone z nanosekund).
    
    | Metryka | Wartość | Opis |
    | :--- | :--- | :--- |
    | **Całkowity czas** | **10.99 s** | Czas od zapytania do końca odpowiedzi. |
    | **Czas ładowania** | 0.06 s | Czas wczytania modelu do pamięci. |
    | **Przetwarzanie promptu** | 0.23 s | Czas "zrozumienia" Twojego pytania. |
    | **Generowanie odp.** | 10.67 s | Czas pisania odpowiedzi przez AI. |
    | **Liczba tokenów (we)** | 71 | Długość Twojego zapytania (prompt). |
    | **Liczba tokenów (wy)** | 54 | Długość odpowiedzi modelu. |
    | **Prędkość (TPS)** | **~5.06 t/s** | Średnia prędkość generowania (tokens per second). |
    
## 3. Konfiguracja systemów agentowych ADK

1. Skonfiguruj swój własny klucz Gemini API

   * Stwórz lub skopiuj istniejący Gemini API key z [Google AI Studio](https://ai.dev).
     
     1 Wybierz pozycję: <ins>Get API Key</ins>

     2 Wybierz pozycję: <ins>Project</ins>

     3 Kliknij w przycisk: <ins>+ Create a new project</ins>

     4 Podaj nazwę swojego projektu w pozycji: *Name your project*:
     
       ```bash
       eskadra-bielik-misja1
       ```

     5 Kliknij w przycisk: <ins>Create project</ins>

     6 Kliknij w kolumnie *Keys* przy nazwie <ins>eskadra-bielik-misja1</ins>
     
     7 Kliknij w przycisk: <ins>Create API key</ins>

     8 Wybierz w pozycji: <ins>Choose an imported project</ins> utworzony projekt o nazwie *eskadra-bielik-misja1*

     9 Podaj w pozycji: <ins>Name you key</ins> nazwę swojego klucza *eskadra-bielik-misja1-klucz-1*

     10 Kliknij w przycisk: <ins>Create key</ins>, aby utworzyć klucz

     11 Kliknij w nowo utworzony klucz. Pojawi się okienko z informacją o nowym kluczu: <ins>API key details</ins>
     
     12 Kliknij w przycisk: <ins>Copy key</ins>, aby skopiować klucz do schowka

   * Dodaj wartość klucza ze swojego Gemini API key jako wartość zmiennej `GOOGLE_API_KEY` w pliku `.env`
   ```bash
   GOOGLE_API_KEY=TWÓJ_KLUCZ
   ```
3. Wczytaj zmienne środowiskowe ponownie
   ```bash
   source reload-env.sh
   ```
4. Przejdź do katalogu z agentami

   ```bash
   cd adk-agents
   ```
   
5. Stwórz i aktywuj wirtualne środowisko Python

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   
6. Zainstaluj wymagane komponenty

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