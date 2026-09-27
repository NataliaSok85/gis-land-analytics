import streamlit as st

st.title("🌳 Анализ земельных участков России")

st.write("Приложение работает!")

st.subheader("Поиск земельного участка")

cadastral = st.text_input(
    "Введите кадастровый квартал",
    placeholder="69:13:0150402"
)

if st.button("Найти"):
    if cadastral:
        st.success(f"Вы ввели: {cadastral}")
    else:
        st.warning("Введите кадастровый квартал")
