import os
import sys
import google.generativeai as genai

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Errore: La variabile d'ambiente 'GEMINI_API_KEY' non è stata impostata.")
        print("Per favore, imposta la tua chiave API e riprova.")
        return

    genai.configure(api_key=api_key)

    if getattr(sys, 'frozen', False):
        # Siamo in un eseguibile PyInstaller, il percorso base è la directory dell'eseguibile
        base_path = os.path.dirname(sys.executable)
    else:
        # Siamo in un ambiente di sviluppo normale
        base_path = os.path.dirname(os.path.abspath(__file__))

    instructions_path = os.path.join(base_path, "istruzioni.txt")

    try:
        with open(instructions_path, "r", encoding="utf-8") as f:
            system_instruction = f.read()
    except FileNotFoundError:
        print("Errore: Il file 'istruzioni.txt' non è stato trovato.")
        print("Assicurati che il file si trovi nella stessa directory dell'eseguibile.")
        return

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

    print("Assistente: Ciao! Sono il tuo assistente per l'apprendimento. Ti farò delle domande e, insieme, ragioneremo sulle risposte.")
    print("Iniziamo subito!")
    print("Assistente: Scrivi 'esci' o 'exit' per terminare la sessione.")
    
    chat = model.start_chat(history=[])

    while True:
        user_input = input("Tu: ")
        if user_input.lower() in ["esci", "exit"]:
            print("Assistente: Alla prossima! Spero di vederti presto.")
            break

        try:
            response = chat.send_message(user_input, stream=True)
            
            print("Assistente: ", end="")
            for chunk in response:
                print(chunk.text, end="")
            print("\n")

        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            break

if __name__ == "__main__":
    main()