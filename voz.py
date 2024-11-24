import speech_recognition as sr
import subprocess
import webbrowser  # Importa el módulo webbrowser

r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Hola, soy tu asistente por voz:")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="es-ES")
            print("Has dicho: {}".format(text))

            # Verificar si el texto incluye "abrir"
            if "abrir" in text.lower():
                print("Abriendo el Bloc de Notas...")
                subprocess.run("notepad.exe")
            
            # Verificar si el texto incluye "beni"
            elif "beni" in text.lower():
                print("Abriendo el enlace de YouTube...")
                webbrowser.open("https://youtu.be/p5M3s3oRY_E?si=INP4BzqpHSjGRXIV")
            
            else:
                print(text)

        except sr.UnknownValueError:
            print("No se te ha entendido")
        except sr.RequestError as e:
            print(f"Error con el servicio de reconocimiento de voz; {e}")
