from flags import *
class Keywords:
    def __init__(self,animals,action,countries):
        self.animals = animals
        self.action = action
        self.countries = countries

ENGLISH_TEST_KEYWORDS = Keywords(
    ['Elephant', 'Tiger', 'calf'],
    ['kill'],
    ['Indonesia', 'Sri-lanka', 'Sri lanka', 'India', 'Malaysia', 'Thailand']
)

ENGLISH_KEYWORDS = Keywords(
    ['Elephant', 'Tiger', 'calf'],
    ['kill', 'kills' , 'killed', 'dead', 'death', 'dies', 'tusker', 'poacher', 'shot', 'electrocuted', 'found dead', 'tusks', 'injured', 'electrocution', 'poisoned', 'ivory'],
    ['Indonesia', 'Sri-lanka', 'Sri lanka', 'India', 'Malaysia', 'Thailand']
)

HINDI_KEYWORDS = Keywords(
    ['हाथी', 'बाघ', 'बछड़ा'],
    ['मार', 'मारता है', 'मारा गया', 'मृत', 'मौत', 'मरता है', 'हाथी नर', 'शिकारी', 'गोली मारी गई', 'बिजली से मारा गया', 'मृत मिला', 'हाथी की दांत', 'घायल', 'बिजली से मौत', 'जहरीला', 'हाथी की इवोरी'],
    ['इंडोनेशिया', 'श्रीलंका', 'श्री लंका', 'भारत', 'मलेशिया', 'थाईलैंड']
)

BENGALI_KEYWORDS = Keywords(
    ['হাতি', 'বাঘ', 'শিশু হাতি'],
    ['হত্যা করা', 'মারে', 'মারা গিয়েছে', 'মৃত', 'মৃত্যু', 'মারা যায়', 'টাসকার', 'শিকারি', 'গুলি মারা', 'বৈদ্যুতিন মৃত্যু', 'মৃত পাওয়া গিয়েছে', 'হাতির দাঁত', 'আহত', 'বৈদ্যুতিন হত্যা', 'জাহার', 'হাতির ইভোরি'],
    ['ইন্দোনেশিয়া', 'শ্রীলংকা', 'শ্রীলংকা', 'ভারত', 'মালয়েশিয়া', 'থাইল্যান্ড']
)

MARATHI_KEYWORDS = Keywords(['हत्ती', 'वाघ', 'कंबळ'],
    ['मारा', 'मारतो', 'मारला', 'मृत्यु', 'मौत', 'मरतो', 'तुस्कर', 'पोचर', 'गोली मारली', 'विद्युतप्रक्रियेन मृत्यु', 'मृत्यू', 'हत्त्यारे दंत', 'जखमी', 'विद्युतप्रक्रियेन मौत', 'विषाक्त', 'इवोरी'],
    ['इंडोनेशिया', 'श्रीलंका', 'श्री लंका', 'भारत', 'मलेशिया', 'थायलंड']
)

TELUGU_KEYWORDS = Keywords(['ఏనుగు', 'పులి', 'కొండ'],
    ['కొల్లు', 'చంపించు', 'చంపబడినది', 'మృతి', 'మరణం', 'చనిపిస్తుంది', 'టస్కర్', 'శికారి', 'గుండు చేసినది', 'ఇలెక్ట్రాక్యూటెడ్', 'మృతికి కనబడినది', 'ఏనుగునారి దంతాలు', 'గాయం పొందినది', 'ఇలెక్ట్రాక్యూటెడ్', 'విషపూరితంగా', 'ఐవరి'],
    ['ఇండోనేషియా', 'శ్రీలంక', 'ఇండియా', 'మలేషియా', 'థాయిలాండ్']
)

INDONESIAN_KEYWORDS = Keywords(
    ['Gajah', 'Harimau', 'Anak gajah'],
    ['Bunuh', 'Membunuh', 'Dibunuh', 'Mati', 'Kematian', 'Matipucuk', 'Gajah jantan', 'Pemburu', 'Ditembak', 'Dielektro', 'Ditemukan mati', 'Gading', 'Terluka', 'Dielektro', 'Diracun', 'Gading gajah'],
    ['Indonesia', 'Sri Lanka', 'India', 'Malaysia', 'Thailand']
)

THAI_KEYWORDS = Keywords(
    ['ช้าง', 'เสือ', 'ลูกช้าง'],
    ['ฆ่า', 'ฆ่า', 'ถูกฆ่า', 'ตาย', 'การตาย', 'ตาย', 'ตัสเกอร์', 'นักล่า', 'ยิง', 'ถูกกระแทกไฟฟ้า', 'พบตาย', 'งานงบ', 'บาดเจ็บ', 'ถูกกระแทกไฟฟ้า', 'ถูกให้พิษ', 'งานงบ象ไทย'],
    ['อินโดนีเซีย', 'ศรีลังกา', 'อินเดีย', 'มาเลเซีย', 'ไทย']
)

def build_keywords():
    keywords_list = []
    if USE_ENGLISH_TEST:
        keywords_list.append(ENGLISH_TEST_KEYWORDS)
    if USE_ENGLISH:
        keywords_list.append(ENGLISH_KEYWORDS)
    if USE_HINDI:
        keywords_list.append(HINDI_KEYWORDS)
    if USE_BENGALI:
        keywords_list.append(BENGALI_KEYWORDS)
    if USE_MARATHI:
        keywords_list.append(MARATHI_KEYWORDS)
    if USE_TELUGU:
        keywords_list.append(TELUGU_KEYWORDS)
    if USE_INDONESIAN:
        keywords_list.append(INDONESIAN_KEYWORDS)
    if USE_THAI:
        keywords_list.append(THAI_KEYWORDS)
    return keywords_list
