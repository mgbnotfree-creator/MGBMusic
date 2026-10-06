# ═══════════════════════════════════════════════════════════════
#                     🎵 MGB NOT FREE CODER
#
#                   © 2026 MGB NOT FREE CODER
#
#                Developed with ❤️ by MGB Not Free Coder
#
#             Do not remove or alter the original credits.
#
#           Copyright © 2026 MGB Not Free Coder. All rights reserved.
# ═══════════════════════════════════════════════════════════════

import asyncio
import logging
import random
import re
from collections import deque
from typing import Dict, List, Optional

import config
from py_yt import VideosSearch

from ShizuMusic.core.queue import add_to_queue, get_queue
from ShizuMusic.utils.db import (
    get_autoplay_lang as _db_get_lang,
    get_autoplay_mood as _db_get_mood,
    is_autoplay_enabled as _db_get_enabled,
    set_autoplay_enabled as _db_set_enabled,
    set_autoplay_lang as _db_set_lang,
    set_autoplay_mood as _db_set_mood,
)
from ShizuMusic.utils.formatters import iso_to_human, iso_to_sec, sec_to_iso
from ShizuMusic.utils.youtube import extract_video_id, related_videos

logger = logging.getLogger(__name__)
AUTOPLAY_TAG = "🔁 AutoPlay"

# ==========================================
# CONFIGURATION
# ==========================================
AUTOPLAY_BUFFER_SIZE = 6    
AUTOPLAY_MIN_BUFFER = 2  
HISTORY_SIZE = 80             
FETCH_TIMEOUT = 25  

# ==========================================
# STATE 
# ==========================================
_enabled: Dict[int, bool] = {}           
_buffer: Dict[int, List[dict]] = {}      
_history: Dict[int, deque] = {}          
_tasks: Dict[int, "asyncio.Task"] = {}  
_locks: Dict[int, asyncio.Lock] = {}   
_YT_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")

# ==========================================
# ON / OFF + LANG / MOOD 
# ==========================================
def is_autoplay(chat_id: int) -> bool:
    mode = _enabled.get(chat_id)
    if mode is not None:
        return mode
    mode = _db_get_enabled(chat_id)
    _enabled[chat_id] = mode
    return mode


def get_autoplay_lang(chat_id: int) -> str:
    return _db_get_lang(chat_id) or "auto"


def set_autoplay_lang(chat_id: int, lang: str) -> None:
    _db_set_lang(chat_id, lang)


def get_autoplay_mood(chat_id: int) -> str:
    return _db_get_mood(chat_id) or "any"


def set_autoplay_mood(chat_id: int, mood: str) -> None:
    _db_set_mood(chat_id, mood)


def start_autoplay(chat_id: int) -> None:
    """Turn AutoPlay ON for this chat."""
    _enabled[chat_id] = True
    _db_set_enabled(chat_id, True)
    current = get_queue(chat_id)
    if current:
        schedule_prefetch(chat_id, current[0])


def stop_autoplay(chat_id: int) -> None:
    """Turn AutoPlay OFF for this chat — only /autoplay off (or the toggle) calls this."""
    _enabled[chat_id] = False
    _db_set_enabled(chat_id, False)
    _buffer.pop(chat_id, None)


def reset_autoplay_state(chat_id: int) -> None:
    _buffer.pop(chat_id, None)
    task = _tasks.pop(chat_id, None)
    if task and not task.done():
        task.cancel()


def toggle_autoplay(chat_id: int) -> bool:
    enable = not is_autoplay(chat_id)
    if enable:
        start_autoplay(chat_id)
    else:
        stop_autoplay(chat_id)
    return enable


