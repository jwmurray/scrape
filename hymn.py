#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import json
import argparse

    

class hymn:
    def __init__(self, number, url, name):
        self.number = number
        self.url = url
        self.name = name

    @classmethod
    def from_hymn_p(cls, hymn_p):
        aref = hymn_p.find('a', class_='featurestext3')
        number = int(aref.text)
        url = aref['href']
        pattern = "([^\\\\]+)\\xa0"
        match = re.search(pattern, hymn_p.text)

        if match:
            name = match.group(1)
        else:
            name = 0
        return cls(number, url, name)


    def print(self):
        print(f"{self.number} {self.name} {self.url}")

    def print_hymn(self):
        verses = self.download_verses()
        print(self.name)
        print()
        for verse in verses:
            print(verse)
            print()
    
    def to_json(self):
        jsonstr = json.dumps(self.__dict__)
        return jsonstr


    def download_verses(self):
        verses = []
        r = requests.get(self.url)
    
        soup = BeautifulSoup(r.content, 'html.parser')

        s = soup.find_all('p', class_ = 'line')
        
        for index, paragraph in enumerate(s):
            verse_number = index + 1
            text = paragraph.get_text("\n").replace("\n\n", "\n")
            pattern = "^\\d+\\."
            match = re.match(pattern, text)
            if not match:
                text = f"{verse_number}. {text}"
            verses.append(text)
        return verses

        # hymns = {}

        # for hymn_p in s:
        #     aref = hymn_p.find('a', class_='featurestext3')
        #     h = hymn.from_hymn_p(hymn_p)
        #     hymns[h.number] = h
        #     continue
        
        # return hymns
    # Making a GET request
    # r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')


def download_hymns():
    r = requests.get('https://www.churchofjesuschrist.org/music/text/hymns?lang=eng')
  
    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find_all('p', class_ = 'Contents4')

    hymns = {}

    for hymn_p in s:
        aref = hymn_p.find('a', class_='featurestext3')
        h = hymn.from_hymn_p(hymn_p)
        hymns[h.number] = h
        continue
    return hymns

def print_hymns(hymns):
    for key in hymns:
        hymns[key].print()

def download_and_print():
    hymns = download_hymns()
    print_hymns(hymns)

def download_and_print_hymn(num):
    hymns = download_hymns()
    print_hymn(hymns, num)

def print_hymn(hymns, num):
    hymns[num].print()

def lambda_handler(event, context):
    hymns = download_hymns()
    hymn = hymns[event['number']]
    jsonstr = hymn.to_json()
    return jsonstr
    # hymn_number = event['hymn']
    # hymns = download_hymns()
    # hymns[hymn_number].print()

def create_hymn_database_code():
    hymns = download_hymns()
    print("def create_hymn_dictionary():")
    print("\thymns = {}")
    hymn_indices = sorted([index for index in hymns])
    for hymn_number in hymn_indices:
        print(f'\thymns[{hymn_number}] = hymn({hymn_number}, "{hymns[hymn_number].url}", "{hymns[hymn_number].name}")')
    print("\treturn hymns")




def test_handler():
    # hymns = download_hymns()
    # hymn = hymns[30]
    # jsonstr = hymn.to_json()
    event = {"number": 30}
    context = None
    jsonstr = lambda_handler(event, context)

    print(jsonstr)

def main():
    # hymns = create_hymn_database_code()

    parser = argparse.ArgumentParser(description="Get Verses for Hymns")
    
    parser.add_argument(
        'hymn_number', metavar='int', type=int,
        help='Hymn Number', default = 1, nargs='?')
    args = parser.parse_args()

    hymns = create_hymn_dictionary()
    hymn = hymns[args.hymn_number]
    hymn.print_hymn()

