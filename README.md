# code_translate
Use a little help from Google Translator to make code from Chinese and Russian guys readable

This script uses [Pygments](http://pygments.org/) as a Lexer for source code, selects only the tokens types you want to translate (e.g., comments), send those to [Google's Cloud Translation API](https://cloud.google.com/translate/) and replace it back on the original file

# API key
You'll need to generate your own Key to Google's Cloud Translation API. See the [quickstart](https://cloud.google.com/translate/docs/getting-started).

# Usage
```
usage: code_translate.py [-h] [--src SRC] [--dest DEST] [--syntax LANG]
                         [--replace] [--tokens TOKEN_TYPE] [--regex REGEX]
                         [--google-api-key GOOGLE_API_KEY]
                         FILE [FILE ...]

Source code translation

positional arguments:
  FILE                  Files to translate

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             Source Language
  --dest DEST           Dest Language
  --syntax LANG         Syntax used to parse the file
  --replace             Replace original file contents
  --tokens TOKEN_TYPE   Comma-separated list of token types to translate.
                        e.g., "String,Comment"
  --regex REGEX         Only translate tokens that match the regex specified.
                        e.g. "\p{IsHan}"
  --google-api-key GOOGLE_API_KEY
                        Google Translator API key.
```

# Example

```
code_translate.py --google-api-key=xxx --replace --src=zh --dest=en --syntax=java --regex="\\p{IsHan}" ChineseCode.java
```
