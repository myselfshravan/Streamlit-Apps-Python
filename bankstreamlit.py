import streamlit as st
import pandas as pd
from datetime import date, datetime
import plotly.express as px

st.title('Visualize Your HDFC Bank Statement')
st.write('Export your HDFC Bank statement as a XLS file and drop it here to analyze your expenses')
st.write("Note: We don't store your data. It's all done locally on your machine")

agree = st.checkbox('Use Sample Data')
if agree:
    uploaded_file = 'https://github.com/myselfshravan/Python/files/10087176/statement23.xls'
else:
    uploaded_file = st.file_uploader("Choose a Excel file of HDFC Bank Statement", type="xls")

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    df = df.iloc[21:-18]

    df = df.drop(df.columns[[0, 2]], axis=1)

    df = df.drop(df.index[1])

    df = df.fillna(0)
    df.rename(
        columns={'Unnamed: 1': 'UPIs', 'Unnamed: 3': 'Date', 'Unnamed: 4': 'Withdrawal', 'Unnamed: 5': 'Deposited',
                 'Unnamed: 6': 'Balance'},
        inplace=True)

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y').dt.date  # Converting date to datetime format
    df['Withdrawal'] = df['Withdrawal'].apply(lambda x: "{:.1f}".format(x)).astype(float)
    df['Deposited'] = df['Deposited'].apply(lambda x: "{:.1f}".format(x)).astype(float)
    df['Balance'] = df['Balance'].astype(float)
    df['UPIs'] = df['UPIs'].astype(str)
    df['UPIs'] = df['UPIs'].str.split('@', expand=True)[0]
    df['UPIs'] = df['UPIs'].str.split('-', expand=True)[1]

    start_date = df['Date'].iloc[0].strftime("%B %d")
    end_date = df['Date'].iloc[-1].strftime("%B %d")

    st.write(f"Statement Period: {start_date} to {end_date}")
    start = datetime.strptime(df['Date'].iloc[0].strftime('%d/%m/%y'), '%d/%m/%y')
    end = datetime.strptime(df['Date'].iloc[-1].strftime('%d/%m/%y'), '%d/%m/%y')
    days = (end - start).days
    st.write(f"Number of Days: {days}")
    total_withdrawal = df['Withdrawal'].sum()
    st.write(f"Total Withdrawal: {total_withdrawal}")
    total_deposit = df['Deposited'].sum()
    st.write(f"Total Deposit: {total_deposit}")

    fig = px.line(df, x='Date', y='Balance', title='Balance Trend', color_discrete_sequence=['#1f77b4'],
                  template='plotly_white', labels={'Date': 'Date', 'Balance': 'Balance'},
                  hover_data={'Date': False, 'Balance': ':.2f'})
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)

    val = st.radio('Select', ('Withdrawal', 'Deposited'))
    if val == 'Withdrawal':
        fig = px.bar(df, x='Date', y='Withdrawal', title='Withdrawals')
        st.plotly_chart(fig, use_container_width=True)
        figs = px.scatter(df, x='Date', y='Withdrawal', color='UPIs', title='Withdrawals')
        st.plotly_chart(figs, use_container_width=True)
    elif val == 'Deposited':
        fig = px.bar(df, x='Date', y='Deposited', title='Deposits')
        st.plotly_chart(fig, use_container_width=True)
        figs = px.scatter(df, x='Date', y='Deposited', color='UPIs', title='Deposits')
        st.plotly_chart(figs, use_container_width=True)

    date_selected = st.date_input('Select Date', value=date(2022, 11, 4))
    selected = df.loc[df['Date'] == date_selected]
    st.dataframe(selected, use_container_width=True)
    st.write("Total Withdrawals on", date_selected, "is", selected['Withdrawal'].sum())
    st.write("Total Deposits on", date_selected, "is", selected['Deposited'].sum())
    st.write("\n")
    st.subheader('Select a date range')
    start_range = df['Date'].iloc[0]
    end_range = df['Date'].iloc[-1]
    start_date = st.date_input('Start date', value=start_range)
    end_date = st.date_input('End date', value=end_range)
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    df = df.loc[mask]
    st.write(df, use_container_width=True)
    st.write(f'Total Deposited: Rs {df["Deposited"].sum()}')
    st.write(f'Total Withdrawal: Rs {df["Withdrawal"].sum()}')

    st.subheader('Total amount spent on each UPI')
    st.write(df.groupby('UPIs')['Withdrawal'].sum().sort_values(ascending=False), use_container_width=True)

    st.subheader('Highest amount spent in one transaction')
    st.write(df.loc[df['Withdrawal'].idxmax()], use_container_width=True)

    inday = df.groupby("Date")['Withdrawal'].sum().sort_values(ascending=False).head(1).index[0].strftime("%d %B")
    st.subheader(f'Highest amount spent in a day')
    amount = df.groupby("Date")['Withdrawal'].sum().sort_values(ascending=False).head(1).values[0]
    st.write(f'{inday} : Rs {amount}')

hide_streamlit_style = """
                    <style>
                    # MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    footer:after {
                    content:'Made with ❤️ by Shravan'; 
                    visibility: visible;
    	            display: block;
    	            position: relative;
    	            # background-color: red;
    	            padding: 15px;
    	            top: 2px;
    	            }
                    </style>
                    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# st.subheader('Select What type of Graph you want to Visualize')
# graph = st.radio('Select', ('Line', 'Bar'))

# fig, ax = plt.subplots()
# ax.plot(df['Date'], df['Balance'], marker='o', linewidth=1, markersize=1)
# plt.xticks(rotation=90)
# plt.yticks(np.arange(0, 17000, 1000))
# ax.set(xlabel='Date', ylabel='Balance', title='Balance')
# ax.grid()
# st.pyplot(fig)