def create_hymn_dictionary():
        hymns = {}
        hymns[1] = hymn(1, "https://www.churchofjesuschrist.org/music/text/hymns/the-morning-breaks?lang=eng", "The Morning Breaks")
        hymns[2] = hymn(2, "https://www.churchofjesuschrist.org/music/text/hymns/the-spirit-of-god?lang=eng", "The Spirit of God")
        hymns[3] = hymn(3, "https://www.churchofjesuschrist.org/music/text/hymns/now-let-us-rejoice?lang=eng", "Now Let Us Rejoice")
        hymns[4] = hymn(4, "https://www.churchofjesuschrist.org/music/text/hymns/truth-eternal?lang=eng", "Truth Eternal")
        hymns[5] = hymn(5, "https://www.churchofjesuschrist.org/music/text/hymns/high-on-the-mountain-top?lang=eng", "High on the Mountain Top")
        hymns[6] = hymn(6, "https://www.churchofjesuschrist.org/music/text/hymns/redeemer-of-israel?lang=eng", "Redeemer of Israel")
        hymns[7] = hymn(7, "https://www.churchofjesuschrist.org/music/text/hymns/israel-israel-god-is-calling?lang=eng", "Israel, Israel, God Is Calling")
        hymns[8] = hymn(8, "https://www.churchofjesuschrist.org/music/text/hymns/awake-and-arise?lang=eng", "Awake and Arise")
        hymns[9] = hymn(9, "https://www.churchofjesuschrist.org/music/text/hymns/come-rejoice?lang=eng", "Come, Rejoice")
        hymns[10] = hymn(10, "https://www.churchofjesuschrist.org/music/text/hymns/come-sing-to-the-lord?lang=eng", "Come, Sing to the Lord")
        hymns[11] = hymn(11, "https://www.churchofjesuschrist.org/music/text/hymns/what-was-witnessed-in-the-heavens?lang=eng", "What Was Witnessed in the Heavens?")
        hymns[12] = hymn(12, "https://www.churchofjesuschrist.org/music/text/hymns/twas-witnessed-in-the-morning-sky?lang=eng", "'Twas Witnessed in the Morning Sky")
        hymns[13] = hymn(13, "https://www.churchofjesuschrist.org/music/text/hymns/an-angel-from-on-high-13?lang=eng", "An Angel from on High")
        hymns[14] = hymn(14, "https://www.churchofjesuschrist.org/music/text/hymns/sweet-is-the-peace-the-gospel-brings?lang=eng", "Sweet Is the Peace the Gospel Brings")
        hymns[15] = hymn(15, "https://www.churchofjesuschrist.org/music/text/hymns/i-saw-a-mighty-angel-fly?lang=eng", "I Saw a Mighty Angel Fly")
        hymns[16] = hymn(16, "https://www.churchofjesuschrist.org/music/text/hymns/what-glorious-scenes-mine-eyes-behold?lang=eng", "What Glorious Scenes Mine Eyes Behold")
        hymns[17] = hymn(17, "https://www.churchofjesuschrist.org/music/text/hymns/awake-ye-saints-of-god-awake?lang=eng", "Awake, Ye Saints of God, Awake!")
        hymns[18] = hymn(18, "https://www.churchofjesuschrist.org/music/text/hymns/the-voice-of-god-again-is-heard?lang=eng", "The Voice of God Again Is Heard")
        hymns[19] = hymn(19, "https://www.churchofjesuschrist.org/music/text/hymns/we-thank-thee-o-god-for-a-prophet?lang=eng", "We Thank Thee, O God, for a Prophet")
        hymns[20] = hymn(20, "https://www.churchofjesuschrist.org/music/text/hymns/god-of-power-god-of-right?lang=eng", "God of Power, God of Right")
        hymns[21] = hymn(21, "https://www.churchofjesuschrist.org/music/text/hymns/come-listen-to-a-prophets-voice?lang=eng", "Come, Listen to a Prophet's Voice")
        hymns[22] = hymn(22, "https://www.churchofjesuschrist.org/music/text/hymns/we-listen-to-a-prophets-voice?lang=eng", "We Listen to a Prophet's Voice")
        hymns[23] = hymn(23, "https://www.churchofjesuschrist.org/music/text/hymns/we-ever-pray-for-thee?lang=eng", "We Ever Pray for Thee")
        hymns[24] = hymn(24, "https://www.churchofjesuschrist.org/music/text/hymns/god-bless-our-prophet-dear?lang=eng", "God Bless Our Prophet Dear")
        hymns[25] = hymn(25, "https://www.churchofjesuschrist.org/music/text/hymns/now-well-sing-with-one-accord?lang=eng", "Now We'll Sing with One Accord")
        hymns[26] = hymn(26, "https://www.churchofjesuschrist.org/music/text/hymns/joseph-smiths-first-prayer?lang=eng", "Oh, how lovely was the morning")
        hymns[27] = hymn(27, "https://www.churchofjesuschrist.org/music/text/hymns/praise-to-the-man?lang=eng", "Praise to the Man")
        hymns[28] = hymn(28, "https://www.churchofjesuschrist.org/music/text/hymns/saints-behold-how-great-jehovah?lang=eng", "Saints, Behold How Great Jehovah")
        hymns[29] = hymn(29, "https://www.churchofjesuschrist.org/music/text/hymns/a-poor-wayfaring-man-of-grief?lang=eng", "A Poor Wayfaring Man of Grief")
        hymns[30] = hymn(30, "https://www.churchofjesuschrist.org/music/text/hymns/come-come-ye-saints?lang=eng", "Come, Come, Ye Saints")
        hymns[31] = hymn(31, "https://www.churchofjesuschrist.org/music/text/hymns/o-god-our-help-in-ages-past?lang=eng", "O God, Our Help in Ages Past")
        hymns[32] = hymn(32, "https://www.churchofjesuschrist.org/music/text/hymns/the-happy-day-at-last-has-come?lang=eng", "The Happy Day at Last Has Come")
        hymns[33] = hymn(33, "https://www.churchofjesuschrist.org/music/text/hymns/our-mountain-home-so-dear?lang=eng", "Our Mountain Home So Dear")
        hymns[34] = hymn(34, "https://www.churchofjesuschrist.org/music/text/hymns/o-ye-mountains-high?lang=eng", "O Ye Mountains High")
        hymns[35] = hymn(35, "https://www.churchofjesuschrist.org/music/text/hymns/for-the-strength-of-the-hills?lang=eng", "For the Strength of the Hills")
        hymns[36] = hymn(36, "https://www.churchofjesuschrist.org/music/text/hymns/they-the-builders-of-the-nation?lang=eng", "They, the Builders of the Nation")
        hymns[37] = hymn(37, "https://www.churchofjesuschrist.org/music/text/hymns/the-wintry-day-descending-to-its-close?lang=eng", "The Wintry Day, Descending to Its Close")
        hymns[38] = hymn(38, "https://www.churchofjesuschrist.org/music/text/hymns/come-all-ye-saints-of-zion?lang=eng", "Come, All Ye Saints of Zion")
        hymns[39] = hymn(39, "https://www.churchofjesuschrist.org/music/text/hymns/o-saints-of-zion?lang=eng", "O Saints of Zion")
        hymns[40] = hymn(40, "https://www.churchofjesuschrist.org/music/text/hymns/arise-o-glorious-zion?lang=eng", "Arise, O Glorious Zion")
        hymns[41] = hymn(41, "https://www.churchofjesuschrist.org/music/text/hymns/let-zion-in-her-beauty-rise?lang=eng", "Let Zion in Her Beauty Rise")
        hymns[42] = hymn(42, "https://www.churchofjesuschrist.org/music/text/hymns/hail-to-the-brightness-of-zions-glad-morning?lang=eng", "Hail to the Brightness of Zion's Glad Morning!")
        hymns[43] = hymn(43, "https://www.churchofjesuschrist.org/music/text/hymns/zion-stands-with-hills-surrounded?lang=eng", "Zion Stands with Hills Surrounded")
        hymns[44] = hymn(44, "https://www.churchofjesuschrist.org/music/text/hymns/beautiful-zion-built-above?lang=eng", "Beautiful Zion, Built Above")
        hymns[45] = hymn(45, "https://www.churchofjesuschrist.org/music/text/hymns/lead-me-into-life-eternal?lang=eng", "Lead Me into Life Eternal")
        hymns[46] = hymn(46, "https://www.churchofjesuschrist.org/music/text/hymns/glorious-things-of-thee-are-spoken?lang=eng", "Glorious Things of Thee Are Spoken")
        hymns[47] = hymn(47, "https://www.churchofjesuschrist.org/music/text/hymns/we-will-sing-of-zion?lang=eng", "We Will Sing of Zion")
        hymns[48] = hymn(48, "https://www.churchofjesuschrist.org/music/text/hymns/glorious-things-are-sung-of-zion?lang=eng", "Glorious Things Are Sung of Zion")
        hymns[49] = hymn(49, "https://www.churchofjesuschrist.org/music/text/hymns/adam-ondi-ahman?lang=eng", "This earth was once a garden place")
        hymns[50] = hymn(50, "https://www.churchofjesuschrist.org/music/text/hymns/come-thou-glorious-day-of-promise?lang=eng", "Come, Thou Glorious Day of Promise")
        hymns[51] = hymn(51, "https://www.churchofjesuschrist.org/music/text/hymns/sons-of-michael-he-approaches?lang=eng", "Sons of Michael, He Approaches")
        hymns[52] = hymn(52, "https://www.churchofjesuschrist.org/music/text/hymns/the-day-dawn-is-breaking?lang=eng", "The Day Dawn Is Breaking")
        hymns[53] = hymn(53, "https://www.churchofjesuschrist.org/music/text/hymns/let-earths-inhabitants-rejoice?lang=eng", "Let Earth's Inhabitants Rejoice")
        hymns[54] = hymn(54, "https://www.churchofjesuschrist.org/music/text/hymns/behold-the-mountain-of-the-lord?lang=eng", "Behold, the Mountain of the Lord")
        hymns[55] = hymn(55, "https://www.churchofjesuschrist.org/music/text/hymns/lo-the-mighty-god-appearing?lang=eng", "Lo, the Mighty God Appearing!")
        hymns[56] = hymn(56, "https://www.churchofjesuschrist.org/music/text/hymns/softly-beams-the-sacred-dawning?lang=eng", "Softly Beams the Sacred Dawning")
        hymns[57] = hymn(57, "https://www.churchofjesuschrist.org/music/text/hymns/were-not-ashamed-to-own-our-lord?lang=eng", "We're Not Ashamed to Own Our Lord")
        hymns[58] = hymn(58, "https://www.churchofjesuschrist.org/music/text/hymns/come-ye-children-of-the-lord?lang=eng", "Come, Ye Children of the Lord")
        hymns[59] = hymn(59, "https://www.churchofjesuschrist.org/music/text/hymns/come-o-thou-king-of-kings?lang=eng", "Come, O Thou King of Kings")
        hymns[60] = hymn(60, "https://www.churchofjesuschrist.org/music/text/hymns/battle-hymn-of-the-republic?lang=eng", "Mine eyes have seen the glory of the coming of the Lord")
        hymns[61] = hymn(61, "https://www.churchofjesuschrist.org/music/text/hymns/raise-your-voices-to-the-lord?lang=eng", "Raise Your Voices to the Lord")
        hymns[62] = hymn(62, "https://www.churchofjesuschrist.org/music/text/hymns/all-creatures-of-our-god-and-king?lang=eng", "All Creatures of Our God and King")
        hymns[63] = hymn(63, "https://www.churchofjesuschrist.org/music/text/hymns/great-king-of-heaven?lang=eng", "Great King of Heaven")
        hymns[64] = hymn(64, "https://www.churchofjesuschrist.org/music/text/hymns/on-this-day-of-joy-and-gladness?lang=eng", "On This Day of Joy and Gladness")
        hymns[65] = hymn(65, "https://www.churchofjesuschrist.org/music/text/hymns/come-all-ye-saints-who-dwell-on-earth?lang=eng", "Come, All Ye Saints Who Dwell on Earth")
        hymns[66] = hymn(66, "https://www.churchofjesuschrist.org/music/text/hymns/rejoice-the-lord-is-king?lang=eng", "Rejoice, the Lord Is King!")
        hymns[67] = hymn(67, "https://www.churchofjesuschrist.org/music/text/hymns/glory-to-god-on-high?lang=eng", "Glory to God on High")
        hymns[68] = hymn(68, "https://www.churchofjesuschrist.org/music/text/hymns/a-mighty-fortress-is-our-god?lang=eng", "A Mighty Fortress Is Our God")
        hymns[69] = hymn(69, "https://www.churchofjesuschrist.org/music/text/hymns/all-glory-laud-and-honor?lang=eng", "All Glory, Laud, and Honor")
        hymns[70] = hymn(70, "https://www.churchofjesuschrist.org/music/text/hymns/sing-praise-to-him?lang=eng", "Sing Praise to Him")
        hymns[71] = hymn(71, "https://www.churchofjesuschrist.org/music/text/hymns/with-songs-of-praise?lang=eng", "With Songs of Praise")
        hymns[72] = hymn(72, "https://www.churchofjesuschrist.org/music/text/hymns/praise-to-the-lord-the-almighty?lang=eng", "Praise to the Lord, the Almighty")
        hymns[73] = hymn(73, "https://www.churchofjesuschrist.org/music/text/hymns/praise-the-lord-with-heart-and-voice?lang=eng", "Praise the Lord with Heart and Voice")
        hymns[74] = hymn(74, "https://www.churchofjesuschrist.org/music/text/hymns/praise-ye-the-lord?lang=eng", "Praise Ye the Lord")
        hymns[75] = hymn(75, "https://www.churchofjesuschrist.org/music/text/hymns/in-hymns-of-praise?lang=eng", "In Hymns of Praise")
        hymns[76] = hymn(76, "https://www.churchofjesuschrist.org/music/text/hymns/god-of-our-fathers-we-come-unto-thee?lang=eng", "God of Our Fathers, We Come unto Thee")
        hymns[77] = hymn(77, "https://www.churchofjesuschrist.org/music/text/hymns/great-is-the-lord?lang=eng", "Great Is the Lord")
        hymns[78] = hymn(78, "https://www.churchofjesuschrist.org/music/text/hymns/god-of-our-fathers-whose-almighty-hand?lang=eng", "God of Our Fathers, Whose Almighty Hand")
        hymns[79] = hymn(79, "https://www.churchofjesuschrist.org/music/text/hymns/with-all-the-power-of-heart-and-tongue?lang=eng", "With All the Power of Heart and Tongue")
        hymns[80] = hymn(80, "https://www.churchofjesuschrist.org/music/text/hymns/god-of-our-fathers-known-of-old?lang=eng", "God of Our Fathers, Known of Old")
        hymns[81] = hymn(81, "https://www.churchofjesuschrist.org/music/text/hymns/press-forward-saints?lang=eng", "Press Forward, Saints")
        hymns[82] = hymn(82, "https://www.churchofjesuschrist.org/music/text/hymns/for-all-the-saints?lang=eng", "For All the Saints")
        hymns[83] = hymn(83, "https://www.churchofjesuschrist.org/music/text/hymns/guide-us-o-thou-great-jehovah?lang=eng", "Guide Us, O Thou Great Jehovah")
        hymns[84] = hymn(84, "https://www.churchofjesuschrist.org/music/text/hymns/faith-of-our-fathers?lang=eng", "Faith of Our Fathers")
        hymns[85] = hymn(85, "https://www.churchofjesuschrist.org/music/text/hymns/how-firm-a-foundation?lang=eng", "How Firm a Foundation")
        hymns[86] = hymn(86, "https://www.churchofjesuschrist.org/music/text/hymns/how-great-thou-art?lang=eng", "How Great Thou Art")
        hymns[87] = hymn(87, "https://www.churchofjesuschrist.org/music/text/hymns/god-is-love?lang=eng", "God Is Love")
        hymns[88] = hymn(88, "https://www.churchofjesuschrist.org/music/text/hymns/great-god-attend-while-zion-sings?lang=eng", "Great God, Attend While Zion Sings")
        hymns[89] = hymn(89, "https://www.churchofjesuschrist.org/music/text/hymns/the-lord-is-my-light?lang=eng", "The Lord Is My Light")
        hymns[90] = hymn(90, "https://www.churchofjesuschrist.org/music/text/hymns/from-all-that-dwell-below-the-skies?lang=eng", "From All That Dwell below the Skies")
        hymns[91] = hymn(91, "https://www.churchofjesuschrist.org/music/text/hymns/father-thy-children-to-thee-now-raise?lang=eng", "Father, Thy Children to Thee Now Raise")
        hymns[92] = hymn(92, "https://www.churchofjesuschrist.org/music/text/hymns/for-the-beauty-of-the-earth?lang=eng", "For the Beauty of the Earth")
        hymns[93] = hymn(93, "https://www.churchofjesuschrist.org/music/text/hymns/prayer-of-thanksgiving?lang=eng", "We gather together to ask the Lord's blessing")
        hymns[94] = hymn(94, "https://www.churchofjesuschrist.org/music/text/hymns/come-ye-thankful-people?lang=eng", "Come, Ye Thankful People")
        hymns[95] = hymn(95, "https://www.churchofjesuschrist.org/music/text/hymns/now-thank-we-all-our-god?lang=eng", "Now Thank We All Our God")
        hymns[96] = hymn(96, "https://www.churchofjesuschrist.org/music/text/hymns/dearest-children-god-is-near-you?lang=eng", "Dearest Children, God Is Near You")
        hymns[97] = hymn(97, "https://www.churchofjesuschrist.org/music/text/hymns/lead-kindly-light?lang=eng", "Lead, Kindly Light")
        hymns[98] = hymn(98, "https://www.churchofjesuschrist.org/music/text/hymns/i-need-thee-every-hour?lang=eng", "I Need Thee Every Hour")
        hymns[99] = hymn(99, "https://www.churchofjesuschrist.org/music/text/hymns/nearer-dear-savior-to-thee?lang=eng", "Nearer, Dear Savior, to Thee")
        hymns[100] = hymn(100, "https://www.churchofjesuschrist.org/music/text/hymns/nearer-my-god-to-thee?lang=eng", "Nearer, My God, to Thee")
        hymns[101] = hymn(101, "https://www.churchofjesuschrist.org/music/text/hymns/guide-me-to-thee?lang=eng", "Jesus, my Savior true")
        hymns[102] = hymn(102, "https://www.churchofjesuschrist.org/music/text/hymns/jesus-lover-of-my-soul?lang=eng", "Jesus, Lover of My Soul")
        hymns[103] = hymn(103, "https://www.churchofjesuschrist.org/music/text/hymns/precious-savior-dear-redeemer?lang=eng", "Precious Savior, Dear Redeemer")
        hymns[104] = hymn(104, "https://www.churchofjesuschrist.org/music/text/hymns/jesus-savior-pilot-me?lang=eng", "Jesus, Savior, Pilot Me")
        hymns[105] = hymn(105, "https://www.churchofjesuschrist.org/music/text/hymns/master-the-tempest-is-raging?lang=eng", "Master, the Tempest Is Raging")
        hymns[106] = hymn(106, "https://www.churchofjesuschrist.org/music/text/hymns/god-speed-the-right?lang=eng", "Now to heav'n our prayer ascending")
        hymns[107] = hymn(107, "https://www.churchofjesuschrist.org/music/text/hymns/lord-accept-our-true-devotion?lang=eng", "Lord, Accept Our True Devotion")
        hymns[108] = hymn(108, "https://www.churchofjesuschrist.org/music/text/hymns/the-lord-is-my-shepherd?lang=eng", "The Lord Is My Shepherd")
        hymns[109] = hymn(109, "https://www.churchofjesuschrist.org/music/text/hymns/the-lord-my-pasture-will-prepare?lang=eng", "The Lord My Pasture Will Prepare")
        hymns[110] = hymn(110, "https://www.churchofjesuschrist.org/music/text/hymns/cast-thy-burden-upon-the-lord?lang=eng", "Cast Thy Burden upon the Lord")
        hymns[111] = hymn(111, "https://www.churchofjesuschrist.org/music/text/hymns/rock-of-ages?lang=eng", "Rock of Ages")
        hymns[112] = hymn(112, "https://www.churchofjesuschrist.org/music/text/hymns/savior-redeemer-of-my-soul?lang=eng", "Savior, Redeemer of My Soul")
        hymns[113] = hymn(113, "https://www.churchofjesuschrist.org/music/text/hymns/our-saviors-love?lang=eng", "Our Savior's Love")
        hymns[114] = hymn(114, "https://www.churchofjesuschrist.org/music/text/hymns/come-unto-him?lang=eng", "I wander through the still of night")
        hymns[115] = hymn(115, "https://www.churchofjesuschrist.org/music/text/hymns/come-ye-disconsolate?lang=eng", "Come, Ye Disconsolate")
        hymns[116] = hymn(116, "https://www.churchofjesuschrist.org/music/text/hymns/come-follow-me?lang=eng", "Come, Follow Me")
        hymns[117] = hymn(117, "https://www.churchofjesuschrist.org/music/text/hymns/come-unto-jesus?lang=eng", "Come unto Jesus")
        hymns[118] = hymn(118, "https://www.churchofjesuschrist.org/music/text/hymns/ye-simple-souls-who-stray?lang=eng", "Ye Simple Souls Who Stray")
        hymns[119] = hymn(119, "https://www.churchofjesuschrist.org/music/text/hymns/come-we-that-love-the-lord?lang=eng", "Come, We That Love the Lord")
        hymns[120] = hymn(120, "https://www.churchofjesuschrist.org/music/text/hymns/lean-on-my-ample-arm?lang=eng", "Lean on My Ample Arm")
        hymns[121] = hymn(121, "https://www.churchofjesuschrist.org/music/text/hymns/im-a-pilgrim-im-a-stranger?lang=eng", "I'm a Pilgrim, I'm a Stranger")
        hymns[122] = hymn(122, "https://www.churchofjesuschrist.org/music/text/hymns/though-deepening-trials?lang=eng", "Though Deepening Trials")
        hymns[123] = hymn(123, "https://www.churchofjesuschrist.org/music/text/hymns/oh-may-my-soul-commune-with-thee?lang=eng", "Oh, May My Soul Commune with Thee")
        hymns[124] = hymn(124, "https://www.churchofjesuschrist.org/music/text/hymns/be-still-my-soul?lang=eng", "Be Still, My Soul")
        hymns[125] = hymn(125, "https://www.churchofjesuschrist.org/music/text/hymns/how-gentle-gods-commands?lang=eng", "How Gentle God's Commands")
        hymns[126] = hymn(126, "https://www.churchofjesuschrist.org/music/text/hymns/how-long-o-lord-most-holy-and-true?lang=eng", "How Long, O Lord Most Holy and True")
        hymns[127] = hymn(127, "https://www.churchofjesuschrist.org/music/text/hymns/does-the-journey-seem-long?lang=eng", "Does the Journey Seem Long?")
        hymns[128] = hymn(128, "https://www.churchofjesuschrist.org/music/text/hymns/when-faith-endures?lang=eng", "When Faith Endures")
        hymns[129] = hymn(129, "https://www.churchofjesuschrist.org/music/text/hymns/where-can-i-turn-for-peace?lang=eng", "Where Can I Turn for Peace?")
        hymns[130] = hymn(130, "https://www.churchofjesuschrist.org/music/text/hymns/be-thou-humble?lang=eng", "Be Thou Humble")
        hymns[131] = hymn(131, "https://www.churchofjesuschrist.org/music/text/hymns/more-holiness-give-me?lang=eng", "More Holiness Give Me")
        hymns[132] = hymn(132, "https://www.churchofjesuschrist.org/music/text/hymns/god-is-in-his-holy-temple?lang=eng", "God Is in His Holy Temple")
        hymns[133] = hymn(133, "https://www.churchofjesuschrist.org/music/text/hymns/father-in-heaven?lang=eng", "Father in Heaven")
        hymns[134] = hymn(134, "https://www.churchofjesuschrist.org/music/text/hymns/i-believe-in-christ?lang=eng", "I Believe in Christ")
        hymns[135] = hymn(135, "https://www.churchofjesuschrist.org/music/text/hymns/my-redeemer-lives?lang=eng", "My Redeemer Lives")
        hymns[136] = hymn(136, "https://www.churchofjesuschrist.org/music/text/hymns/i-know-that-my-redeemer-lives?lang=eng", "I Know That My Redeemer Lives")
        hymns[137] = hymn(137, "https://www.churchofjesuschrist.org/music/text/hymns/testimony?lang=eng", "Testimony")
        hymns[138] = hymn(138, "https://www.churchofjesuschrist.org/music/text/hymns/bless-our-fast-we-pray?lang=eng", "On bended knees, with broken hearts")
        hymns[139] = hymn(139, "https://www.churchofjesuschrist.org/music/text/hymns/in-fasting-we-approach-thee?lang=eng", "In Fasting We Approach Thee")
        hymns[140] = hymn(140, "https://www.churchofjesuschrist.org/music/text/hymns/did-you-think-to-pray?lang=eng", "Ere you left your room this morning")
        hymns[141] = hymn(141, "https://www.churchofjesuschrist.org/music/text/hymns/jesus-the-very-thought-of-thee?lang=eng", "Jesus, the Very Thought of Thee")
        hymns[142] = hymn(142, "https://www.churchofjesuschrist.org/music/text/hymns/sweet-hour-of-prayer?lang=eng", "Sweet Hour of Prayer")
        hymns[143] = hymn(143, "https://www.churchofjesuschrist.org/music/text/hymns/let-the-holy-spirit-guide?lang=eng", "Let the Holy Spirit Guide")
        hymns[144] = hymn(144, "https://www.churchofjesuschrist.org/music/text/hymns/secret-prayer?lang=eng", "There is an hour of peace and rest")
        hymns[145] = hymn(145, "https://www.churchofjesuschrist.org/music/text/hymns/prayer-is-the-souls-sincere-desire?lang=eng", "Prayer Is the Soul's Sincere Desire")
        hymns[146] = hymn(146, "https://www.churchofjesuschrist.org/music/text/hymns/gently-raise-the-sacred-strain?lang=eng", "Gently Raise the Sacred Strain")
        hymns[147] = hymn(147, "https://www.churchofjesuschrist.org/music/text/hymns/sweet-is-the-work?lang=eng", "Sweet Is the Work")
        hymns[148] = hymn(148, "https://www.churchofjesuschrist.org/music/text/hymns/sabbath-day?lang=eng", "Sabbath Day")
        hymns[149] = hymn(149, "https://www.churchofjesuschrist.org/music/text/hymns/as-the-dew-from-heaven-distilling?lang=eng", "As the Dew from Heaven Distilling")
        hymns[150] = hymn(150, "https://www.churchofjesuschrist.org/music/text/hymns/o-thou-kind-and-gracious-father?lang=eng", "O Thou Kind and Gracious Father")
        hymns[151] = hymn(151, "https://www.churchofjesuschrist.org/music/text/hymns/we-meet-dear-lord?lang=eng", "We Meet, Dear Lord")
        hymns[152] = hymn(152, "https://www.churchofjesuschrist.org/music/text/hymns/god-be-with-you-till-we-meet-again?lang=eng", "God Be with You Till We Meet Again")
        hymns[153] = hymn(153, "https://www.churchofjesuschrist.org/music/text/hymns/lord-we-ask-thee-ere-we-part?lang=eng", "Lord, We Ask Thee Ere We Part")
        hymns[154] = hymn(154, "https://www.churchofjesuschrist.org/music/text/hymns/father-this-hour-has-been-one-of-joy?lang=eng", "Father, This Hour Has Been One of Joy")
        hymns[155] = hymn(155, "https://www.churchofjesuschrist.org/music/text/hymns/we-have-partaken-of-thy-love?lang=eng", "We Have Partaken of Thy Love")
        hymns[156] = hymn(156, "https://www.churchofjesuschrist.org/music/text/hymns/sing-we-now-at-parting?lang=eng", "Sing We Now at Parting")
        hymns[157] = hymn(157, "https://www.churchofjesuschrist.org/music/text/hymns/thy-spirit-lord-has-stirred-our-souls?lang=eng", "Thy Spirit, Lord, Has Stirred Our Souls")
        hymns[158] = hymn(158, "https://www.churchofjesuschrist.org/music/text/hymns/before-thee-lord-i-bow-my-head?lang=eng", "Before Thee, Lord, I Bow My Head")
        hymns[159] = hymn(159, "https://www.churchofjesuschrist.org/music/text/hymns/now-the-day-is-over?lang=eng", "Now the Day Is Over")
        hymns[160] = hymn(160, "https://www.churchofjesuschrist.org/music/text/hymns/softly-now-the-light-of-day?lang=eng", "Softly Now the Light of Day")
        hymns[161] = hymn(161, "https://www.churchofjesuschrist.org/music/text/hymns/the-lord-be-with-us?lang=eng", "The Lord Be with Us")
        hymns[162] = hymn(162, "https://www.churchofjesuschrist.org/music/text/hymns/lord-we-come-before-thee-now?lang=eng", "Lord, We Come before Thee Now")
        hymns[163] = hymn(163, "https://www.churchofjesuschrist.org/music/text/hymns/lord-dismiss-us-with-thy-blessing?lang=eng", "Lord, Dismiss Us with Thy Blessing")
        hymns[164] = hymn(164, "https://www.churchofjesuschrist.org/music/text/hymns/great-god-to-thee-my-evening-song?lang=eng", "Great God, to Thee My Evening Song")
        hymns[165] = hymn(165, "https://www.churchofjesuschrist.org/music/text/hymns/abide-with-me-tis-eventide?lang=eng", "Abide with Me; 'Tis Eventide")
        hymns[166] = hymn(166, "https://www.churchofjesuschrist.org/music/text/hymns/abide-with-me?lang=eng", "Abide with Me!")
        hymns[167] = hymn(167, "https://www.churchofjesuschrist.org/music/text/hymns/come-let-us-sing-an-evening-hymn?lang=eng", "Come, Let Us Sing an Evening Hymn")
        hymns[168] = hymn(168, "https://www.churchofjesuschrist.org/music/text/hymns/as-the-shadows-fall?lang=eng", "As the Shadows Fall")
        hymns[169] = hymn(169, "https://www.churchofjesuschrist.org/music/text/hymns/as-now-we-take-the-sacrament?lang=eng", "As Now We Take the Sacrament")
        hymns[170] = hymn(170, "https://www.churchofjesuschrist.org/music/text/hymns/god-our-father-hear-us-pray?lang=eng", "God, Our Father, Hear Us Pray")
        hymns[171] = hymn(171, "https://www.churchofjesuschrist.org/music/text/hymns/with-humble-heart?lang=eng", "With Humble Heart")
        hymns[172] = hymn(172, "https://www.churchofjesuschrist.org/music/text/hymns/in-humility-our-savior?lang=eng", "In Humility, Our Savior")
        hymns[173] = hymn(173, "https://www.churchofjesuschrist.org/music/text/hymns/while-of-these-emblems-we-partake-173?lang=eng", "While of These Emblems We Partake")
        hymns[174] = hymn(174, "https://www.churchofjesuschrist.org/music/text/hymns/while-of-these-emblems-we-partake-174?lang=eng", "While of These Emblems We Partake")
        hymns[175] = hymn(175, "https://www.churchofjesuschrist.org/music/text/hymns/o-god-the-eternal-father?lang=eng", "O God, the Eternal Father")
        hymns[176] = hymn(176, "https://www.churchofjesuschrist.org/music/text/hymns/tis-sweet-to-sing-the-matchless-love-176?lang=eng", "'Tis Sweet to Sing the Matchless Love")
        hymns[177] = hymn(177, "https://www.churchofjesuschrist.org/music/text/hymns/tis-sweet-to-sing-the-matchless-love-177?lang=eng", "'Tis Sweet To Sing the Matchless Love")
        hymns[178] = hymn(178, "https://www.churchofjesuschrist.org/music/text/hymns/o-lord-of-hosts?lang=eng", "O Lord of Hosts")
        hymns[179] = hymn(179, "https://www.churchofjesuschrist.org/music/text/hymns/again-our-dear-redeeming-lord?lang=eng", "Again, Our Dear Redeeming Lord")
        hymns[180] = hymn(180, "https://www.churchofjesuschrist.org/music/text/hymns/father-in-heaven-we-do-believe?lang=eng", "Father in Heaven, We Do Believe")
        hymns[181] = hymn(181, "https://www.churchofjesuschrist.org/music/text/hymns/jesus-of-nazareth-savior-and-king?lang=eng", "Jesus of Nazareth, Savior and King")
        hymns[182] = hymn(182, "https://www.churchofjesuschrist.org/music/text/hymns/well-sing-all-hail-to-jesus-name?lang=eng", "We'll Sing All Hail to Jesus' Name")
        hymns[183] = hymn(183, "https://www.churchofjesuschrist.org/music/text/hymns/in-remembrance-of-thy-suffering?lang=eng", "In Remembrance of Thy Suffering")
        hymns[184] = hymn(184, "https://www.churchofjesuschrist.org/music/text/hymns/upon-the-cross-of-calvary?lang=eng", "Upon the Cross of Calvary")
        hymns[185] = hymn(185, "https://www.churchofjesuschrist.org/music/text/hymns/reverently-and-meekly-now?lang=eng", "Reverently and Meekly Now")
        hymns[186] = hymn(186, "https://www.churchofjesuschrist.org/music/text/hymns/again-we-meet-around-the-board?lang=eng", "Again We Meet around the Board")
        hymns[187] = hymn(187, "https://www.churchofjesuschrist.org/music/text/hymns/god-loved-us-so-he-sent-his-son?lang=eng", "God Loved Us, So He Sent His Son")
        hymns[188] = hymn(188, "https://www.churchofjesuschrist.org/music/text/hymns/thy-will-o-lord-be-done?lang=eng", "When in the wondrous realms above")
        hymns[189] = hymn(189, "https://www.churchofjesuschrist.org/music/text/hymns/o-thou-before-the-world-began?lang=eng", "O Thou, Before the World Began")
        hymns[190] = hymn(190, "https://www.churchofjesuschrist.org/music/text/hymns/in-memory-of-the-crucified?lang=eng", "In Memory of the Crucified")
        hymns[191] = hymn(191, "https://www.churchofjesuschrist.org/music/text/hymns/behold-the-great-redeemer-die?lang=eng", "Behold the Great Redeemer Die")
        hymns[192] = hymn(192, "https://www.churchofjesuschrist.org/music/text/hymns/he-died-the-great-redeemer-died?lang=eng", "He Died! The Great Redeemer Died")
        hymns[193] = hymn(193, "https://www.churchofjesuschrist.org/music/text/hymns/i-stand-all-amazed?lang=eng", "I Stand All Amazed")
        hymns[194] = hymn(194, "https://www.churchofjesuschrist.org/music/text/hymns/there-is-a-green-hill-far-away?lang=eng", "There Is a Green Hill Far Away")
        hymns[195] = hymn(195, "https://www.churchofjesuschrist.org/music/text/hymns/how-great-the-wisdom-and-the-love?lang=eng", "How Great the Wisdom and the Love")
        hymns[196] = hymn(196, "https://www.churchofjesuschrist.org/music/text/hymns/jesus-once-of-humble-birth?lang=eng", "Jesus, Once of Humble Birth")
        hymns[197] = hymn(197, "https://www.churchofjesuschrist.org/music/text/hymns/o-savior-thou-who-wearest-a-crown?lang=eng", "O Savior, Thou Who Wearest a Crown")
        hymns[198] = hymn(198, "https://www.churchofjesuschrist.org/music/text/hymns/that-easter-morn?lang=eng", "That Easter Morn")
        hymns[199] = hymn(199, "https://www.churchofjesuschrist.org/music/text/hymns/he-is-risen?lang=eng", "He Is Risen!")
        hymns[200] = hymn(200, "https://www.churchofjesuschrist.org/music/text/hymns/christ-the-lord-is-risen-today?lang=eng", "Christ the Lord Is Risen Today")
        hymns[201] = hymn(201, "https://www.churchofjesuschrist.org/music/text/hymns/joy-to-the-world?lang=eng", "Joy to the World")
        hymns[202] = hymn(202, "https://www.churchofjesuschrist.org/music/text/hymns/oh-come-all-ye-faithful?lang=eng", "Oh, Come, All Ye Faithful")
        hymns[203] = hymn(203, "https://www.churchofjesuschrist.org/music/text/hymns/angels-we-have-heard-on-high?lang=eng", "Angels We Have Heard on High")
        hymns[204] = hymn(204, "https://www.churchofjesuschrist.org/music/text/hymns/silent-night?lang=eng", "Silent Night")
        hymns[205] = hymn(205, "https://www.churchofjesuschrist.org/music/text/hymns/once-in-royal-davids-city?lang=eng", "Once in Royal David's City")
        hymns[206] = hymn(206, "https://www.churchofjesuschrist.org/music/text/hymns/away-in-a-manger?lang=eng", "Away in a Manger")
        hymns[207] = hymn(207, "https://www.churchofjesuschrist.org/music/text/hymns/it-came-upon-the-midnight-clear?lang=eng", "It Came upon the Midnight Clear")
        hymns[208] = hymn(208, "https://www.churchofjesuschrist.org/music/text/hymns/o-little-town-of-bethlehem?lang=eng", "O Little Town of Bethlehem")
        hymns[209] = hymn(209, "https://www.churchofjesuschrist.org/music/text/hymns/hark-the-herald-angels-sing?lang=eng", "Hark! The Herald Angels Sing")
        hymns[210] = hymn(210, "https://www.churchofjesuschrist.org/music/text/hymns/with-wondering-awe?lang=eng", "With Wondering Awe")
        hymns[211] = hymn(211, "https://www.churchofjesuschrist.org/music/text/hymns/while-shepherds-watched-their-flocks?lang=eng", "While Shepherds Watched Their Flocks")
        hymns[212] = hymn(212, "https://www.churchofjesuschrist.org/music/text/hymns/far-far-away-on-judeas-plains?lang=eng", "Far, Far Away on Judea's Plains")
        hymns[213] = hymn(213, "https://www.churchofjesuschrist.org/music/text/hymns/the-first-noel?lang=eng", "The First Noel")
        hymns[214] = hymn(214, "https://www.churchofjesuschrist.org/music/text/hymns/i-heard-the-bells-on-christmas-day?lang=eng", "I Heard the Bells on Christmas Day")
        hymns[215] = hymn(215, "https://www.churchofjesuschrist.org/music/text/hymns/ring-out-wild-bells?lang=eng", "Ring Out, Wild Bells")
        hymns[216] = hymn(216, "https://www.churchofjesuschrist.org/music/text/hymns/we-are-sowing?lang=eng", "We Are Sowing")
        hymns[217] = hymn(217, "https://www.churchofjesuschrist.org/music/text/hymns/come-let-us-anew?lang=eng", "Come, Let Us Anew")
        hymns[218] = hymn(218, "https://www.churchofjesuschrist.org/music/text/hymns/we-give-thee-but-thine-own?lang=eng", "We Give Thee But Thine Own")
        hymns[219] = hymn(219, "https://www.churchofjesuschrist.org/music/text/hymns/because-i-have-been-given-much?lang=eng", "Because I Have Been Given Much")
        hymns[220] = hymn(220, "https://www.churchofjesuschrist.org/music/text/hymns/lord-i-would-follow-thee?lang=eng", "Savior, may I learn to love thee")
        hymns[221] = hymn(221, "https://www.churchofjesuschrist.org/music/text/hymns/dear-to-the-heart-of-the-shepherd?lang=eng", "Dear to the Heart of the Shepherd")
        hymns[222] = hymn(222, "https://www.churchofjesuschrist.org/music/text/hymns/hear-thou-our-hymn-o-lord?lang=eng", "Hear Thou Our Hymn, O Lord")
        hymns[223] = hymn(223, "https://www.churchofjesuschrist.org/music/text/hymns/have-i-done-any-good?lang=eng", "Have I Done Any Good?")
        hymns[224] = hymn(224, "https://www.churchofjesuschrist.org/music/text/hymns/i-have-work-enough-to-do?lang=eng", "I Have Work Enough to Do")
        hymns[225] = hymn(225, "https://www.churchofjesuschrist.org/music/text/hymns/we-are-marching-on-to-glory?lang=eng", "We Are Marching On to Glory")
        hymns[226] = hymn(226, "https://www.churchofjesuschrist.org/music/text/hymns/improve-the-shining-moments?lang=eng", "Improve the Shining Moments")
        hymns[227] = hymn(227, "https://www.churchofjesuschrist.org/music/text/hymns/there-is-sunshine-in-my-soul-today?lang=eng", "There Is Sunshine in My Soul Today")
        hymns[228] = hymn(228, "https://www.churchofjesuschrist.org/music/text/hymns/you-can-make-the-pathway-bright?lang=eng", "You Can Make the Pathway Bright")
        hymns[229] = hymn(229, "https://www.churchofjesuschrist.org/music/text/hymns/today-while-the-sun-shines?lang=eng", "Today, While the Sun Shines")
        hymns[230] = hymn(230, "https://www.churchofjesuschrist.org/music/text/hymns/scatter-sunshine?lang=eng", "Scatter Sunshine")
        hymns[231] = hymn(231, "https://www.churchofjesuschrist.org/music/text/hymns/father-cheer-our-souls-tonight?lang=eng", "Father, Cheer Our Souls Tonight")
        hymns[232] = hymn(232, "https://www.churchofjesuschrist.org/music/text/hymns/let-us-oft-speak-kind-words?lang=eng", "Let Us Oft Speak Kind Words")
        hymns[233] = hymn(233, "https://www.churchofjesuschrist.org/music/text/hymns/nay-speak-no-ill?lang=eng", "Nay, Speak No Ill")
        hymns[234] = hymn(234, "https://www.churchofjesuschrist.org/music/text/hymns/jesus-mighty-king-in-zion?lang=eng", "Jesus, Mighty King in Zion")
        hymns[235] = hymn(235, "https://www.churchofjesuschrist.org/music/text/hymns/should-you-feel-inclined-to-censure?lang=eng", "Should You Feel Inclined to Censure")
        hymns[236] = hymn(236, "https://www.churchofjesuschrist.org/music/text/hymns/lord-accept-into-thy-kingdom?lang=eng", "Lord, Accept into Thy Kingdom")
        hymns[237] = hymn(237, "https://www.churchofjesuschrist.org/music/text/hymns/do-what-is-right?lang=eng", "Do What Is Right")
        hymns[238] = hymn(238, "https://www.churchofjesuschrist.org/music/text/hymns/behold-thy-sons-and-daughters-lord?lang=eng", "Behold Thy Sons and Daughters, Lord")
        hymns[239] = hymn(239, "https://www.churchofjesuschrist.org/music/text/hymns/choose-the-right?lang=eng", "Choose the Right")
        hymns[240] = hymn(240, "https://www.churchofjesuschrist.org/music/text/hymns/know-this-that-every-soul-is-free?lang=eng", "Know This, That Every Soul Is Free")
        hymns[241] = hymn(241, "https://www.churchofjesuschrist.org/music/text/hymns/count-your-blessings?lang=eng", "When upon life's billows you are tempest-tossed")
        hymns[242] = hymn(242, "https://www.churchofjesuschrist.org/music/text/hymns/praise-god-from-whom-all-blessings-flow?lang=eng", "Praise God, from Whom All Blessings Flow")
        hymns[243] = hymn(243, "https://www.churchofjesuschrist.org/music/text/hymns/let-us-all-press-on?lang=eng", "Let Us All Press On")
        hymns[244] = hymn(244, "https://www.churchofjesuschrist.org/music/text/hymns/come-along-come-along?lang=eng", "Come Along, Come Along")
        hymns[245] = hymn(245, "https://www.churchofjesuschrist.org/music/text/hymns/this-house-we-dedicate-to-thee?lang=eng", "This House We Dedicate to Thee")
        hymns[246] = hymn(246, "https://www.churchofjesuschrist.org/music/text/hymns/onward-christian-soldiers?lang=eng", "Onward, Christian Soldiers")
        hymns[247] = hymn(247, "https://www.churchofjesuschrist.org/music/text/hymns/we-love-thy-house-o-god?lang=eng", "We Love Thy House, O God")
        hymns[248] = hymn(248, "https://www.churchofjesuschrist.org/music/text/hymns/up-awake-ye-defenders-of-zion?lang=eng", "Up, Awake, Ye Defenders of Zion")
        hymns[249] = hymn(249, "https://www.churchofjesuschrist.org/music/text/hymns/called-to-serve?lang=eng", "Called to Serve")
        hymns[250] = hymn(250, "https://www.churchofjesuschrist.org/music/text/hymns/we-are-all-enlisted?lang=eng", "We Are All Enlisted")
        hymns[251] = hymn(251, "https://www.churchofjesuschrist.org/music/text/hymns/behold-a-royal-army?lang=eng", "Behold! A Royal Army")
        hymns[252] = hymn(252, "https://www.churchofjesuschrist.org/music/text/hymns/put-your-shoulder-to-the-wheel?lang=eng", "The world has need of willing men")
        hymns[253] = hymn(253, "https://www.churchofjesuschrist.org/music/text/hymns/like-ten-thousand-legions-marching?lang=eng", "Like Ten Thousand Legions Marching")
        hymns[254] = hymn(254, "https://www.churchofjesuschrist.org/music/text/hymns/true-to-the-faith?lang=eng", "True to the Faith")
        hymns[255] = hymn(255, "https://www.churchofjesuschrist.org/music/text/hymns/carry-on?lang=eng", "Firm as the mountains around us")
        hymns[256] = hymn(256, "https://www.churchofjesuschrist.org/music/text/hymns/as-zions-youth-in-latter-days?lang=eng", "As Zion's Youth in Latter Days")
        hymns[257] = hymn(257, "https://www.churchofjesuschrist.org/music/text/hymns/rejoice-a-glorious-sound-is-heard?lang=eng", "Rejoice! A Glorious Sound Is Heard")
        hymns[258] = hymn(258, "https://www.churchofjesuschrist.org/music/text/hymns/o-thou-rock-of-our-salvation?lang=eng", "O Thou Rock of Our Salvation")
        hymns[259] = hymn(259, "https://www.churchofjesuschrist.org/music/text/hymns/hope-of-israel?lang=eng", "Hope of Israel")
        hymns[260] = hymn(260, "https://www.churchofjesuschrist.org/music/text/hymns/whos-on-the-lords-side?lang=eng", "Who's on the Lord's Side?")
        hymns[261] = hymn(261, "https://www.churchofjesuschrist.org/music/text/hymns/thy-servants-are-prepared?lang=eng", "Thy Servants Are Prepared")
        hymns[262] = hymn(262, "https://www.churchofjesuschrist.org/music/text/hymns/go-ye-messengers-of-glory?lang=eng", "Go, Ye Messengers of Glory")
        hymns[263] = hymn(263, "https://www.churchofjesuschrist.org/music/text/hymns/go-forth-with-faith?lang=eng", "Go Forth with Faith")
        hymns[264] = hymn(264, "https://www.churchofjesuschrist.org/music/text/hymns/hark-all-ye-nations?lang=eng", "Hark, All Ye Nations!")
        hymns[265] = hymn(265, "https://www.churchofjesuschrist.org/music/text/hymns/arise-o-god-and-shine?lang=eng", "Arise, O God, and Shine")
        hymns[266] = hymn(266, "https://www.churchofjesuschrist.org/music/text/hymns/the-time-is-far-spent?lang=eng", "The Time Is Far Spent")
        hymns[267] = hymn(267, "https://www.churchofjesuschrist.org/music/text/hymns/how-wondrous-and-great?lang=eng", "How Wondrous and Great")
        hymns[268] = hymn(268, "https://www.churchofjesuschrist.org/music/text/hymns/come-all-whose-souls-are-lighted?lang=eng", "Come, All Whose Souls Are Lighted")
        hymns[269] = hymn(269, "https://www.churchofjesuschrist.org/music/text/hymns/jehovah-lord-of-heaven-and-earth?lang=eng", "Jehovah, Lord of Heaven and Earth")
        hymns[270] = hymn(270, "https://www.churchofjesuschrist.org/music/text/hymns/ill-go-where-you-want-me-to-go?lang=eng", "I'll Go Where You Want Me to Go")
        hymns[271] = hymn(271, "https://www.churchofjesuschrist.org/music/text/hymns/oh-holy-words-of-truth-and-love?lang=eng", "Oh, Holy Words of Truth and Love")
        hymns[272] = hymn(272, "https://www.churchofjesuschrist.org/music/text/hymns/oh-say-what-is-truth?lang=eng", "Oh Say, What Is Truth?")
        hymns[273] = hymn(273, "https://www.churchofjesuschrist.org/music/text/hymns/truth-reflects-upon-our-senses?lang=eng", "Truth Reflects upon Our Senses")
        hymns[274] = hymn(274, "https://www.churchofjesuschrist.org/music/text/hymns/the-iron-rod?lang=eng", "The Iron Rod")
        hymns[275] = hymn(275, "https://www.churchofjesuschrist.org/music/text/hymns/men-are-that-they-might-have-joy?lang=eng", "Men Are That They Might Have Joy")
        hymns[276] = hymn(276, "https://www.churchofjesuschrist.org/music/text/hymns/come-away-to-the-sunday-school?lang=eng", "When the rosy light of morning")
        hymns[277] = hymn(277, "https://www.churchofjesuschrist.org/music/text/hymns/as-i-search-the-holy-scriptures?lang=eng", "As I Search the Holy Scriptures")
        hymns[278] = hymn(278, "https://www.churchofjesuschrist.org/music/text/hymns/thanks-for-the-sabbath-school?lang=eng", "Thanks for the Sabbath School")
        hymns[279] = hymn(279, "https://www.churchofjesuschrist.org/music/text/hymns/thy-holy-word?lang=eng", "We love to hear thy holy word")
        hymns[280] = hymn(280, "https://www.churchofjesuschrist.org/music/text/hymns/welcome-welcome-sabbath-morning?lang=eng", "Welcome, Welcome, Sabbath Morning")
        hymns[281] = hymn(281, "https://www.churchofjesuschrist.org/music/text/hymns/help-me-teach-with-inspiration?lang=eng", "Help Me Teach with Inspiration")
        hymns[282] = hymn(282, "https://www.churchofjesuschrist.org/music/text/hymns/we-meet-again-in-sabbath-school?lang=eng", "We Meet Again in Sabbath School")
        hymns[283] = hymn(283, "https://www.churchofjesuschrist.org/music/text/hymns/the-glorious-gospel-light-has-shone?lang=eng", "The Glorious Gospel Light Has Shone")
        hymns[284] = hymn(284, "https://www.churchofjesuschrist.org/music/text/hymns/if-you-could-hie-to-kolob?lang=eng", "If You Could Hie to Kolob")
        hymns[285] = hymn(285, "https://www.churchofjesuschrist.org/music/text/hymns/god-moves-in-a-mysterious-way?lang=eng", "God Moves in a Mysterious Way")
        hymns[286] = hymn(286, "https://www.churchofjesuschrist.org/music/text/hymns/oh-what-songs-of-the-heart?lang=eng", "Oh, What Songs of the Heart")
        hymns[287] = hymn(287, "https://www.churchofjesuschrist.org/music/text/hymns/rise-ye-saints-and-temples-enter?lang=eng", "Rise, Ye Saints, and Temples Enter")
        hymns[288] = hymn(288, "https://www.churchofjesuschrist.org/music/text/hymns/how-beautiful-thy-temples-lord?lang=eng", "How Beautiful Thy Temples, Lord")
        hymns[289] = hymn(289, "https://www.churchofjesuschrist.org/music/text/hymns/holy-temples-on-mount-zion?lang=eng", "Holy Temples on Mount Zion")
        hymns[290] = hymn(290, "https://www.churchofjesuschrist.org/music/text/hymns/rejoice-ye-saints-of-latter-days?lang=eng", "Rejoice, Ye Saints of Latter Days")
        hymns[291] = hymn(291, "https://www.churchofjesuschrist.org/music/text/hymns/turn-your-hearts?lang=eng", "Turn Your Hearts")
        hymns[292] = hymn(292, "https://www.churchofjesuschrist.org/music/text/hymns/o-my-father?lang=eng", "O My Father")
        hymns[293] = hymn(293, "https://www.churchofjesuschrist.org/music/text/hymns/each-life-that-touches-ours-for-good?lang=eng", "Each Life That Touches Ours for Good")
        hymns[294] = hymn(294, "https://www.churchofjesuschrist.org/music/text/hymns/love-at-home?lang=eng", "There is beauty all around")
        hymns[295] = hymn(295, "https://www.churchofjesuschrist.org/music/text/hymns/o-love-that-glorifies-the-son?lang=eng", "O Love That Glorifies the Son")
        hymns[296] = hymn(296, "https://www.churchofjesuschrist.org/music/text/hymns/our-father-by-whose-name?lang=eng", "Our Father, by Whose Name")
        hymns[297] = hymn(297, "https://www.churchofjesuschrist.org/music/text/hymns/from-homes-of-saints-glad-songs-arise?lang=eng", "From Homes of Saints Glad Songs Arise")
        hymns[298] = hymn(298, "https://www.churchofjesuschrist.org/music/text/hymns/home-can-be-a-heaven-on-earth?lang=eng", "Home Can Be a Heaven on Earth")
        hymns[299] = hymn(299, "https://www.churchofjesuschrist.org/music/text/hymns/children-of-our-heavenly-father?lang=eng", "Children of Our Heavenly Father")
        hymns[300] = hymn(300, "https://www.churchofjesuschrist.org/music/text/hymns/families-can-be-together-forever?lang=eng", "I have a fam'ly here on earth.")
        hymns[301] = hymn(301, "https://www.churchofjesuschrist.org/music/text/hymns/i-am-a-child-of-god?lang=eng", "I Am a Child of God")
        hymns[302] = hymn(302, "https://www.churchofjesuschrist.org/music/text/hymns/i-know-my-father-lives?lang=eng", "I Know My Father Lives")
        hymns[303] = hymn(303, "https://www.churchofjesuschrist.org/music/text/hymns/keep-the-commandments?lang=eng", "Keep the Commandments")
        hymns[304] = hymn(304, "https://www.churchofjesuschrist.org/music/text/hymns/teach-me-to-walk-in-the-light?lang=eng", "Teach Me to Walk in the Light")
        hymns[305] = hymn(305, "https://www.churchofjesuschrist.org/music/text/hymns/the-light-divine?lang=eng", "The Light Divine")
        hymns[306] = hymn(306, "https://www.churchofjesuschrist.org/music/text/hymns/gods-daily-care?lang=eng", "God's Daily Care")
        hymns[307] = hymn(307, "https://www.churchofjesuschrist.org/music/text/hymns/in-our-lovely-deseret?lang=eng", "In Our Lovely Deseret")
        hymns[308] = hymn(308, "https://www.churchofjesuschrist.org/music/text/hymns/love-one-another?lang=eng", "Love One Another")
        hymns[309] = hymn(309, "https://www.churchofjesuschrist.org/music/text/hymns/as-sisters-in-zion-women?lang=eng", "As Sisters in Zion (Women)")
        hymns[310] = hymn(310, "https://www.churchofjesuschrist.org/music/text/hymns/a-key-was-turned-in-latter-days-women?lang=eng", "A Key Was Turned in Latter Days (Women)")
        hymns[311] = hymn(311, "https://www.churchofjesuschrist.org/music/text/hymns/we-meet-again-as-sisters-women?lang=eng", "We Meet Again as Sisters (Women)")
        hymns[312] = hymn(312, "https://www.churchofjesuschrist.org/music/text/hymns/we-ever-pray-for-thee-women?lang=eng", "We Ever Pray for Thee (Women)")
        hymns[313] = hymn(313, "https://www.churchofjesuschrist.org/music/text/hymns/god-is-love-women?lang=eng", "God Is Love (Women)")
        hymns[314] = hymn(314, "https://www.churchofjesuschrist.org/music/text/hymns/how-gentle-gods-commands-women?lang=eng", "How Gentle God's Commands (Women)")
        hymns[315] = hymn(315, "https://www.churchofjesuschrist.org/music/text/hymns/jesus-the-very-thought-of-thee-women?lang=eng", "Jesus, the Very Thought of Thee (Women)")
        hymns[316] = hymn(316, "https://www.churchofjesuschrist.org/music/text/hymns/the-lord-is-my-shepherd-women?lang=eng", "The Lord Is My Shepherd (Women)")
        hymns[317] = hymn(317, "https://www.churchofjesuschrist.org/music/text/hymns/sweet-is-the-work-women?lang=eng", "Sweet Is the Work (Women)")
        hymns[318] = hymn(318, "https://www.churchofjesuschrist.org/music/text/hymns/love-at-home-women?lang=eng", "There is beauty all around (women)")
        hymns[319] = hymn(319, "https://www.churchofjesuschrist.org/music/text/hymns/ye-elders-of-israel-men?lang=eng", "Ye Elders of Israel (Men)")
        hymns[320] = hymn(320, "https://www.churchofjesuschrist.org/music/text/hymns/the-priesthood-of-our-lord-men?lang=eng", "The Priesthood of Our Lord (Men)")
        hymns[321] = hymn(321, "https://www.churchofjesuschrist.org/music/text/hymns/ye-who-are-called-to-labor-men?lang=eng", "Ye Who Are Called to Labor (Men)")
        hymns[322] = hymn(322, "https://www.churchofjesuschrist.org/music/text/hymns/come-all-ye-sons-of-god-men?lang=eng", "Come, All Ye Sons of God (Men)")
        hymns[323] = hymn(323, "https://www.churchofjesuschrist.org/music/text/hymns/rise-up-o-men-of-god-mens-choir?lang=eng", "Rise Up, O Men of God (Men's Choir)")
        hymns[324] = hymn(324, "https://www.churchofjesuschrist.org/music/text/hymns/rise-up-o-men-of-god-men?lang=eng", "Rise Up, O Men of God (Men)")
        hymns[325] = hymn(325, "https://www.churchofjesuschrist.org/music/text/hymns/see-the-mighty-priesthood-gathered-mens-choir?lang=eng", "See the Mighty Priesthood Gathered (Men's Choir)")
        hymns[326] = hymn(326, "https://www.churchofjesuschrist.org/music/text/hymns/come-come-ye-saints-mens-choir?lang=eng", "Come, Come, Ye Saints (Men's Choir)")
        hymns[327] = hymn(327, "https://www.churchofjesuschrist.org/music/text/hymns/go-ye-messengers-of-heaven-mens-choir?lang=eng", "Go, Ye Messengers of Heaven (Men's Choir)")
        hymns[328] = hymn(328, "https://www.churchofjesuschrist.org/music/text/hymns/an-angel-from-on-high-328?lang=eng", "An Angel from on High")
        hymns[329] = hymn(329, "https://www.churchofjesuschrist.org/music/text/hymns/thy-servants-are-prepared-mens-choir?lang=eng", "Thy Servants Are Prepared (Men's Choir)")
        hymns[330] = hymn(330, "https://www.churchofjesuschrist.org/music/text/hymns/see-the-mighty-angel-flying-mens-choir?lang=eng", "See, the Mighty Angel Flying (Men's Choir)")
        hymns[331] = hymn(331, "https://www.churchofjesuschrist.org/music/text/hymns/oh-say-what-is-truth-mens-choir?lang=eng", "Oh Say, What Is Truth? (Men's Choir)")
        hymns[332] = hymn(332, "https://www.churchofjesuschrist.org/music/text/hymns/come-o-thou-king-of-kings-mens-choir?lang=eng", "Come, O Thou King of Kings (Men's Choir)")
        hymns[333] = hymn(333, "https://www.churchofjesuschrist.org/music/text/hymns/high-on-the-mountain-top-mens-choir?lang=eng", "High on the Mountain Top (Men's Choir)")
        hymns[334] = hymn(334, "https://www.churchofjesuschrist.org/music/text/hymns/i-need-thee-every-hour-mens-choir?lang=eng", "I Need Thee Every Hour (Men's Choir)")
        hymns[335] = hymn(335, "https://www.churchofjesuschrist.org/music/text/hymns/brightly-beams-our-fathers-mercy-mens-choir?lang=eng", "Brightly Beams Our Father's Mercy (Men's Choir)")
        hymns[336] = hymn(336, "https://www.churchofjesuschrist.org/music/text/hymns/school-thy-feelings-mens-choir?lang=eng", "School Thy Feelings (Men's Choir)")
        hymns[337] = hymn(337, "https://www.churchofjesuschrist.org/music/text/hymns/o-home-beloved-mens-choir?lang=eng", "O Home Beloved (Men's Choir)")
        hymns[338] = hymn(338, "https://www.churchofjesuschrist.org/music/text/hymns/america-the-beautiful?lang=eng", "Oh, beautiful for spacious skies")
        hymns[339] = hymn(339, "https://www.churchofjesuschrist.org/music/text/hymns/my-country-tis-of-thee?lang=eng", "My Country, 'Tis of Thee")
        hymns[340] = hymn(340, "https://www.churchofjesuschrist.org/music/text/hymns/the-star-spangled-banner?lang=eng", "The Star-Spangled Banner")
        hymns[341] = hymn(341, "https://www.churchofjesuschrist.org/music/text/hymns/god-save-the-king?lang=eng", "God Save the King")
        return hymns

if __name__ == '__main__':
    main()
