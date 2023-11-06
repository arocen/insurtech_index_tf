# test preprocess

import preprocess as pr

# get sentences which have been cut into words
def main():
    docs_by_year = pr.load_doc()
    cleaned_docs_by_year = pr.remove_nonsense(docs_by_year)
    new_cleaned_docs_by_year = pr.remove_href(cleaned_docs_by_year)
    splitted_docs = pr.split_docs(new_cleaned_docs_by_year)
    sentences = pr.split_into_sentences(splitted_docs)

    # cut into words
    cut_sentences = pr.cut(sentences)
    print(len(cut_sentences))

    # save cut sentences as external txt file
    pr.save_sentences(cut_sentences)

if __name__ == "__main__":
    main()