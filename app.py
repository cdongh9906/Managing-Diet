import streamlit as st
from openai import OpenAI
import json

# ── 페이지 설정 ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="내 손안의 스마트 PT",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 스타일 ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

/* 메인 앱 배경 테마 연동 */
.stApp { background-color: var(--background-color) !important; }

/* 사이드바 텍스트 기본색 */
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: var(--text-color) !important; }
[data-testid="stSidebar"] hr { border-color: rgba(128,128,128,0.2); }
[data-testid="stSidebar"] label {
    color: var(--text-color) !important;
    opacity: 0.7;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* 🚨 사이드바 입력창만 타겟팅 (메인 영역 절대 침범 안 함!) */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] div[data-baseweb="select"] > div,
[data-testid="stSidebar"] div[data-baseweb="select"] span {
    background-color: var(--secondary-background-color) !important; /* 옅은 회색 적용 */
    color: var(--text-color) !important;
    border: 1px solid rgba(128, 128, 128, 0.3) !important;
    border-radius: 6px;
}
[data-testid="stSidebar"] [data-baseweb="select"] input {
    display: none !important;
    pointer-events: none !important;
}

/* 메인 텍스트 테마 연동 */
.hero-title { font-size: 2rem; font-weight: 700; color: var(--text-color); letter-spacing: -0.02em; line-height: 1.2; }
.hero-sub { font-size: 0.95rem; color: var(--text-color); opacity: 0.7; margin-top: 4px; margin-bottom: 28px; }
.section-header { font-size: 1rem; font-weight: 700; color: var(--text-color); letter-spacing: -0.01em; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid rgba(128,128,128,0.2); }

