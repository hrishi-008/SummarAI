"""
Main application file for SummarAI (formerly SearchGPT).

This module implements the core functionality of the SummarAI application, which:
1. Takes user queries through a Streamlit interface
2. Orchestrates the search, scraping, and summarization pipeline
3. Displays results and saves summaries

The application follows this workflow:
1. User enters a query in the Streamlit interface
2. Google search results are scraped (google_search_results.py)
3. Website content is extracted from search results (scrape_websites.py)
4. Content is indexed and retrieved using FAISS (faiss_db.py)
5. Retrieved content is summarized using LLM (summarise.py)
6. Results are displayed and saved to markdown

Classes:
    SearchGpt: Main class that orchestrates the entire pipeline

Dependencies:
    - streamlit: For the web interface
    - google_search_results: For scraping Google search results
    - scrape_websites: For extracting website content
    - summarise: For generating summaries
    - faiss_db: For vector storage and retrieval

Author: Hrishikesh
Date: March 2024
"""
import streamlit as st
import google_search_results as gsr
import scrape_websites as scraper
import summarise as summ
import faiss_db as db

class SearchGpt:
    def __init__(self, query):
        self.query = query
        self.googler = gsr
        self.scraper = scraper
        self.summariser = summ
        self.db = db
        self.results = []
        self.index = 1

    def get_results(self, index=1):
        self.index = index
        self.googler.google_search(self.query)
        self.scraper.parse_search_results()
        docs = self.db.search_with_faiss(self.query)
        for doc in docs:
            summary = self.summariser.generate_summary(doc.page_content, self.query, self.index)
            self.results.append(summary)
            self.index += 1
        return self.results

def main():
    st.title("Search GPT")
    st.write("A tool for summarizing search results and website content using FAISS and LLMs.")

    query = st.text_input("Enter your search query:", value="Best holiday destinations in India, Diwali")
    
    if st.button("Search and Summarize"):
        search = SearchGpt(query)
        results = search.get_results()
        if results:
            st.write("### Summary of Search Results:")
            for i, result in enumerate(results, 1):
                with st.expander(f"# Result {i}"):
                    st.write(result)

            # Save the summaries to a markdown file
            with open('searchResults/summary.md', 'w') as f:
                for result in results:
                    f.write(result + "\n")
            st.success("Summary saved to searchResults/summary.md")

if __name__ == '__main__':
    main()
