
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 🔹 기존 함수들 유지
def estimate_t_half(age):
    f = lambda age: -0.009 *(age**2) + 0.754 * age
    t_half_43 = 4
    return t_half_43 * (f(43)/ f(age))

def estimate_Tx(week_number):
    if week_number <= 5:
        return -0.1 * week_number + 1
    else:
        return 0.3

def g(age):
    return -0.00375 * age + 0.525

def concentration_t(t, dose, weight, t_half):
    Vd = 0.7 * weight
    k = np.log(2) / t_half
    return (dose / Vd) * np.exp(-k * t)

def effect_t(t, C_t, EC50, Emax, week_number, age):
    Tn = estimate_Tx(week_number)
    gx = g(age)
    numerator = Emax * gx * Tn * C_t * 1.2
    denominator = EC50 + C_t
    return numerator / denominator

# 🔸 Streamlit 앱 구성
def simulate_custom_model(age, weight, week_number, D, Emax=1.0, EC50=2.0, effect_ylim=(0, 0.7)):
    t = np.linspace(0, 12, 500)
    t_half = estimate_t_half(age)
    C_t = concentration_t(t, D, weight, t_half)
    E_t = effect_t(t, C_t, EC50, Emax, week_number, age)

    # 정보 출력
    st.markdown("###  입력 정보 및 계산 결과")
    st.write(f"• 나이: {age}세")
    st.write(f"• 체중: {weight} kg")
    st.write(f"• 주당 카페인 섭취 횟수: {week_number} 회")
    st.write(f"• 1회 섭취량: {D} mg")
    st.write(f"• 계산된 반감기 (t½): {t_half:.2f} 시간")
    st.write(f"• 수용체 민감도 계수 g(age): {g(age):.4f}")
    st.write(f"• 섭취 민감도 계수 T(n): {estimate_Tx(week_number):.4f}")
    st.write(f"• 최대 효과 Emax: {Emax}, EC50: {EC50}")

    # 그래프 그리기
    plt.figure(figsize=(10, 5))
    plt.plot(t, E_t, label=f'Age={age}, Weight={weight}kg, {week_number}times/week', color='orange')

    # 혈중 농도 1~3mg 구간 파란색 영역
    in_zone = (C_t >= 1) & (C_t <= 3)
    if np.any(in_zone):
        t_zone = t[in_zone]
        plt.axvspan(t_zone[0], t_zone[-1], color='skyblue', alpha=0.3, label='Concentration 1~3mg/L')

    # 수직선 (사용자 체감 마지노선)
    plt.axvline(x=3.17925, color='red', linestyle='--', label='perceived_effect_limit (t=3.17925h)')

    plt.xlabel('Time (hours)')
    plt.ylabel('Caffeine Effect E(t)')
    plt.title('Customized PK-PD Caffeine Model')
    plt.grid(True)
    plt.ylim(effect_ylim)
    plt.legend()

    st.pyplot(plt)

# 🔹 입력창 UI
st.title(" 개인 맞춤형 카페인 효과 예측 시뮬레이터")
st.markdown("나이, 체중, 주당 카페인 섭취 횟수, 1회 섭취량을 입력하세요.")

input_str = st.text_input("(나이, 체중, 섭취 횟수, 약물양)을 ( , , , ) 형식으로 입력", "(20, 60, 3, 150)")

if st.button("시뮬레이션 실행"):
    try:
        age, weight, week_number, dose = eval(input_str)
        simulate_custom_model(age, weight, week_number, dose)
    except Exception as e:
        st.error(" 입력 오류: (나이, 체중, 횟수, 약물양) 형식으로 입력하세요.")
