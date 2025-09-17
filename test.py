import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
api_key = os.getenv("api-key")
client = OpenAI(api_key = api_key)

title = "프로그래밍 언어 번역기"

# 시작색과 끝색 (빨강 → 보라)
start_color = (255, 0, 0)   # 빨강
end_color   = (139, 0, 255) # 보라

def rgb_to_hex(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

colored_title = ""
n = len(title)

for i, char in enumerate(title):
    # 글자 위치 비율
    ratio = i / (n - 1)
    # 선형 보간
    r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
    
    colored_title += f"<span style='color:{rgb_to_hex((r,g,b))}'>{char}</span>"


#타이틀 생성
st.markdown(f"<h1 style='text-align:center'>{colored_title}</h1>", unsafe_allow_html=True)

#radio 버튼 생성
start_lang = st.radio("원본 언어는 무엇인가요?", ("C", "C++", "C#", "java", "java script", "python"), horizontal = True)
end_lang = st.radio("어떤 언어로 변경할까요?", ("C", "C++", "C#", "java", "java script", "python"), horizontal = True)

#코드 입력 창 생성
st.text_area("번역할 코드를 개발자가 가장 잘 하는 방식으로 쓰세요.", key = "code")

#번역 버튼 눌렀을 때
if st.button("번역"):
    sys_prompt = '''
    #입력
    (프로그래밍 언어) -> (프로그래밍 언어)
    (프로그래밍 코드)
    
    #역할
    해당 입력과 동일한 역할을 하는 프로그래밍 코드를 화살표 뒤 언어로 작성
    
    #주의사항
    1. 해당 코드 부분만이 아니라, 똑같은 기능을 하도록 모든 부분을 작성
    2. 식별자는 변경하지 않을 것.
    3. 정의 되어 있지 않은 변수가 사용되는 부분에는 줄 마지막에 주석으로 '(변수의 식별자)은/는 정의되지 않았다'고 출력.
    4. 3의 상황을 제외하고는 주석을 달지 않을 것.(단, 원본 코드에 주석이 있을 경우 작성.)
    5. 시작 언어의 문법이 잘못된 부분이 있거나, 해당 언어가 아닐 경우 '코드에 문제가 있습니다.'출력
    6. 반드시 코드 혹은 정해진 메세지만 출력할 것.
    7. markdown 문법 쓰지 마.
    8. python으로 번역할 경우에는 메인 클래스와 함수를 필요하지 않은 경우에는 구현하지 않는다.
    '''
    #openAI API 호출
    response = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
            {"role" : "system",
             "content" : sys_prompt},
            {"role" : "user",
             "content" : f"{start_lang} -> {end_lang}"},
            {"role" : "user",
             "content" : st.session_state.code}
        ]
    )

    #웹 페이지에 코드 띄우기
    st.code(response.choices[0].message.content)