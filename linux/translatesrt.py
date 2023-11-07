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
# ADDITIONAL IMPORT
from datetime import datetime, timedelta
import time
from glob import glob, escape
from pathlib import Path
import shlex
import shutil


VERSION = "0.0.4"


class Language:
    def __init__(self):
        self.list_codes = []
        self.list_codes.append("af")
        self.list_codes.append("sq")
        self.list_codes.append("am")
        self.list_codes.append("ar")
        self.list_codes.append("hy")
        self.list_codes.append("as")
        self.list_codes.append("ay")
        self.list_codes.append("az")
        self.list_codes.append("bm")
        self.list_codes.append("eu")
        self.list_codes.append("be")
        self.list_codes.append("bn")
        self.list_codes.append("bho")
        self.list_codes.append("bs")
        self.list_codes.append("bg")
        self.list_codes.append("ca")
        self.list_codes.append("ceb")
        self.list_codes.append("ny")
        self.list_codes.append("zh")
        self.list_codes.append("zh-CN")
        self.list_codes.append("zh-TW")
        self.list_codes.append("co")
        self.list_codes.append("hr")
        self.list_codes.append("cs")
        self.list_codes.append("da")
        self.list_codes.append("dv")
        self.list_codes.append("doi")
        self.list_codes.append("nl")
        self.list_codes.append("en")
        self.list_codes.append("eo")
        self.list_codes.append("et")
        self.list_codes.append("ee")
        self.list_codes.append("fil")
        self.list_codes.append("fi")
        self.list_codes.append("fr")
        self.list_codes.append("fy")
        self.list_codes.append("gl")
        self.list_codes.append("ka")
        self.list_codes.append("de")
        self.list_codes.append("el")
        self.list_codes.append("gn")
        self.list_codes.append("gu")
        self.list_codes.append("ht")
        self.list_codes.append("ha")
        self.list_codes.append("haw")
        self.list_codes.append("he")
        self.list_codes.append("hi")
        self.list_codes.append("hmn")
        self.list_codes.append("hu")
        self.list_codes.append("is")
        self.list_codes.append("ig")
        self.list_codes.append("ilo")
        self.list_codes.append("id")
        self.list_codes.append("ga")
        self.list_codes.append("it")
        self.list_codes.append("ja")
        self.list_codes.append("jv")
        self.list_codes.append("kn")
        self.list_codes.append("kk")
        self.list_codes.append("km")
        self.list_codes.append("rw")
        self.list_codes.append("gom")
        self.list_codes.append("ko")
        self.list_codes.append("kri")
        self.list_codes.append("kmr")
        self.list_codes.append("ckb")
        self.list_codes.append("ky")
        self.list_codes.append("lo")
        self.list_codes.append("la")
        self.list_codes.append("lv")
        self.list_codes.append("ln")
        self.list_codes.append("lt")
        self.list_codes.append("lg")
        self.list_codes.append("lb")
        self.list_codes.append("mk")
        self.list_codes.append("mg")
        self.list_codes.append("ms")
        self.list_codes.append("ml")
        self.list_codes.append("mt")
        self.list_codes.append("mi")
        self.list_codes.append("mr")
        self.list_codes.append("mni-Mtei")
        self.list_codes.append("lus")
        self.list_codes.append("mn")
        self.list_codes.append("my")
        self.list_codes.append("ne")
        self.list_codes.append("no")
        self.list_codes.append("or")
        self.list_codes.append("om")
        self.list_codes.append("ps")
        self.list_codes.append("fa")
        self.list_codes.append("pl")
        self.list_codes.append("pt")
        self.list_codes.append("pa")
        self.list_codes.append("qu")
        self.list_codes.append("ro")
        self.list_codes.append("ru")
        self.list_codes.append("sm")
        self.list_codes.append("sa")
        self.list_codes.append("gd")
        self.list_codes.append("nso")
        self.list_codes.append("sr")
        self.list_codes.append("st")
        self.list_codes.append("sn")
        self.list_codes.append("sd")
        self.list_codes.append("si")
        self.list_codes.append("sk")
        self.list_codes.append("sl")
        self.list_codes.append("so")
        self.list_codes.append("es")
        self.list_codes.append("su")
        self.list_codes.append("sw")
        self.list_codes.append("sv")
        self.list_codes.append("tg")
        self.list_codes.append("ta")
        self.list_codes.append("tt")
        self.list_codes.append("te")
        self.list_codes.append("th")
        self.list_codes.append("ti")
        self.list_codes.append("ts")
        self.list_codes.append("tr")
        self.list_codes.append("tk")
        self.list_codes.append("tw")
        self.list_codes.append("uk")
        self.list_codes.append("ur")
        self.list_codes.append("ug")
        self.list_codes.append("uz")
        self.list_codes.append("vi")
        self.list_codes.append("cy")
        self.list_codes.append("xh")
        self.list_codes.append("yi")
        self.list_codes.append("yo")
        self.list_codes.append("zu")

        self.list_names = []
        self.list_names.append("Afrikaans")
        self.list_names.append("Albanian")
        self.list_names.append("Amharic")
        self.list_names.append("Arabic")
        self.list_names.append("Armenian")
        self.list_names.append("Assamese")
        self.list_names.append("Aymara")
        self.list_names.append("Azerbaijani")
        self.list_names.append("Bambara")
        self.list_names.append("Basque")
        self.list_names.append("Belarusian")
        self.list_names.append("Bengali")
        self.list_names.append("Bhojpuri")
        self.list_names.append("Bosnian")
        self.list_names.append("Bulgarian")
        self.list_names.append("Catalan")
        self.list_names.append("Cebuano")
        self.list_names.append("Chichewa")
        self.list_names.append("Chinese")
        self.list_names.append("Chinese (Simplified)")
        self.list_names.append("Chinese (Traditional)")
        self.list_names.append("Corsican")
        self.list_names.append("Croatian")
        self.list_names.append("Czech")
        self.list_names.append("Danish")
        self.list_names.append("Dhivehi")
        self.list_names.append("Dogri")
        self.list_names.append("Dutch")
        self.list_names.append("English")
        self.list_names.append("Esperanto")
        self.list_names.append("Estonian")
        self.list_names.append("Ewe")
        self.list_names.append("Filipino")
        self.list_names.append("Finnish")
        self.list_names.append("French")
        self.list_names.append("Frisian")
        self.list_names.append("Galician")
        self.list_names.append("Georgian")
        self.list_names.append("German")
        self.list_names.append("Greek")
        self.list_names.append("Guarani")
        self.list_names.append("Gujarati")
        self.list_names.append("Haitian Creole")
        self.list_names.append("Hausa")
        self.list_names.append("Hawaiian")
        self.list_names.append("Hebrew")
        self.list_names.append("Hindi")
        self.list_names.append("Hmong")
        self.list_names.append("Hungarian")
        self.list_names.append("Icelandic")
        self.list_names.append("Igbo")
        self.list_names.append("Ilocano")
        self.list_names.append("Indonesian")
        self.list_names.append("Irish")
        self.list_names.append("Italian")
        self.list_names.append("Japanese")
        self.list_names.append("Javanese")
        self.list_names.append("Kannada")
        self.list_names.append("Kazakh")
        self.list_names.append("Khmer")
        self.list_names.append("Kinyarwanda")
        self.list_names.append("Konkani")
        self.list_names.append("Korean")
        self.list_names.append("Krio")
        self.list_names.append("Kurdish (Kurmanji)")
        self.list_names.append("Kurdish (Sorani)")
        self.list_names.append("Kyrgyz")
        self.list_names.append("Lao")
        self.list_names.append("Latin")
        self.list_names.append("Latvian")
        self.list_names.append("Lingala")
        self.list_names.append("Lithuanian")
        self.list_names.append("Luganda")
        self.list_names.append("Luxembourgish")
        self.list_names.append("Macedonian")
        self.list_names.append("Malagasy")
        self.list_names.append("Malay")
        self.list_names.append("Malayalam")
        self.list_names.append("Maltese")
        self.list_names.append("Maori")
        self.list_names.append("Marathi")
        self.list_names.append("Meiteilon (Manipuri)")
        self.list_names.append("Mizo")
        self.list_names.append("Mongolian")
        self.list_names.append("Myanmar (Burmese)")
        self.list_names.append("Nepali")
        self.list_names.append("Norwegian")
        self.list_names.append("Odiya (Oriya)")
        self.list_names.append("Oromo")
        self.list_names.append("Pashto")
        self.list_names.append("Persian")
        self.list_names.append("Polish")
        self.list_names.append("Portuguese")
        self.list_names.append("Punjabi")
        self.list_names.append("Quechua")
        self.list_names.append("Romanian")
        self.list_names.append("Russian")
        self.list_names.append("Samoan")
        self.list_names.append("Sanskrit")
        self.list_names.append("Scots Gaelic")
        self.list_names.append("Sepedi")
        self.list_names.append("Serbian")
        self.list_names.append("Sesotho")
        self.list_names.append("Shona")
        self.list_names.append("Sindhi")
        self.list_names.append("Sinhala")
        self.list_names.append("Slovak")
        self.list_names.append("Slovenian")
        self.list_names.append("Somali")
        self.list_names.append("Spanish")
        self.list_names.append("Sundanese")
        self.list_names.append("Swahili")
        self.list_names.append("Swedish")
        self.list_names.append("Tajik")
        self.list_names.append("Tamil")
        self.list_names.append("Tatar")
        self.list_names.append("Telugu")
        self.list_names.append("Thai")
        self.list_names.append("Tigrinya")
        self.list_names.append("Tsonga")
        self.list_names.append("Turkish")
        self.list_names.append("Turkmen")
        self.list_names.append("Twi (Akan)")
        self.list_names.append("Ukrainian")
        self.list_names.append("Urdu")
        self.list_names.append("Uyghur")
        self.list_names.append("Uzbek")
        self.list_names.append("Vietnamese")
        self.list_names.append("Welsh")
        self.list_names.append("Xhosa")
        self.list_names.append("Yiddish")
        self.list_names.append("Yoruba")
        self.list_names.append("Zulu")

        # NOTE THAT Google Translate AND Vosk Speech Recognition API USE ISO-639-1 STANDARD CODE ('al', 'af', 'as', ETC)
        # WHEN ffmpeg SUBTITLES STREAMS USE ISO 639-2 STANDARD CODE ('afr', 'alb', 'amh', ETC)

        self.list_ffmpeg_codes = []
        self.list_ffmpeg_codes.append("afr")  # Afrikaans
        self.list_ffmpeg_codes.append("alb")  # Albanian
        self.list_ffmpeg_codes.append("amh")  # Amharic
        self.list_ffmpeg_codes.append("ara")  # Arabic
        self.list_ffmpeg_codes.append("hye")  # Armenian
        self.list_ffmpeg_codes.append("asm")  # Assamese
        self.list_ffmpeg_codes.append("aym")  # Aymara
        self.list_ffmpeg_codes.append("aze")  # Azerbaijani
        self.list_ffmpeg_codes.append("bam")  # Bambara
        self.list_ffmpeg_codes.append("eus")  # Basque
        self.list_ffmpeg_codes.append("bel")  # Belarusian
        self.list_ffmpeg_codes.append("ben")  # Bengali
        self.list_ffmpeg_codes.append("bho")  # Bhojpuri
        self.list_ffmpeg_codes.append("bos")  # Bosnian
        self.list_ffmpeg_codes.append("bul")  # Bulgarian
        self.list_ffmpeg_codes.append("cat")  # Catalan
        self.list_ffmpeg_codes.append("ceb")  # Cebuano
        self.list_ffmpeg_codes.append("nya")  # Chichewa
        self.list_ffmpeg_codes.append("zho")  # Chinese
        self.list_ffmpeg_codes.append("zho-CN")  # Chinese (Simplified)
        self.list_ffmpeg_codes.append("zho-TW")  # Chinese (Traditional)
        self.list_ffmpeg_codes.append("cos")  # Corsican
        self.list_ffmpeg_codes.append("hrv")  # Croatian
        self.list_ffmpeg_codes.append("ces")  # Czech
        self.list_ffmpeg_codes.append("dan")  # Danish
        self.list_ffmpeg_codes.append("div")  # Dhivehi
        self.list_ffmpeg_codes.append("doi")  # Dogri
        self.list_ffmpeg_codes.append("nld")  # Dutch
        self.list_ffmpeg_codes.append("eng")  # English
        self.list_ffmpeg_codes.append("epo")  # Esperanto
        self.list_ffmpeg_codes.append("est")  # Estonian
        self.list_ffmpeg_codes.append("ewe")  # Ewe
        self.list_ffmpeg_codes.append("fil")  # Filipino
        self.list_ffmpeg_codes.append("fin")  # Finnish
        self.list_ffmpeg_codes.append("fra")  # French
        self.list_ffmpeg_codes.append("fry")  # Frisian
        self.list_ffmpeg_codes.append("glg")  # Galician
        self.list_ffmpeg_codes.append("kat")  # Georgian
        self.list_ffmpeg_codes.append("deu")  # German
        self.list_ffmpeg_codes.append("ell")  # Greek
        self.list_ffmpeg_codes.append("grn")  # Guarani
        self.list_ffmpeg_codes.append("guj")  # Gujarati
        self.list_ffmpeg_codes.append("hat")  # Haitian Creole
        self.list_ffmpeg_codes.append("hau")  # Hausa
        self.list_ffmpeg_codes.append("haw")  # Hawaiian
        self.list_ffmpeg_codes.append("heb")  # Hebrew
        self.list_ffmpeg_codes.append("hin")  # Hindi
        self.list_ffmpeg_codes.append("hmn")  # Hmong
        self.list_ffmpeg_codes.append("hun")  # Hungarian
        self.list_ffmpeg_codes.append("isl")  # Icelandic
        self.list_ffmpeg_codes.append("ibo")  # Igbo
        self.list_ffmpeg_codes.append("ilo")  # Ilocano
        self.list_ffmpeg_codes.append("ind")  # Indonesian
        self.list_ffmpeg_codes.append("gle")  # Irish
        self.list_ffmpeg_codes.append("ita")  # Italian
        self.list_ffmpeg_codes.append("jpn")  # Japanese
        self.list_ffmpeg_codes.append("jav")  # Javanese
        self.list_ffmpeg_codes.append("kan")  # Kannada
        self.list_ffmpeg_codes.append("kaz")  # Kazakh
        self.list_ffmpeg_codes.append("khm")  # Khmer
        self.list_ffmpeg_codes.append("kin")  # Kinyarwanda
        self.list_ffmpeg_codes.append("kok")  # Konkani
        self.list_ffmpeg_codes.append("kor")  # Korean
        self.list_ffmpeg_codes.append("kri")  # Krio
        self.list_ffmpeg_codes.append("kmr")  # Kurdish (Kurmanji)
        self.list_ffmpeg_codes.append("ckb")  # Kurdish (Sorani)
        self.list_ffmpeg_codes.append("kir")  # Kyrgyz
        self.list_ffmpeg_codes.append("lao")  # Lao
        self.list_ffmpeg_codes.append("lat")  # Latin
        self.list_ffmpeg_codes.append("lav")  # Latvian
        self.list_ffmpeg_codes.append("lin")  # Lingala
        self.list_ffmpeg_codes.append("lit")  # Lithuanian
        self.list_ffmpeg_codes.append("lug")  # Luganda
        self.list_ffmpeg_codes.append("ltz")  # Luxembourgish
        self.list_ffmpeg_codes.append("mkd")  # Macedonian
        self.list_ffmpeg_codes.append("mlg")  # Malagasy
        self.list_ffmpeg_codes.append("msa")  # Malay
        self.list_ffmpeg_codes.append("mal")  # Malayalam
        self.list_ffmpeg_codes.append("mlt")  # Maltese
        self.list_ffmpeg_codes.append("mri")  # Maori
        self.list_ffmpeg_codes.append("mar")  # Marathi
        self.list_ffmpeg_codes.append("mni-Mtei")  # Meiteilon (Manipuri)
        self.list_ffmpeg_codes.append("lus")  # Mizo
        self.list_ffmpeg_codes.append("mon")  # Mongolian
        self.list_ffmpeg_codes.append("mya")  # Myanmar (Burmese)
        self.list_ffmpeg_codes.append("nep")  # Nepali
        self.list_ffmpeg_codes.append("nor")  # Norwegian
        self.list_ffmpeg_codes.append("ori")  # Odiya (Oriya)
        self.list_ffmpeg_codes.append("orm")  # Oromo
        self.list_ffmpeg_codes.append("pus")  # Pashto
        self.list_ffmpeg_codes.append("fas")  # Persian
        self.list_ffmpeg_codes.append("pol")  # Polish
        self.list_ffmpeg_codes.append("por")  # Portuguese
        self.list_ffmpeg_codes.append("pan")  # Punjabi
        self.list_ffmpeg_codes.append("que")  # Quechua
        self.list_ffmpeg_codes.append("ron")  # Romanian
        self.list_ffmpeg_codes.append("rus")  # Russian
        self.list_ffmpeg_codes.append("smo")  # Samoan
        self.list_ffmpeg_codes.append("san")  # Sanskrit
        self.list_ffmpeg_codes.append("gla")  # Scots Gaelic
        self.list_ffmpeg_codes.append("nso")  # Sepedi
        self.list_ffmpeg_codes.append("srp")  # Serbian
        self.list_ffmpeg_codes.append("sot")  # Sesotho
        self.list_ffmpeg_codes.append("sna")  # Shona
        self.list_ffmpeg_codes.append("snd")  # Sindhi
        self.list_ffmpeg_codes.append("sin")  # Sinhala
        self.list_ffmpeg_codes.append("slk")  # Slovak
        self.list_ffmpeg_codes.append("slv")  # Slovenian
        self.list_ffmpeg_codes.append("som")  # Somali
        self.list_ffmpeg_codes.append("spa")  # Spanish
        self.list_ffmpeg_codes.append("sun")  # Sundanese
        self.list_ffmpeg_codes.append("swa")  # Swahili
        self.list_ffmpeg_codes.append("swe")  # Swedish
        self.list_ffmpeg_codes.append("tgk")  # Tajik
        self.list_ffmpeg_codes.append("tam")  # Tamil
        self.list_ffmpeg_codes.append("tat")  # Tatar
        self.list_ffmpeg_codes.append("tel")  # Telugu
        self.list_ffmpeg_codes.append("tha")  # Thai
        self.list_ffmpeg_codes.append("tir")  # Tigrinya
        self.list_ffmpeg_codes.append("tso")  # Tsonga
        self.list_ffmpeg_codes.append("tur")  # Turkish
        self.list_ffmpeg_codes.append("tuk")  # Turkmen
        self.list_ffmpeg_codes.append("twi")  # Twi (Akan)
        self.list_ffmpeg_codes.append("ukr")  # Ukrainian
        self.list_ffmpeg_codes.append("urd")  # Urdu
        self.list_ffmpeg_codes.append("uig")  # Uyghur
        self.list_ffmpeg_codes.append("uzb")  # Uzbek
        self.list_ffmpeg_codes.append("vie")  # Vietnamese
        self.list_ffmpeg_codes.append("wel")  # Welsh
        self.list_ffmpeg_codes.append("xho")  # Xhosa
        self.list_ffmpeg_codes.append("yid")  # Yiddish
        self.list_ffmpeg_codes.append("yor")  # Yoruba
        self.list_ffmpeg_codes.append("zul")  # Zulu

        self.code_of_name = dict(zip(self.list_names, self.list_codes))
        self.code_of_ffmpeg_code = dict(zip(self.list_ffmpeg_codes, self.list_codes))

        self.name_of_code = dict(zip(self.list_codes, self.list_names))
        self.name_of_ffmpeg_code = dict(zip(self.list_ffmpeg_codes, self.list_names))

        self.ffmpeg_code_of_name = dict(zip(self.list_names, self.list_ffmpeg_codes))
        self.ffmpeg_code_of_code = dict(zip(self.list_codes, self.list_ffmpeg_codes))

        self.dict = {
                        'af': 'Afrikaans',
                        'sq': 'Albanian',
                        'am': 'Amharic',
                        'ar': 'Arabic',
                        'hy': 'Armenian',
                        'as': 'Assamese',
                        'ay': 'Aymara',
                        'az': 'Azerbaijani',
                        'bm': 'Bambara',
                        'eu': 'Basque',
                        'be': 'Belarusian',
                        'bn': 'Bengali',
                        'bho': 'Bhojpuri',
                        'bs': 'Bosnian',
                        'bg': 'Bulgarian',
                        'ca': 'Catalan',
                        'ceb': 'Cebuano',
                        'ny': 'Chichewa',
                        'zh': 'Chinese',
                        'zh-CN': 'Chinese (Simplified)',
                        'zh-TW': 'Chinese (Traditional)',
                        'co': 'Corsican',
                        'hr': 'Croatian',
                        'cs': 'Czech',
                        'da': 'Danish',
                        'dv': 'Dhivehi',
                        'doi': 'Dogri',
                        'nl': 'Dutch',
                        'en': 'English',
                        'eo': 'Esperanto',
                        'et': 'Estonian',
                        'ee': 'Ewe',
                        'fil': 'Filipino',
                        'fi': 'Finnish',
                        'fr': 'French',
                        'fy': 'Frisian',
                        'gl': 'Galician',
                        'ka': 'Georgian',
                        'de': 'German',
                        'el': 'Greek',
                        'gn': 'Guarani',
                        'gu': 'Gujarati',
                        'ht': 'Haitian Creole',
                        'ha': 'Hausa',
                        'haw': 'Hawaiian',
                        'he': 'Hebrew',
                        'hi': 'Hindi',
                        'hmn': 'Hmong',
                        'hu': 'Hungarian',
                        'is': 'Icelandic',
                        'ig': 'Igbo',
                        'ilo': 'Ilocano',
                        'id': 'Indonesian',
                        'ga': 'Irish',
                        'it': 'Italian',
                        'ja': 'Japanese',
                        'jv': 'Javanese',
                        'kn': 'Kannada',
                        'kk': 'Kazakh',
                        'km': 'Khmer',
                        'rw': 'Kinyarwanda',
                        'gom': 'Konkani',
                        'ko': 'Korean',
                        'kri': 'Krio',
                        'kmr': 'Kurdish (Kurmanji)',
                        'ckb': 'Kurdish (Sorani)',
                        'ky': 'Kyrgyz',
                        'lo': 'Lao',
                        'la': 'Latin',
                        'lv': 'Latvian',
                        'ln': 'Lingala',
                        'lt': 'Lithuanian',
                        'lg': 'Luganda',
                        'lb': 'Luxembourgish',
                        'mk': 'Macedonian',
                        'mg': 'Malagasy',
                        'ms': 'Malay',
                        'ml': 'Malayalam',
                        'mt': 'Maltese',
                        'mi': 'Maori',
                        'mr': 'Marathi',
                        'mni-Mtei': 'Meiteilon (Manipuri)',
                        'lus': 'Mizo',
                        'mn': 'Mongolian',
                        'my': 'Myanmar (Burmese)',
                        'ne': 'Nepali',
                        'no': 'Norwegian',
                        'or': 'Odiya (Oriya)',
                        'om': 'Oromo',
                        'ps': 'Pashto',
                        'fa': 'Persian',
                        'pl': 'Polish',
                        'pt': 'Portuguese',
                        'pa': 'Punjabi',
                        'qu': 'Quechua',
                        'ro': 'Romanian',
                        'ru': 'Russian',
                        'sm': 'Samoan',
                        'sa': 'Sanskrit',
                        'gd': 'Scots Gaelic',
                        'nso': 'Sepedi',
                        'sr': 'Serbian',
                        'st': 'Sesotho',
                        'sn': 'Shona',
                        'sd': 'Sindhi',
                        'si': 'Sinhala',
                        'sk': 'Slovak',
                        'sl': 'Slovenian',
                        'so': 'Somali',
                        'es': 'Spanish',
                        'su': 'Sundanese',
                        'sw': 'Swahili',
                        'sv': 'Swedish',
                        'tg': 'Tajik',
                        'ta': 'Tamil',
                        'tt': 'Tatar',
                        'te': 'Telugu',
                        'th': 'Thai',
                        'ti': 'Tigrinya',
                        'ts': 'Tsonga',
                        'tr': 'Turkish',
                        'tk': 'Turkmen',
                        'tw': 'Twi (Akan)',
                        'uk': 'Ukrainian',
                        'ur': 'Urdu',
                        'ug': 'Uyghur',
                        'uz': 'Uzbek',
                        'vi': 'Vietnamese',
                        'cy': 'Welsh',
                        'xh': 'Xhosa',
                        'yi': 'Yiddish',
                        'yo': 'Yoruba',
                        'zu': 'Zulu',
                    }

        self.ffmpeg_dict = {
                                'af': 'afr', # Afrikaans
                                'sq': 'alb', # Albanian
                                'am': 'amh', # Amharic
                                'ar': 'ara', # Arabic
                                'hy': 'arm', # Armenian
                                'as': 'asm', # Assamese
                                'ay': 'aym', # Aymara
                                'az': 'aze', # Azerbaijani
                                'bm': 'bam', # Bambara
                                'eu': 'baq', # Basque
                                'be': 'bel', # Belarusian
                                'bn': 'ben', # Bengali
                                'bho': 'bho', # Bhojpuri
                                'bs': 'bos', # Bosnian
                                'bg': 'bul', # Bulgarian
                                'ca': 'cat', # Catalan
                                'ceb': 'ceb', # Cebuano
                                'ny': 'nya', # Chichewa
                                'zh': 'chi', # Chinese
                                'zh-CN': 'chi', # Chinese (Simplified)
                                'zh-TW': 'chi', # Chinese (Traditional)
                                'co': 'cos', # Corsican
                                'hr': 'hrv', # Croatian
                                'cs': 'cze', # Czech
                                'da': 'dan', # Danish
                                'dv': 'div', # Dhivehi
                                'doi': 'doi', # Dogri
                                'nl': 'dut', # Dutch
                                'en': 'eng', # English
                                'eo': 'epo', # Esperanto
                                'et': 'est', # Estonian
                                'ee': 'ewe', # Ewe
                                'fil': 'fil', # Filipino
                                'fi': 'fin', # Finnish
                                'fr': 'fre', # French
                                'fy': 'fry', # Frisian
                                'gl': 'glg', # Galician
                                'ka': 'geo', # Georgian
                                'de': 'ger', # German
                                'el': 'gre', # Greek
                                'gn': 'grn', # Guarani
                                'gu': 'guj', # Gujarati
                                'ht': 'hat', # Haitian Creole
                                'ha': 'hau', # Hausa
                                'haw': 'haw', # Hawaiian
                                'he': 'heb', # Hebrew
                                'hi': 'hin', # Hindi
                                'hmn': 'hmn', # Hmong
                                'hu': 'hun', # Hungarian
                                'is': 'ice', # Icelandic
                                'ig': 'ibo', # Igbo
                                'ilo': 'ilo', # Ilocano
                                'id': 'ind', # Indonesian
                                'ga': 'gle', # Irish
                                'it': 'ita', # Italian
                                'ja': 'jpn', # Japanese
                                'jv': 'jav', # Javanese
                                'kn': 'kan', # Kannada
                                'kk': 'kaz', # Kazakh
                                'km': 'khm', # Khmer
                                'rw': 'kin', # Kinyarwanda
                                'gom': 'kok', # Konkani
                                'ko': 'kor', # Korean
                                'kri': 'kri', # Krio
                                'kmr': 'kur', # Kurdish (Kurmanji)
                                'ckb': 'kur', # Kurdish (Sorani)
                                'ky': 'kir', # Kyrgyz
                                'lo': 'lao', # Lao
                                'la': 'lat', # Latin
                                'lv': 'lav', # Latvian
                                'ln': 'lin', # Lingala
                                'lt': 'lit', # Lithuanian
                                'lg': 'lug', # Luganda
                                'lb': 'ltz', # Luxembourgish
                                'mk': 'mac', # Macedonian
                                'mg': 'mlg', # Malagasy
                                'ms': 'may', # Malay
                                'ml': 'mal', # Malayalam
                                'mt': 'mlt', # Maltese
                                'mi': 'mao', # Maori
                                'mr': 'mar', # Marathi
                                'mni-Mtei': 'mni', # Meiteilon (Manipuri)
                                'lus': 'lus', # Mizo
                                'mn': 'mon', # Mongolian
                                'my': 'bur', # Myanmar (Burmese)
                                'ne': 'nep', # Nepali
                                'no': 'nor', # Norwegian
                                'or': 'ori', # Odiya (Oriya)
                                'om': 'orm', # Oromo
                                'ps': 'pus', # Pashto
                                'fa': 'per', # Persian
                                'pl': 'pol', # Polish
                                'pt': 'por', # Portuguese
                                'pa': 'pan', # Punjabi
                                'qu': 'que', # Quechua
                                'ro': 'rum', # Romanian
                                'ru': 'rus', # Russian
                                'sm': 'smo', # Samoan
                                'sa': 'san', # Sanskrit
                                'gd': 'gla', # Scots Gaelic
                                'nso': 'nso', # Sepedi
                                'sr': 'srp', # Serbian
                                'st': 'sot', # Sesotho
                                'sn': 'sna', # Shona
                                'sd': 'snd', # Sindhi
                                'si': 'sin', # Sinhala
                                'sk': 'slo', # Slovak
                                'sl': 'slv', # Slovenian
                                'so': 'som', # Somali
                                'es': 'spa', # Spanish
                                'su': 'sun', # Sundanese
                                'sw': 'swa', # Swahili
                                'sv': 'swe', # Swedish
                                'tg': 'tgk', # Tajik
                                'ta': 'tam', # Tamil
                                'tt': 'tat', # Tatar
                                'te': 'tel', # Telugu
                                'th': 'tha', # Thai
                                'ti': 'tir', # Tigrinya
                                'ts': 'tso', # Tsonga
                                'tr': 'tur', # Turkish
                                'tk': 'tuk', # Turkmen
                                'tw': 'twi', # Twi (Akan)
                                'uk': 'ukr', # Ukrainian
                                'ur': 'urd', # Urdu
                                'ug': 'uig', # Uyghur
                                'uz': 'uzb', # Uzbek
                                'vi': 'vie', # Vietnamese
                                'cy': 'wel', # Welsh
                                'xh': 'xho', # Xhosa
                                'yi': 'yid', # Yiddish
                                'yo': 'yor', # Yoruba
                                'zu': 'zul', # Zulu
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
    def __init__(self, src, dst, patience=-1, timeout=30, error_messages_callback=None):
        self.src = src
        self.dst = dst
        self.patience = patience
        self.timeout = timeout
        self.error_messages_callback = error_messages_callback

    def __call__(self, sentence):
        try:
            translated_sentence = []
            # handle the special case: empty string.
            if not sentence:
                return None
            translated_sentence = self.GoogleTranslate(sentence, src=self.src, dst=self.dst, timeout=self.timeout)
            fail_to_translate = translated_sentence[-1] == '\n'
            while fail_to_translate and patience:
                translated_sentence = self.GoogleTranslate(translated_sentence, src=self.src, dst=self.dst, timeout=self.timeout).text
                if translated_sentence[-1] == '\n':
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
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return

    def GoogleTranslate(self, text, src, dst, timeout=30):
        url = 'https://translate.googleapis.com/translate_a/'
        params = 'single?client=gtx&sl='+src+'&tl='+dst+'&dt=t&q='+text;
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Referer': 'https://translate.google.com',}

        try:
            response = requests.get(url+params, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                response_json = response.json()[0]
                length = len(response_json)
                translation = ""
                for i in range(length):
                    translation = translation + response_json[i][0]
                return translation
            return

        except requests.exceptions.ConnectionError:
            with httpx.Client() as client:
                response = client.get(url+params, headers=headers, timeout=self.timeout)
                if response.status_code == 200:
                    response_json = response.json()[0]
                    length = len(response_json)
                    translation = ""
                    for i in range(length):
                        translation = translation + response_json[i][0]
                    return translation
                return

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class SubtitleFormatter:
    supported_formats = ['srt', 'vtt', 'json', 'raw']

    def __init__(self, format_type, error_messages_callback=None):
        self.format_type = format_type.lower()
        self.error_messages_callback = error_messages_callback
        
    def __call__(self, subtitles, padding_before=0, padding_after=0):
        try:
            if self.format_type == 'srt':
                return self.srt_formatter(subtitles, padding_before, padding_after)
            elif self.format_type == 'vtt':
                return self.vtt_formatter(subtitles, padding_before, padding_after)
            elif self.format_type == 'json':
                return self.json_formatter(subtitles)
            elif self.format_type == 'raw':
                return self.raw_formatter(subtitles)
            else:
                if error_messages_callback:
                    error_messages_callback(f"Unsupported format type: '{self.format_type}'")
                else:
                    raise ValueError(f"Unsupported format type: '{self.format_type}'")

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return

    def srt_formatter(self, subtitles, padding_before=0, padding_after=0):
        """
        Serialize a list of subtitles according to the SRT format, with optional time padding.
        """
        sub_rip_file = pysrt.SubRipFile()
        for i, ((start, end), text) in enumerate(subtitles, start=1):
            item = pysrt.SubRipItem()
            item.index = i
            item.text = six.text_type(text)
            item.start.seconds = max(0, start - padding_before)
            item.end.seconds = end + padding_after
            sub_rip_file.append(item)
        return '\n'.join(six.text_type(item) for item in sub_rip_file)

    def vtt_formatter(self, subtitles, padding_before=0, padding_after=0):
        """
        Serialize a list of subtitles according to the VTT format, with optional time padding.
        """
        text = self.srt_formatter(subtitles, padding_before, padding_after)
        text = 'WEBVTT\n\n' + text.replace(',', '.')
        return text

    def json_formatter(self, subtitles):
        """
        Serialize a list of subtitles as a JSON blob.
        """
        subtitle_dicts = [
            {
                'start': start,
                'end': end,
                'content': text,
            }
            for ((start, end), text)
            in subtitles
        ]
        return json.dumps(subtitle_dicts)

    def raw_formatter(self, subtitles):
        """
        Serialize a list of subtitles as a newline-delimited string.
        """
        return ' '.join(text for (_rng, text) in subtitles)


class SubtitleWriter:
    def __init__(self, regions, transcripts, format, error_messages_callback=None):
        self.regions = regions
        self.transcripts = transcripts
        self.format = format
        self.timed_subtitles = [(r, t) for r, t in zip(self.regions, self.transcripts) if t]
        self.error_messages_callback = error_messages_callback

    def get_timed_subtitles(self):
        return self.timed_subtitles

    def write(self, declared_subtitle_filepath):
        try:
            formatter = SubtitleFormatter(self.format)
            formatted_subtitles = formatter(self.timed_subtitles)
            saved_subtitle_filepath = declared_subtitle_filepath
            if saved_subtitle_filepath:
                subtitle_file_base, subtitle_file_ext = os.path.splitext(saved_subtitle_filepath)
                if not subtitle_file_ext:
                    saved_subtitle_filepath = f"{subtitle_file_base}.{self.format}"
                else:
                    saved_subtitle_filepath = declared_subtitle_filepath
            with open(saved_subtitle_filepath, 'wb') as f:
                f.write(formatted_subtitles.encode("utf-8"))

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class SRTFileReader:
    def __init__(self, error_messages_callback=None):
        self.error_messages_callback = error_messages_callback
        self.timed_subtitles = []

    def __call__(self, subtitle_file_path):
        try:
            """
            Read SRT formatted subtitles file and return subtitles as list of tuples
            """
            with open(subtitle_file_path, 'r') as srt_file:
                lines = srt_file.readlines()
                # Split the subtitles file into subtitles blocks
                subtitle_blocks = []
                block = []
                for line in lines:
                    if line.strip() == '':
                        subtitle_blocks.append(block)
                        block = []
                    else:
                        block.append(line.strip())
                subtitle_blocks.append(block)

                # Parse each subtitles block and store as tuple in timed_subtitles list
                for block in subtitle_blocks:
                    if block:
                        # Extract start and end times from subtitles block
                        start_time_str, end_time_str = block[1].split(' --> ')
                        time_format = '%H:%M:%S,%f'
                        start_time_time_delta = datetime.strptime(start_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                        start_time_total_seconds = start_time_time_delta.total_seconds()
                        end_time_time_delta = datetime.strptime(end_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                        end_time_total_seconds = end_time_time_delta.total_seconds()
                        # Extract subtitles text from subtitles block
                        subtitles = ' '.join(block[2:])
                        self.timed_subtitles.append(((start_time_total_seconds, end_time_total_seconds), subtitles))
                return self.timed_subtitles

        except FileNotFoundError:
            print(f"Subtitle file '{subtitle_file_path}' not found.")
            return []

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class JSONFileReader:
    def __init__(self, error_messages_callback=None):
        self.error_messages_callback = error_messages_callback
        self.timed_subtitles = []

    def format_time(self, decimal_time):
        hours = int(decimal_time // 3600)
        minutes = int((decimal_time % 3600) // 60)
        seconds = int(decimal_time % 60)
        milliseconds = int((decimal_time % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def __call__(self, subtitle_file_path):
        try:
            """
            Read JSON formatted subtitles file and return subtitles as list of tuples
            """
            with open(subtitle_file_path, 'r') as json_file:
                data = json.load(json_file)

                for entry in data:
                    start_time = entry.get("start", "")
                    start_time_str = self.format_time(start_time)

                    end_time = entry.get("end", "")
                    end_time_str = self.format_time(end_time)

                    subtitle_text = entry.get("content", "")

                    time_format = '%H:%M:%S,%f'
                    start_time_time_delta = datetime.strptime(start_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                    start_time_total_seconds = start_time_time_delta.total_seconds()
                    end_time_time_delta = datetime.strptime(end_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                    end_time_total_seconds = end_time_time_delta.total_seconds()

                    if start_time_str and end_time_str and subtitle_text:
                        #self.timed_subtitles.append(((start_time_str, end_time_str), subtitle_text))
                        self.timed_subtitles.append(((start_time_total_seconds, end_time_total_seconds), subtitle_text))

                return self.timed_subtitles

        except FileNotFoundError:
            print(f"Subtitle file '{subtitle_file_path}' not found.")
            return []

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class VTTFileReader:
    def __init__(self, error_messages_callback=None):
        self.error_messages_callback = error_messages_callback
        self.timed_subtitles = []

    def format_vtt_time(self, vtt_time):
        hours, minutes, seconds = map(float, vtt_time.replace(',', '.').split(':'))
        formatted_time = f"{int(hours):02}:{int(minutes):02}:{seconds:.3f}".replace(".", ",")
        return formatted_time

    def __call__(self, subtitle_file_path):
        try:
            """
            Read VTT formatted subtitles file and return subtitles as list of tuples
            """

            start_time = None
            end_time = None
            subtitle_blocks = []

            with open(subtitle_file_path, 'r') as vtt_file:
                lines = vtt_file.readlines()

                # Split the subtitles file into subtitles blocks
                subtitle_blocks = []
                block = []

                for line in lines:
                    line = line.strip()
                    if '-->' in line:
                        if start_time and end_time:
                            start_time_str = self.format_vtt_time(start_time)
                            end_time_str = self.format_vtt_time(end_time)
                            subtitle = ' '.join(subtitle_blocks)

                            time_format = '%H:%M:%S,%f'
                            start_time_time_delta = datetime.strptime(start_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                            start_time_total_seconds = start_time_time_delta.total_seconds()
                            end_time_time_delta = datetime.strptime(end_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                            end_time_total_seconds = end_time_time_delta.total_seconds()

                            #self.timed_subtitles.append(((start_time_str, end_time_str), subtitle))
                            self.timed_subtitles.append(((start_time_total_seconds, end_time_total_seconds), subtitle))

                        start_time, end_time = line.split('-->')
                        subtitle_blocks = []
                    elif line and not line.isdigit():  # Skip lines that contain only digits
                        subtitle_blocks.append(line)

                # Handle the last subtitle entry
                if start_time and end_time and subtitle_blocks:
                    start_time_str = self.format_vtt_time(start_time)
                    end_time_str = self.format_vtt_time(end_time)
                    subtitle = ' '.join(subtitle_blocks)

                    time_format = '%H:%M:%S,%f'
                    start_time_time_delta = datetime.strptime(start_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                    start_time_total_seconds = start_time_time_delta.total_seconds()
                    end_time_time_delta = datetime.strptime(end_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                    end_time_total_seconds = end_time_time_delta.total_seconds()

                    #self.timed_subtitles.append(((start_time_str, end_time_str), subtitle))
                    self.timed_subtitles.append(((start_time_total_seconds, end_time_total_seconds), subtitle))

                return self.timed_subtitles

        except FileNotFoundError:
            print(f"Subtitle file '{subtitle_file_path}' not found.")
            return []

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class RAWFileReader:
    def __init__(self, error_messages_callback=None):
        self.error_messages_callback = error_messages_callback
        self.timed_subtitles = []

    def __call__(self, subtitle_file_path):
        try:
            """
            Read RAW formatted subtitles file and return subtitles as list of tuples
            """
            with open(subtitle_file_path, 'r') as raw_file:
                lines = raw_file.readlines()
                # Split the subtitles file into subtitles blocks
                subtitle_blocks = []
                block = []
                for line in lines:
                    if line.strip() == '':
                        subtitle_blocks.append(block)
                        #print("subtitle_blocks = ",  subtitle_blocks)
                        block = []
                    else:
                        block.append(line.strip())
                        #print("block = ",  block)
                subtitle_blocks.append(block)
                #print("subtitle_blocks = ",  subtitle_blocks)

                # Parse each subtitles block and store as tuple in timed_subtitles list
                for block in subtitle_blocks:
                    if block:
                        # Extract subtitles text from subtitles block
                        start_time_total_seconds = 0
                        end_time_total_seconds = 0
                        subtitles = ' '.join(block)
                        #print("subtitles =", subtitles)
                        #self.timed_subtitles.append((subtitles))
                        self.timed_subtitles.append(((start_time_total_seconds, end_time_total_seconds), subtitles))
                return self.timed_subtitles

        except FileNotFoundError:
            print(f"Subtitle file '{file_path}' not found.")
            return []

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


def is_same_language(src, dst, error_messages_callback=None):
    try:
        return src.split("-")[0] == dst.split("-")[0]
    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return


def show_error_messages(messages):
    print(messages)


def is_valid_subtitle_file(subtitle_filepath, error_messages_callback=None):
    base, ext = os.path.splitext(subtitle_filepath)
    timed_subtitles = []
    is_valid_subtitle = False

    if "\\" in subtitle_filepath:
        subtitle_filepath = subtitle_filepath.replace("\\", "/")

    if not os.path.isfile(subtitle_filepath):
        if error_messages_callback:
           error_messages_callback(f"The given file does not exist: '{subtitle_filepath}'")
        else:
            print(f"The given file does not exist: '{subtitle_filepath}'")
            raise Exception(f"Invalid file: '{subtitle_filepath}'")

    if ext[1:] == "srt" or ext[1:] == "SRT":
        srt_reader = SRTFileReader()
        timed_subtitles = srt_reader(subtitle_filepath)
    elif ext[1:] == "vtt" or ext[1:] == "VTT":
        vtt_reader = VTTFileReader()
        timed_subtitles = vtt_reader(subtitle_filepath)
    elif ext[1:] == "json" or ext[1:] == "JSON":
        json_reader = JSONFileReader()
        timed_subtitles = json_reader(subtitle_filepath)
    elif ext[1:] == "raw" or ext[1:] == "RAW":
        raw_reader = RAWFileReader()
        timed_subtitles = raw_reader(subtitle_filepath)

    if timed_subtitles:
        #print(timed_subtitles)
        is_valid_subtitle = True
    else:
        is_valid_subtitle = False
    return is_valid_subtitle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('subtitle_file_path', help="Subtitle file path you want to translate (use wildcard for multiple files or separate them with a space character e.g. \"file 1.srt\" \"file 2.srt\")", nargs='*')
    parser.add_argument('-S', '--src-language', help="Language code of subtitle file you want to translate", default="en")
    parser.add_argument('-D', '--dst-language', help="Desired translation language code for the subtitles", default=None)
    parser.add_argument('-ll', '--list-languages', help="List all supported languages", action='store_true')
    parser.add_argument('-F', '--format', help="Desired subtitles file format", default="srt")
    parser.add_argument('-lf', '--list-formats', help="List all supported subtitles file formats", action='store_true')
    parser.add_argument('-C', '--concurrency', help="Number of concurrent API requests to make", type=int, default=10)
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    args = parser.parse_args()

    language = Language()

    if args.list_languages:
        print("List of supported languages:")
        for code, language in sorted(language.name_of_code.items()):
            print("%-8s : %s" %(code, language))
        return 0

    if args.src_language not in language.name_of_code.keys():
        print("Source language is not supported. Run with --list-languages to see all supported languages.")
        return 1

    if args.dst_language:
        if not args.dst_language in language.name_of_code.keys():
            print("Destination language is not supported. Run with --list-languages to see all supported languages.")
            return 1
        if not is_same_language(args.src_language, args.dst_language, error_messages_callback=show_error_messages):
            do_translate = True
        else:
            do_translate = False
    else:
        do_translate = False

    if args.list_formats:
        print("List of supported subtitle formats:")
        for subtitle_format in SubtitleFormatter.supported_formats:
            print(f"{subtitle_format}")
        return 0

    if args.format not in SubtitleFormatter.supported_formats:
        print("Subtitle format is not supported. Run with --list-formats to see all supported formats.")
        return 1

    if not args.subtitle_file_path:
        parser.print_help(sys.stderr)
        return 1

    completed_tasks = 0
    subtitle_filepaths = []
    arg_filepaths = []
    invalid_subtitle_filepaths = []
    not_exist_subtitle_filepaths = []
    argpath = None
    args_subtitle_file_path = args.subtitle_file_path

    if (not "*" in str(args_subtitle_file_path)) and (not "?" in str(args_subtitle_file_path)):
        for filepath in args_subtitle_file_path:
            fpath = Path(filepath)
            #print("fpath = %s" %fpath)
            if not os.path.isfile(fpath):
                not_exist_subtitle_filepaths.append(filepath)
                #print(str(fpath) + " is not exist")

    if sys.platform == "win32":
        for i in range(len(args.subtitle_file_path)):
            if ("[" or "]") in args.subtitle_file_path[i]:
                placeholder = "#TEMP#"
                args_subtitle_file_path[i] = args.subtitle_file_path[i].replace("[", placeholder)
                args_subtitle_file_path[i] = args_subtitle_file_path[i].replace("]", "[]]")
                args_subtitle_file_path[i] = args_subtitle_file_path[i].replace(placeholder, "[[]")
                #print("args_subtitle_file_path = %s" %(args_subtitle_file_path))

    for arg in args_subtitle_file_path:
        if not sys.platform == "win32" :
            arg = escape(arg)

        #print("glob(arg) = %s" %(glob(arg)))

        arg_filepaths += glob(arg)
        #print("arg_filepaths = %s" %(arg_filepaths))

    if arg_filepaths:
        for argpath in arg_filepaths:
            #print("argpath = ", argpath)
            if os.path.isfile(argpath):
                if is_valid_subtitle_file(argpath, error_messages_callback=show_error_messages) == True:
                    subtitle_filepaths.append(argpath)
                else:
                    invalid_subtitle_filepaths.append(argpath)
            else:
                not_exist_subtitle_filepaths.append(argpath)

        if invalid_subtitle_filepaths:
            for invalid_subtitle_filepath in invalid_subtitle_filepaths:
                msg = f"'{invalid_subtitle_filepath}' is not valid subtitle files"
                print(msg)

    #print("not_exist_subtitle_filepaths = %s" %(not_exist_subtitle_filepaths))

    if not_exist_subtitle_filepaths:
        if (not "*" in str(args_subtitle_file_path)) and (not "?" in str(args_subtitle_file_path)):
            for not_exist_subtitle_filepaths in not_exist_subtitle_filepaths:
                msg = f"'{not_exist_subtitle_filepaths}' is not exist"
                print(msg)
                sys.exit(0)

    if not arg_filepaths and not not_exist_subtitle_filepaths:
        print("No any files matching filenames you typed")
        sys.exit(0)

    subtitle_format = args.format

    translate_end_time = None
    translate_elapsed_time = None
    translate_start_time = time.time()

    #print("subtitle_filepaths = ", subtitle_filepaths)

    for subtitle_filepath in subtitle_filepaths:
        print(f"Processing '{subtitle_filepath}'")
        base, ext = os.path.splitext(subtitle_filepath)
        timed_subtitles = []

        if ext[1:] == "srt" or ext[1:] == "SRT":
            srt_reader = SRTFileReader()
            timed_subtitles = srt_reader(subtitle_filepath)
        elif ext[1:] == "vtt" or ext[1:] == "VTT":
            vtt_reader = VTTFileReader()
            timed_subtitles = vtt_reader(subtitle_filepath)
        elif ext[1:] == "json" or ext[1:] == "JSON":
            json_reader = JSONFileReader()
            timed_subtitles = json_reader(subtitle_filepath)
        elif ext[1:] == "raw" or ext[1:] == "RAW":
            raw_reader = RAWFileReader()
            timed_subtitles = raw_reader(subtitle_filepath)

        #print("timed_subtitles = ", timed_subtitles)

        regions = []
        transcripts = []

        for entry in timed_subtitles:
            regions.append(entry[0])
            transcripts.append(entry[1])

        if do_translate == True:

            if timed_subtitles and ext[1:] != ("raw" or "RAW"):
                prompt = "Translating from %s to %s   : " %(args.src_language.center(8), args.dst_language.center(8))
                widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
                pbar = ProgressBar(widgets=widgets, maxval=len(timed_subtitles)).start()

                transcript_translator = SentenceTranslator(src=args.src_language, dst=args.dst_language, error_messages_callback=show_error_messages)

                pool = multiprocessing.Pool(args.concurrency)

                translated_transcripts = []
                for i, translated_transcript in enumerate(pool.imap(transcript_translator, transcripts)):
                    translated_transcripts.append(translated_transcript)
                    pbar.update(i)
                pbar.finish()

                dst_subtitle_filepath = f"{base}.{args.dst_language}.{subtitle_format}"

                translation_writer = SubtitleWriter(regions, translated_transcripts, subtitle_format, error_messages_callback=show_error_messages)
                translation_writer.write(dst_subtitle_filepath)

                print(f"Translated subtitles file saved as      : '{dst_subtitle_filepath}'")
                print("")

                completed_tasks += 1

            elif timed_subtitles and ext[1:] == ("raw" or "RAW"):
                if args.format and args.format != "raw":
                    print(f"Cannot convert raw subtitle format to %s format, subtitle file will be saved in raw format" %args.format)

                prompt = "Translating from %s to %s   : " %(args.src_language.center(8), args.dst_language.center(8))
                widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
                pbar = ProgressBar(widgets=widgets, maxval=len(timed_subtitles)).start()

                subtitle_format = "raw"
                transcript_translator = SentenceTranslator(src=args.src_language, dst=args.dst_language, error_messages_callback=show_error_messages)

                pool = multiprocessing.Pool(args.concurrency)

                translated_transcripts = []
                for i, translated_transcript in enumerate(pool.imap(transcript_translator, transcripts)):
                    translated_transcripts.append(translated_transcript)
                    pbar.update(i)
                pbar.finish()

                dst_subtitle_filepath = f"{base}.{args.dst_language}.{subtitle_format}"

                translation_writer = SubtitleWriter(regions, translated_transcripts, subtitle_format, error_messages_callback=show_error_messages)
                translation_writer.write(dst_subtitle_filepath)

                print(f"Translated subtitles file saved as      : '{dst_subtitle_filepath}'")
                print("")

                completed_tasks += 1

            else:
                sys.exit(1)

        else:
            if ext[1:] == subtitle_format:
                if timed_subtitles:
                    print("Nothing to do")
                    sys.exit(1)
                else:
                    sys.exit(1)
            else:
                dst_subtitle_filepath = f"{base}.{subtitle_format}"

                writer = SubtitleWriter(regions, transcripts, subtitle_format, error_messages_callback=show_error_messages)
                writer.write(dst_subtitle_filepath)

                print(f"Subtitles file saved as      : '{dst_subtitle_filepath}'")
                print("")

                completed_tasks += 1

    if len(subtitle_filepaths)>0 and completed_tasks == len(subtitle_filepaths):
        translate_end_time = time.time()
        translate_elapsed_time = translate_end_time - translate_start_time
        translate_elapsed_time_seconds = timedelta(seconds=int(translate_elapsed_time))
        translate_elapsed_time_str = str(translate_elapsed_time_seconds)
        hour, minute, second = translate_elapsed_time_str.split(":")
        msg = "Total running time                      : %s:%s:%s" %(hour.zfill(2), minute, second)
        print(msg)

if __name__ == '__main__':
    sys.exit(main())
