import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import os
import folium
from streamlit_folium import folium_static
from matplotlib import rc


# 한글 폰트 경로 설정
font_path = "/content/drive/MyDrive/워드클라우드/KOTRA_BOLD.ttf"  # 폰트 경로를 적절히 변경
rc('font', family='KOTRA_BOLD')  # Matplotlib에 폰트 적용

from PIL import Image, ImageFile
Image.MAX_IMAGE_PIXELS = None  # 이미지 크기 제한 해제
ImageFile.LOAD_TRUNCATED_IMAGES = True  # 잘린 이미지도 로드 가능

st.write('수원 문화재단 랩미인 사업 - 아주대학교 나우어스팀')

# 기본 Stopwords 리스트
default_stopwords = set(["은", "는", "이", "가", "을", "를", "에", "의", "와", "과", "도", "로", "에서", "으로", "하지만", '이제', '데리', '인계동', '수원역','편이','인식','약간','워낙','때문','보고','간다','가지','보기','의치','인근', '이유진', '천윤희','윤희','정민규','정민',\
             '민규', '이선우', '박상균', '박상','수원','느낌','생각','자주', '이혜','정승환','김영재','임채영','박채','이윤영','사고','지고','이채','정혜영','뭔가','라다','사실','참석자','가기',\
             '거기','거의','조금','태현','공간','가면','진짜','보통','거리','몰이','경우','대가','주변','사람','바로','학교','정도','타임','그냥','이용','자체'\
             ,'동훈','그냥', '이채민','박채현','오세연','안성준', '정민규', '이유진', '이선우', '박상균', '천윤희', '김영재', '권재현', '김두환', '안태현','정승환',\
            '이윤영', '정혜영', '이혜지', '김유나', '임채영', '강가연', '좌민', '김주성', '문정현', '나현욱','강동훈', '권민소','김소언',':',';',"-",'_',')','한', '것',',','–'])

# 사용자 정의 Stopwords 추가
#user_stopwords = st.sidebar.text_area(
#    "추가할 Stopwords (쉼표로 구분)", 
#    placeholder="예: 수원, 아주대, 화성"
#)

#custom_stopwords = set(user_stopwords.split(",")) if user_stopwords else set()
stopwords = default_stopwords#.union(custom_stopwords)

# 지도 데이터 정의
highlights = pd.DataFrame({
    'latitude': [37.28192317530337, 37.2610, 37.2970, 37.2792],
    'longitude': [127.0166211927431, 127.0300, 127.0470, 127.0435],
    'location': ['화성행궁', '인계동', '광교신도시', '아주대학교'],
    'image_url':['/content/drive/MyDrive/워드클라우드/광교_전체.png',
                 '/content/drive/MyDrive/워드클라우드/아주대_전체.png',
                 '/content/drive/MyDrive/워드클라우드/인계동_전체.png',
                 '/content/drive/MyDrive/워드클라우드/행궁_전체.png']
})


# 데이터 로드 함수
def load_text_data(directory):
    texts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            location = filename.split(".")[0]  # 파일명에서 위치 이름 추출
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                texts[location] = file.read()
    return texts

# 텍스트 데이터 로드
directory_path = "/content/drive/MyDrive/워드클라우드/txt파일"  # 텍스트 파일이 저장된 폴더
text_data = load_text_data(directory_path)

# 단어 빈도 계산 함수
def get_word_frequencies(text):
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return Counter(filtered_words)

# 감정 점수 계산 함수
positive_words = ["좋다", "아름답다", "뛰어나다", "행복하다", "현대적", '자주간다','좋은','좋고','좋음','제일']
negative_words = ["문제", "낙후", "불편하다", "부족하다", "혼잡하다", '별로다','별로', '안간다', '싫다','안감']

def calculate_sentiment_score(text):
    words = text.split()
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    return positive_score - negative_score

# Streamlit 앱 시작
st.title("수원 데이터 대시보드")
st.write("이 대시보드는 수원의 주요 지리적 정보와 텍스트 데이터를 분석합니다.")

# 페이지 선택
page = st.sidebar.selectbox(
    "위치를 선택하세요:",
    options=["전체 지도"] + list(highlights['location'])
)

# 메인 탭 생성
tabs = st.tabs(["지도", "텍스트 데이터 분석", '아주대 맛집 지도'])

