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

def score_job_description(job_title, job_description):
    job_title_keywords = preprocess_text(job_title).split()
    job_description_keywords = preprocess_text(job_description).split()

    # Calculate the score based on keyword matching
    score = 0
    for keyword in job_title_keywords:
        if keyword in job_description_keywords:
            score += 1

    # Normalize the score to a value between 0 and 1
    normalized_score = score / max(len(job_title_keywords), len(job_description_keywords))
    return normalized_score

def recommend_enhancements(job_title, job_description):
    job_title_keywords = set(preprocess_text(job_title).split())
    job_description_keywords = set(preprocess_text(job_description).split())

    # Find keywords missing from the job description
    missing_keywords = job_title_keywords.difference(job_description_keywords)

    # Find keywords present in the job description but not in the job title
    extra_keywords = job_description_keywords.difference(job_title_keywords)

    return missing_keywords, extra_keywords

def main():
    # Input: Job title
    job_title = input("Enter the job title: ")

    # Input: Job description
    job_description = input("Enter the job description: ")

    # Score the job description
    score = score_job_description(job_title, job_description)
    print(f"Job Description Score: {score:.2f}")

    # Provide recommendations for enhancements
    missing_keywords, extra_keywords = recommend_enhancements(job_title, job_description)

    if len(missing_keywords) > 0:
        print("\nRecommendations for Enhancements:")
        print("Add the following keywords to the job description:")
        print(', '.join(missing_keywords))

    if len(extra_keywords) > 0:
        print("\nOptional Enhancements:")
        print("Consider removing the following keywords from the job description:")
        print(', '.join(extra_keywords))

    # Option to incorporate suggested changes
    choice = input("\nDo you want to incorporate the suggested changes? (y/n): ")
    if choice.lower() == 'y':
        # Modify the job description based on the suggestions
        recommended_job_description = job_description
        recommended_job_description += ' '.join(missing_keywords)
        recommended_job_description = ' '.join([word for word in recommended_job_description.split() if word not in extra_keywords])

        print("\nModified Job Description:")
        print(recommended_job_description)

if __name__ == "__main__":
    main()
