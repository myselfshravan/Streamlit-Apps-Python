import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.express as px

st.title('Visualize Your Bank Statement')

agree = st.checkbox('Use Demo Data')

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

    fig = px.line(df, x='Date', y='Balance', title='Bank Balance')
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
    st.write("Total Withdrawals on", date_selected, "is", selected['Withdrawal'].sum())
    st.write("Total Deposits on", date_selected, "is", selected['Deposited'].sum())
    st.write("\n")
    st.subheader('Select a date range')
    start_date = st.date_input('Start date', datetime(2022, 11, 3))
    end_date = st.date_input('End date', datetime(2022, 11, 17))
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    df = df.loc[mask]
    st.write(df, use_container_width=True)
    st.write('Total Deposited: ', df['Deposited'].sum())
    st.write('Total Withdrawal: ', df['Withdrawal'].sum())

    # st.subheader('Select What type of Graph you want to Visualize')
    # graph = st.radio('Select', ('Line', 'Bar'))

    # fig, ax = plt.subplots()
    # ax.plot(df['Date'], df['Balance'], marker='o', linewidth=1, markersize=1)
    # plt.xticks(rotation=90)
    # plt.yticks(np.arange(0, 17000, 1000))
    # ax.set(xlabel='Date', ylabel='Balance', title='Balance')
    # ax.grid()
    # st.pyplot(fig)

    # st.write(df)
    # st.write("This is a bar chart of the bank statement")
    # fig = px.bar(df, x='Date', y='Amount', color='Type')
    # st.plotly_chart(fig)
    # st.write("This is a pie chart of the bank statement")
    # fig = px.pie(df, values='Amount', names='Type')
    # st.plotly_chart(fig)
    # st.write("This is a line chart of the bank statement")
    # fig = px.line(df, x='Date', y='Amount', color='Type')
    # st.plotly_chart(fig)
    # st.write("This is a histogram of the bank statement")
    # fig = px.histogram(df, x='Amount', color='Type')
    # st.plotly_chart(fig)
    # st.write("This is a box plot of the bank statement")
    # fig = px.box(df, x='Amount', color='Type')
    # st.plotly_chart(fig)
    # st.write("This is a violin plot of the bank statement")
    # fig = px.violin(df, y='Amount', color='Type')
    # st.plotly_chart(fig)
    # st.write("This is a scatter plot of the bank statement")
    # fig = px.scatter(df, x='Date', y='Amount', color='Type')
    # st.plotly_chart(fig)
