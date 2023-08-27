"""Synthesizes speech from input strings of template-files with multiple cloud providers.
"""
import os
import platform
import glob
import shutil
import csv
import codecs

# GOOGLE
# install: google-cloud-texttospeech
from google.cloud import texttospeech

# AMAZON
# install: boto3 
from boto3 import Session
from contextlib import closing





SERVICE_PROVIDERS = ['google', 'amazon']
TEMPLATE_FILE_EXTENSION = '.csv'
OUTPUT_FILE_EXTENSION = '.mp3'



def setup_environment():
    service = display_menu("Select a provider: ", SERVICE_PROVIDERS)
    if service == 'amazon':
        setup_environment_amazon()
    elif service == 'google':
        setup_environment_google()
    return service
def setup_environment_amazon():
    user_home = os.environ.get('USERPROFILE') or os.environ.get('HOME')
    credential_path = os.path.join(user_home, '.aws', 'credentials')
    config_path = os.path.join(user_home, '.aws', 'config')

    if not os.path.isfile(credential_path) or not os.access(credential_path, os.R_OK):
        raise ValueError(f"The file {credential_path} does not exist or is not readable.")
    if not os.path.isfile(config_path) or not os.access(config_path, os.R_OK):
        raise ValueError(f"The file {config_path} does not exist or is not readable.")
def setup_environment_google():
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        path_to_credential_file = None
        while path_to_credential_file is None:
            path = input("Please enter full path to 'text-to-speech-key.json' / credential-file: ")
            if os.path.isfile(path):
                if os.access(path, os.R_OK):
                    path_to_credential_file = path
                else:
                    raise ValueError("The file exists but is not readable. Please try again.")
            else:
                raise ValueError("The file does not exist. Please try again.")

        # unix -> export GOOGLE_APPLICATION_CREDENTIALS=Pfad/zu/Ihrer/Datei/text-to-speech-key.json
        # windows -> setx GOOGLE_APPLICATION_CREDENTIALS "Pfad\zu\Ihrer\Datei\text-to-speech-key.json"
        if platform.system() == "Windows":
            os.system(f'setx GOOGLE_APPLICATION_CREDENTIALS "{path_to_credential_file}"')
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_credential_file
        else:
            os.system(f'export GOOGLE_APPLICATION_CREDENTIALS={path_to_credential_file}')
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_credential_file


def binary_dialog(question, default = 'no'):
    while True:
        user_input = input(question).lower()
        if user_input == '':
            user_input = default

        if user_input == 'yes' or user_input == '':
            return True
        elif user_input == 'no':
            return False
        else:
            print("Invalid input. Please respond with 'yes' or 'no'.")
def get_files(pattern):
    return glob.glob(pattern)
def display_menu(text, options):
    if not options:
        raise ValueError("No options provided.")
     
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    selection = -1
    while not(1 <= selection <= len(options)):
        try:
            selection = int(input(text))
            if not(1 <= selection <= len(options)):
                print("Invalid selection, please try again.")
        except ValueError:
            print("Invalid selection, please try again.")

    return options[selection - 1]

def list_template_files():
    return get_files(f'*-*-v*{TEMPLATE_FILE_EXTENSION}')
def choose_template_file():
    template_files = list_template_files()
    return display_menu("Select a template file to use: ", template_files)

def choose_generation_path():
    while True:
        save_path = input("Please enter a generation path: ")
        if os.path.exists(save_path):
            if os.access(save_path, os.W_OK):
                return save_path
            else:
                print("The path exists but is not writable. Please try again.")
        else:
            print("The path does not exist. Please try again.")

def list_voice_names(provider, language_code):
    if provider == 'amazon':
        return list_amazon_voice_names(language_code)
    elif provider == 'google':
        return list_google_voice_names(language_code)
def list_amazon_voice_names(language_code):   
    # Create a client using the credentials and region defined in the [autodarts-caller] section of the AWS credentials file (~/.aws/credentials).
    # profile_name="autodarts-caller"
    session = Session()
    client = session.client("polly")

    voices = client.describe_voices(
            # 'en-GB'
            LanguageCode=language_code,
            Engine='neural'
        )
    # print(voices)
    
    results = []  
    for voice in voices['Voices']:
        voice_entry = voice['Name'] + "-" + voice['Gender']
        results.append(voice_entry)
    return results
def list_google_voice_names(language_code):
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
def choose_voice_name(provider, voices):
    return display_menu(f"Select a {provider}-voice to use: ", voices)

