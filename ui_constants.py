CSS = """
    <style>
        header {visibility: hidden;}
        div[class^='block-container'] { padding-top: 2rem; }

        section[data-testid="stSidebar"] {
            width: 1000px !important; # Set the width to your desired value
        }
    </style>
"""

TAB_ICON = None

JAPANESE = 'Japanese'
SPANISH = 'Spanish'
INDONESIAN = 'Indonesian'
KOREAN = 'Korean'
VIETNAMESE = 'Vietnamese'
THAI = 'Thai'
ENGLISH = 'English'


def TAB_TITLE(l):
    return 'YPP AI Assistant'


def TITLE(l):
    if l == JAPANESE:
        return 'パートナーマネージャー AI サポート'
    else:
        return 'Partner Manager AI Support'

def SUBTITLE(l):
    if l == JAPANESE:
        return '⚠️ YouTubeクリエーターサポートに書いている情報のみ答えられます。AIの情報を鵜呑みにせずに、左カラムの情報ソースのリンクを必ず確認して下さい。'
    elif l == SPANISH:
        return '⚠️ Solo puedo responder con información escrita en el Soporte para Creadores de YouTube. No tome la información de IA al pie de la letra y siempre verifique los enlaces de las fuentes de información en la columna izquierda.'
    elif l == INDONESIAN:
        return '⚠️ Saya hanya dapat menjawab berdasarkan informasi yang tertulis di Dukungan Kreator YouTube. Jangan langsung mempercayai informasi AI dan selalu periksa tautan sumber informasi di kolom sebelah kiri.'
    elif l == KOREAN:
        return '⚠️ YouTube 크리에이터 지원에 작성된 정보만 답변할 수 있습니다. AI 정보를 그대로 받아들이지 마시고 왼쪽 열의 정보 출처 링크를 반드시 확인해 주세요.'
    elif l == VIETNAMESE:
        return '⚠️ Chỉ có thể trả lời thông tin được viết trên Hỗ trợ người sáng tạo của YouTube. Đừng tin hoàn toàn vào thông tin từ AI, hãy luôn kiểm tra các liên kết nguồn thông tin trong cột bên trái.'
    elif l == THAI:
        return 'ฉันสามารถตอบได้ตามข้อมูลที่เขียนไว้ใน YouTube Creator Support เท่านั้น กรุณาอย่ารับข้อมูลจาก AI อย่างผิวเผิน และโปรดตรวจสอบลิงก์แหล่งข้อมูลที่อยู่ในคอลัมน์ด้านซ้ายเสมอ'
    else:
        return '⚠️ I can only answer based on information written in YouTube Creator Support. Please do not take AI information at face value and always check the information source links in the left column.'


def INPUT_HOLDER(l):
    if l == JAPANESE:
        return 'YouTubeに関する質問をして下さい。過去の会話は記憶しないことにご留意ください。'
    elif l == SPANISH:
        return 'Por favor, haga una pregunta sobre YouTube. Tenga en cuenta que las conversaciones anteriores no se recuerdan.'
    elif l == INDONESIAN:
        return 'Silakan ajukan pertanyaan tentang YouTube. Harap diingat bahwa percakapan sebelumnya tidak diingat.'
    elif l == KOREAN:
        return 'YouTube에 대한 질문을 해 주세요. 이전 대화는 기억하지 않는다는 점을 유의해 주세요.'
    elif l == VIETNAMESE:
        return 'YouTube liên quan đến câu hỏi. Xin lưu ý rằng cuộc trò chuyện trước đó sẽ không được ghi nhớ.'
    elif l == THAI:
        return 'กรุณาถามคำถามเกี่ยวกับ YouTube และโปรดทราบว่าฉันจะไม่จดจำการสนทนาในอดีต'
    else:
        return 'Please ask a question about YouTube. Please note that previous conversations are not remembered.'


def CLEAR_BUTTON(l):
    return 'CLEAR'

def DOC_HISTORY(l):
    return 'Doc History'

def SIDEBAR_SUBTITLE(l):
    if l == JAPANESE:
        return '[情報ソース]'
    elif l == SPANISH:
        return '[FUENTES]'
    elif l == INDONESIAN:
        return '[SUMBER]'
    elif l == KOREAN:
        return '[출처]'
    elif l == VIETNAMESE:
        return '[NGUỒN THÔNG TIN]'
    elif l == THAI:
        return '[แหล่งข้อมูล]'
    else:
        return '[SOURCES]'