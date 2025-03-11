import streamlit as st
import json
import time


# Page Configuration

# File handling functions
def load_books():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_books(books):
    with open("library.json", "w") as file:
        json.dump(books, file, indent=4)

# Load existing books
books = load_books()

st.markdown(
    """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 1.5s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("📚 Library Manager")
option = st.sidebar.radio("Navigate", ["📚 Home","➕ Add Book", "❌ Remove a Book", "🔍Search for a book", "📖 Display all books  ", "📊 Display statistics","🚪 Exit"])

if option == "📚 Home":
    st.markdown(
        """
        <div class="fade-in" style="text-align: ;">
            <h1 style="margin-bottom:15px;">📖 Welcome to Your Personal Library Manager!</h1>
            <p style="color:#888;">📚
                Easily manage your book collection, track your reading progress, and explore statistics with this interactive tool.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    


# Add a Book
if option == "➕ Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read")
    if st.button("Add Book"):
        if title and author and genre:
            books.append({"Title": title, "Author": author, "Year": year, "Genre": genre, "Read": read_status})
            save_books(books)
            st.success(f"✅ '{title}' added to your library!")
            st.balloons()
        else:
            st.error("❌ Please fill all fields.")

# Remove a Book
elif option == "❌ Remove a Book":
    st.header("🗑 Remove a Book")
    titles = [book["Title"] for book in books]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            books = [book for book in books if book["Title"] != book_to_remove]
            save_books(books)
            st.toast("📕 Book removed successfully!", icon="🔥")
            st.success(f"✅ '{book_to_remove}' removed from library!")
            st.snow()  
    else:
        st.info("📌 No books available.")

# Search a Book
elif option == "🔍Search for a book":
    st.header("🔍Search a Book")
    search_query = st.text_input("Enter book title or author")
    if st.button("Search"):
        results = [book for book in books if search_query.lower() in book["Title"].lower() or search_query.lower() in book["Author"].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {'✔ Read' if book['Read'] else '❌ Unread'}")
        else:
            st.warning("❌ No books found.")

# Display all books  
elif option == "📖 Display all books  ":
    st.header("📚 Your Book Collection")
    
    if books:
        # Creating a grid layout
        cols = st.columns(3)  # 3 columns per row
        for idx, book in enumerate(books):
            with cols[idx % 3]:  # Placing books in a 3-column layout
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; 
                                background-color: ; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                        <h4 style="color: [#ffff];font-style: bold; ">📖 {book['Title']}</h4>
                        <p style="font-style: italic;"><b>Author:</b> {book['Author']}</p>
                        <p style="font-style: italic;"><b>Year:</b> {book['Year']}</p>
                        <p style="font-style: italic;"><b>Genre:</b> {book['Genre']}</p>
                        <p style="font-style: italic;"><b>Status:</b> {"✅ Read" if book['Read'] else "❌ Unread"}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("📌 No books added yet.")


# Display statistics 
elif option == "📊 Display statistics":
    st.header("📊 Library Display statistics ")
    total_books = len(books)
    read_books = len([book for book in books if book["Read"]])
    st.metric("Total Books", total_books)
    st.metric("Books Read", read_books)
    if total_books > 0:
        st.metric("Percentage Read", f"{(read_books / total_books) * 100:.2f}%")
    else:
        st.info("📌 No books available to calculate statistics.")

st.sidebar.write("📌 Use the sidebar to navigate different sections.")

# Exit Library
if option == "🚪 Exit":
    st.header("🚪 Exit Library")
    if st.button("Exit"):
        save_books(books)  # Save library before exiting
        st.success("✅ Library saved to file. Goodbye! 👋")
        st.balloons()  # 🎈 Fun effect on exit
        time.sleep(2)  # Delay before clearing UI
        st.rerun()  # Refresh app


# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: gray;'>© 2025 Library Manager | Developed with ❤️ by Ayesha</p>
""", unsafe_allow_html=True)