def read_generation_keys(template_file):
    keys = []
    with codecs.open(template_file, 'r', encoding='utf-8-sig') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
            keys.append(row[0])
    return keys
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
def generate(provider, template_file, generation_path, language_code, voice_name, raw_mode):
    voice_name_path = voice_name
    if not voice_name.lower().startswith(language_code.lower()):
        voice_name_path = language_code + '-' + voice_name

    generation_path_main = os.path.join(generation_path, voice_name_path)

    # Make sure the directory exists
    os.makedirs(generation_path_main, exist_ok=True)
    if os.access(generation_path_main, os.W_OK) == False:
        raise FileNotFoundError(f"{generation_path_main} is not writeable")

    generation_path = generation_path_main
    if not raw_mode:
        # add template-file to generation-path
        shutil.copy(template_file, generation_path_main)

        generation_path = os.path.join(generation_path_main, voice_name_path)
        os.makedirs(generation_path, exist_ok=True)
        if os.access(generation_path, os.W_OK) == False:
            raise FileNotFoundError(f"{generation_path} is not writeable")


    keys = read_generation_keys(template_file)

    # Remove gender-suffix
    voice_name = voice_name.rpartition("-")[0]

    errors = 0
    if provider == 'amazon':
        errors = generate_amazon(keys, generation_path, language_code, voice_name, raw_mode)
    elif provider == 'google':
        errors = generate_google(keys, generation_path, language_code, voice_name, raw_mode)

    print(f"Generation finished with {errors} errors")

    if not raw_mode:
        # Erstellen Sie die ZIP-Datei
        # Der Name des zu erstellenden Archivs (ohne .zip Erweiterung)
        archive_name = os.path.basename(generation_path)

        # Der Pfad, in dem das Archiv erstellt wird
        archive_dir = os.path.dirname(generation_path)

        # Erstellen Sie die ZIP-Datei
        shutil.make_archive(os.path.join(archive_dir, archive_name), 'zip', archive_dir, archive_name)

        # Löscht den Ursprungsordner
        shutil.rmtree(generation_path)

        restructure_generated_files(generation_path_main)
def generate_amazon(keys, generation_path, language_code, language_name, raw_mode):
    # Create a client using the credentials and region defined in the [default] section of the AWS credentials file (~/.aws/credentials).
    # profile_name="autodart-caller"
    session = Session()
    client = session.client("polly")

    errors = 0
    print(f"Generating {len(keys)} sounds:")
    for key_index, key in enumerate(keys):
        print(f"{key_index}) {key}")

        try:
            response = client.synthesize_speech(
                Text=key, 
                OutputFormat="mp3", 
                VoiceId=language_name,
                Engine='neural',
                SampleRate='24000'
                )

            # Access the audio stream from the response
            if "AudioStream" in response:
                    # Note: Closing the stream is important because the service throttles on the
                    # number of parallel connections. Here we are using contextlib.closing to
                    # ensure the close method of the stream object will be called automatically
                    # at the end of the with statement's scope.
                    with closing(response["AudioStream"]) as stream:
                        file_output = f"{key}{OUTPUT_FILE_EXTENSION}"
                        if not raw_mode:
                            # BL-00001_0_48k_stereo.mp3
                            file_output = f"AM-{str(key_index).zfill(5)}_{key_index}_mono{OUTPUT_FILE_EXTENSION}"

                        output_file_path = os.path.join(generation_path, file_output)

                        with open(output_file_path, "wb") as file:
                            file.write(stream.read())    
        except Exception as e:
            errors += 1
            print(str(e))
    return errors   
def generate_google(keys, generation_path, language_code, language_name, raw_mode):
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

    errors = 0
    print(f"Generating {len(keys)} sounds:")
    for key_index, key in enumerate(keys):
        print(f"{key_index}) {key}")

        try:
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=key)

            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = client.synthesize_speech(
                input=synthesis_input, 
                voice=voice, 
                audio_config=audio_config
            )

            file_output = f"{key}{OUTPUT_FILE_EXTENSION}"
            if not raw_mode:
                # BL-00001_0_48k_stereo.mp3
                file_output = f"GO-{str(key_index).zfill(5)}_{key_index}_mono{OUTPUT_FILE_EXTENSION}"

            output_file_path = os.path.join(generation_path, file_output)

            # The response's audio_content is binary.
            with open(output_file_path, "wb") as out:
                # Write the response to the output file.
                out.write(response.audio_content)
        except Exception as e:
            errors += 1
            print(str(e))
    return errors






if __name__ == "__main__":

    # Ablauf:
    # 0) Welchen Cloud-provider möchten Sie benutzen?
    # 1) Mit welchem template möchten Sie arbeiten? -> Vorschau verfügbarer templates
    # 2) Wo sollen die generierten Sounds gespeichert werden?
    # 3) Soll im 'raw'-Modus generiert werden? (Sollen die Sounds für den Caller strukturiert werden?)
    # 4) Welche Stimme möchten Sie nutzen? Anzeige gültiger Stimmen für die ausgewählte Sprache (Die Sprache wird aus dem template-namen interpretiert)
    # 5) Bestätigen Sie und starten Sie die Generierung
    # 6) Wiederholung ab 4)

    # 0)
    provider = setup_environment()

    # 1)
    template_file = choose_template_file() 
    language_code = template_file.split("-v")[0]   

    # 2)
    generation_path = choose_generation_path()

    # 3) 
    raw_mode = binary_dialog("Do you want to generate in raw mode (Default: no)?: ")

    # 4) 
    voices = list_voice_names(provider, language_code)

    # 6)
    while 1:
        voice_name = choose_voice_name(provider, voices)

        # 5)
        confirm = binary_dialog("Are you sure you want to proceed (yes/no)? You may face some bill by provider (Default: no): ")
        if confirm:
            generate(provider, template_file, generation_path, language_code, voice_name, raw_mode)

                



