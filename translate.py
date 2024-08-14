from deep_translator import GoogleTranslator
import langid

# Detect language function
def detect_language(userInput):
    language, _ = langid.classify(userInput)
    print(language)
    return language

# Translate text function based on the desired language
def translate_text(text, language):
    translated = GoogleTranslator(source='auto', target=language).translate(text)
    return translated

# Example usage
#print(translate_text("Hi, Maria, how are you doing?", detect_language("Mi nombre es Maria!")))
