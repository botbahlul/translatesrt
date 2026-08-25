from __future__ import absolute_import, print_function, unicode_literals

import argparse
import multiprocessing
import os
import sys
import json
import requests
import httpx

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from progressbar import ProgressBar, Percentage, Bar, ETA
import pysrt
import six

from datetime import datetime, timedelta
import time
from glob import glob, escape
from pathlib import Path

VERSION = "0.0.5"

class Language:
    def __init__(self):
        self.list_codes = [
            "af", "sq", "am", "ar", "hy", "as", "ay", "az", "bm", "eu",
            "be", "bn", "bho", "bs", "bg", "ca", "ceb", "ny", "zh", "zh-CN",
            "zh-TW", "co", "hr", "cs", "da", "dv", "doi", "nl", "en",
            "eo", "et", "ee", "fil", "fi", "fr", "fy", "gl", "ka", "de",
            "el", "gn", "gu", "ht", "ha", "haw", "he", "hi", "hmn", "hu",
            "is", "ig", "ilo", "id", "ga", "it", "ja", "jv", "kn", "kk",
            "km", "rw", "gom", "ko", "kri", "kmr", "ckb", "ky", "lo", "la",
            "lv", "ln", "lt", "lg", "lb", "mk", "mg", "ms", "ml", "mt",
            "mi", "mr", "mni-Mtei", "lus", "mn", "my", "ne", "no", "or",
            "om", "ps", "fa", "pl", "pt", "pa", "qu", "ro", "ru", "sm",
            "sa", "gd", "nso", "sr", "st", "sn", "sd", "si", "sk", "sl",
            "so", "es", "su", "sw", "sv", "tg", "ta", "tt", "te", "th",
            "ti", "ts", "tr", "tk", "tw", "uk", "ur", "ug", "uz", "vi",
            "cy", "xh", "yi", "yo", "zu"
        ]

        self.list_names = [
            "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian",
            "Assamese", "Aymara", "Azerbaijani", "Bambara", "Basque",
            "Belarusian", "Bengali", "Bhojpuri", "Bosnian", "Bulgarian",
            "Catalan", "Cebuano", "Chichewa", "Chinese",
            "Chinese (Simplified)", "Chinese (Traditional)", "Corsican",
            "Croatian", "Czech", "Danish", "Dhivehi", "Dogri", "Dutch",
            "English", "Esperanto", "Estonian", "Ewe", "Filipino", "Finnish",
            "French", "Frisian", "Galician", "Georgian", "German", "Greek",
            "Guarani", "Gujarati", "Haitian Creole", "Hausa", "Hawaiian",
            "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo",
            "Ilocano", "Indonesian", "Irish", "Italian", "Japanese",
            "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda",
            "Konkani", "Korean", "Krio", "Kurdish (Kurmanji)",
            "Kurdish (Sorani)", "Kyrgyz", "Lao", "Latin", "Latvian",
            "Lingala", "Lithuanian", "Luganda", "Luxembourgish", "Macedonian",
            "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi",
            "Meiteilon (Manipuri)", "Mizo", "Mongolian", "Myanmar (Burmese)",
            "Nepali", "Norwegian", "Odiya (Oriya)", "Oromo", "Pashto",
            "Persian", "Polish", "Portuguese", "Punjabi", "Quechua",
            "Romanian", "Russian", "Samoan", "Sanskrit", "Scots Gaelic",
            "Sepedi", "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala",
            "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese",
            "Swahili", "Swedish", "Tajik", "Tamil", "Tatar", "Telugu",
            "Thai", "Tigrinya", "Tsonga", "Turkish", "Turkmen", "Twi (Akan)",
            "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh",
            "Xhosa", "Yiddish", "Yoruba", "Zulu"
        ]

        self.list_ffmpeg_codes = [
            "afr", "alb", "amh", "ara", "hye", "asm", "aym", "aze", "bam",
            "eus", "bel", "ben", "bho", "bos", "bul", "cat", "ceb", "nya",
            "zho", "zho-CN", "zho-TW", "cos", "hrv", "ces", "dan", "div",
            "doi", "nld", "eng", "epo", "est", "ewe", "fil", "fin", "fra",
            "fry", "glg", "kat", "deu", "ell", "grn", "guj", "hat", "hau",
            "haw", "heb", "hin", "hmn", "hun", "isl", "ibo", "ilo", "ind",
            "gle", "ita", "jpn", "jav", "kan", "kaz", "khm", "kin", "kok",
            "kor", "kri", "kmr", "ckb", "kir", "lao", "lat", "lav", "lin",
            "lit", "lug", "ltz", "mkd", "mlg", "msa", "mal", "mlt", "mri",
            "mar", "mni-Mtei", "lus", "mon", "mya", "nep", "nor", "ori",
            "orm", "pus", "fas", "pol", "por", "pan", "que", "ron", "rus",
            "smo", "san", "gla", "nso", "srp", "sot", "sna", "snd", "sin",
            "slk", "slv", "som", "spa", "sun", "swa", "swe", "tgk", "tam",
            "tat", "tel", "tha", "tir", "tso", "tur", "tuk", "twi", "ukr",
            "urd", "uig", "uzb", "vie", "wel", "xho", "yid", "yor", "zul"
        ]

        self.code_of_name = dict(zip(self.list_names, self.list_codes))
        self.code_of_ffmpeg_code = dict(
            zip(self.list_ffmpeg_codes, self.list_codes)
        )

        self.name_of_code = dict(zip(self.list_codes, self.list_names))
        self.name_of_ffmpeg_code = dict(
            zip(self.list_ffmpeg_codes, self.list_names)
        )

        self.ffmpeg_code_of_name = dict(
            zip(self.list_names, self.list_ffmpeg_codes)
        )
        self.ffmpeg_code_of_code = dict(
            zip(self.list_codes, self.list_ffmpeg_codes)
        )

        self.dict = dict(zip(self.list_codes, self.list_names))

        self.ffmpeg_dict = {
            'af': 'afr',
            'sq': 'alb',
            'am': 'amh',
            'ar': 'ara',
            'hy': 'arm',
            'as': 'asm',
            'ay': 'aym',
            'az': 'aze',
            'bm': 'bam',
            'eu': 'baq',
            'be': 'bel',
            'bn': 'ben',
            'bho': 'bho',
            'bs': 'bos',
            'bg': 'bul',
            'ca': 'cat',
            'ceb': 'ceb',
            'ny': 'nya',
            'zh': 'chi',
            'zh-CN': 'chi',
            'zh-TW': 'chi',
            'co': 'cos',
            'hr': 'hrv',
            'cs': 'cze',
            'da': 'dan',
            'dv': 'div',
            'doi': 'doi',
            'nl': 'dut',
            'en': 'eng',
            'eo': 'epo',
            'et': 'est',
            'ee': 'ewe',
            'fil': 'fil',
            'fi': 'fin',
            'fr': 'fre',
            'fy': 'fry',
            'gl': 'glg',
            'ka': 'geo',
            'de': 'ger',
            'el': 'gre',
            'gn': 'grn',
            'gu': 'guj',
            'ht': 'hat',
            'ha': 'hau',
            'haw': 'haw',
            'he': 'heb',
            'hi': 'hin',
            'hmn': 'hmn',
            'hu': 'hun',
            'is': 'ice',
            'ig': 'ibo',
            'ilo': 'ilo',
            'id': 'ind',
            'ga': 'gle',
            'it': 'ita',
            'ja': 'jpn',
            'jv': 'jav',
            'kn': 'kan',
            'kk': 'kaz',
            'km': 'khm',
            'rw': 'kin',
            'gom': 'kok',
            'ko': 'kor',
            'kri': 'kri',
            'kmr': 'kur',
            'ckb': 'kur',
            'ky': 'kir',
            'lo': 'lao',
            'la': 'lat',
            'lv': 'lav',
            'ln': 'lin',
            'lt': 'lit',
            'lg': 'lug',
            'lb': 'ltz',
            'mk': 'mac',
            'mg': 'mlg',
            'ms': 'may',
            'ml': 'mal',
            'mt': 'mlt',
            'mi': 'mao',
            'mr': 'mar',
            'mni-Mtei': 'mni',
            'lus': 'lus',
            'mn': 'mon',
            'my': 'bur',
            'ne': 'nep',
            'no': 'nor',
            'or': 'ori',
            'om': 'orm',
            'ps': 'pus',
            'fa': 'per',
            'pl': 'pol',
            'pt': 'por',
            'pa': 'pan',
            'qu': 'que',
            'ro': 'rum',
            'ru': 'rus',
            'sm': 'smo',
            'sa': 'san',
            'gd': 'gla',
            'nso': 'nso',
            'sr': 'srp',
            'st': 'sot',
            'sn': 'sna',
            'sd': 'snd',
            'si': 'sin',
            'sk': 'slo',
            'sl': 'slv',
            'so': 'som',
            'es': 'spa',
            'su': 'sun',
            'sw': 'swa',
            'sv': 'swe',
            'tg': 'tgk',
            'ta': 'tam',
            'tt': 'tat',
            'te': 'tel',
            'th': 'tha',
            'ti': 'tir',
            'ts': 'tso',
            'tr': 'tur',
            'tk': 'tuk',
            'tw': 'twi',
            'uk': 'ukr',
            'ur': 'urd',
            'ug': 'uig',
            'uz': 'uzb',
            'vi': 'vie',
            'cy': 'wel',
            'xh': 'xho',
            'yi': 'yid',
            'yo': 'yor',
            'zu': 'zul'
        }

    def get_code_of_name(self, name):
        return self.code_of_name[name]

    def get_code_of_ffmpeg_code(self, ffmpeg_code):
        return self.code_of_ffmpeg_code[ffmpeg_code]

    def get_name_of_code(self, code):
        return self.name_of_code[code]

    def get_name_of_ffmpeg_code(self, ffmpeg_code):
        return self.name_of_ffmpeg_code[ffmpeg_code]

    def get_ffmpeg_code_of_name(self, name):
        return self.ffmpeg_code_of_name[name]

    def get_ffmpeg_code_of_code(self, code):
        return self.ffmpeg_code_of_code[code]


