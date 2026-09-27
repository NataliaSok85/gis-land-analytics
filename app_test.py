import streamlit as st

from gis_torgi import (
    load_torgi_data,
    search_cadastral_quarter,
    normalize_results
)


st.title("🌳 Анализ земельных участков России")

st.write("Поиск торгов ГИС ТОРГИ")


st.subheader("Поиск по кадастровому кварталу")

cadastral = st.text_input(
    "Введите кадастровый квартал",
    placeholder="69:13:0150402"
)


if st.button("🔎 Найти в ГИС ТОРГИ"):

    if not cadastral:

        st.warning("Введите кадастровый квартал")

    else:

        with st.spinner("Загружаю данные ГИС ТОРГИ..."):

            try:

                data = load_torgi_data()

                st.success("Данные ГИС ТОРГИ загружены")

                results = search_cadastral_quarter(
                    cadastral,
                    data
                )

                df = normalize_results(results)

                if df.empty:

                    st.info(
                        "По этому кадастровому кварталу "
                        "пока ничего не найдено."
                    )

                else:

                    st.success(
                        f"Найдено записей: {len(df)}"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    "Не удалось получить данные ГИС ТОРГИ."
                )

                st.write(
                    "Техническая ошибка:"
                )

                st.code(str(e))