# classifier.py
URGENT_KEYWORDS = [
    'help', 'beating', 'hit', 'kill', 'hurt', 'bleeding', 'knife', 'police', 
    'danger', 'emergency', 'abuse', 'raping', 'choking', 'scared',
    'ударил', 'ударит', 'убить', 'убьет', 'убьют', 'угрожает', 'угрожал',
    'нож', 'кровь', 'помогите', 'насилие', 'избил', 'избивает', 'душит',
    'душил', 'напал', 'нападает', 'опасно', 'срочно', 'умру', 'умираю',
    'побои', 'запер', 'заперта', 'связал', 'режет', 'ранил',
    'урду', 'ур-тепсейт', 'өлтүр', 'өлтүрөт', 'коркутат', 'коркутту',
    'бычак', 'кан', 'жардам', 'зомбулук', 'муунтуп', 'муунтту',
    'кол салды', 'шашылыш', 'өлөм', 'өлүп жатам', 'качырды', 'байлады'
]

HIGH_KEYWORDS = [
    'harass', 'follow', 'stalk', 'money', 'control',
    'харасмент', 'преследует', 'преследовал', 'следит', 'следил',
    'не пускает', 'не выпускает', 'забирает деньги', 'запрещает',
    'изолирует', 'контролирует', 'оскорбляет', 'унижает', 'шантажирует',
    'отбирает телефон', 'читает сообщения',
    'кысым', 'көзөмөлдөйт', 'көзөмөлдөдү', 'акча албайт', 'акча бербейт',
    'кордойт', 'кордоду', 'басмырлайт', 'басмырлады', 'телефон албайт',
    'эшик ачпайт', 'үйгө киргизбейт'
]

MEDIUM_KEYWORDS = [
    'scared', 'cry', 'lonely', 'depress', 'anxiety', 'sad',
    'страшно', 'боюсь', 'плачу', 'одиноко', 'депрессия', 'тревога',
    'не могу', 'устала', 'помощь', 'поддержка', 'консультация',
    'не знаю что делать', 'нет сил', 'хочу уйти', 'устала терпеть',
    'корком', 'корктом', 'ыйлайм', 'ыйладым', 'жалгыз', 'көмөк',
    'колдоо', 'кеңеш', 'эмне кыларымды билбейм', 'күчүм жок',
    'кетким келет', 'чарчадым'
]

CALLBACK_KEYWORDS = ['call me', 'callback', 'ring me', 'позвони', 'перезвони', 'позвоните', 'чал', 'чалыңыз', 'кайра чал']

CATEGORY_MAP = {
    'violence': ['help', 'beating', 'hit', 'kill', 'hurt', 'knife', 'ударил', 'ударит', 'избил', 'избивает', 'нож', 'кровь', 'душит', 'душил', 'напал', 'нападает', 'побои', 'ранил', 'режет', 'урду', 'ур-тепсейт', 'бычак', 'кан', 'муунтуп', 'муунтту', 'кол салды'],
    'threats': ['убить', 'убьет', 'убьют', 'угрожает', 'угрожал', 'запер', 'заперта', 'связал', 'өлтүр', 'өлтүрөт', 'коркутат', 'коркутту', 'байлады'],
    'harassment': ['stalk', 'follow', 'преследует', 'преследовал', 'следит', 'следил', 'харасмент', 'көзөмөлдөйт', 'көзөмөлдөдү'],
    'economic': ['money', 'деньги', 'забирает', 'не пускает', 'не выпускает', 'акча', 'акча албайт', 'акча бербейт', 'телефон албайт'],
    'psychological': ['scared', 'cry', 'sad', 'оскорбляет', 'унижает', 'страшно', 'боюсь', 'кордойт', 'кордоду', 'басмырлайт', 'басмырлады', 'корком', 'корктом']
}

def classify(text):
    text_lower = text.lower()
    if any(kw in text_lower for kw in URGENT_KEYWORDS): severity = 'urgent'
    elif any(kw in text_lower for kw in HIGH_KEYWORDS): severity = 'high'
    elif any(kw in text_lower for kw in MEDIUM_KEYWORDS): severity = 'medium'
    else: severity = 'low'

    category = 'general'
    for cat, keywords in CATEGORY_MAP.items():
        if any(kw in text_lower for kw in keywords):
            category = cat
            break
    return severity, category

def detect_callback(text):
    return any(kw in text.lower() for kw in CALLBACK_KEYWORDS)

def detect_codeword(text):
    stripped = text.strip()
    if stripped.startswith('KOD:'): return stripped[4:].strip()
    words = stripped.split()
    if len(words) == 1 and words[0].isupper() and len(words[0]) >= 4: return words[0]
    return None