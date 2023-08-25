"""Synthesizes speech from input strings of caller-template-files.
https://cloud.google.com/text-to-speech?utm_source=google&utm_medium=cpc&utm_campaign=emea-de-all-de-dr-bkws-all-all-trial-b-gcp-1011340&utm_content=text-ad-none-any-dev_c-cre_654782172903-adgp_Hybrid%20%7C%20BKWS%20-%20BRO%20%7C%20Txt%20~%20AI%20&%20ML%20~%20Text-to-Speech&hl=de#v1-kwid_43700076017151607-aud-606988878854:kwd-1192006603412-userloc_9043912&utm_term=kw_google%20text%20to%20speech-net_g-plac_&gad=1&gclid=Cj0KCQjwiIOmBhDjARIsAP6YhSXPvIvzrbxc4WLGzZ2KNMeVA0BQmNsmzI9YteXptAlh28F4WJEETn4aAsS7EALw_wcB&gclsrc=aw.ds&hl=de
https://cloud.google.com/text-to-speech/pricing?hl=de
"""
import os
import glob
import shutil
import csv
import codecs
from google.cloud import texttospeech
# unix -> export GOOGLE_APPLICATION_CREDENTIALS=Pfad/zu/Ihrer/Datei/text-to-speech-key.json
# windows -> setx GOOGLE_APPLICATION_CREDENTIALS "Pfad\zu\Ihrer\Datei\text-to-speech-key.json"

TEMPLATE_FILE_EXTENSION = '.csv'
OUTPUT_FILE_EXTENSION = '.mp3'


def confirmation_dialog():
    while True:
        user_input = input("Are you sure you want to proceed? You may face some bill by Google (yes/no): ")
        if user_input.lower() == 'yes':
            return True
        elif user_input.lower() == 'no':
            print("You have chosen not to proceed.")
            return False
        else:
            print("Invalid input. Please respond with 'yes' or 'no'.")
def get_files(pattern):
    return glob.glob(pattern)
def display_menu(options):
    if not options:
        raise ValueError("No options provided.")
     
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    selection = -1
    while not(1 <= selection <= len(options)):
        try:
            selection = int(input("Select an option: "))
            if not(1 <= selection <= len(options)):
                print("Invalid selection, please try again.")
        except ValueError:
            print("Invalid selection, please try again.")

    return options[selection - 1]  # Return selected string from options list

def list_template_files():
    return get_files(f'*-*-v*{TEMPLATE_FILE_EXTENSION}')
def choose_template_file():
    template_files = list_template_files()
    return display_menu(template_files)

def choose_generation_path():
    while True:
        save_path = input("Please enter the generation path: ")
        if os.path.exists(save_path):
            if os.access(save_path, os.W_OK):
                return save_path
            else:
                print("The path exists but is not writable. Please try again.")
        else:
            print("The path does not exist. Please try again.")

def list_google_voice_names(language_code):
    """Lists the available voices."""

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices(language_code=language_code)

    results = []  
    for voice in voices.voices:

        voice_entry = voice.name 

        # Display the supported language codes for this voice. Example: "en-US"
        # for language_code in voice.language_codes:
        #     voice_entry += "-" + language_code
        # # voice.natural_sample_rate_hertz

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        voice_entry += "-" + ssml_gender.name

        results.append(voice_entry)
    return results
def choose_google_voice_name(language_code):
    google_voices = list_google_voice_names(language_code)
    return display_menu(google_voices)

def read_generation_keys(template_file):
    keys = []
    with codecs.open(template_file, 'r', encoding='utf-8-sig') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
            keys.append(row[0])
    return keys
