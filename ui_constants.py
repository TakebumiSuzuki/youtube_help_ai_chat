CSS = """
    <style>
        header {visibility: hidden;}
        div[class^='block-container'] { padding-top: 2rem; }
    </style>
"""

TAB_ICON = None

def TAB_TITLE(l):
    return 'YPP AI Assistant'


def TITLE(l):
    if l == 'Japanse':
        return 'パートナーマネージャー AI サポート'
    else:
        return 'Partner Manager AI Support'

def SUBTITLE(l):
    if l == 'Japanse':
        return '⚠️ YouTubeクリエーターサポートに書いている情報のみ答えられます。AIの情報を鵜呑みにせずに、左カラムの情報ソースのリンクを必ず確認して下さい。'
    elif l == 'Spanish':
        return '⚠️ Solo puedo responder con información escrita en el Soporte para Creadores de YouTube. No tome la información de IA al pie de la letra y siempre verifique los enlaces de las fuentes de información en la columna izquierda.'
    elif l == 'Indonesian':
        return '⚠️ Saya hanya dapat menjawab berdasarkan informasi yang tertulis di Dukungan Kreator YouTube. Jangan langsung mempercayai informasi AI dan selalu periksa tautan sumber informasi di kolom sebelah kiri.'
    elif l == 'Korean':
        return '⚠️ YouTube 크리에이터 지원에 작성된 정보만 답변할 수 있습니다. AI 정보를 그대로 받아들이지 마시고 왼쪽 열의 정보 출처 링크를 반드시 확인해 주세요.'
    elif l == 'Vietnamese':
        return '⚠️ Chỉ có thể trả lời thông tin được viết trên Hỗ trợ người sáng tạo của YouTube. Đừng tin hoàn toàn vào thông tin từ AI, hãy luôn kiểm tra các liên kết nguồn thông tin trong cột bên trái.'
    else:
        return '⚠️ I can only answer based on information written in YouTube Creator Support. Please do not take AI information at face value and always check the information source links in the left column.'


def INPUT_HOLDER(l):
    if l == 'Japanse':
        return 'YouTubeに関する質問をして下さい。過去の会話は記憶しないことにご留意ください。'
    elif l == 'Spanish':
        return 'Por favor, haga una pregunta sobre YouTube. Tenga en cuenta que las conversaciones anteriores no se recuerdan.'
    elif l == 'Indonesian':
        return 'Silakan ajukan pertanyaan tentang YouTube. Harap diingat bahwa percakapan sebelumnya tidak diingat.'
    elif l == 'Korean':
        return 'YouTube에 대한 질문을 해 주세요. 이전 대화는 기억하지 않는다는 점을 유의해 주세요.'
    elif l == 'Vietnamese':
        return 'YouTube liên quan đến câu hỏi. Xin lưu ý rằng cuộc trò chuyện trước đó sẽ không được ghi nhớ.'
    else:
        return 'Please ask a question about YouTube. Please note that previous conversations are not remembered.'


def CLEAR_BUTTON(l):
    return 'CLEAR'

def DOC_HISTORY(l):
    return 'Doc History'

def SIDEBAR_SUBTITLE(l):
    if l == 'Japanse':
        return '[情報ソース]'
    elif l == 'Spanish':
        return '[FUENTES]'
    elif l == 'Indonesian':
        return '[SUMBER]'
    elif l == 'Korean':
        return '[출처]'
    elif l == 'Vietnamese':
        return '[NGUỒN THÔNG TIN]'
    else:
        return '[SOURCES]'