# A simple way to construct InsurTech Index with co-occurrence matrix

corpus: news about InsurTech

1. Collect keywords and company names(property insurance companies)
2. Statistic co-occurrence matrix of collected words and company names(same article, paragraph, sentence or window)
3. Assign weights
4. Calculate InsurTech Index by year and company

Question: Should we divide indices with numbers of total words of each year? How about numbers of reports of each year?

To-do: 
1. Add more company names and keywords about InsurTech to dictionary
2. Write functions to sum up term frequencies of different company names which are indeed a same company