def generate(template_file, generation_path, language_code, language_name):
    generation_path_main = os.path.join(generation_path, google_voice_name)

    # Make sure the directory exists
    os.makedirs(generation_path_main, exist_ok=True)
    if os.access(generation_path_main, os.W_OK) == False:
        raise FileNotFoundError(f"{generation_path_main} is not writeable")

    # add template-file to generation-path
    shutil.copy(template_file, generation_path_main)

    generation_path = os.path.join(generation_path_main, google_voice_name)

    # Make sure the directory exists
    os.makedirs(generation_path, exist_ok=True)
    if os.access(generation_path, os.W_OK) == False:
        raise FileNotFoundError(f"{generation_path} is not writeable")

    keys = read_generation_keys(template_file)

    # Remove gender-suffix
    language_name = language_name.rpartition("-")[0]

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Build the voice request, select the language code ("en-US") and the ssml voice gender ("neutral")
    # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
    voice = texttospeech.VoiceSelectionParams(
        # ex: "en-US"
        language_code=language_code, 
        # ex: "en-AU-Wavenet-D"
        name=language_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        sample_rate_hertz=44100,
        # https://cloud.google.com/text-to-speech/docs/audio-profiles?hl=de
        effects_profile_id=["large-home-entertainment-class-device"],
    )

    print(f"Generating {len(keys)} sounds:")
    for key_index, key in enumerate(keys):

        print(f"{key_index}) {key}")

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=key)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, 
            voice=voice, 
            audio_config=audio_config
        )

        # BL-00001_0_48k_stereo
        file_output = f"GO-{str(key_index).zfill(5)}_{key_index}_mono{OUTPUT_FILE_EXTENSION}"
        output_file_path = os.path.join(generation_path, file_output)

        # The response's audio_content is binary.
        with open(output_file_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)

    # Erstellen Sie die ZIP-Datei
    # Der Name des zu erstellenden Archivs (ohne .zip Erweiterung)
    archive_name = os.path.basename(generation_path)

    # Der Pfad, in dem das Archiv erstellt wird
    archive_dir = os.path.dirname(generation_path)

    # Erstellen Sie die ZIP-Datei
    shutil.make_archive(os.path.join(archive_dir, archive_name), 'zip', archive_dir, archive_name)

    # Löscht den Ursprungsordner
    shutil.rmtree(generation_path)

    return generation_path_main

def restructure_dialog():
    while True:
        user_input = input("Do you want to generate a caller-voice-pack (Default: yes)?:").lower()
        if user_input == 'yes' or user_input == '':
            return True
        elif user_input == 'no':
            return False
        else:
            print("Invalid input. Please respond with 'yes' or 'no'.")
def restructure_generated_files(generation_path):
    archive_name = os.path.basename(generation_path)
    archive_dir = os.path.dirname(generation_path)

    # Liste aller Dateien und Ordner im gegebenen Pfad
    files_and_folders = os.listdir(generation_path)

    # Temporärer Ordner zum Speichern der Dateien und Ordner vor dem Zippen
    temp_dir = os.path.join(archive_dir, "temp")

    # Erstelle den temporären Ordner, wenn er nicht existiert
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Verschieben Sie alle Dateien und Ordner in den temporären Ordner
    for item in files_and_folders:
        shutil.move(os.path.join(generation_path, item), temp_dir)

    # Erstellen Sie das ZIP-Archiv aus dem temporären Ordner
    shutil.make_archive(os.path.join(archive_dir, archive_name), 'zip', temp_dir)

    # Verschieben Sie alle Dateien und Ordner zurück in den ursprünglichen Ordner
    for item in os.listdir(temp_dir):
        shutil.move(os.path.join(temp_dir, item), generation_path)

    # Löschen Sie den temporären Ordner
    shutil.rmtree(temp_dir)
    # Löscht den Ursprungsordner
    shutil.rmtree(generation_path)





if __name__ == "__main__":

    # Ablauf:
    # 1) Mit welchem template möchten Sie arbeiten? -> Vorschau verfügbarer templates
    # 2) Wo sollen die generierten Sounds gespeichert werden?
    # 3) Welche Google-Stimme möchten Sie nutzen? Anzeige gültiger Stimmen für die ausgewählte Sprache (Die Sprache wird aus dem template-namen interpretiert)
    # 4) Bestätigen Sie und starten Sie die Generierung (verursacht Kosten!)
    # 5) Restrukturierung nach benötigtem Format (siehe Github ## CONTRIBUTE)

    template_file = choose_template_file() 
    language_code = template_file.split("-v")[0]
    generation_path = choose_generation_path()
    restructure = restructure_dialog()

    while 1:
        google_voice_name = choose_google_voice_name(language_code)
        confirm = confirmation_dialog()
        if confirm:
            generation_path = generate(template_file, generation_path, language_code, google_voice_name)
            if restructure:
                restructure_generated_files(generation_path)