/* 매크로 카드 및 칩 테마 자동 대응 */
.macro-card { background: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.2); border-radius: 16px; padding: 20px 24px; color: var(--text-color); margin-bottom: 20px; }
.macro-card .label { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.6; margin-bottom: 2px; }
.macro-card .value { font-size: 2rem; font-weight: 700; color: var(--text-color); line-height: 1.1; }
.macro-card .unit  { font-size: 0.85rem; opacity: 0.6; }
.macro-row { display: flex; gap: 12px; margin-top: 14px; }
.macro-chip { flex: 1; background: var(--background-color); border-radius: 10px; padding: 10px 12px; border: 1px solid rgba(128,128,128,0.1); }
.macro-chip .chip-label { font-size: 0.65rem; opacity: 0.6; letter-spacing: 0.08em; text-transform: uppercase; }
.macro-chip .chip-val { font-size: 1.1rem; font-weight: 600; margin-top: 2px; }
.carb { color: #F4A261; } .prot { color: #6FCF97; } .fat  { color: #7EB8F7; }

/* 개별 식단 카드 테마 자동 대응 */
.meal-card { background: var(--background-color); border-radius: 14px; padding: 18px 20px; margin-bottom: 12px; border: 1px solid rgba(128,128,128,0.2); position: relative; }
.meal-tag { display: inline-block; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; padding: 3px 8px; border-radius: 6px; margin-bottom: 8px; }
.tag-breakfast { background: rgba(45,122,79,0.1); color: #2D7A4F; } .tag-lunch { background: rgba(74,95,193,0.1); color: #4A5FC1; } .tag-dinner { background: rgba(196,122,58,0.1); color: #C47A3A; }
.meal-name   { font-size: 1.05rem; font-weight: 600; color: var(--text-color); margin-bottom: 4px; }
.meal-detail { font-size: 0.82rem; color: var(--text-color); opacity: 0.7; line-height: 1.5; }
.meal-kcal   { position: absolute; top: 18px; right: 20px; font-size: 0.8rem; opacity: 0.6; font-weight: 500; }

.edit-panel { background: var(--secondary-background-color); border-radius: 14px; padding: 16px 20px; margin-top: 8px; }
.edit-panel-title { font-size: 0.8rem; font-weight: 600; opacity: 0.8; margin-bottom: 10px; letter-spacing: 0.04em; }

.empty-state { text-align: center; padding: 80px 20px; opacity: 0.6; color: var(--text-color); }
.empty-state .icon { font-size: 3rem; margin-bottom: 12px; }
.empty-state .msg  { font-size: 1rem; }

.stButton button { border-radius: 10px !important; font-family: 'Noto Sans KR', sans-serif !important; font-weight: 500 !important; }

/* ✅ 캘린더형 주간표 테마 자동 대응 */
.week-cal-wrap { margin-top: 8px; }
.week-cal-grid { display: grid; grid-template-columns: repeat(7, minmax(180px, 1fr)); gap: 10px; }
.day-card { background: var(--background-color); border: 1px solid rgba(128,128,128,0.2); border-radius: 12px; padding: 10px 10px 12px 10px; min-height: 360px; box-shadow: 0 1px 0 rgba(0,0,0,0.02); }
.day-head { border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 8px; margin-bottom: 8px; }
.day-title { font-size: 0.93rem; font-weight: 700; color: var(--text-color); }
.day-kcal { font-size: 0.75rem; opacity: 0.6; margin-top: 2px; }
.meal-block { background: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.1); border-radius: 8px; padding: 8px; margin-bottom: 8px; }
.meal-type { font-size: 0.72rem; font-weight: 700; letter-spacing: .04em; opacity: 0.7; margin-bottom: 4px; }
.meal-name-mini { font-size: 0.82rem; font-weight: 700; color: var(--text-color); margin-bottom: 4px; line-height: 1.35; }
.material-line { font-size: 0.76rem; opacity: 0.8; line-height: 1.35; }
.meal-kcal-mini { margin-top: 4px; font-size: 0.75rem; opacity: 0.6; font-weight: 600; }
.cheat-box { background: rgba(245, 215, 171, 0.15); border: 1px solid rgba(245, 215, 171, 0.5); border-radius: 8px; padding: 10px; font-size: 0.82rem; color: #D48000; line-height: 1.4; }
@media (max-width: 1400px) { .week-cal-grid { grid-template-columns: repeat(4, minmax(180px, 1fr)); } }
@media (max-width: 1000px) { .week-cal-grid { grid-template-columns: repeat(2, minmax(180px, 1fr)); } }
@media (max-width: 640px) { .week-cal-grid { grid-template-columns: 1fr; } }
</style>
""", unsafe_allow_html=True)

# ── 상수 ──────────────────────────────────────────────────────────────────────
GOAL_ADJUST = {
    "다이어트": -400, "린매스업 (상승 다이어트)": -100, "체중 유지": 0,
    "린매스업 (벌크)": +200, "벌크업": +400,
}
MACRO_RATIO = {
    "다이어트": {"carb": 0.40, "prot": 0.35, "fat": 0.25},
    "린매스업 (상승 다이어트)": {"carb": 0.42, "prot": 0.33, "fat": 0.25},
    "체중 유지": {"carb": 0.45, "prot": 0.30, "fat": 0.25},
    "린매스업 (벌크)": {"carb": 0.48, "prot": 0.28, "fat": 0.24},
    "벌크업": {"carb": 0.50, "prot": 0.25, "fat": 0.25},
}
ACTIVITY_MET = {
    "사무직 (앉아있는 시간이 김)": 1.2, "반-현장직 (사무와 현장 점검을 병행)": 1.375, "현장직 (신체 활동이 많음)": 1.55,
}
EXERCISE_ADD = {
    "0회": 0.0, "1회": 0.05, "2회": 0.10, "3회": 0.15, "4회": 0.175, "5회": 0.19, "6회 이상": 0.20,
}
ALLERGY_OPTIONS = ["유제품", "갑각류", "견과류", "글루텐 (밀)", "달걀", "콩류", "생선", "돼지고기", "소고기"]
PROTEIN_OPTIONS = ["닭가슴살", "소고기", "돼지고기 (삼겹살 제외)", "달걀", "연어", "참치 (캔)", "두부", "견과류", "그릭요거트", "프로틴 파우더"]
STYLE_OPTIONS = ["한식 (밥 위주)", "양식 (파스타/빵 위주)", "멕시칸 (부리또/타코)", "일식 (덮밥/스시)", "간편식 (샌드위치/샐러드)", "골고루"]

# ── 백엔드 로직 ───────────────────────────────────────────────────────────────
def calc_tdee(gender, age, height, weight, activity, exercise_freq):
    bmr = (10 * weight + 6.25 * height - 5 * age + 5) if gender == "남성" else (10 * weight + 6.25 * height - 5 * age - 161)
    return bmr * (ACTIVITY_MET[activity] + EXERCISE_ADD[exercise_freq])

def calc_target(tdee, goal):
    return tdee + GOAL_ADJUST[goal]

def calc_macros(kcal, goal):
    r = MACRO_RATIO[goal]
    return {"carb": round(kcal * r["carb"] / 4), "prot": round(kcal * r["prot"] / 4), "fat": round(kcal * r["fat"] / 9)}

# ── GitHub Models 클라이언트 및 API 연동 ──────────────────────────────────────
@st.cache_resource
def configure_llm():
    token = st.secrets.get("GITHUB_TOKEN", "")
    base_url = st.secrets.get("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference")
    if not token:
        raise ValueError("GITHUB_TOKEN이 비어 있습니다. .streamlit/secrets.toml을 확인하세요.")
    return OpenAI(base_url=base_url, api_key=token)

def call_llm(prompt, spinner_msg):
    client = configure_llm()
    model_name = st.secrets.get("GITHUB_MODEL", "openai/gpt-4.1-mini")

    with st.spinner(spinner_msg):
        resp = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "당신은 영양사이자 식단 전문가입니다. 반드시 유효한 JSON만 출력하세요."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

    raw = (resp.choices[0].message.content or "").strip()
    return json.loads(raw)

def build_diet_prompt(params, kcal, macros):
    allergy_str = ", ".join(params["allergies"]) if params["allergies"] else "없음"
    protein_str = ", ".join(params["proteins"]) if params["proteins"] else "제한 없음"
    style_str = ", ".join(params["meal_styles"]) if params["meal_styles"] else "제한 없음"
    veg_str = "채식 (동물성 단백질 제외)" if params["vegetarian"] else "일반식"
    cheat = params.get("cheat_day", "일요일")

    return f"""당신은 영양사이자 식단 전문가입니다. 아래 조건에 맞는 일주일 식단표를 JSON으로 생성해주세요.
## 사용자 정보
- 목표: {params['goal']} (일일 목표 칼로리: {kcal} kcal)
- 탄수화물: {macros['carb']}g / 단백질: {macros['prot']}g / 지방: {macros['fat']}g
- 식이 유형: {veg_str}
- 알레르기/기피 식품: {allergy_str}
- 선호 단백질 급원: {protein_str}
- 식단 스타일: {style_str}

## 식단 설계 규칙
1. {cheat}을 치팅 데이로 지정. 나머지 6일은 목표 칼로리 ±80 kcal 이내로 맞춰주세요.
2. {cheat}의 meals는 빈 배열([])로 두고 is_cheat을 true로 표기하세요.
3. 치팅 데이 외 식단은 탄·단·지 비율을 지켜주세요.
4. 단백질 급원은 선호 재료 위주로, 식단 스타일을 자연스럽게 반영하세요.
5. 메뉴명은 구체적으로 작성하세요. 알레르기/기피 식품은 절대 사용 금지.
6. 일주일 내 메뉴가 지나치게 반복되지 않도록 다양하게 구성하세요.
7. 각 meals 항목에 portion 필드를 반드시 포함하고, 재료별 중량(g) 또는 개수(예: 달걀 2개)를 구체적으로 작성하세요.
8. portion 안 재료 개수는 필요 시 4개 이상도 자유롭게 작성하세요. 절대 생략하지 마세요.

## 출력 형식 (순수 JSON만)
{{
  "week": [
    {{
      "day": "월요일",
      "is_cheat": false,
      "total_kcal": 2100,
      "meals": [
        {{
          "type": "아침",
          "name": "메뉴명",
          "detail": "설명",
          "portion": "현미밥 200g, 닭가슴살 150g, 브로콜리 120g, 올리브오일 8g",
          "kcal": 500
        }}
      ]
    }}
  ]
}}"""

def build_edit_prompt(day, meal_type, current_meal, user_request, kcal, macros, params):
    allergy_str = ", ".join(params["allergies"]) if params["allergies"] else "없음"
    protein_str = ", ".join(params["proteins"]) if params["proteins"] else "제한 없음"
    style_str = ", ".join(params["meal_styles"]) if params["meal_styles"] else "제한 없음"

    return f"""사용자가 특정 끼니의 메뉴 교체를 요청했습니다. 대체 메뉴 3가지를 JSON으로 생성해주세요.
## 수정 대상: {day} / {meal_type} / 현재 메뉴: {current_meal['name']} ({current_meal['kcal']} kcal)
## 사용자 요청: "{user_request}"
## 제약 조건: {current_meal['kcal']} kcal ±100 이내, 선호 단백질: {protein_str}, 기피: {allergy_str}, 스타일: {style_str}
## 필수 조건: alternatives의 각 항목에 portion 필드를 포함하고, 재료별 중량(g)/개수를 구체적으로 적으세요. 재료 개수 생략 금지.

## 출력 형식 (순수 JSON만)
{{
  "alternatives": [
    {{
      "name": "메뉴명",
      "detail": "재료 및 설명",
      "portion": "예: 현미밥 180g, 소고기 우둔 140g, 샐러드 100g, 방울토마토 80g, 아보카도 50g",
      "kcal": 520
    }}
  ]
}}"""

def generate_diet(params, kcal, macros):
    try:
        data = call_llm(build_diet_prompt(params, kcal, macros), "🍽️ 식단 생성 중...")
        for d in data.get("week", []):
            if not d.get("is_cheat"):
                for m in d.get("meals", []):
                    m.setdefault("portion", "정보 없음")
        return data
    except Exception as e:
        st.error(f"식단 생성 오류: {e}")
        return None

def generate_alternatives(day, meal_type, current_meal, user_request, kcal, macros, params):
    try:
        data = call_llm(build_edit_prompt(day, meal_type, current_meal, user_request, kcal, macros, params), "🔍 대체 메뉴 생성 중...")
        for a in data.get("alternatives", []):
            a.setdefault("portion", "정보 없음")
        return data
    except Exception as e:
        st.error(f"대체 메뉴 오류: {e}")
        return None

def portion_to_lines(portion_text: str):
    items = [x.strip() for x in str(portion_text).split(",") if x.strip()]
    if not items:
        return ["정보 없음"]
    return items

# ── 세션 초기화 ───────────────────────────────────────────────────────────────
defaults = {
    "ui_height_slider": 178.0, "ui_height_input": 178.0,
    "ui_weight_slider": 79.0, "ui_weight_input": 79.0,
    "ui_muscle_slider": 35.0, "ui_muscle_input": 35.0,
    "ui_fat_slider": 15.0, "ui_fat_input": 15.0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def sync_height_from_slider(): st.session_state.ui_height_input = st.session_state.ui_height_slider
def sync_height_from_input(): st.session_state.ui_height_slider = st.session_state.ui_height_input
def sync_weight_from_slider(): st.session_state.ui_weight_input = st.session_state.ui_weight_slider
def sync_weight_from_input(): st.session_state.ui_weight_slider = st.session_state.ui_weight_input
def sync_muscle_from_slider(): st.session_state.ui_muscle_input = st.session_state.ui_muscle_slider
def sync_muscle_from_input(): st.session_state.ui_muscle_slider = st.session_state.ui_muscle_input
def sync_fat_from_slider(): st.session_state.ui_fat_input = st.session_state.ui_fat_slider
def sync_fat_from_input(): st.session_state.ui_fat_slider = st.session_state.ui_fat_input

for k, v in {
    "diet_data": None, "kcal_target": None, "macros": None, "params": None,
    "selected_day": 0, "editing": None, "edit_request": "", "alternatives": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# 사이드바
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📊 나의 신체 데이터")
    st.markdown("---")
    gender = st.selectbox("성별", ["남성", "여성"], filter_mode="None")
    age = st.number_input("나이", min_value=15, max_value=100, value=25)

    height_col1, height_col2 = st.columns([3, 1])
    with height_col1:
        st.slider("키 (cm)", 140.0, 210.0, key="ui_height_slider", on_change=sync_height_from_slider)
    with height_col2:
        st.number_input("cm", min_value=140.0, max_value=210.0, key="ui_height_input", on_change=sync_height_from_input)

    weight_col1, weight_col2 = st.columns([3, 1])
    with weight_col1:
        st.slider("체중 (kg)", 40.0, 150.0, key="ui_weight_slider", on_change=sync_weight_from_slider)
    with weight_col2:
        st.number_input("kg", min_value=40.0, max_value=150.0, key="ui_weight_input", on_change=sync_weight_from_input)

    mm_col1, mm_col2 = st.columns([3, 1])
    with mm_col1:
        st.slider("골격근량 (kg)", 15.0, 60.0, key="ui_muscle_slider", step=0.1, on_change=sync_muscle_from_slider)
    with mm_col2:
        st.number_input("kg ", min_value=15.0, max_value=60.0, key="ui_muscle_input", step=0.1, on_change=sync_muscle_from_input)

    bf_col1, bf_col2 = st.columns([3, 1])
    with bf_col1:
        st.slider("체지방률 (%)", 3.0, 50.0, key="ui_fat_slider", step=0.1, on_change=sync_fat_from_slider)
    with bf_col2:
        st.number_input("% ", min_value=3.0, max_value=50.0, key="ui_fat_input", step=0.1, on_change=sync_fat_from_input)

    height = st.session_state.ui_height_slider
    weight = st.session_state.ui_weight_slider
    body_fat = st.session_state.ui_fat_slider

    st.markdown("---")
    st.markdown("#### 💡 현재 체성분 분석")
    bmi = round(weight / ((height / 100) ** 2), 1)
    ffm = round(weight * (1 - body_fat / 100), 1)
    st.markdown(f"BMI **{bmi}** · 제지방량 **{ffm} kg** · 체지방 **{round(weight * body_fat / 100, 1)} kg**")

# ══════════════════════════════════════════════════════════════════════════════
# 메인
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="hero-title">💪 맞춤형 식단 / 건강 큐레이터</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">바쁜 일상 속에서도 확실한 성장을! 체성분과 라이프스타일에 맞춘 일주일 식단표를 생성합니다.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown('<div class="section-header">🏃‍♂️ 라이프스타일 & 목표</div>', unsafe_allow_html=True)
    activity_level = st.selectbox("평소 직무 활동량", list(ACTIVITY_MET.keys()))
    workout_days = st.select_slider("주당 땀 흘리는 운동 횟수", options=list(EXERCISE_ADD.keys()), value="3회")
    goal = st.selectbox("목표", list(GOAL_ADJUST.keys()), help="린매스업은 소폭 적자(상승 다이어트)와 소폭 흑자(벌크) 두 가지로 나뉩니다.")
    cheat_day = st.selectbox("치팅 데이", ["토요일", "일요일"], help="해당 요일은 자유식으로 배정됩니다.")
    vegetarian = st.toggle("🌿 채식 (동물성 단백질 제외)")

with col2:
    st.markdown('<div class="section-header">🥗 식단 커스텀</div>', unsafe_allow_html=True)
    allergies = st.multiselect("알레르기 또는 못 먹는 음식", ALLERGY_OPTIONS, placeholder="해당 항목을 모두 선택하세요")
    proteins = st.multiselect("선호하는 단백질 급원", PROTEIN_OPTIONS, default=["닭가슴살", "달걀"], placeholder="선호하는 단백질 식품을 선택하세요")
    meal_styles = st.multiselect("선호하는 식단 스타일 (밀프렙 기준)", STYLE_OPTIONS, default=["한식 (밥 위주)"], placeholder="식단 스타일을 선택하세요")

st.divider()
if st.button("🔥 맞춤형 일주일 식단 생성하기", use_container_width=True, type="primary"):
    tdee = calc_tdee(gender, age, height, weight, activity_level, workout_days)
    target = round(calc_target(tdee, goal))
    macros = calc_macros(target, goal)
    params = {"goal": goal, "vegetarian": vegetarian, "allergies": allergies, "proteins": proteins, "meal_styles": meal_styles, "cheat_day": cheat_day}

    result = generate_diet(params, target, macros)
    if result:
        st.session_state.diet_data = result.get("week", [])
        st.session_state.kcal_target, st.session_state.macros, st.session_state.params = target, macros, params
        st.session_state.selected_day, st.session_state.editing, st.session_state.alternatives = 0, None, None
        st.rerun()

if st.session_state.diet_data is None:
    st.markdown('<div class="empty-state"><div class="icon">🥗</div><div class="msg">위에서 정보를 입력하고 <strong>식단 생성</strong>을 눌러주세요.</div></div>', unsafe_allow_html=True)
else:
    diet = st.session_state.diet_data
    kcal = st.session_state.kcal_target
    macros = st.session_state.macros
    params = st.session_state.params

    st.markdown("---")
    st.markdown(f"""
    <div class="macro-card">
        <div class="label">일일 목표 칼로리</div><div class="value">{kcal:,} <span class="unit">kcal</span></div>
        <div class="macro-row">
            <div class="macro-chip"><div class="chip-label">탄수화물</div><div class="chip-val carb">{macros['carb']}g</div></div>
            <div class="macro-chip"><div class="chip-label">단백질</div><div class="chip-val prot">{macros['prot']}g</div></div>
            <div class="macro-chip"><div class="chip-label">지방</div><div class="chip-val fat">{macros['fat']}g</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ 캘린더형 주간표 (생략 없음)
    st.markdown("### 📅 주간 식단 캘린더")
    cards_html = ['<div class="week-cal-wrap"><div class="week-cal-grid">']

    meal_order = ["아침", "점심", "저녁"]
    for d in diet:
        day = d.get("day", "-")
        total_k = d.get("total_kcal", "-")

        cards_html.append('<div class="day-card">')
        cards_html.append(f'<div class="day-head"><div class="day-title">{day}</div><div class="day-kcal">총 {total_k} kcal</div></div>')

        if d.get("is_cheat"):
            cards_html.append('<div class="cheat-box">🎉 치팅 데이<br>원하는 식사를 즐기세요.</div>')
        else:
            meals_map = {m.get("type", ""): m for m in d.get("meals", [])}
            for mt in meal_order:
                m = meals_map.get(mt)
                if not m:
                    cards_html.append(f'<div class="meal-block"><div class="meal-type">{mt}</div><div class="material-line">-</div></div>')
                    continue

                name = m.get("name", "-")
                portion_lines = portion_to_lines(m.get("portion", "정보 없음"))
                meal_kcal = m.get("kcal", "-")

                cards_html.append('<div class="meal-block">')
                cards_html.append(f'<div class="meal-type">{mt}</div>')
                cards_html.append(f'<div class="meal-name-mini">{name}</div>')
                for line in portion_lines:
                    cards_html.append(f'<div class="material-line">• {line}</div>')
                cards_html.append(f'<div class="meal-kcal-mini">{meal_kcal} kcal</div>')
                cards_html.append('</div>')

        cards_html.append('</div>')

    cards_html.append('</div></div>')
    st.markdown("".join(cards_html), unsafe_allow_html=True)

    # 기존 요일 상세 탭 (유지)
    tab_cols = st.columns(7)
    for i, day_data in enumerate(diet):
        label = f"🎉 {day_data.get('day','')[:1]}요" if day_data.get("is_cheat") else f"{day_data.get('day','')[:1]}요"
        with tab_cols[i]:
            if st.button(label, key=f"day_tab_{i}", use_container_width=True):
                st.session_state.selected_day, st.session_state.editing, st.session_state.alternatives = i, None, None
                st.rerun()

    st.markdown("---")
    sel_idx = st.session_state.selected_day
    sel_day = diet[sel_idx]

    if sel_day.get("is_cheat"):
        st.markdown(f"### 🎉 {sel_day.get('day','')} — 치팅 데이")
        st.info("오늘은 자유식 날이에요! 먹고 싶은 걸 마음껏 즐기세요 😄\n\n내일부터 다시 식단으로 돌아가면 됩니다.")
    else:
        st.markdown(f"### {sel_day.get('day','')} <span style='font-size:0.9rem;color:#888;font-weight:400;'>{sel_day.get('total_kcal', '—')} kcal</span>", unsafe_allow_html=True)
        meal_tag_map = {"아침": "tag-breakfast", "점심": "tag-lunch", "저녁": "tag-dinner"}

        for m_idx, meal in enumerate(sel_day.get("meals", [])):
            editing_this = (st.session_state.editing == (sel_idx, m_idx))
            st.markdown(f"""
            <div class="meal-card">
                <span class="meal-tag {meal_tag_map.get(meal.get('type',''), '')}">{meal.get('type','-')}</span>
                <span class="meal-kcal">{meal.get('kcal','-')} kcal</span>
                <div class="meal-name">{meal.get('name','-')}</div>
                <div class="meal-detail">{meal.get('detail','-')}</div>
                <div class="meal-detail"><b>권장 섭취량:</b> {meal.get('portion', '정보 없음')}</div>
            </div>
            """, unsafe_allow_html=True)

            btn_col, _ = st.columns([1, 4])
            with btn_col:
                if st.button("✕ 닫기" if editing_this else "✏️ 수정하기", key=f"edit_btn_{sel_idx}_{m_idx}", use_container_width=True):
                    st.session_state.editing = None if editing_this else (sel_idx, m_idx)
                    st.session_state.alternatives, st.session_state.edit_request = None, ""
                    st.rerun()

            if editing_this:
                with st.container():
                    st.markdown(f'<div class="edit-panel-title">✏️ {meal.get("type","")} 메뉴 교체 요청</div>', unsafe_allow_html=True)
                    user_req = st.text_input("요청", placeholder="예) 닭가슴살 말고 소고기로...", key=f"req_input_{sel_idx}_{m_idx}", label_visibility="collapsed")
                    req_col, _ = st.columns([1, 4])
                    with req_col:
                        if st.button("대체 메뉴 찾기", key=f"req_submit_{sel_idx}_{m_idx}", type="primary", use_container_width=True):
                            if user_req.strip():
                                st.session_state.alternatives = generate_alternatives(sel_day.get("day",""), meal.get("type",""), meal, user_req, kcal, macros, params)
                                st.session_state.edit_request = user_req
                                st.rerun()
                            else:
                                st.warning("요청 내용을 입력해주세요.")

                    if st.session_state.alternatives:
                        st.markdown("**대체 메뉴 — 하나를 선택하세요:**")
                        for a_idx, alt in enumerate(st.session_state.alternatives.get("alternatives", [])):
                            a_col1, a_col2 = st.columns([5, 1])
                            with a_col1:
                                st.markdown(
                                    f"**{alt.get('name','-')}** — {alt.get('kcal','-')} kcal  \n"
                                    f"<span style='font-size:0.82rem;color:#888;'>{alt.get('detail','-')}</span><br>"
                                    f"<span style='font-size:0.82rem;color:#666;'><b>권장 섭취량:</b> {alt.get('portion','정보 없음')}</span>",
                                    unsafe_allow_html=True
                                )
                            with a_col2:
                                if st.button("선택", key=f"alt_{sel_idx}_{m_idx}_{a_idx}", use_container_width=True):
                                    st.session_state.diet_data[sel_idx]["meals"][m_idx] = {
                                        "type": meal.get("type", ""),
                                        "name": alt.get("name", ""),
                                        "detail": alt.get("detail", ""),
                                        "portion": alt.get("portion", "정보 없음"),
                                        "kcal": alt.get("kcal", meal.get("kcal", 0)),
                                    }
                                    st.session_state.diet_data[sel_idx]["total_kcal"] = sum(
                                        m.get("kcal", 0) for m in st.session_state.diet_data[sel_idx]["meals"]
                                    )
                                    st.session_state.editing, st.session_state.alternatives = None, None
                                    st.rerun()

    st.markdown("---")
    if st.button("🔄 식단 전체 재생성", use_container_width=False):
        result = generate_diet(params, kcal, macros)
        if result:
            st.session_state.diet_data, st.session_state.selected_day = result.get("week", []), 0
            st.session_state.editing, st.session_state.alternatives = None, None
            st.rerun()