class SentenceTranslator(object):
    def __init__(
        self,
        src,
        dst,
        endpoint_config,
        patience=-1,
        timeout=30,
        error_messages_callback=None
    ):
        self.src = src
        self.dst = dst
        self.endpoint_config = endpoint_config
        self.patience = patience
        self.timeout = timeout
        self.error_messages_callback = error_messages_callback

    def __call__(self, sentence):

        try:

            if not sentence:
                return None

            translated_sentence = self.GoogleTranslate(
                sentence,
                src=self.src,
                dst=self.dst,
                timeout=self.timeout
            )

            if translated_sentence is None:
                return None

            translated_sentence = str(translated_sentence)

            if not translated_sentence:
                return None

            fail_to_translate = translated_sentence.endswith('\n')

            patience = self.patience

            while fail_to_translate and patience:

                translated_sentence = self.GoogleTranslate(
                    translated_sentence,
                    src=self.src,
                    dst=self.dst,
                    timeout=self.timeout
                )

                if translated_sentence is None:
                    return None

                translated_sentence = str(translated_sentence)

                if translated_sentence.endswith('\n'):

                    if patience == -1:
                        continue

                    patience -= 1

                else:
                    fail_to_translate = False

            return translated_sentence

        except KeyboardInterrupt:

            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")

            return None

        except Exception as e:

            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)

            return None

    def GoogleTranslate(self, text, src, dst, timeout=30):
        endpoint_type = self.endpoint_config.get("type")

        try:
            # ========================================================
            # ENDPOINT 1
            # ========================================================
            if endpoint_type == 1:
                url = self.endpoint_config["url"]
                params = {
                    "client": "gtx",
                    "sl": src,
                    "tl": dst,
                    "dt": "t",
                    "q": text
                }
                headers = self.endpoint_config["headers"]

                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=timeout
                )

                if response.status_code != 200:
                    print(
                        "Google Translate HTTP error: %s"
                        % response.status_code
                    )
                    return None

                try:
                    data = response.json()
                except ValueError:
                    print("Google Translate returned invalid JSON:")
                    print(response.text[:500])
                    return None

                if not isinstance(data, list) or not data:
                    return None

                response_json = data[0]

                if not isinstance(response_json, list):
                    return None

                translation = ""

                for item in response_json:

                    if isinstance(item, list) and len(item) > 0:
                        if isinstance(item[0], str):
                            translation += item[0]

                if translation:
                    return translation

                return None

            # ========================================================
            # ENDPOINT 2
            # ========================================================

            elif endpoint_type == 2:
                url = self.endpoint_config["url"]
                params = {
                    "client": "dict-chrome-ex",
                    "sl": src,
                    "tl": dst,
                    "q": text
                }
                headers = self.endpoint_config["headers"]

                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=timeout
                )

                if response.status_code != 200:
                    print(
                        "Google Translate HTTP error: %s"
                        % response.status_code
                    )
                    return None

                try:
                    data = response.json()
                except ValueError:
                    print("Google Translate returned invalid JSON:")
                    print(response.text[:500])
                    return None

                if isinstance(data, list) and len(data) > 0:

                    translation = data[0]

                    # Normal response:
                    # ["Halo"]

                    if isinstance(translation, str):
                        return translation

                    # Nested response

                    if isinstance(translation, list):

                        result = ""

                        for item in translation:

                            if isinstance(item, str):
                                result += item

                            elif isinstance(item, list) and len(item) > 0:

                                if isinstance(item[0], str):
                                    result += item[0]

                        if result:
                            return result

                print("Unexpected Google Translate response:")
                print(data)

                return None

            else:
                print("Invalid Google Translate endpoint configuration.")
                return None

        except requests.exceptions.ConnectionError:

            # ========================================================
            # FALLBACK HTTPX
            # ========================================================

            try:

                if endpoint_type == 1:
                    url = self.endpoint_config["url"]
                    params = {
                        "client": "gtx",
                        "sl": src,
                        "tl": dst,
                        "dt": "t",
                        "q": text
                    }

                elif endpoint_type == 2:
                    url = self.endpoint_config["url"]
                    params = {
                        "client": "dict-chrome-ex",
                        "sl": src,
                        "tl": dst,
                        "q": text
                    }

                else:
                    return None

                headers = self.endpoint_config["headers"]

                with httpx.Client() as client:
                    response = client.get(
                        url,
                        params=params,
                        headers=headers,
                        timeout=timeout
                    )

                if response.status_code != 200:
                    return None

                try:
                    data = response.json()
                except ValueError:
                    return None

                # Endpoint 1

                if endpoint_type == 1:

                    if isinstance(data, list) and len(data) > 0:

                        response_json = data[0]

                        if isinstance(response_json, list):

                            translation = ""

                            for item in response_json:

                                if (
                                    isinstance(item, list)
                                    and len(item) > 0
                                    and isinstance(item[0], str)
                                ):
                                    translation += item[0]

                            if translation:
                                return translation

                # Endpoint 2

                elif endpoint_type == 2:

                    if isinstance(data, list) and len(data) > 0:

                        translation = data[0]

                        if isinstance(translation, str):
                            return translation

                        if isinstance(translation, list):

                            result = ""

                            for item in translation:

                                if isinstance(item, str):
                                    result += item

                                elif (
                                    isinstance(item, list)
                                    and len(item) > 0
                                    and isinstance(item[0], str)
                                ):
                                    result += item[0]

                            if result:
                                return result

                return None

            except Exception as e:

                if self.error_messages_callback:
                    self.error_messages_callback(e)
                else:
                    print(e)

                return None

        except KeyboardInterrupt:

            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")

            return None

        except Exception as e:

            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)

            return None


