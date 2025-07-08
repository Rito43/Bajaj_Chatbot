

'''import streamlit as st
from transcript_bot import answer_query as transcript_answer
from stock_queries import answer_query as stock_answer

def route_query(user_input):
    stock_keywords = [
        "highest stock", "lowest stock", "average stock", "compare", "sensex", "stock price"
    ]
    transcript_keywords = [
        "organic traffic", "headwinds", "rationale", "Allianz", "stake", "Hero", "CFO", "commentary", "investor call"
    ]

    user_input_lower = user_input.lower()
    if any(kw in user_input_lower for kw in stock_keywords):
        return "stock"
    elif any(kw in user_input_lower for kw in transcript_keywords):
        return "transcript"
    else:
        return "unknown"

# --- Streamlit UI ---
st.set_page_config(page_title="Bajaj Finserv Chatbot", page_icon="🤖")
st.title("🤖 Bajaj Finserv Assistant Chatbot")
st.write("Ask me questions about stock trends or earnings call insights.")

user_input = st.text_input("🧠 Your question")

if user_input:
    route = route_query(user_input)

    with st.spinner("Generating answer..."):
        try:
            if route == "stock":
                response = stock_answer(user_input)
                st.success("📈 StockBot:")
                st.write(response)

            elif route == "transcript":
                response = transcript_answer(user_input)
                st.success("📋 TranscriptBot:")
                st.write(response)

            else:
                st.warning("🤔 I couldn't classify your question. Try rephrasing it.")

        except Exception as e:
            st.error(f"❌ Error: {e}")'''


import streamlit as st
from transcript_bot import answer_query as transcript_answer
from stock_queries import answer_query as stock_answer

# --- Routing Logic ---
def route_query(user_input):
    stock_keywords = [
        "highest stock", "lowest stock", "average stock", "compare", "sensex", "stock price"
    ]
    transcript_keywords = [
        "organic traffic", "headwinds", "rationale", "Allianz", "stake", "Hero", "CFO", "commentary", "investor call"
    ]

    user_input_lower = user_input.lower()
    if any(kw in user_input_lower for kw in stock_keywords):
        return "stock"
    elif any(kw in user_input_lower for kw in transcript_keywords):
        return "transcript"
    else:
        return "unknown"

# --- Streamlit UI ---
st.set_page_config(page_title="Bajaj Finserv Chatbot", page_icon="🤖")
st.title("🤖 Bajaj Finserv Assistant Chatbot")
st.write("Ask me questions about stock trends or earnings call insights.")

user_input = st.text_input("🧠 Your question")

if user_input:
    route = route_query(user_input)

    with st.spinner("Generating answer..."):
        try:
            if route == "stock":
                response = stock_answer(user_input)
                st.success("📈 StockBot:")
                st.write(response)

            elif route == "transcript":
                response = transcript_answer(user_input)
                st.success("📋 TranscriptBot:")

                # ✅ Check for table-like response
                if isinstance(response, list) and all(isinstance(row, dict) for row in response):
                    st.table(response)
                else:
                    st.write(response)

            else:
                st.warning("🤔 I couldn't classify your question. Try rephrasing it.")

        except Exception as e:
            st.error(f"❌ Error: {e}")

