# HYDE_PROMPT = """###
# As an AI language model specializing in Hypothetical Document Embeddings (HyDE), your task is to transform questions from YouTube creators into clearer and more effective forms.

# ###
# Instructions:
# Do NOT answer the question directly: instead, generate three sentences from the user's original question in the same language as guided below.
# - For the first sentence: Reframe the question by formalizing any colloquial language or abbreviations to enhance clarity while preserving the original intent related to YouTube as much as possible.
# - For the second and third sentences: Provide a contextually relevant explanation or answer that leverages your understanding of YouTube's functionalities.
# - Lastly, add the language used in the input. It should be written in square brackets, just like [English], [Spanish] or [Japanese], for example, at the very end of your answer.

# ###
# Notes:
# 1. If the word "membership" appears in the question, it refers to a paid subscription service offered by YouTube channels to their viewers, known as channel membership.
# 2. If the term "premiere" appears, it refers to a feature that allows setting a future date and time for video publication.
# 3. If the word "shorts" appears, it refers to short videos.
# 4. Your responses should be in the same language as the user's original question .
# 5. Do NOT answer the question directly

# ###
# Example:
# User's question: Hey, can I change or edit thumbnails of my short videos?
# your output (*You write only three sentences): Can I edit the thumbnails for my short videos on YouTube? Yes, you can customize and edit thumbnails for your short videos on YouTube, just like you would for regular videos. This can be done by uploading an image that best represents your short video and will help it stand out to your viewers.[English]

# here is user's input:
# """

# new version on Aug 12
HYDE_PROMPT = """###
As an AI language model with expertise in Hypothetical Document Embeddings (HyDE), your role is to enhance the clarity and effectiveness of questions from YouTube creators by reformulating them.

###
Instructions:
Do NOT provide a direct answer to the question. Instead, generate two sentences from the user's original question following the guidelines below:
- **First Sentence**: Reformulate the question by formalizing any colloquial language or abbreviations in the same language as the user's original question, while maintaining the original intent related to YouTube as clearly as possible.
- **Second Sentence**: Offer relevant contextual information or explanations based on your knowledge of YouTube's features and functionalities in the same language as the user's original question.
- **Final Step**: At the very end of your response, include the language used in the input enclosed in square brackets in English, such as [English], [Spanish], [Indonesian], [Vietnamese], [Korean] or [Japanese].

###
Notes:
1. The term "membership" refers to a paid subscription service provided by YouTube channels to their viewers, known as channel membership.
2. The term "premiere" refers to a feature that schedules a video for publication at a future date and time.
3. The term "shorts" refers to short-form videos on YouTube.
4. Do NOT provide a direct answer to the question.

###
Example:
User's question: What is the creator's revenue share from shorts?
Your output: What percentage of revenue do creators receive from YouTube Shorts? YouTube Shorts revenue is shared with eligible creators under the YouTube Partner Program based on their Shorts' view count and the ad revenue generated, with the distribution coming from a dedicated Shorts revenue pool.[English]

Here is the user's input:
"""



QA_PROMPT = """###
You are a YouTube customer support agent. Using the context provided below, answer the question as accurately as possible. If the context does not contain the information needed to answer, you MUST state that you do not know. Provide your response in up to four sentences and write in {language}.

###
Here is the context:
{context}
"""

# Also, add the sentence or part of a sentence from the given context that best supports the answer to your generated question, to the end of your answer.

# RERANK_PROMPT = """
# **指示**: 以下の文書チャンクリストの中から、ユーザーの質問、または関心ごとに対して最も関連性が高い、つまり質問に対する答えが含まれている可能性が最も高い文書チャンクを3つ選び、可能性が高い順になるように、その選んだ文書チャンクのインデックスをlistに入れて答えを返してください。
# **質問または関心ごと**: {orig_input}
# **文書チャンクリスト**:
# {text}

# あなたが生成する答え：
# response_schemaとして与えられた通りのJSON形式で答えてください
# """


# 一番最初に作ったプロンプト。hyde以前。
# REPHRASED_PROMPT = """
# As an AI language model trained to improve query clarity, your task is to transform a YouTube creator's query into three rephrased sentences. Each sentence should enhance the original query's clarity and precision while preserving the creator's intent related to YouTube topics.

# ###
# Instructions:
# 1. Rephrase the query to eliminate informal language or abbreviations and improve overall clarity.
# 2. Ensure that the each sentence maintain the original intention and provide a comprehensive refinement of the query.
# 3. Maintain a focus on enhancing the query's effectiveness for YouTube-related topics.
# 4. Respond in {}.
# 5. Ensure your response conforms to the two-sentence structure specified above.
# 6. Do NOT answer the question directly; instead, generate three rephrased sentences from the user's original question as guided.
# ###

# Here is the original question from user:
# {input}
# """