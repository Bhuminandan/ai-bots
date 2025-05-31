import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def get_sql_query_from_text(user_input):
    # Model
    system_prompt = ChatPromptTemplate.from_template(
        """"
    Your a expert in converting natural language questions into optimized SQL queries.
    The sql database has name student with the following columns:
    NAME, COURSE, SECTION, MARKS.
    For example, 
    1) if the user asks "What is the name of the student with the highest marks?",
    you should return a SQL query like:
    SELECT NAME FROM STUDENT ORDER BY MARKS DESC LIMIT 1;
    2) if the user asks "What are the names of students in Data science course?",
    you should return a SQL query like:
    SELECT NAME FROM STUDENT WHERE COURSE = 'Data science';

    also the sql code should not have ``` in the beginning and end of the code block.
    Now convert the following question into a SQL query:
    {user_input}
    No preamble, just the valid SQL query.
    """
    )
    # Set the model to use
    model = "llama3-8b-8192"

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model=model,
        temperature=0,
    )

    chain = system_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_input": user_input})
    sql_query = response.strip()

    return sql_query

def get_data_from_sql(sql_query):
    # Connect to the SQLite database
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    try:
        # Execute the SQL query
        cursor.execute(sql_query)
        data = cursor.fetchall()
        return data

    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")

    finally:
        # Close the database connection
        cursor.close()
        connection.close()

def main():
    st.title("Talk to your data")

    text_input = st.text_input("Ask here...", placeholder="Type your question here...")
    submit_button = st.button("Submit")
    if submit_button:
        if text_input:
            sql_query = get_sql_query_from_text(text_input)
            st.write("Generated SQL Query:")
            st.code(sql_query, language='sql')
            st.write("Executing SQL Query...")
            data = get_data_from_sql(sql_query)
            if data:
                st.write("Query Results:")
                for row in data:
                    st.write(row)
            else:
                st.write("No results found or an error occurred.")
        else:
            st.warning("Please enter a question before submitting.")

if __name__ == "__main__":
    main()