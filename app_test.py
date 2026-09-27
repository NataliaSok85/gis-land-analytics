import streamlit as st

from gis_torgi import load_torgi_data


st.title("🌳 Анализ земельных участков России")

st.subheader("Поиск по кадастровому кварталу")

cadastral = st.text_input(
    "Введите кадастровый квартал",
    placeholder="69:13:0150402"
)


if st.button("🔎 Проверить ГИС ТОРГИ"):

    if not cadastral:

        st.warning(
            "Введите кадастровый квартал"
        )

    else:

        with st.spinner(
            "Проверяю подключение к ГИС ТОРГИ..."
        ):

            try:

                result = load_torgi_data()

                st.success(
                    "ГИС ТОРГИ доступна"
                )

                st.write(
                    "Кадастровый квартал:",
                    cadastral
                )

                if result["meta_url"]:

                    st.info(
                        "Найдено описание набора "
                        "открытых данных."
                    )

                    st.code(
                        result["meta_url"]
                    )

                else:

                    st.warning(
                        "Набор найден, "
                        "но ссылка на meta.json "
                        "пока не определена."
                    )

            except Exception as error:

                st.error(
                    "Ошибка подключения к ГИС ТОРГИ"
                )

                st.code(
                    str(error)
                )