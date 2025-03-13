import streamlit as st
from database import add_book, get_all_books, delete_book
import pandas as pd
from datetime import date
import plotly.express as px

st.set_page_config(page_title="Bayt-al-Hikma Library", layout="wide", page_icon="favicon.ico")

# Custom CSS for better styling
st.markdown("""
    <style>
    .sidebar .sidebar-content { background-color: #f4f4f4; }
    .block-container { padding: 2rem; }
    .stButton>button { border-radius: 8px; color: white; }
    .stDownloadButton>button { background-color: #0073e6; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Bayt al-Hikma: Personal Library Manager")

# Sidebar: Display added books with filters
st.sidebar.title("📚 Your Library Collection")
books = get_all_books()

# Sidebar: Filters
st.sidebar.subheader("Filter by")
filter_genre = st.sidebar.selectbox("Genre", ["All"] + list(set(book.genre for book in books)))

filtered_books = [
    book for book in books
    if filter_genre == "All" or book.genre == filter_genre
]

# Display books in sidebar with better design
if filtered_books:
    for book in filtered_books:
        with st.sidebar.expander(f"📖 {book.title} by {book.author}"):
            st.markdown(f"**Genre:** {book.genre}")
            st.markdown(f"**Added on:** {book.added_on}")
            if st.button("❌ Delete", key=f"del_{book.id}"):
                delete_book(book.id)
                st.rerun()
else:
    st.sidebar.info("No books match your filters.")

# Main: Add a new book form
if "form_key" not in st.session_state:
    st.session_state.form_key = ""

with st.form("add_book_form"):
    st.subheader("📚 Add a New Book")
    title = st.text_input("Book Title", value=st.session_state.form_key)
    author = st.text_input("Author", value=st.session_state.form_key)
    genre = st.selectbox("Genre", ["Fiction", "Non-fiction", "Mystery", "Fantasy", "Sci-Fi", "Biography", "History", "Other"])
    added_on = st.date_input("Date Added", value=date.today())
    submit = st.form_submit_button("➕ Add Book")

    if submit and title and author:
        add_book(title, author, genre)
        st.success(f"Added '{title}' by {author}")
        st.session_state.form_key = ""  # Reset form fields
        st.rerun()

# Export to CSV

def export_books():
    data = [{"Title": book.title, "Author": book.author, "Genre": book.genre, "Added On": book.added_on} for book in books]
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')

st.download_button("📥 Export Library to CSV", data=export_books(), file_name="library_collection.csv", mime="text/csv")

# Statistics & Insights
st.subheader("📊 Library Insights")

total_books = len(books)
genre_counts = pd.Series([book.genre for book in books]).value_counts()

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Books", total_books)
with col2:
    st.metric("Unique Genres", len(genre_counts))

# Enhanced bar chart using Plotly
fig = px.bar(x=genre_counts.index, y=genre_counts.values, labels={'x': 'Genre', 'y': 'Count'}, title="Books by Genre")
st.plotly_chart(fig, use_container_width=True)

st.sidebar.info("📡 Connected to Database")