# 첫 번째 탭: 지도
with tabs[0]:
    st.subheader("수원 주요 하이라이트 지도")
    # 전체 지도 화면
    if page == "전체 지도":
        #st.title("수원시 주요 하이라이트")
        st.map(highlights, zoom=12)
        st.write("지도를 클릭하거나 왼쪽에서 위치를 선택하세요!")

# 개별 페이지 화면
    else:
        st.title(f"{page} 정보")
    
    # 선택된 위치의 정보 가져오기
        selected = highlights[highlights['location'] == page].iloc[0]
        st.write(f"**위치 이름:** {page}")
        #st.write(f"**위도:** {selected['latitude']}")
        #st.write(f"**경도:** {selected['longitude']}")
    
    # 지도에 선택된 위치만 표시
        st.map(pd.DataFrame([selected]))
    
    # 선택한 위치의 이미지 표시
        st.image(selected['image_url'], caption=f"{page} 워드클라우드", use_container_width=True)
# 두 번째 탭: 텍스트 데이터 분석
with tabs[1]:
    st.subheader("수원 텍스트 데이터 분석")

    # 지역별 하위 탭 생성
    text_tabs = st.tabs(list(text_data.keys()))

    for i, location in enumerate(text_data.keys()):
        with text_tabs[i]:
            st.subheader(f"{location} 데이터 분석")
            
            # 텍스트 데이터 표시
            #st.write("**텍스트 미리보기:**")
            #st.text_area("텍스트 내용", text_data[location][:500] + "...", height=150)

            # 워드클라우드 생성 및 표시
            #st.write("**워드클라우드:**")
            #wc = generate_wordcloud(text_data[location])
            #fig, ax = plt.subplots()
            #ax.imshow(wc, interpolation="bilinear")
            #ax.axis("off")
            #st.pyplot(fig)

            # 단어 빈도 분석
            st.write("**단어 빈도 분석:**")
            word_frequencies = get_word_frequencies(text_data[location])
            freq_df = pd.DataFrame(word_frequencies.items(), columns=["단어", "빈도수"]).sort_values(by="빈도수", ascending=False)
            st.dataframe(freq_df)

            # 빈도수 상위 10개 단어 그래프
            st.write("**상위 10개 단어 그래프:**")
            fig, ax = plt.subplots()
            ax.bar(freq_df["단어"][:10], freq_df["빈도수"][:10])
            ax.set_title(f"{location} 상위 10개 단어 빈도수")
            ax.set_ylabel("빈도수")
            st.pyplot(fig)

            # 감정 분석
            st.subheader("감정 분석 (예제)")
            sentiment_score = calculate_sentiment_score(text_data[location])
            if sentiment_score > 0:
                sentiment = "긍정적"
            elif sentiment_score < 0:
                sentiment = "부정적"
            else:
                sentiment = "중립적"
            st.write(f"**감정 점수:** {sentiment_score} ({sentiment})")

            # 감정 점수 시각화
            fig, ax = plt.subplots()
            ax.bar(["긍정 단어", "부정 단어"], [sum(1 for word in text_data[location].split() if word in positive_words),
                                               sum(1 for word in text_data[location].split() if word in negative_words)])
            ax.set_title(f"{location} 감정 분석")
            ax.set_ylabel("단어 수")
            st.pyplot(fig)

with tabs[2]:
    # 데이터 로드
    @st.cache_data
    def load_data():
        return pd.read_csv('/content/drive/MyDrive/워드클라우드/아주 맛집.csv')

    data = load_data()

    # Streamlit UI
    st.title("아주대 인근 맛집 지도")
    st.sidebar.header("필터")

    # 음식 종류 필터 추가
    selected_type = st.sidebar.multiselect(
        "음식 종류 필터",
        options=data['description'].unique(),
        default=data['description'].unique()
    )

    filtered_data = data[data['description'].isin(selected_type)]

    # Folium 지도 생성
    st.subheader("맛집 지도")
    m = folium.Map(location=[37.2833, 127.0457], zoom_start=15)

    for index, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"<b>{row['name']}</b><br>{row['description']}",
            tooltip=row['name']
        ).add_to(m)

    # Streamlit에 지도 표시
    folium_static(m)

    # 맛집 목록 표시
    st.subheader("맛집 목록")
    st.write(filtered_data[['name', 'description']])


