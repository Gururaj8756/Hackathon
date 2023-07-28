import os
import docx2txt
import PyPDF2 
import textract
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = text.lower()
    text = text.replace('.', ' ').replace(',', ' ').replace(';', ' ').replace(':', ' ')
    # Tokenize the text and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return " ".join(words)

def calculate_similarity(job_description, cv_text):
    preprocessed_job_description = preprocess_text(job_description)
    preprocessed_cv_text = preprocess_text(cv_text)
    # You can use any similarity metric here (e.g., Jaccard, Cosine similarity, etc.)
    # For simplicity, we will use Jaccard similarity.
    job_set = set(preprocessed_job_description.split())
    cv_set = set(preprocessed_cv_text.split())
    common_words = job_set.intersection(cv_set)
    similarity = len(common_words) / (len(job_set) + len(cv_set) - len(common_words))
    return similarity

def main():
    # Input: Job description
    job_description = input("Enter the job description: ")

    # Input: Folder containing CVs in various formats (DOCX, PDF, etc.)
    cv_folder = input("Enter the folder path containing CVs: ")

    # Collect all CVs in the folder
    cv_files = [f for f in os.listdir(cv_folder) if os.path.isfile(os.path.join(cv_folder, f))]

    # Process each CV
    for cv_file in cv_files:
        cv_path = os.path.join(cv_folder, cv_file)
        if cv_file.lower().endswith('.docx'):
            cv_text = docx2txt.process(cv_path)
        elif cv_file.lower().endswith('.pdf'):
            with open(cv_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfFileReader(file)
                cv_text = ""
                for page_num in range(pdf_reader.getNumPages()):
                    page = pdf_reader.getPage(page_num)
                    cv_text += page.extract_text()
        else:
            cv_text = textract.process(cv_path).decode('utf-8', errors='ignore')

        similarity_score = calculate_similarity(job_description, cv_text)
        print(f"CV: {cv_file} - Similarity: {similarity_score:.2f}")

if __name__ == "__main__":
    main()
