#!/usr/bin/python3
import argparse
import os

from pygments import highlight, token
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.formatters import NullFormatter, Terminal256Formatter
from pygments.filter import simplefilter
from pygments.token import string_to_tokentype

from googleapiclient.discovery import build as googleapi_build

import regex as re

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

@simplefilter
def translate_filter(self, lexer, stream, options):
    def filter_ttype(ttype, value):
        while ttype:
            if ttype in options['tokens']:
                return True
            else:
                ttype = ttype.parent

    def filter_chars(ttype, value):
        return bool(options['regex'].search(value))


    all_tokens = [
        [ttype, value]
        for ttype, value in stream
    ]
    filtered_tokens = [
        token
        for token in all_tokens
        if filter_ttype(*token) and filter_chars(*token)
    ]

    googleapi = googleapi_build('translate', 'v2', developerKey=options['google_api_key'])

    translations = []
    for chunk in chunks(filtered_tokens, 100):
        translations += googleapi.translations().list(
            format='text',
            source=options['src'],
            target=options['dest'],
            q=[token[1] for token in chunk]
        ).execute()['translations']
    for x, translation in zip(filtered_tokens, translations):
        translation
        x[1] = translation['translatedText']



    return all_tokens


def main():
    parser = argparse.ArgumentParser(description='Source code translation')
    parser.add_argument('files', metavar='FILE', type=argparse.FileType('r+b', 0), nargs='+', help='Files to translate')

    parser.add_argument('--src', metavar='SRC', type=str, default=None, help='Source Language')
    parser.add_argument('--dest', metavar='DEST', type=str, default='en', help='Dest Language')
    parser.add_argument('--syntax', metavar='LANG', type=get_lexer_by_name, help='Syntax used to parse the file')
    parser.add_argument('--replace', action='store_true', help='Replace original file contents')

    parser.add_argument('--tokens', metavar='TOKEN_TYPE', type=lambda x: [string_to_tokentype(t) for t in x.split(',')], default=[token.String, token.Comment], help='Comma-separated list of token types to translate. e.g., "String,Comment"')

    parser.add_argument('--regex', metavar='REGEX', type=lambda x: re.compile(x, re.UNICODE), default=re.compile('.'), help='Only translate tokens that match the regex specified. e.g. "\\p{IsHan}"')

    parser.add_argument('--google-api-key', default=os.environ.get('GOOGLE_API_KEY', 'NOKEY'), help='Google Translator API key.')

    args = parser.parse_args()

    for file in args.files:
        print(file.name, '...', sep='')
        code = file.read()
        lexer = args.syntax or guess_lexer_for_filename(file.name, code)
        lexer.filters = [ translate_filter(**vars(args)) ]
        output = highlight(code, lexer, NullFormatter() if args.replace else Terminal256Formatter())
        if args.replace:
            file.seek(0)
            file.write(output.encode('utf-8'))
            file.truncate()
        else:
            print(output)
            print()

if __name__ == "__main__":
    main()
