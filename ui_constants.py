CSS = """
    <style>
        header {visibility: hidden;}
        div[class^='block-container'] { padding-top: 2rem; }
    </style>
"""

TAB_ICON = None

def TAB_TITLE(l):
    return (
        'YPP AI Assistant' if l == "English" else
        'YPP AI アシスタント'
    )

def TITLE(l):
    return (
        'Partner Manager AI Support' if l == "English" else
        'パートナーマネージャー AI サポート'
        )

def SUBTITLE(l):
    return (
        '☝ I can only answer information written in the Creator Support, which is public info. Please make sure to check the link to the information source in the left column and do not blindly accept AI-generated information.' if l == "English" else
        '☝ YouTubeクリエーターサポートに書いている情報のみ答えられます。AIの情報を鵜呑みにせずに、左カラムの情報ソースのリンクを必ず確認して下さい。'
    )

def INPUT_HOLDER(l):
    return (
        'Ask me a question about YouTube!  I will not remember previous conversations.' if l == "English" else
        'YouTubeに関する質問をして下さい。過去の会話は記憶しないことにご留意ください。'
    )

def CLEAR_BUTTON(l):
    return (
        'Clear' if l == "English" else
        '会話をクリア'
    )

def SIDEBAR_SUBTITLE(l):
    return (
        '[ Resources ]' if l == "English" else
        '[ 情報ソース ]'
    )