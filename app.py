import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from scipy.stats import chisquare

from utils import get_digit_df


@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", dtype=str)
    df['Ngay'] = pd.DatetimeIndex(df['Ngay'])
    df['Nam'] = pd.DatetimeIndex(df['Ngay']).year
    df['Thu'] = df['Thu'].astype(int)
    return df


def masking(df_copy):

    if not st.session_state['var_2023'] and df_copy.shape[0] != 0:
        df_copy = df_copy[df_copy['Nam'] != 2023]

    if not st.session_state['var_2022'] and df_copy.shape[0] != 0:
        df_copy = df_copy[df_copy['Nam'] != 2022]

    if not st.session_state['var_2021'] and df_copy.shape[0] != 0:
        df_copy = df_copy[df_copy['Nam'] != 2021]

    if not st.session_state['thu_2'] and df_copy.shape[0] != 0:
        df_copy = df_copy[df_copy['Thu'] != 2]

    if not st.session_state['thu_7'] and df_copy.shape[0] != 0:
        df_copy = df_copy[df_copy['Thu'] != 7]

    return df_copy


def run_chi2(hist, name):
    stats, pvalue = chisquare(hist, axis=0)

    index.append(name)
    statistics.append(stats)
    Pvalues.append(pvalue)

    if pvalue <= SIGNIFICANT_LEVEL:
        msg.append("Không Phân Bố Đều")
    else:
        msg.append("Chưa thể kết luận")


df = load_data()
df_copy = df

st.title("Phân tích vé số đài Tp Hồ Chí Minh")
st.write("Phân tích kết quả xổ số TP.HCM thứ 2, thứ 7 hàng tuần qua các năm 2021, 2022, 2023")
st.write('-------------------------------------------------------')

st.sidebar.markdown("### Bộ Lọc")
with st.sidebar.form("Option"):
    col1, col2 = st.columns(2)
    with col1:
        st.write('Chọn Năm')
        st.checkbox('2023', value=True, key='var_2023')
        st.checkbox('2022', value=True, key='var_2022')
        st.checkbox('2021', value=True, key='var_2021')

    with col2:
        st.write('Chọn Thứ')
        st.checkbox('Thứ Hai', value=True, key='thu_2')
        st.checkbox('Thứ Bảy', value=True, key='thu_7')

    GIAI = st.selectbox("Chọn giải để phân tích",
                        options=df.columns[2:-1][::-1])

    st.write()
    SIGNIFICANT_LEVEL = st.slider(
        "Mức ý nghĩa cho Kiểm định Chi2", min_value=0.01, max_value=0.2, value=0.1)

    submitted = st.form_submit_button("Chọn", type='primary')

    if submitted:
        df_copy = masking(df.copy())


with st.expander("Xem Bảng Số Liệu"):
    st.dataframe(df_copy.style.applymap(
        lambda x: 'color: #F05B5E', subset=['G8', 'DB']), width=3000)


df_digit = get_digit_df(df_copy, GIAI)

if df_digit is not None:
    num_of_digits = len(df_digit[GIAI][0].split()[0])

    for i in range(num_of_digits):
        df_digit[f'digit_{i+1}'] = df_digit[f'digit_{i+1}'].astype('Int8')

    st.write('-------------------------------------------------------')
    st.markdown(f'### Kiểm định Chi-2 cho GIẢI {GIAI}')

    with st.container():
        overall_frequency = np.zeros(10)
        index = []
        statistics = []
        Pvalues = []
        msg = []

        for i in range(num_of_digits):
            hist, _ = np.histogram(df_digit[f'digit_{i+1}'], bins=10)

            overall_frequency += hist

            run_chi2(hist, f'Chữ số số {i+1}')

        run_chi2(overall_frequency, 'TOÀN BỘ')

        result = pd.DataFrame(np.array([statistics, Pvalues, msg]).T, columns=[
            'Giá Trị Thống Kê', 'P-value', 'Kết Luận'], index=index)

        result[['Giá Trị Thống Kê', 'P-value']
               ] = result[['Giá Trị Thống Kê', 'P-value']].astype(float)

        def highlight_rows(df):
            if df['P-value'] <= SIGNIFICANT_LEVEL:
                return ['background-color: #F05B5E']*3
            else:
                return ['background-color: #55A3F2']*3

        st.dataframe(result.style.apply(
            highlight_rows, axis=1), width=3000)

    st.write('-------------------------------------------------------')

    st.markdown(f"### Phân Bố Các Chữ Số của GIẢI {GIAI}")
    with st.container():
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.write('Phân bố theo Ngày')
            for i in range(num_of_digits):
                fig = px.histogram(data_frame=df_digit, x=f'digit_{i+1}', color='Thu',
                                   nbins=20,
                                   histnorm='percent',
                                   opacity=0.8,
                                   width=350,
                                   height=400,
                                   )
                st.plotly_chart(fig)

        with col2:
            st.write('Phân bố theo Năm')
            for i in range(num_of_digits):
                fig = px.histogram(data_frame=df_digit, x=f'digit_{i+1}', color='Nam',
                                   nbins=20,
                                   histnorm='percent',
                                   opacity=0.8,
                                   width=350,
                                   height=400,
                                   )
                st.plotly_chart(fig)

st.write('-------------------------------------------------------')
st.markdown("Created by Tri Cao Chanh 2023")