# ==========================================
# GLOBAL MUSIC DATABASE
# ==========================================
GLOBAL_MUSIC_DATABASE = {
    "hindi": {
        "romantic": [
            "Arijit Singh", "Shreya Ghoshal", "Jubin Nautiyal", "Armaan Malik", "T-Series",
            "Sonu Nigam", "KK", "Mohit Chauhan", "Atif Aslam", "Darshan Raval",
            "Vishal Mishra", "Asees Kaur", "Sunidhi Chauhan", "Monali Thakur",
            "Neeti Mohan", "Palak Muchhal", "Sachet Tandon", "Parampara Tandon",
            "Papon", "Rahat Fateh Ali Khan", "Javed Ali", "Benny Dayal",
            "Mithoon", "Tulsi Kumar", "Arijit Singh Live", "Ankit Tiwari",
            "Shaan", "Abhijeet", "Udit Narayan", "Alka Yagnik",
            "Kumar Sanu", "Sadhana Sargam", "Hariharan", "Mahalakshmi Iyer",
            "Jonita Gandhi", "Arjun Kanungo", "Dhvani Bhanushali",
            "Yasser Desai", "Stebin Ben", "Armaan Bedil"
        ],
    
        "sad": [
            "Arijit Singh", "Jubin Nautiyal", "B Praak", "T-Series",
            "KK", "Atif Aslam", "Vishal Mishra", "Ankit Tiwari",
            "Sonu Nigam", "Rahat Fateh Ali Khan", "Mohit Chauhan",
            "Darshan Raval", "Papon", "Mithoon", "Armaan Malik",
            "Javed Ali", "Stebin Ben", "Yasser Desai", "Tulsi Kumar",
            "Palak Muchhal", "Asees Kaur", "Shreya Ghoshal",
            "Neeti Mohan", "Hariharan", "Shaan"
        ],
    
        "happy": [
            "Neha Kakkar", "Tony Kakkar", "Mika Singh", "Badshah", "T-Series",
            "Benny Dayal", "Sunidhi Chauhan", "Sukhbir", "Shaan",
            "Armaan Malik", "Dhvani Bhanushali", "Jonita Gandhi",
            "Vishal Dadlani", "Shankar Mahadevan", "Salim Merchant",
            "Jubin Nautiyal", "Tulsi Kumar", "Aastha Gill",
            "Guru Randhawa", "Meet Bros", "Kanika Kapoor"
        ],
    
        "party": [
            "Neha Kakkar", "Badshah", "Raftaar", "Yo Yo Honey Singh", "T-Series",
            "Mika Singh", "Aastha Gill", "Guru Randhawa",
            "Kanika Kapoor", "Meet Bros", "DJ Chetas",
            "Nakash Aziz", "Vishal Dadlani", "Benny Dayal",
            "Tony Kakkar", "Tanishk Bagchi", "Jasmine Sandlas",
            "Akhil", "Ikka", "Bohemia"
        ],
    
        "chill": [
            "Anuv Jain", "Prateek Kuhad", "Ritviz", "T-Series Acoustic",
            "When Chai Met Toast", "The Local Train",
            "Zaeden", "Anumita Nadesan", "Sanam",
            "Papon", "Raghav Chaitanya", "Ankur Tewari",
            "Arjun Kanungo", "Dhvani Bhanushali", "Jonita Gandhi",
            "Swarathma", "Easy Wanderlings"
        ],
    
        "workout": [
            "Badshah", "Raftaar", "Divine", "T-Series",
            "Yo Yo Honey Singh", "Emiway Bantai",
            "Ikka", "King", "Krsna",
            "MC Stan", "Seedhe Maut",
            "Brodha V", "Naezy", "Bohemia",
            "Fotty Seven", "Karma", "Bella"
        ],
    
        "bhajan": [
            "T-Series Bhakti Sagar", "Shemaroo Bhakti", "Gulshan Kumar",
            "Anuradha Paudwal", "Hariharan", "Lakhbir Singh Lakkha",
            "Narendra Chanchal", "Jaya Kishori", "Devi Chitralekha",
            "Sadhvi Purnima", "Kumar Vishu", "Suresh Wadkar",
            "Anup Jalota", "Jagjit Singh"
        ],
    
        "retro": [
            "Kishore Kumar", "Lata Mangeshkar",
            "Mohammed Rafi", "Asha Bhosle",
            "Mukesh", "Manna Dey",
            "Mahendra Kapoor", "Hemant Kumar",
            "Geeta Dutt", "Talat Mahmood",
            "Jagjit Singh", "Bhupinder Singh",
            "Yesudas", "Usha Mangeshkar"
        ],
    
        "rap": [
            "Divine", "Raftaar", "Badshah", "Emiway Bantai",
            "Krsna", "MC Stan", "Seedhe Maut",
            "Naezy", "King", "Ikka",
            "Bohemia", "Brodha V", "Fotty Seven",
            "Karma", "Bella", "EPR",
            "Muhfaad", "Young Stunners"
        ],
    
        "acoustic": [
            "Anuv Jain", "Prateek Kuhad", "Ritviz",
            "Sanam", "Papon", "When Chai Met Toast",
            "Easy Wanderlings", "Ankur Tewari",
            "Anumita Nadesan", "The Local Train",
            "Arjun Kanungo", "Raghav Chaitanya"
        ],
    
        "funk": [
            "Ritviz", "Nucleya", "When Chai Met Toast",
            "Parvaaz", "The Local Train",
            "Easy Wanderlings"
        ],
    
        "phonk": [
            "Kordhell", "MoonDeity", "Dxrk",
            "INTERWORLD", "DVRST",
            "Pharmacist", "Ghostface Playa"
        ]
    },
    "english": {
        "romantic": [
            "Alan Walker", "Ed Sheeran", "Taylor Swift", "John Legend", "Sam Smith", "Shawn Mendes", "Adele",
            "Charlie Puth", "James Arthur", "Lewis Capaldi", "Harry Styles", "Zayn",
            "Niall Horan", "One Direction", "Conan Gray", "Benson Boone",
            "Olivia Rodrigo", "Lana Del Rey", "The Weeknd", "Justin Bieber",
            "Selena Gomez", "Ariana Grande", "Bruno Mars", "Sia",
            "Dean Lewis", "Stephen Sanchez", "Calum Scott", "John Mayer",
            "Jason Mraz", "Passenger", "Damiano David", "Tate McRae",
            "Lauv", "Alec Benjamin", "Khalid", "Troye Sivan",
            "Westlife", "Backstreet Boys", "Boyz II Men", "Celine Dion"
        ],
    
        "sad": [
            "Billie Eilish", "Lewis Capaldi", "Olivia Rodrigo", "Halsey", "The Weeknd",
            "Adele", "James Arthur", "Dean Lewis", "Calum Scott",
            "Sam Smith", "Conan Gray", "Alec Benjamin", "Lana Del Rey",
            "Sia", "Passenger", "Birdy", "Christina Perri",
            "Demi Lovato", "Linkin Park", "Harry Styles",
            "Zayn", "Benson Boone", "Tate McRae", "Lewis Watson",
            "Tom Odell", "Sleeping At Last", "Cigarettes After Sex"
        ],
    
        "happy": [
            "Bruno Mars", "Pharrell Williams", "Justin Bieber", "Katy Perry", "Dua Lipa",
            "Taylor Swift", "Ed Sheeran", "Ariana Grande", "Selena Gomez",
            "OneRepublic", "Maroon 5", "Imagine Dragons", "Charlie Puth",
            "Meghan Trainor", "Jason Derulo", "Pitbull", "Flo Rida",
            "Bebe Rexha", "Ava Max", "Camila Cabello", "Shawn Mendes",
            "Jonas Brothers", "Panic! At The Disco", "Walk The Moon"
        ],
    
        "party": [
            "David Guetta", "Calvin Harris", "Marshmello", "Martin Garrix", "The Chainsmokers",
            "DJ Snake", "Tiesto", "Steve Aoki", "Kygo", "Alan Walker",
            "Avicii", "Zedd", "Skrillex", "Don Diablo",
            "Hardwell", "Afrojack", "Alesso", "R3HAB",
            "Dimitri Vegas & Like Mike", "Nicky Romero", "Joel Corry",
            "Robin Schulz", "Major Lazer", "Pitbull", "Flo Rida"
        ],
    
        "chill": [
            "Alan Walker", "Kygo", "Lofi Girl", "ChilledCow",
            "Lauv", "Alec Benjamin", "Khalid", "Joji",
            "Keshi", "Jeremy Zucker", "Powfu", "JVKE",
            "Ruth B", "Cigarettes After Sex", "Novo Amor",
            "Sleeping At Last", "BoyWithUke", "Rxseboy",
            "Sasha Alex Sloan", "Conan Gray"
        ],
    
        "workout": [
            "Eminem", "Imagine Dragons", "Post Malone", "Kanye West", "Travis Scott",
            "Drake", "50 Cent", "Jay-Z", "Kendrick Lamar",
            "Future", "Lil Wayne", "21 Savage", "Metro Boomin",
            "The Weeknd", "Linkin Park", "Fall Out Boy",
            "Skillet", "NF", "Logic", "Machine Gun Kelly",
            "Denzel Curry", "A$AP Rocky", "DMX"
        ],
    
        "bhajan": [
            "Gregorian Chants", "Christian Worship Music", "Hillsong Worship",
            "Elevation Worship", "Bethel Music", "Chris Tomlin",
            "Don Moen", "Matt Redman", "Phil Wickham"
        ],
    
        "retro": [
            "Michael Jackson", "Queen", "The Beatles", "Elton John", "Madonna",
            "Whitney Houston", "George Michael", "ABBA", "Bee Gees",
            "Frank Sinatra", "Elvis Presley", "Billy Joel",
            "Bon Jovi", "Journey", "The Rolling Stones",
            "Eagles", "Fleetwood Mac", "Prince",
            "Lionel Richie", "Tina Turner", "Phil Collins",
            "Rod Stewart", "Chicago", "Earth, Wind & Fire"
        ],
    
        "rap": [
            "Eminem", "Drake", "Kendrick Lamar", "Jay-Z", "Travis Scott",
            "J. Cole", "Future", "Lil Wayne", "50 Cent",
            "21 Savage", "Logic", "NF", "A$AP Rocky",
            "Tyler, The Creator", "Snoop Dogg", "Tupac",
            "The Notorious B.I.G.", "Nas", "Joey Bada$$",
            "Denzel Curry", "Cordae", "Machine Gun Kelly",
            "Jack Harlow", "Juice WRLD", "Pop Smoke"
        ],
    
        "acoustic": [
            "Ed Sheeran", "John Mayer", "James Arthur", "Lewis Capaldi",
            "Passenger", "Jason Mraz", "Damien Rice",
            "Alec Benjamin", "Dean Lewis", "Calum Scott",
            "Shawn Mendes", "Harry Styles", "Niall Horan",
            "Birdy", "Vance Joy", "Ben Howard",
            "George Ezra", "Tom Odell", "Hozier"
        ],
    
        "funk": [
            "Bruno Mars", "Anderson .Paak", "Vulf", "Jamiroquai",
            "Earth, Wind & Fire", "Stevie Wonder", "Prince",
            "Parliament Funkadelic", "Kool & The Gang",
            "Chic", "Tower of Power", "The Brothers Johnson",
            "Daft Punk", "Silk Sonic"
        ],
    
        "phonk": [
            "Kordhell", "MoonDeity", "Dxrk", "Phonk Music",
            "DVRST", "INTERWORLD", "Ghostface Playa",
            "Pharmacist", "Sxmpra", "RAIZHELL",
            "KSLV Noh", "MC ORSEN", "DJ Smokey",
            "DJ Sacred", "Sadfriendd", "Mupp"
        ]
    },
    "punjabi": {
        "romantic": [
            "Guru Randhawa", "Diljit Dosanjh", "Hardy Sandhu", "Neha Kakkar",
            "Jass Manak", "Ammy Virk", "Karan Aujla", "AP Dhillon",
            "Shubh", "Maninder Buttar", "Jassie Gill", "Akhil",
            "Parmish Verma", "Ninja", "Jordan Sandhu", "Gurnam Bhullar",
            "Ranjit Bawa", "Kaka", "Satinder Sartaaj", "B Praak",
            "Gurinder Gill", "Shinda Kahlon", "Arjan Dhillon",
            "Amrinder Gill", "Harbhajan Mann", "Kamal Khan",
            "Rahat Fateh Ali Khan", "Afsana Khan", "Jasmine Sandlas",
            "Shipra Goyal", "Sunanda Sharma", "Nimrat Khaira",
            "Khan Bhaini", "R Nait", "Prem Dhillon", "A Kay"
        ],
    
        "sad": [
            "Sidhu Moose Wala", "B Praak", "Jass Manak", "Karan Aujla",
            "Kaka", "Amrinder Gill", "Satinder Sartaaj", "Ninja",
            "Afsana Khan", "R Nait", "Khan Bhaini", "Prem Dhillon",
            "Gurnam Bhullar", "Ammy Virk", "Arjan Dhillon",
            "Maninder Buttar", "Akhil", "Jassie Gill",
            "Harbhajan Mann", "Kamal Khan", "Rahat Fateh Ali Khan",
            "Shubh", "AP Dhillon", "Gurinder Gill"
        ],
    
        "happy": [
            "Diljit Dosanjh", "Guru Randhawa", "Mankirt Aulakh", "Ninja",
            "Ammy Virk", "Gippy Grewal", "Parmish Verma",
            "Jassie Gill", "Akhil", "Jordan Sandhu",
            "Gurnam Bhullar", "Amrinder Gill", "Sharry Mann",
            "Karan Sehmbi", "Jass Bajwa", "Ranjit Bawa",
            "Kaka", "Sunanda Sharma", "Nimrat Khaira",
            "Shipra Goyal", "Afsana Khan"
        ],
    
        "party": [
            "Badshah", "Raftaar", "Mika Singh", "Gippy Grewal",
            "Diljit Dosanjh", "Guru Randhawa", "Yo Yo Honey Singh",
            "Parmish Verma", "Mankirt Aulakh", "Jassie Gill",
            "Jass Manak", "Sharry Mann", "Jordan Sandhu",
            "Ammy Virk", "Karan Aujla", "AP Dhillon",
            "Shubh", "Bohemia", "Ikka", "Jasmine Sandlas",
            "Aastha Gill", "Navaan Sandhu", "Cheema Y"
        ],
    
        "chill": [
            "AP Dhillon", "Shinda Kahlon", "Gurinder Gill",
            "Shubh", "Karan Aujla", "Amrinder Gill",
            "Satinder Sartaaj", "Kaka", "Akhil",
            "Maninder Buttar", "Prem Dhillon", "Arjan Dhillon",
            "Navaan Sandhu", "Jordan Sandhu", "Ninja",
            "Harnoor", "Talwiinder", "Zehr Vibe"
        ],
    
        "workout": [
            "Sidhu Moose Wala", "Karan Aujla", "Diljit Dosanjh",
            "Shubh", "AP Dhillon", "Parmish Verma",
            "Mankirt Aulakh", "Navaan Sandhu", "Prem Dhillon",
            "Khan Bhaini", "R Nait", "Arjan Dhillon",
            "Bohemia", "Badshah", "Raftaar",
            "Ikka", "Cheema Y", "Gur Sidhu"
        ],
    
        "bhajan": [
            "Bhai Harjinder Singh", "Shemaroo Bhakti",
            "Bhai Jujhar Singh", "Bhai Ravinder Singh",
            "Bhai Onkar Singh", "Bhai Satvinder Singh",
            "Bhai Balwinder Singh", "Bhai Sarabjit Singh",
            "Hazoori Ragi", "Gurbani Kirtan",
            "Bhai Chamanjit Singh", "Bhai Gurpreet Singh"
        ],
    
        "retro": [
            "Gurdas Maan", "Surinder Kaur", "Mohammed Rafi",
            "Kuldeep Manak", "Yamla Jatt", "Surjit Bindrakhia",
            "Amar Singh Chamkila", "Lal Chand Yamla Jatt",
            "K Deep", "Jagmohan Kaur", "Harbhajan Mann",
            "Hans Raj Hans", "Malkit Singh", "Sardool Sikander",
            "Asa Singh Mastana"
        ],
    
        "rap": [
            "Sidhu Moose Wala", "Karan Aujla", "Raftaar", "Divine",
            "Bohemia", "Badshah", "Ikka", "AP Dhillon",
            "Shubh", "Cheema Y", "Navaan Sandhu",
            "Yo Yo Honey Singh", "King", "MC Stan",
            "Krsna", "Seedhe Maut", "Emiway Bantai",
            "Talha Anjum", "Talhah Yunus"
        ],
    
        "acoustic": [
            "AP Dhillon", "Shinda Kahlon",
            "Gurinder Gill", "Amrinder Gill",
            "Satinder Sartaaj", "Kaka",
            "Akhil", "Maninder Buttar",
            "Harnoor", "Talwiinder",
            "Zehr Vibe", "Ninja"
        ],
    
        "funk": [
            "Brar Brothers", "Malkit Singh",
            "Punjabi MC", "Diljit Dosanjh",
            "Gippy Grewal", "Jazzy B",
            "Apache Indian", "Bally Sagoo"
        ],
    
        "phonk": [
            "Kordhell", "MoonDeity", "Dxrk",
            "DVRST", "INTERWORLD",
            "Ghostface Playa", "Pharmacist",
            "Sxmpra", "MC ORSEN"
        ]
    },
    "brazilian": {
        "romantic": [
            "Anitta", "Luan Santana", "Gusttavo Lima",
            "Jorge & Mateus", "Henrique & Juliano",
            "Marília Mendonça", "Zé Neto & Cristiano",
            "Maiara & Maraisa", "Matheus & Kauan",
            "Thiaguinho", "Sorriso Maroto",
            "Ferrugem", "Ludmilla", "Péricles",
            "Paula Fernandes", "Daniel", "Leonardo",
            "Michel Teló", "Luísa Sonza", "Melim",
            "Jão", "Vitor Kley", "Tiago Iorc",
            "Roupa Nova", "Fábio Jr."
        ],
    
        "sad": [
            "Marília Mendonça", "Jorge & Mateus",
            "Henrique & Juliano", "Maiara & Maraisa",
            "Zé Neto & Cristiano", "Matheus & Kauan",
            "Gusttavo Lima", "Luan Santana",
            "Tiago Iorc", "Jão", "Melim",
            "Paula Fernandes", "Ferrugem",
            "Péricles", "Sorriso Maroto",
            "Leonardo", "Daniel", "Ludmilla"
        ],
    
        "happy": [
            "Anitta", "Luan Santana", "Wesley Safadão",
            "Ludmilla", "Luísa Sonza", "Ivete Sangalo",
            "Michel Teló", "Thiaguinho",
            "Sorriso Maroto", "Ferrugem",
            "Melim", "Vitor Kley",
            "Jorge & Mateus", "Matheus & Kauan",
            "Dennis DJ", "Pedro Sampaio",
            "MC Kevinho", "Alok"
        ],
    
        "party": [
            "MC Kevinho", "Anitta", "Alok", "Dennis DJ",
            "Pedro Sampaio", "Ludmilla",
            "Luísa Sonza", "MC Hariel",
            "MC Ryan SP", "MC IG",
            "MC Cabelinho", "MC Paiva",
            "Wesley Safadão", "Ivete Sangalo",
            "Pedro Sampaio", "KVSH",
            "Vintage Culture", "Cat Dealers",
            "Dubdogz", "Bhaskar"
        ],
    
        "chill": [
            "Bossa Nova Music", "Tom Jobim",
            "Joao Gilberto", "Elis Regina",
            "Vinicius de Moraes",
            "Nara Leão", "Toquinho",
            "Tiago Iorc", "Melim",
            "Vitor Kley", "Jão",
            "Djavan", "Gilberto Gil",
            "Caetano Veloso"
        ],
    
        "workout": [
            "MC Kevinho", "Alok", "Brazilian Bass",
            "Vintage Culture", "Cat Dealers",
            "Dubdogz", "KVSH",
            "Pedro Sampaio", "MC Hariel",
            "MC Ryan SP", "MC IG",
            "MC Cabelinho", "Ludmilla",
            "Anitta", "Dennis DJ",
            "Matuê", "Orochi"
        ],
    
        "bhajan": [
            "Padre Marcelo Rossi",
            "Aline Barros",
            "Anderson Freire",
           