# ================================================================
# TEST ENDPOINT
# ================================================================

def test_translation_endpoint(src, dst, error_messages_callback=None):
    """
    Menguji kedua endpoint Google Translate.

    Return:
        dictionary endpoint aktif
        atau None jika kedua endpoint gagal.

    Struktur:
        {
            "type": 1 atau 2,
            "url": "...",
            "params": {...},
            "headers": {...}
        }
    """

    test_sentence = "Hello"

    print("CHECKING GOOGLE TRANSLATE ENDPOINT AVAILABILITY")
    print("===============================================")

    # ============================================================
    # ENDPOINT 1
    # ============================================================

    endpoint1 = {
        "type": 1,

        "url": (
            "https://translate.googleapis.com/"
            "translate_a/single"
        ),

        "params": {
            "client": "gtx",
            "sl": src,
            "tl": dst,
            "dt": "t",
            "q": test_sentence
        },

        "headers": {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            ),
            "Referer": "https://translate.google.com"
        }
    }

    try:
        print("Testing SentenceTranslator Endpoint 1...")
        print("URL: %s" % endpoint1["url"])

        response = requests.get(
            endpoint1["url"],
            params=endpoint1["params"],
            headers=endpoint1["headers"],
            timeout=10
        )

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                data = None

            translation = None

            if isinstance(data, list) and len(data) > 0:
                response_json = data[0]

                if isinstance(response_json, list):
                    result = ""
                    for item in response_json:
                        if (
                            isinstance(item, list)
                            and len(item) > 0
                            and isinstance(item[0], str)
                        ):
                            result += item[0]

                    if result:
                        translation = result

            if translation:
                print("SentenceTranslator endpoint 1 : OK")
                #print("Translation test result       : %s " % translation)
                print("Using Endpoint 1")
                print("")
                return endpoint1

        print("SentenceTranslator Endpoint 1 : FAILED " "(HTTP %s)" % response.status_code)

    except Exception as e:
        print("SentenceTranslator Endpoint 1 : FAILED")
        print("Error: %s" % e)

    # ============================================================
    # ENDPOINT 2
    # ============================================================

    endpoint2 = {
        "type": 2,

        "url": "https://clients5.google.com/translate_a/t",

        "params": {
            "client": "dict-chrome-ex",
            "sl": src,
            "tl": dst,
            "q": test_sentence
        },

        "headers": {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/139.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json,text/plain,*/*"
        }
    }

    try:

        print("Testing SentenceTranslator Endpoint 2...")
        print("URL: %s" % endpoint2["url"])

        response = requests.get(
            endpoint2["url"],
            params=endpoint2["params"],
            headers=endpoint2["headers"],
            timeout=10
        )

        if response.status_code == 200:

            try:
                data = response.json()
            except ValueError:
                data = None

            translation = None

            if isinstance(data, list) and len(data) > 0:

                first = data[0]

                if isinstance(first, str):

                    translation = first

                elif isinstance(first, list):

                    result = ""

                    for item in first:

                        if isinstance(item, str):
                            result += item

                        elif (
                            isinstance(item, list)
                            and len(item) > 0
                            and isinstance(item[0], str)
                        ):
                            result += item[0]

                    if result:
                        translation = result

            if translation:
                print("SentenceTranslator Endpoint 2 : OK")
                #print("Translation test result       : %s" % translation)
                print("Using Endpoint 2")
                print("")
                return endpoint2

        print("SentenceTranslator Endpoint 2 : FAILED " "(HTTP %s)" % response.status_code)

    except Exception as e:
        print("SentenceTranslator Endpoint 2 : FAILED")
        print("Error: %s" % e)

    print("")
    print("ERROR: Both Google Translate endpoints are unavailable.")
    print("")

    return None


# ================================================================
# SUBTITLE FORMATTER
# ================================================================

class SubtitleFormatter:

    supported_formats = ['srt', 'vtt', 'json', 'raw']

    def __init__(self, format_type, error_messages_callback=None):
        self.format_type = format_type.lower()
        self.error_messages_callback = error_messages_callback

    def __call__(
        self,
        subtitles,
        padding_before=0,
        padding_after=0
    ):
        try:

            if self.format_type == 'srt':
                return self.srt_formatter(
                    subtitles,
                    padding_before,
                    padding_after
                )

            elif self.format_type == 'vtt':
                return self.vtt_formatter(
                    subtitles,
                    padding_before,
                    padding_after
                )

            elif self.format_type == 'json':
                return self.json_formatter(subtitles)

            elif self.format_type == 'raw':
                return self.raw_formatter(subtitles)

            else:

                if self.error_messages_callback:
                    self.error_messages_callback(
                        "Unsupported format type: '%s'"
                        % self.format_type
                    )

                return None

        except KeyboardInterrupt:

            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")

            return None

        except Exception as e:

            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)

            return None

    def srt_formatter(
        self,
        subtitles,
        padding_before=0,
        padding_after=0
    ):

        sub_rip_file = pysrt.SubRipFile()

        for i, ((start, end), text) in enumerate(
            subtitles,
            start=1
        ):

            item = pysrt.SubRipItem()

            item.index = i
            item.text = six.text_type(text)
            item.start.seconds = max(
                0,
                start - padding_before
            )
            item.end.seconds = end + padding_after

            sub_rip_file.append(item)

        return '\n'.join(
            six.text_type(item)
            for item in sub_rip_file
        )

    def vtt_formatter(
        self,
        subtitles,
        padding_before=0,
        padding_after=0
    ):

        text = self.srt_formatter(
            subtitles,
            padding_before,
            padding_after
        )

        return 'WEBVTT\n\n' + text.replace(',', '.')

    def json_formatter(self, subtitles):

        subtitle_dicts = [
            {
                'start': start,
                'end': end,
                'content': text
            }

            for ((start, end), text)
            in subtitles
        ]

        return json.dumps(subtitle_dicts)

    def raw_formatter(self, subtitles):

        return ' '.join(
            text
            for (_rng, text)
            in subtitles
        )


# ================================================================
# SUBTITLE WRITER
# ================================================================

class SubtitleWriter:

    def __init__(
        self,
        regions,
        transcripts,
        format,
        error_messages_callback=None
    ):

        self.regions = regions
        self.transcripts = transcripts
        self.format = format

        self.timed_subtitles = [
            (r, t)
            for r, t in zip(
                self.regions,
                self.transcripts
            )
            if t
        ]

        self.error_messages_callback = error_messages_callback

    def get_timed_subtitles(self):
        return self.timed_subtitles

    def write(self, declared_subtitle_filepath):

        try:

            formatter = SubtitleFormatter(self.format)

            formatted_subtitles = formatter(
                self.timed_subtitles
            )

            saved_subtitle_filepath = declared_subtitle_filepath

            if saved_subtitle_filepath:

                subtitle_file_base, subtitle_file_ext = (
                    os.path.splitext(
                        saved_subtitle_filepath
                    )
                )

                if not subtitle_file_ext:

                    saved_subtitle_filepath = (
                        "%s.%s"
                        % (
                            subtitle_file_base,
                            self.format
                        )
                    )

            with open(
                saved_subtitle_filepath,
                'wb'
            ) as f:

                f.write(
                    formatted_subtitles.encode("utf-8")
                )

        except KeyboardInterrupt:

            if self.error_messages_callback:
                self.error_messages_callback(
                    "Cancelling all tasks"
                )
            else:
                print("Cancelling all tasks")

        except Exception as e:

            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)


# ================================================================
# SRT READER
# ================================================================

class SRTFileReader:

    def __init__(self, error_messages_callback=None):

        self.error_messages_callback = error_messages_callback
        self.timed_subtitles = []

    def __call__(self, subtitle_file_path):

        try:

            with open(
                subtitle_file_path,
                'r',
                encoding='utf-8'
            ) as srt_file:

                lines = srt_file.readlines()

            subtitle_blocks = []
            block = []

            for line in lines:

                if line.strip() == '':

                    subtitle_blocks.append(block)
                    block = []

                else:
                    block.append(line.strip())

            subtitle_blocks.append(block)

            for block in subtitle_blocks:

                if len(block) >= 3:

                    try:

                        start_time_str, end_time_str = (
                            block[1].split(' --> ')
                        )

                        time_format = '%H:%M:%S,%f'

                        start_time_total_seconds = (
                            datetime.strptime(
                                start_time_str,
                                time_format
                            )
                            - datetime.strptime(
                                '00:00:00,000',
                                time_format
                            )
                        ).total_seconds()

                        end_time_total_seconds = (
                            datetime.strptime(
                                end_time_str,
                                time_format
                            )
                            - datetime.strptime(
                                '00:00:00,000',
                                time_format
                            )
                        ).total_seconds()

                        subtitles = ' '.join(block[2:])

                        self.timed_subtitles.append(
                            (
                                (
                                    start_time_total_seconds,
                                    end_time_total_seconds
                                ),
                                subtitles
                            )
                        )

                    except Exception:
                        continue

            return self.timed_subtitles

        except FileNotFoundError:

            print(
                "Subtitle file '%s' not found."
                % subtitle_file_path
            )

            return []

        except Exception as e:

            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)

            return []


# ================================================================
# JSON READER
# ================================================================

class JSONFileReader:

    def __init__(self, error_messages_callback=None):

        self.error_messages_callback = error_messages_callback
        self.timed_subtitles = []

    def format_time(self, decimal_time):

        hours = int(decimal_time // 3600)
        minutes = int((decimal_time % 3600) // 60)
        seconds = int(decimal_time % 60)
        milliseconds = int(
            (decimal_time % 1) * 1000
        )

        return (
            "%02d:%02d:%02d,%03d"
            % (
                hours,
                minutes,
                seconds,
                milliseconds
            )
        )

    def __call__(self, subtitle_file_path):

        try:

            with open(
                subtitle_file_path,
                'r',
                encoding='utf-8'
            ) as json_file:

                data = json.load(json_file)

            for entry in data:

                start_time = entry.get("start", 0)
                end_time = entry.get("end", 0)
                subtitle_text = entry.get(
                    "content",
                    ""
                )

                if not subtitle_text:
                    continue

                start_time_str = self.format_time(
                    start_time
                )

                end_time_str = self.format_time(
                    end_time
                )

                time_format = '%H:%M:%S,%f'

                start_time_total_seconds = (
                    datetime.strptime(
                        start_time_str,
                        time_format
                    )
                    - datetime.strptime(
                        '00:00:00,000',
                        time_format
                    )
                ).total_seconds()

                end_time_total_seconds = (
                    datetime.strptime(
                        end_time_str,
                        time_format
                    )
                    - datetime.strptime(
                        '00:00:00,000',
                        time_format
                    )
                ).total_seconds()

                self.timed_subtitles.append(
                    (
                        (
                            start_time_total_seconds,
                            end_time_total_seconds
                        ),
                        subtitle_text
                    )
                )

            return self.timed_subtitles

        except FileNotFoundError:

            print(
                "Subtitle file '%s' not found."
                % subtitle_file_path
            )

            return []

        except Exception as e:

            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)

            return []


# ================================================================
# VTT READER
# ================================================================

class VTTFileReader:

    def __init__(self, error_messages_callback=None):

        self.error_messages_callback = error_messages_callback
        self.timed_subtitles = []

    def format_vtt_time(self, vtt_time):

        vtt_time = vtt_time.strip()

        hours, minutes, seconds = (
            vtt_time.replace(',', '.').split(':')
        )

        return (
            "%02d:%02d:%06.3f"
            % (
                int(float(hours)),
                int(float(minutes)),
                float(seconds)
            )
        ).replace('.', ',')

    def __call__(self, subtitle_file_path):

        try:

            start_time = None
            end_time = None
            subtitle_blocks = []

            with open(
                subtitle_file_path,
                'r',
                encoding='utf-8'
            ) as vtt_file:

                lines = vtt_file.readlines()

            for line in lines:

                line = line.strip()

                if '-->' in line:

                    if start_time and end_time:

                        start_time_str = self.format_vtt_time(
                            start_time
                        )

                        end_time_str = self.format_vtt_time(
                            end_time
                        )

                        subtitle = ' '.join(
                            subtitle_blocks
                        )

                        time_format = '%H:%M:%S,%f'

                        start_time_total_seconds = (
                            datetime.strptime(
                                start_time_str,
                                time_format
                            )
                            - datetime.strptime(
                                '00:00:00,000',
                                time_format
                            )
                        ).total_seconds()

                        end_time_total_seconds = (
                            datetime.strptime(
                                end_time_str,
                                time_format
                            )
                            - datetime.strptime(
                                '00:00:00,000',
                                time_format
                            )
                        ).total_seconds()

                        self.timed_subtitles.append(
                            (
                                (
                                    start_time_total_seconds,
                                    end_time_total_seconds
                                ),
                                subtitle
                            )
                        )

                    start_time, end_time = line.split('-->')
                    subtitle_blocks = []

                elif line and not line.isdigit():

                    subtitle_blocks.append(line)

            if start_time and end_time and subtitle_blocks:

                start_time_str = self.format_vtt_time(
                    start_time
                )

                end_time_str = self.format_vtt_time(
                    end_time
                )

                subtitle = ' '.join(
                    subtitle_blocks
                )

                time_format = '%H:%M:%S,%f'

                start_time_total_seconds = (
                    datetime.strptime(
                        start_time_str,
                        time_format
                    )
                    - datetime.strptime(
                        '00:00:00,000',
                        time_format
                    )
                ).total_seconds()

                end_time_total_seconds = (
                    datetime.strptime(
                        end_time_str,
                        time_format
                    )
                    - datetime.strptime(
                        '00:00:00,000',
                        time_format
                    )
                ).total_seconds()

                self.timed_subtitles.append(
                    (
                        (
                            start_time_total_seconds,
                            end_time_total_seconds
                        ),
                        subtitle
                    )
                )

            return self.timed_subtitles

        except FileNotFoundError:

            print(
                "Subtitle file '%s' not found."
                % subtitle_file_path
            )

            return []

        except Exception as e:

            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)

            return []


# ================================================================
# RAW READER
# ================================================================

class RAWFileReader:

    def __init__(self, error_messages_callback=None):

        self.error_messages_callback = error_messages_callback
        self.timed_subtitles = []

    def __call__(self, subtitle_file_path):

        try:

            with open(
                subtitle_file_path,
                'r',
                encoding='utf-8'
            ) as raw_file:

                lines = raw_file.readlines()

            subtitle_blocks = []
            block = []

            for line in lines:

                if line.strip() == '':

                    subtitle_blocks.append(block)
                    block = []

                else:

                    block.append(line.strip())

            subtitle_blocks.append(block)

            for block in subtitle_blocks:

                if block:

                    subtitles = ' '.join(block)

                    self.timed_subtitles.append(
                        (
                            (0, 0),
                            subtitles
                        )
                    )

            return self.timed_subtitles

        except FileNotFoundError:

            print(
                "Subtitle file '%s' not found."
                % subtitle_file_path
            )

            return []

        except Exception as e:

            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)

            return []


# ================================================================
# UTILITIES
# ================================================================

def is_same_language(
    src,
    dst,
    error_messages_callback=None
):

    try:

        return (
            src.split("-")[0]
            ==
            dst.split("-")[0]
        )

    except Exception as e:

        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)

        return False


def show_error_messages(messages):
    print(messages)


def is_valid_subtitle_file(
    subtitle_filepath,
    error_messages_callback=None
):

    base, ext = os.path.splitext(
        subtitle_filepath
    )

    timed_subtitles = []

    if "\\" in subtitle_filepath:
        subtitle_filepath = subtitle_filepath.replace(
            "\\",
            "/"
        )

    if not os.path.isfile(subtitle_filepath):

        message = (
            "The given file does not exist: '%s'"
            % subtitle_filepath
        )

        if error_messages_callback:
            error_messages_callback(message)
        else:
            print(message)

        return False

    extension = ext.lower()

    if extension == ".srt":

        reader = SRTFileReader()

    elif extension == ".vtt":

        reader = VTTFileReader()

    elif extension == ".json":

        reader = JSONFileReader()

    elif extension == ".raw":

        reader = RAWFileReader()

    else:

        return False

    timed_subtitles = reader(
        subtitle_filepath
    )

    return bool(timed_subtitles)


# ================================================================
# MAIN
# ================================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'subtitle_file_path',
        help=(
            "Subtitle file path you want to translate "
            "(use wildcard for multiple files or separate "
            "them with a space character)"
        ),
        nargs='*'
    )

    parser.add_argument(
        '-S',
        '--src-language',
        help="Language code of subtitle file",
        default="en"
    )

    parser.add_argument(
        '-D',
        '--dst-language',
        help="Desired translation language code",
        default=None
    )

    parser.add_argument(
        '-ll',
        '--list-languages',
        help="List all supported languages",
        action='store_true'
    )

    parser.add_argument(
        '-F',
        '--format',
        help="Desired subtitles file format",
        default="srt"
    )

    parser.add_argument(
        '-lf',
        '--list-formats',
        help="List all supported subtitle formats",
        action='store_true'
    )

    parser.add_argument(
        '-C',
        '--concurrency',
        help="Number of concurrent API requests",
        type=int,
        default=10
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=VERSION
    )

    args = parser.parse_args()

    language = Language()

    # ============================================================
    # LIST LANGUAGES
    # ============================================================

    if args.list_languages:

        print("List of supported languages:")

        for code, lang_name in sorted(
            language.name_of_code.items()
        ):

            print(
                "%-8s : %s"
                % (
                    code,
                    lang_name
                )
            )

        return 0

    # ============================================================
    # VALIDATE SOURCE
    # ============================================================

    if args.src_language not in language.name_of_code:

        print(
            "Source language is not supported. "
            "Run with --list-languages."
        )

        return 1

    # ============================================================
    # TRANSLATION MODE
    # ============================================================

    if args.dst_language:

        if args.dst_language not in language.name_of_code:

            print(
                "Destination language is not supported. "
                "Run with --list-languages."
            )

            return 1

        if not is_same_language(
            args.src_language,
            args.dst_language,
            error_messages_callback=show_error_messages
        ):

            do_translate = True

        else:

            do_translate = False

    else:

        do_translate = False

    # ============================================================
    # LIST FORMATS
    # ============================================================

    if args.list_formats:

        print("List of supported subtitle formats:")

        for subtitle_format in (
            SubtitleFormatter.supported_formats
        ):

            print(subtitle_format)

        return 0

    # ============================================================
    # VALIDATE FORMAT
    # ============================================================

    if (
        args.format
        not in SubtitleFormatter.supported_formats
    ):

        print(
            "Subtitle format is not supported. "
            "Run with --list-formats."
        )

        return 1

    # ============================================================
    # VALIDATE INPUT
    # ============================================================

    if not args.subtitle_file_path:

        parser.print_help(sys.stderr)

        return 1

    completed_tasks = 0

    subtitle_filepaths = []
    arg_filepaths = []
    invalid_subtitle_filepaths = []
    not_exist_subtitle_filepaths = []

    args_subtitle_file_path = list(
        args.subtitle_file_path
    )

    # ============================================================
    # CHECK NON-WILDCARD FILES
    # ============================================================

    if (
        "*" not in str(args_subtitle_file_path)
        and "?" not in str(args_subtitle_file_path)
    ):

        for filepath in args_subtitle_file_path:

            if not os.path.isfile(filepath):

                not_exist_subtitle_filepaths.append(
                    filepath
                )

    # ============================================================
    # WINDOWS BRACKET HANDLING
    # ============================================================

    if sys.platform == "win32":

        for i in range(
            len(args_subtitle_file_path)
        ):

            if (
                "["
                in args_subtitle_file_path[i]
                or "]"
                in args_subtitle_file_path[i]
            ):

                placeholder = "#TEMP#"

                args_subtitle_file_path[i] = (
                    args_subtitle_file_path[i]
                    .replace(
                        "[",
                        placeholder
                    )
                )

                args_subtitle_file_path[i] = (
                    args_subtitle_file_path[i]
                    .replace(
                        "]",
                        "[]]"
                    )
                )

                args_subtitle_file_path[i] = (
                    args_subtitle_file_path[i]
                    .replace(
                        placeholder,
                        "[[]"
                    )
                )

    # ============================================================
    # EXPAND FILES
    # ============================================================

    for arg in args_subtitle_file_path:

        arg_filepaths += glob(arg)

    # ============================================================
    # VALIDATE FILES
    # ============================================================

    if arg_filepaths:

        for argpath in arg_filepaths:

            if os.path.isfile(argpath):

                if is_valid_subtitle_file(
                    argpath,
                    error_messages_callback=show_error_messages
                ):

                    subtitle_filepaths.append(argpath)

                else:

                    invalid_subtitle_filepaths.append(
                        argpath
                    )

            else:

                not_exist_subtitle_filepaths.append(
                    argpath
                )

    if invalid_subtitle_filepaths:

        for invalid_filepath in (
            invalid_subtitle_filepaths
        ):

            print(
                "'%s' is not valid subtitle files"
                % invalid_filepath
            )

    if not_exist_subtitle_filepaths:

        if (
            "*"
            not in str(args_subtitle_file_path)
            and "?"
            not in str(args_subtitle_file_path)
        ):

            for filepath in (
                not_exist_subtitle_filepaths
            ):

                print(
                    "'%s' does not exist"
                    % filepath
                )

            return 1

    if (
        not arg_filepaths
        and not not_exist_subtitle_filepaths
    ):

        print(
            "No files matching filenames you typed"
        )

        return 1

    subtitle_format = args.format

    # ============================================================
    # TEST ENDPOINT ONCE
    # ============================================================
    endpoint_config = None
    if do_translate:
        endpoint_config = test_translation_endpoint(args.src_language, args.dst_language, error_messages_callback=show_error_messages)
        if endpoint_config is None:
            print("ERROR: No working Google Translate endpoint.")
            return 1

        #print("Selected Google Translate endpoint : %d" % endpoint_config["type"])
        #print("Selected URL                      : %s" % endpoint_config["url"])
        #print("")

    # ============================================================
    # PROCESS FILES
    # ============================================================

    translate_start_time = time.time()

    for subtitle_filepath in subtitle_filepaths:

        print(
            "Processing '%s'"
            % subtitle_filepath
        )

        base, ext = os.path.splitext(
            subtitle_filepath
        )

        extension = ext.lower()

        # ========================================================
        # READ SUBTITLE
        # ========================================================

        if extension == ".srt":

            reader = SRTFileReader()

        elif extension == ".vtt":

            reader = VTTFileReader()

        elif extension == ".json":

            reader = JSONFileReader()

        elif extension == ".raw":

            reader = RAWFileReader()

        else:

            continue

        timed_subtitles = reader(
            subtitle_filepath
        )

        regions = []
        transcripts = []

        for entry in timed_subtitles:

            regions.append(entry[0])
            transcripts.append(entry[1])

        # ========================================================
        # TRANSLATE
        # ========================================================

        if do_translate:

            if (
                timed_subtitles
                and extension != ".raw"
            ):

                prompt = (
                    "Translating from %s to %s   : "
                    % (
                        args.src_language.center(8),
                        args.dst_language.center(8)
                    )
                )

                widgets = [
                    prompt,
                    Percentage(),
                    ' ',
                    Bar(),
                    ' ',
                    ETA()
                ]

                pbar = ProgressBar(
                    widgets=widgets,
                    maxval=len(timed_subtitles)
                ).start()

                transcript_translator = SentenceTranslator(
                    src=args.src_language,
                    dst=args.dst_language,
                    endpoint_config=endpoint_config,
                    error_messages_callback=show_error_messages
                )

                pool = multiprocessing.Pool(
                    args.concurrency
                )

                translated_transcripts = []

                try:

                    for i, translated_transcript in enumerate(
                        pool.imap(
                            transcript_translator,
                            transcripts
                        ),
                        start=1
                    ):

                        translated_transcripts.append(
                            translated_transcript
                        )

                        pbar.update(i)

                finally:

                    pool.close()
                    pool.join()

                pbar.finish()

                dst_subtitle_filepath = (
                    "%s.%s.%s"
                    % (
                        base,
                        args.dst_language,
                        subtitle_format
                    )
                )

                translation_writer = SubtitleWriter(
                    regions,
                    translated_transcripts,
                    subtitle_format,
                    error_messages_callback=show_error_messages
                )

                translation_writer.write(
                    dst_subtitle_filepath
                )

                print(
                    "Translated subtitles file saved as      : '%s'"
                    % dst_subtitle_filepath
                )

                print("")

                completed_tasks += 1

            elif (
                timed_subtitles
                and extension == ".raw"
            ):

                if (
                    args.format
                    and args.format != "raw"
                ):

                    print(
                        "Cannot convert raw subtitle format "
                        "to %s format, subtitle file will "
                        "be saved in raw format"
                        % args.format
                    )

                prompt = (
                    "Translating from %s to %s   : "
                    % (
                        args.src_language.center(8),
                        args.dst_language.center(8)
                    )
                )

                widgets = [
                    prompt,
                    Percentage(),
                    ' ',
                    Bar(),
                    ' ',
                    ETA()
                ]

                pbar = ProgressBar(
                    widgets=widgets,
                    maxval=len(timed_subtitles)
                ).start()

                subtitle_format = "raw"

                transcript_translator = SentenceTranslator(
                    src=args.src_language,
                    dst=args.dst_language,
                    endpoint_config=endpoint_config,
                    error_messages_callback=show_error_messages
                )

                pool = multiprocessing.Pool(
                    args.concurrency
                )

                translated_transcripts = []

                try:

                    for i, translated_transcript in enumerate(
                        pool.imap(
                            transcript_translator,
                            transcripts
                        ),
                        start=1
                    ):

                        translated_transcripts.append(
                            translated_transcript
                        )

                        pbar.update(i)

                finally:

                    pool.close()
                    pool.join()

                pbar.finish()

                dst_subtitle_filepath = (
                    "%s.%s.%s"
                    % (
                        base,
                        args.dst_language,
                        subtitle_format
                    )
                )

                translation_writer = SubtitleWriter(
                    regions,
                    translated_transcripts,
                    subtitle_format,
                    error_messages_callback=show_error_messages
                )

                translation_writer.write(
                    dst_subtitle_filepath
                )

                print(
                    "Translated subtitles file saved as      : '%s'"
                    % dst_subtitle_filepath
                )

                print("")

                completed_tasks += 1

            else:

                return 1

        # ========================================================
        # CONVERT WITHOUT TRANSLATION
        # ========================================================

        else:

            if extension == "." + subtitle_format:

                print("Nothing to do")

                return 1

            else:

                dst_subtitle_filepath = (
                    "%s.%s"
                    % (
                        base,
                        subtitle_format
                    )
                )

                writer = SubtitleWriter(
                    regions,
                    transcripts,
                    subtitle_format,
                    error_messages_callback=show_error_messages
                )

                writer.write(
                    dst_subtitle_filepath
                )

                print(
                    "Subtitles file saved as      : '%s'"
                    % dst_subtitle_filepath
                )

                print("")

                completed_tasks += 1

    # ============================================================
    # FINISH
    # ============================================================

    if (
        len(subtitle_filepaths) > 0
        and completed_tasks
        == len(subtitle_filepaths)
    ):

        translate_end_time = time.time()

        translate_elapsed_time = (
            translate_end_time
            - translate_start_time
        )

        translate_elapsed_time_seconds = timedelta(
            seconds=int(translate_elapsed_time)
        )

        translate_elapsed_time_str = str(
            translate_elapsed_time_seconds
        )

        hour, minute, second = (
            translate_elapsed_time_str.split(":")
        )

        msg = (
            "Total running time                      : "
            "%s:%s:%s"
            % (
                hour.zfill(2),
                minute,
                second
            )
        )

        print(msg)

    return 0


if __name__ == '__main__':
    sys.exit(main())
